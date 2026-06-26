from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.models.donateur import TypeCompte


class DonateurBase(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    telephone: str | None = None
    pays: str | None = None


class DonateurCreate(DonateurBase):
    mot_de_passe: str
    type_compte: TypeCompte = TypeCompte.enregistre


class DonateurUpdate(BaseModel):
    nom: str | None = None
    prenom: str | None = None
    telephone: str | None = None
    pays: str | None = None


class DonateurResponse(DonateurBase):
    id: int
    type_compte: TypeCompte
    date_inscription: datetime
    est_actif: bool

    model_config = {"from_attributes": True}


class DonateurList(BaseModel):
    items: list[DonateurResponse]
    total: int
