import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
SUBSCRIPTIONS_FILE = DATA_DIR / "subscriptions.json"


def _load_all():
    if not SUBSCRIPTIONS_FILE.exists():
        return []
    try:
        with open(SUBSCRIPTIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_all(items):
    with open(SUBSCRIPTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2, default=str)


def add_subscription(cnj: str, contato: str, tipo: str):
    """Add subscription if not exists. Returns (True, message) or (False, message)."""
    cnj = cnj.strip()
    contato = contato.strip()
    tipo = tipo.strip().lower()

    if not cnj or not contato or tipo not in ("email", "whatsapp"):
        return False, "Dados inválidos para inscrição"

    items = _load_all()
    # avoid duplicates by cnj+contato
    for it in items:
        if it.get("cnj") == cnj and it.get("contato") == contato:
            if it.get("ativo", True):
                return False, "Você já está inscrito para este contato."
            else:
                it["ativo"] = True
                it["atualizado_em"] = datetime.utcnow().isoformat()
                _save_all(items)
                return True, "Inscrição reativada com sucesso"

    new = {
        "id": f"sub_{int(datetime.utcnow().timestamp())}",
        "cnj": cnj,
        "contato": contato,
        "tipo": tipo,
        "ultimo_mov_data": None,
        "ultimo_mov_descricao": None,
        "ativo": True,
        "criado_em": datetime.utcnow().isoformat(),
        "atualizado_em": datetime.utcnow().isoformat(),
    }
    items.append(new)
    _save_all(items)
    return True, "Inscrição realizada com sucesso. Você receberá notificações por {}.".format(tipo)


def list_subscriptions():
    return _load_all()


def deactivate_subscription(subscription_id: str):
    items = _load_all()
    for it in items:
        if it.get("id") == subscription_id:
            it["ativo"] = False
            it["atualizado_em"] = datetime.utcnow().isoformat()
            _save_all(items)
            return True
    return False
