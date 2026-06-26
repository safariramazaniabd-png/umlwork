from datetime import datetime

from pydantic import BaseModel

from app.models.paiement import MethodePaiement, StatutPaiement


class PaiementBase(BaseModel):
    methode: MethodePaiement
    montant: float
    don_id: int
    code_pays: str | None = None


class PaiementCreate(PaiementBase):
    pass


class PaiementResponse(PaiementBase):
    id: int
    reference: str
    statut: StatutPaiement
    date_transaction: datetime

    model_config = {"from_attributes": True}


class PaiementList(BaseModel):
    items: list[PaiementResponse]
    total: int
