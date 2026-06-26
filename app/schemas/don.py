from datetime import datetime

from pydantic import BaseModel

from app.models.don import FrequenceDon, StatutDon


class DonBase(BaseModel):
    montant: float
    devise: str = "EUR"
    frequence: FrequenceDon = FrequenceDon.ponctuel
    message: str | None = None
    campagne_id: int


class DonCreate(DonBase):
    donateur_id: int


class DonResponse(DonBase):
    id: int
    date: datetime
    statut: StatutDon
    donateur_id: int

    model_config = {"from_attributes": True}


class DonList(BaseModel):
    items: list[DonResponse]
    total: int
