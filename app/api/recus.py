from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.database import get_db
from app.models.recu import Recu
from app.models.don import Don
from app.models.donateur import Donateur
from app.models.campagne import Campagne
from app.schemas.recu import RecuBase, RecuResponse, RecuList

router = APIRouter()


@router.post("/", response_model=RecuResponse, status_code=status.HTTP_201_CREATED)
async def create_recu(data: RecuBase, db: AsyncSession = Depends(get_db)):
    don = await db.execute(
        select(Don).where(Don.id == data.don_id)
    )
    don_obj = don.scalar_one_or_none()
    if not don_obj:
        raise HTTPException(status_code=404, detail="Don introuvable")

    donateur = await db.execute(select(Donateur).where(Donateur.id == don_obj.donateur_id))
    donateur_obj = donateur.scalar_one()
    campagne = await db.execute(select(Campagne).where(Campagne.id == don_obj.campagne_id))
    campagne_obj = campagne.scalar_one()

    recu = Recu(
        numero=f"REC-{uuid.uuid4().hex[:8].upper()}",
        montant=don_obj.montant,
        donateur_nom=f"{donateur_obj.prenom} {donateur_obj.nom}",
        campagne_titre=campagne_obj.titre,
        don_id=data.don_id,
    )
    db.add(recu)
    await db.commit()
    await db.refresh(recu)
    return recu


@router.get("/", response_model=RecuList)
async def list_recus(
    skip: int = 0,
    limit: int = 100,
    donateur_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Recu)
    if donateur_id:
        query = query.join(Don).where(Don.donateur_id == donateur_id)

    count_q = select(func.count(Recu.id))
    if donateur_id:
        count_q = count_q.join(Don).where(Don.donateur_id == donateur_id)
    total = (await db.execute(count_q)).scalar()
    result = await db.execute(query.offset(skip).limit(limit))
    items = result.scalars().all()
    return RecuList(items=items, total=total)


@router.get("/{recu_id}", response_model=RecuResponse)
async def get_recu(recu_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Recu).where(Recu.id == recu_id))
    recu = result.scalar_one_or_none()
    if not recu:
        raise HTTPException(status_code=404, detail="Reçu introuvable")
    return recu
