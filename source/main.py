import uvicorn
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi import BackgroundTasks, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from source.controller.processos import get_processo_info_by_id
from source.controller import processos
from source.services.subscriptions import add_subscription
from source.services.notifications import send_subscription_confirmation
from source.services.scheduler import set_interval_seconds, check_once

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "front-end" / "static"
TEMPLATES_DIR = BASE_DIR / "front-end" / "templates"

app = FastAPI()
app.include_router(processos.router)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
from source.services.scheduler import start_scheduler, stop_scheduler


def get_jinja_templates():
    return templates


class AdminSchedulerPayload(BaseModel):
    interval_seconds: int = Field(
        ...,
        ge=1,
        description="Intervalo de verificação do scheduler em segundos.",
        examples=[60],
    )


class AdminManualCheckPayload(BaseModel):
    cnjs: Optional[list[str]] = Field(
        default=None,
        description="Lista opcional de CNJs para filtrar a checagem. Se omitido, todos os inscritos são verificados.",
        examples=[["0000000-00.0000.0.00.0000", "1234567-89.2024.8.26.0100"]],
    )


@app.on_event("startup")
def _startup_event():
    try:
        start_scheduler(app)
    except Exception:
        pass


@app.on_event("shutdown")
def _shutdown_event():
    try:
        stop_scheduler(app)
    except Exception:
        pass


@app.post(
    '/admin/scheduler',
    tags=["admin"],
    summary="Set scheduler interval",
    description="Define o intervalo de execução do scheduler em segundos.",
)
async def admin_set_interval(
    payload: AdminSchedulerPayload = Body(
        ...,
        examples={
            "default": {
                "summary": "Ajuste padrão do intervalo",
                "value": {"interval_seconds": 60},
            }
        },
    )
):
    """Admin endpoint to set scheduler interval (seconds). JSON: {"interval_seconds": 60} """
    seconds = int(payload.interval_seconds)
    set_interval_seconds(seconds)
    return {"ok": True, "interval_seconds": seconds}


@app.post(
    '/admin/check',
    tags=["admin"],
    summary="Trigger manual check",
    description="Executa uma checagem manual do scheduler. Pode receber uma lista opcional de CNJs para restringir a consulta.",
    response_model=None,
)
async def admin_manual_check(
    payload: AdminManualCheckPayload | None = Body(
        default=None,
        examples={
            "check-all": {
                "summary": "Checar todos os inscritos",
                "value": {},
            },
            "check-selected": {
                "summary": "Checar apenas alguns CNJs",
                "value": {"cnjs": ["0000000-00.0000.0.00.0000", "1234567-89.2024.8.26.0100"]},
            },
        },
    ),
    background = None,
):
    """Trigger a manual check. Optional JSON: {"cnjs": ["123", ...]}"""
    cnjs = payload.cnjs if payload else None
    # run check_once in background so endpoint returns quickly
    if background is not None:
        background.add_task(check_once, cnjs)
        return {"ok": True, "queued": True}
    else:
        await check_once(cnjs)
        return {"ok": True, "queued": False}


@app.get(
    '/unsubscribe',
    response_class=HTMLResponse,
    tags=["subscriptions"],
    summary="Cancel subscription",
    description="Cancela a inscrição do CNJ informado para o e-mail informado. Esse endpoint é usado pelo link de descadastro enviado nas notificações.",
)
def unsubscribe(request: Request, cnj: str = None, email: str = None):
    """Endpoint hit from unsubscribe links in emails. Deactivates subscription(s) by CNJ+email."""
    if not cnj or not email:
        return get_jinja_templates().TemplateResponse('unsubscribe.html', {'request': request, 'success': False, 'message': 'Parâmetros faltando (cnj e email são necessários).'})

    from source.services.subscriptions import deactivate_by_cnj_email

    try:
        updated = deactivate_by_cnj_email(cnj, email)
        if updated:
            msg = 'Inscrição cancelada com sucesso.'
            success = True
        else:
            msg = 'Nenhuma inscrição encontrada para este e-mail e processo.'
            success = False
    except Exception:
        msg = 'Erro ao processar cancelamento.'
        success = False

    return get_jinja_templates().TemplateResponse('unsubscribe.html', {'request': request, 'success': success, 'message': msg})


def normalize_process_result_for_template(id_processo: str, result):
    if not isinstance(result, dict):
        return {"id": id_processo, "ERROR": "Erro ao consultar processo"}

    if "id" in result:
        # If result has nested "Resultado" structure, flatten it
        if "Resultado" in result and isinstance(result["Resultado"], dict):
            normalized = {k: v for k, v in result.items() if k != "Resultado"}
            normalized.update(result["Resultado"])
            return normalized
        return result

    error_message = "Erro ao consultar processo"
    for value in result.values():
        if isinstance(value, list) and value:
            error_message = value[0]
            break
        if isinstance(value, str) and value:
            error_message = value
            break

    return {"id": id_processo, "ERROR": error_message}


@app.get('/', response_class=HTMLResponse, tags=["home"], include_in_schema=False)
def main(request: Request):
    return get_jinja_templates().TemplateResponse('home.html', {'request': request})


@app.get('/sobre', response_class=HTMLResponse, tags=["about"], include_in_schema=False)
def about(request: Request):
    return get_jinja_templates().TemplateResponse('sobre.html', {'request': request})


@app.post('/buscaprocesso', include_in_schema=False)
def buscar_processo_pelo_form(request: Request, id_processo: str = Form()):
    id_processo = id_processo.strip()
    try:
        result = get_processo_info_by_id(id_processo)
    except HTTPException as exc:
        # Captura erro de validação e renderiza no template
        error_detail = exc.detail
        error_message = "Erro ao validar processo"
        
        # Extrair mensagem legível do dicionário de erros
        if isinstance(error_detail, dict):
            for field, messages in error_detail.items():
                if isinstance(messages, list) and messages:
                    error_message = messages[0]
                    break
            if isinstance(error_detail, dict) and "detail" in error_detail:
                error_detail = error_detail["detail"]
                if isinstance(error_detail, dict):
                    for field, messages in error_detail.items():
                        if isinstance(messages, list) and messages:
                            error_message = messages[0]
                            break
        elif isinstance(error_detail, str):
            error_message = error_detail
        
        normalized_result = {
            "id": id_processo,
            "ERROR": error_message
        }
        return get_jinja_templates().TemplateResponse('processo.html', {'request': request, 'result': normalized_result})
    
    normalized_result = normalize_process_result_for_template(id_processo, result)
    return get_jinja_templates().TemplateResponse('processo.html', {'request': request, 'result': normalized_result})


@app.post('/subscribe', include_in_schema=False)
def subscribe(request: Request, id_processo: str = Form(), contato: str = Form(...)):
    """Handle subscription from processo page form and render the processo page with a message."""
    id_processo = id_processo.strip()
    success, msg = add_subscription(id_processo, contato, 'email')

    # Send confirmation email if subscription was successful
    if success:
        email_sent = send_subscription_confirmation(contato, id_processo, 'email')
        if not email_sent:
            msg = "Inscrição realizada, mas houve falha no envio do email de confirmação."

    result = get_processo_info_by_id(id_processo)
    normalized_result = normalize_process_result_for_template(id_processo, result)
    context = {'request': request, 'result': normalized_result, 'subscribe_message': msg}
    if success:
        context['subscribe_success'] = True
    else:
        context['subscribe_success'] = False
    return get_jinja_templates().TemplateResponse('processo.html', context)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
