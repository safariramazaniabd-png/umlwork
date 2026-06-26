from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.database import get_db
from app.models.paiement import Paiement, StatutPaiement
from app.models.don import Don
from app.schemas.paiement import PaiementCreate, PaiementResponse, PaiementList

router = APIRouter()


@router.post("/", response_model=PaiementResponse, status_code=status.HTTP_201_CREATED)
async def create_paiement(data: PaiementCreate, db: AsyncSession = Depends(get_db)):
    don = await db.execute(select(Don).where(Don.id == data.don_id))
    if not don.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Don introuvable")

    paiement = Paiement(
        reference=str(uuid.uuid4()),
        methode=data.methode,
        montant=data.montant,
        don_id=data.don_id,
        code_pays=data.code_pays,
    )
    db.add(paiement)
    await db.commit()
    await db.refresh(paiement)
    return paiement


@router.get("/", response_model=PaiementList)
async def list_paiements(
    skip: int = 0,
    limit: int = 100,
    statut: StatutPaiement | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Paiement)
    if statut:
        query = query.where(Paiement.statut == statut)
    count_q = select(func.count(Paiement.id))
    if statut:
        count_q = count_q.where(Paiement.statut == statut)
    total = (await db.execute(count_q)).scalar()
    result = await db.execute(query.offset(skip).limit(limit))
    items = result.scalars().all()
    return PaiementList(items=items, total=total)


@router.get("/{paiement_id}", response_model=PaiementResponse)
async def get_paiement(paiement_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Paiement).where(Paiement.id == paiement_id))
    paiement = result.scalar_one_or_none()
    if not paiement:
        raise HTTPException(status_code=404, detail="Paiement introuvable")
    return paiement
