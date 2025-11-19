from backend.app.tasks.celery_app import celery
from backend.app.db.base import SessionLocal
from backend.app.db.crud import upsert_batch
from backend.app.services.csv_processor import stream_csv_rows
from backend.app.utils import normalize_sku
from backend.app.config import settings
import redis
import json

r = redis.from_url(settings.REDIS_URL)


@celery.task(bind=True)
def import_csv_task(self, path, job_id):

    # ------- Count total rows (ignore header + empty lines) -------
    total = 0
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.strip():
                total += 1
    total = max(total - 1, 0)

    db = SessionLocal()
    processed = 0
    batch = []

    PROGRESS_INTERVAL = getattr(settings, "PROGRESS_INTERVAL", 200)

    # ------- Process CSV rows -------
    for row in stream_csv_rows(path):

        row = {k.lower().strip(): v for k, v in row.items()}

        processed += 1

        sku_val = row.get("sku", "")
        if not sku_val.strip():
            continue

        item = {
            "sku": sku_val.strip(),
            "sku_lower": normalize_sku(sku_val),
            "name": row.get("name", "").strip(),
            "description": row.get("description", "").strip(),
            "active": True,
        }

        batch.append(item)

        if len(batch) >= settings.BATCH_SIZE:
            upsert_batch(db, batch)
            batch = []

        if processed % PROGRESS_INTERVAL == 0:
            r.publish(
                f"progress:{job_id}",
                json.dumps({"processed": processed, "total": total})
            )

    if batch:
        upsert_batch(db, batch)

    r.publish(
        f"progress:{job_id}",
        json.dumps({"processed": processed, "total": total, "status": "complete"})
    )

    return {"processed": processed, "total": total}
