import os
import asyncio
import logging
from collections import defaultdict

from source.services.subscriptions import list_subscriptions, update_last_movement
from source.services.notifications import send_update_notification
from source.controller.processos import fetch_processo_info

logger = logging.getLogger(__name__)

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL_SECONDS", "43200"))  # default 12 hours


def set_interval_seconds(seconds: int):
    """Set the check interval (seconds) at runtime."""
    global CHECK_INTERVAL
    try:
        CHECK_INTERVAL = int(seconds)
    except Exception:
        pass


async def check_once(cnjs=None):
    """Run a single check iteration. If cnjs provided (list), check only those CNJs."""
    subs = list_subscriptions()
    by_cnj = defaultdict(list)
    for s in subs:
        if s.get("ativo"):
            by_cnj[s.get("cnj")].append(s)

    # if cnjs provided, filter
    if cnjs:
        requested = set(cnjs)
        by_cnj = {k: v for k, v in by_cnj.items() if k in requested}

    for cnj, sub_list in list(by_cnj.items()):
        try:
            data = await asyncio.to_thread(fetch_processo_info, cnj)
        except ValueError as e:
            logger.debug("Validation error for CNJ %s: %s", cnj, e)
            continue
        except Exception:
            logger.exception("Error fetching process %s", cnj)
            continue

        latest_mov = None
        for grau, grau_data in data.items():
            if grau == "id":
                continue
            movs = []
            if isinstance(grau_data, dict):
                movs = grau_data.get("movimentações") or grau_data.get("movimentacoes") or []
            if movs:
                candidate = movs[0]
                if candidate and isinstance(candidate, dict):
                    latest_mov = candidate
                    break

        if not latest_mov:
            continue

        mov_data = latest_mov.get("data")
        mov_desc = latest_mov.get("descricao") or latest_mov.get("descricao_simplificada") or ""

        for s in sub_list:
            if s.get("ultimo_mov_data") != mov_data or s.get("ultimo_mov_descricao") != mov_desc:
                update_last_movement(s.get("id"), mov_data, mov_desc)
                send_update_notification(s.get("contato"), cnj, s.get("tipo", "email"), {"data": mov_data, "descricao": mov_desc})


async def _check_loop(app):
    logger.info("Scheduler loop started, interval=%s seconds", CHECK_INTERVAL)
    try:
        while True:
            try:
                subs = list_subscriptions()
                # group subscriptions by cnj to avoid duplicate fetches
                by_cnj = defaultdict(list)
                for s in subs:
                    if s.get("ativo"):
                        by_cnj[s.get("cnj")].append(s)

                for cnj, sub_list in by_cnj.items():
                    # fetch process data in thread to avoid blocking
                    try:
                        data = await asyncio.to_thread(fetch_processo_info, cnj)
                    except ValueError as e:
                        logger.warning("Validation error for CNJ %s: %s", cnj, e)
                        continue
                    except Exception:
                        logger.exception("Error fetching process %s", cnj)
                        continue
                    # data is a dict per grau
                    latest_mov = None
                    # try to find the most recent movimentacao across degrees
                    for grau, grau_data in data.items():
                        if grau == "id":
                            continue
                        movs = []
                        if isinstance(grau_data, dict):
                            movs = grau_data.get("movimentações") or grau_data.get("movimentacoes") or []
                        if movs:
                            # assume first is newest
                            candidate = movs[0]
                            if candidate and isinstance(candidate, dict):
                                # pick the first non-empty
                                latest_mov = candidate
                                break

                    if not latest_mov:
                        continue

                    mov_data = latest_mov.get("data")
                    mov_desc = latest_mov.get("descricao") or latest_mov.get("descricao_simplificada") or ""

                    # notify subscribers where stored last movement differs
                    for s in sub_list:
                        if s.get("ultimo_mov_data") != mov_data or s.get("ultimo_mov_descricao") != mov_desc:
                            # update DB
                            update_last_movement(s.get("id"), mov_data, mov_desc)
                            # send notification
                            send_update_notification(s.get("contato"), cnj, s.get("tipo", "email"), {"data": mov_data, "descricao": mov_desc})

            except Exception as e:
                logger.exception("Error in scheduler iteration: %s", e)

            await asyncio.sleep(CHECK_INTERVAL)
    except asyncio.CancelledError:
        logger.info("Scheduler loop cancelled")


def start_scheduler(app):
    loop = asyncio.get_event_loop()
    task = loop.create_task(_check_loop(app))
    app.state._subscription_task = task


def stop_scheduler(app):
    task = getattr(app.state, "_subscription_task", None)
    if task:
        task.cancel()
