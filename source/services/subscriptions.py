import json
import sqlite3
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "subscriptions.db"
LEGACY_JSON_PATH = DATA_DIR / "subscriptions.json"

_initialized = False


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_schema(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS subscriptions (
            id TEXT PRIMARY KEY,
            cnj TEXT NOT NULL,
            contato TEXT NOT NULL,
            tipo TEXT NOT NULL,
            ultimo_mov_data TEXT,
            ultimo_mov_descricao TEXT,
            ativo INTEGER NOT NULL DEFAULT 1,
            criado_em TEXT NOT NULL,
            atualizado_em TEXT NOT NULL,
            UNIQUE(cnj, contato)
        )
        """
    )
    conn.commit()


def _migrate_legacy_json(conn):
    if not LEGACY_JSON_PATH.exists():
        return
    try:
        with open(LEGACY_JSON_PATH, "r", encoding="utf-8") as f:
            items = json.load(f)
    except Exception:
        return

    for item in items:
        now = datetime.utcnow().isoformat()
        conn.execute(
            """
            INSERT OR IGNORE INTO subscriptions (
                id, cnj, contato, tipo, ultimo_mov_data, ultimo_mov_descricao,
                ativo, criado_em, atualizado_em
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item.get("id") or f"sub_{int(datetime.utcnow().timestamp())}",
                item.get("cnj", "").strip(),
                item.get("contato", "").strip(),
                item.get("tipo", "email").strip().lower() or "email",
                item.get("ultimo_mov_data"),
                item.get("ultimo_mov_descricao"),
                1 if item.get("ativo", True) else 0,
                item.get("criado_em") or now,
                item.get("atualizado_em") or now,
            ),
        )
    conn.commit()


def _init_db_once():
    global _initialized
    if _initialized:
        return
    with _connect() as conn:
        _ensure_schema(conn)
        _migrate_legacy_json(conn)
    _initialized = True


def add_subscription(cnj: str, contato: str, tipo: str = 'email'):
    """Add subscription if not exists. Returns (True, message) or (False, message)."""
    _init_db_once()
    cnj = cnj.strip()
    contato = contato.strip()
    tipo = 'email'  # Only email supported

    if not cnj or not contato:
        return False, "Dados inválidos para inscrição"

    now = datetime.utcnow().isoformat()
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, ativo FROM subscriptions WHERE cnj = ? AND contato = ?",
            (cnj, contato),
        ).fetchone()

        if row:
            if int(row["ativo"]) == 1:
                return False, "Você já está inscrito para este contato."
            conn.execute(
                """
                UPDATE subscriptions
                SET ativo = 1, tipo = ?, atualizado_em = ?
                WHERE id = ?
                """,
                (tipo, now, row["id"]),
            )
            conn.commit()
            return True, "Inscrição reativada com sucesso"

        subscription_id = f"sub_{int(datetime.utcnow().timestamp() * 1000)}"
        conn.execute(
            """
            INSERT INTO subscriptions (
                id, cnj, contato, tipo, ultimo_mov_data, ultimo_mov_descricao,
                ativo, criado_em, atualizado_em
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (subscription_id, cnj, contato, tipo, None, None, 1, now, now),
        )
        conn.commit()

    return True, "Inscrição realizada com sucesso. Você receberá notificações por {}.".format(tipo)


def list_subscriptions():
    _init_db_once()
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT id, cnj, contato, tipo, ultimo_mov_data, ultimo_mov_descricao,
                   ativo, criado_em, atualizado_em
            FROM subscriptions
            ORDER BY criado_em DESC
            """
        ).fetchall()

    return [
        {
            "id": row["id"],
            "cnj": row["cnj"],
            "contato": row["contato"],
            "tipo": row["tipo"],
            "ultimo_mov_data": row["ultimo_mov_data"],
            "ultimo_mov_descricao": row["ultimo_mov_descricao"],
            "ativo": bool(row["ativo"]),
            "criado_em": row["criado_em"],
            "atualizado_em": row["atualizado_em"],
        }
        for row in rows
    ]


def deactivate_subscription(subscription_id: str):
    _init_db_once()
    now = datetime.utcnow().isoformat()
    with _connect() as conn:
        cursor = conn.execute(
            """
            UPDATE subscriptions
            SET ativo = 0, atualizado_em = ?
            WHERE id = ?
            """,
            (now, subscription_id),
        )
        conn.commit()
        return cursor.rowcount > 0
