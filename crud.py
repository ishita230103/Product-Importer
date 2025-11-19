from sqlalchemy.orm import Session
from backend.app.db.models import Product, Webhook
from backend.app.utils import normalize_sku


# --------------------------------------------------------
# UPSERT PRODUCTS (no price field)
# --------------------------------------------------------
def upsert_batch(session: Session, items):

    sku_lowers = [normalize_sku(i["sku"]) for i in items]

    existing_products = (
        session.query(Product)
        .filter(Product.sku_lower.in_(sku_lowers))
        .all()
    )

    existing_map = {p.sku_lower: p for p in existing_products}

    for item in items:
        sku_lower = item["sku_lower"]

        if sku_lower in existing_map:
            # UPDATE existing
            p = existing_map[sku_lower]
            p.sku = item["sku"]
            p.name = item["name"]
            p.description = item["description"]
            p.active = item["active"]
        else:
            # INSERT new
            session.add(Product(**item))

    session.commit()


# --------------------------------------------------------
# PRODUCT LIST / COUNT / DELETE
# --------------------------------------------------------
def get_products(session: Session, skip: int, limit: int):
    return (
        session.query(Product)
        .order_by(Product.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_products(session: Session):
    return session.query(Product).count()


def delete_all_products(session: Session):
    session.query(Product).delete()
    session.commit()


# --------------------------------------------------------
# WEBHOOK CRUD  (this was missing in your file!)
# --------------------------------------------------------
def create_webhook(session: Session, data: dict):
    w = Webhook(**data)
    session.add(w)
    session.commit()
    session.refresh(w)
    return w


def list_webhooks(session: Session):
    return session.query(Webhook).order_by(Webhook.id).all()


def update_webhook(session: Session, webhook_id: int, data: dict):
    w = session.query(Webhook).get(webhook_id)
    if not w:
        return None

    for k, v in data.items():
        setattr(w, k, v)

    session.commit()
    session.refresh(w)
    return w


def delete_webhook(session: Session, webhook_id: int):
    w = session.query(Webhook).get(webhook_id)
    if not w:
        return False

    session.delete(w)
    session.commit()
    return True

# --------------------------------------------------------
# WEBHOOK CRUD HELPERS
# --------------------------------------------------------

def get_webhook_by_id(session, webhook_id: int):
    return session.query(Webhook).filter(Webhook.id == webhook_id).first()


def delete_webhook_by_id(session, webhook_id: int):
    obj = session.query(Webhook).filter(Webhook.id == webhook_id).first()
    if not obj:
        return False
    session.delete(obj)
    session.commit()
    return True

