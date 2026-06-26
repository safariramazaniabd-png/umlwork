from datetime import datetime

from pydantic import BaseModel


class RecuBase(BaseModel):
    don_id: int


class RecuResponse(BaseModel):
    id: int
    numero: str
    date_emission: datetime
    montant: float
    donateur_nom: str
    campagne_titre: str
    envoye: bool
    pdf_url: str | None = None

    model_config = {"from_attributes": True}


class RecuList(BaseModel):
    items: list[RecuResponse]
    total: int
