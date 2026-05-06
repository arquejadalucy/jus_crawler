import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv
from urllib.parse import quote_plus


def _smtp_config():
    # Reload .env on each send so changes are picked up without restarting the app.
    load_dotenv(override=False)
    smtp_user = os.getenv("SMTP_USER", "")
    return {
        "server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        "port": int(os.getenv("SMTP_PORT", "587")),
        "user": smtp_user,
        "password": os.getenv("SMTP_PASSWORD", ""),
        "sender": os.getenv("SENDER_EMAIL", smtp_user or "noreply@juscrawler.com"),
    }


def send_subscription_confirmation(contato: str, cnj: str, tipo: str):
    """
    Send subscription confirmation email.
    If SMTP credentials not set, logs to file instead (for demo/testing).
    Returns True if sent or logged successfully, False otherwise.
    """
    assunto = "🔔 Inscrição confirmada - JUS CRAWLER"

    base = os.getenv("APP_BASE_URL", "http://localhost:8000")
    unsubscribe_url = f"{base}/unsubscribe?cnj={quote_plus(cnj)}&email={quote_plus(contato)}"

    corpo = f"""
Olá!

Sua inscrição foi confirmada com sucesso!

📋 Detalhes da inscrição:
- Processo: {cnj}
- Tipo de notificação: {tipo}
- Contato: {contato}
- Data: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}

A partir de agora, você receberá notificações sempre que houver novas movimentações neste processo.

Obrigado por usar JUS CRAWLER!
---
Este é um email automático. Não responda diretamente.
"""
    corpo += f"\nCancelar inscrição: {unsubscribe_url}\n"

    cfg = _smtp_config()
    if not cfg["user"] or not cfg["password"]:
        # Demo mode: log to file
        log_path = "/tmp/juscrawler_notifications.log"
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"\n[{datetime.now().isoformat()}] DEMO EMAIL\n")
                f.write(f"  To: {contato}\n")
                f.write(f"  Subject: {assunto}\n")
                f.write(f"  Body Preview: {corpo[:200]}...\n")
            print(f"✓ Notificação registrada em {log_path}")
            return True
        except Exception as e:
            print(f"✗ Erro ao registrar notificação: {e}")
            return False

    # Production mode: send via SMTP
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = assunto
        msg["From"] = cfg["sender"]
        msg["To"] = contato

        part = MIMEText(corpo, "plain", "utf-8")
        msg.attach(part)

        with smtplib.SMTP(cfg["server"], cfg["port"], timeout=10) as server:
            server.starttls()
            server.login(cfg["user"], cfg["password"])
            server.sendmail(cfg["sender"], contato, msg.as_string())

        print(f"✓ Email enviado para {contato}")
        return True
    except Exception as e:
        print(f"✗ Erro ao enviar email para {contato}: {e}")
        return False


def send_update_notification(contato: str, cnj: str, tipo: str, ultima_movimentacao: dict):
    """
    Send notification about new process update.
    """
    assunto = f"⚖️ Atualização no processo {cnj}"
    
    mov_data = ultima_movimentacao.get("data", "N/A")
    mov_desc = ultima_movimentacao.get("descricao", "N/A")
    
    corpo = f"""
Olá!

Há uma atualização no processo que você está acompanhando:

📋 Processo: {cnj}
📅 Data: {mov_data}
📝 Descrição: {mov_desc}

Acesse {cnj} para ver mais detalhes.

---
JUS CRAWLER - Notificações Automáticas
Este é um email automático. Não responda diretamente.
"""
    base = os.getenv("APP_BASE_URL", "http://localhost:8000")
    unsubscribe_url = f"{base}/unsubscribe?cnj={quote_plus(cnj)}&email={quote_plus(contato)}"
    corpo += f"\nCancelar inscrição: {unsubscribe_url}\n"

    cfg = _smtp_config()
    if not cfg["user"] or not cfg["password"]:
        # Demo mode: log to file
        log_path = "/tmp/juscrawler_notifications.log"
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"  To: {contato}\n")
                f.write(f"  Subject: {assunto}\n")
                f.write(f"  Process: {cnj}\n")
                f.write(f"  Movement: {mov_data} - {mov_desc[:50]}...\n")
            return True
        except Exception as e:
            print(f"✗ Erro ao registrar notificação de atualização: {e}")
            return False
    
    # Production mode: send via SMTP
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = assunto
        msg["From"] = cfg["sender"]
        msg["To"] = contato
        
        part = MIMEText(corpo, "plain", "utf-8")
        msg.attach(part)
        
        with smtplib.SMTP(cfg["server"], cfg["port"], timeout=10) as server:
            server.starttls()
            server.login(cfg["user"], cfg["password"])
            server.sendmail(cfg["sender"], contato, msg.as_string())
        
        return True
    except Exception as e:
        print(f"✗ Erro ao enviar notificação para {contato}: {e}")
        return False
