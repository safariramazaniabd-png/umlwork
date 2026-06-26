from datetime import datetime

from pydantic import BaseModel

from app.models.campagne import StatutCampagne


class CampagneBase(BaseModel):
    titre: str
    description: str | None = None
    objectif: float
    date_debut: datetime
    date_fin: datetime


class CampagneCreate(CampagneBase):
    pass


class CampagneUpdate(BaseModel):
    titre: str | None = None
    description: str | None = None
    objectif: float | None = None
    date_debut: datetime | None = None
    date_fin: datetime | None = None
    statut: StatutCampagne | None = None


class CampagneResponse(CampagneBase):
    id: int
    montant_collecte: float
    statut: StatutCampagne
    cree_par: str
    date_creation: datetime
    progression: float = 0.0

    model_config = {"from_attributes": True}


class CampagneList(BaseModel):
    items: list[CampagneResponse]
    total: int
