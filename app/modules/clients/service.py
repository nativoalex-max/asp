from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.clients.model import Client
from app.modules.clients.schema import ClientCreate, ClientUpdate


def get_clients(db: Session):
    return db.query(Client).order_by(Client.name).all()


def get_client_by_id(db: Session, client_id: UUID):
    return db.query(Client).filter(Client.id == client_id).first()


def get_client_by_code(db: Session, code: str):
    return db.query(Client).filter(Client.code == code).first()


def create_client(db: Session, client: ClientCreate):
    db_client = Client(
        name=client.name,
        code=client.code,
        description=client.description,
        contact_name=client.contact_name,
        contact_email=client.contact_email,
        contact_phone=client.contact_phone,
        is_active=client.is_active,
    )

    db.add(db_client)
    db.commit()
    db.refresh(db_client)

    return db_client


def update_client(
    db: Session,
    db_client: Client,
    client: ClientUpdate,
):
    data = client.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(db_client, key, value)

    db.commit()
    db.refresh(db_client)

    return db_client


def delete_client(
    db: Session,
    db_client: Client,
):
    db.delete(db_client)
    db.commit()
