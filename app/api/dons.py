from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.don import Don
from app.models.donateur import Donateur
from app.models.campagne import Campagne
from app.schemas.don import DonCreate, DonResponse, DonList

router = APIRouter()


@router.post("/", response_model=DonResponse, status_code=status.HTTP_201_CREATED)
async def create_don(data: DonCreate, db: AsyncSession = Depends(get_db)):
    donateur = await db.execute(select(Donateur).where(Donateur.id == data.donateur_id))
    if not donateur.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Donateur introuvable")

    campagne = await db.execute(select(Campagne).where(Campagne.id == data.campagne_id))
    campagne_obj = campagne.scalar_one_or_none()
    if not campagne_obj:
        raise HTTPException(status_code=404, detail="Campagne introuvable")

    don = Don(
        montant=data.montant,
        devise=data.devise,
        frequence=data.frequence,
        message=data.message,
        donateur_id=data.donateur_id,
        campagne_id=data.campagne_id,
    )
    db.add(don)
    await db.commit()
    await db.refresh(don)
    return don


@router.get("/", response_model=DonList)
async def list_dons(
    skip: int = 0,
    limit: int = 100,
    donateur_id: int | None = None,
    campagne_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Don)
    if donateur_id:
        query = query.where(Don.donateur_id == donateur_id)
    if campagne_id:
        query = query.where(Don.campagne_id == campagne_id)
    count_q = select(func.count(Don.id))
    if donateur_id:
        count_q = count_q.where(Don.donateur_id == donateur_id)
    if campagne_id:
        count_q = count_q.where(Don.campagne_id == campagne_id)
    total = (await db.execute(count_q)).scalar()
    result = await db.execute(query.offset(skip).limit(limit))
    items = result.scalars().all()
    return DonList(items=items, total=total)


@router.get("/{don_id}", response_model=DonResponse)
async def get_don(don_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Don).where(Don.id == don_id))
    don = result.scalar_one_or_none()
    if not don:
        raise HTTPException(status_code=404, detail="Don introuvable")
    return don


@router.delete("/{don_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_don(don_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Don).where(Don.id == don_id))
    don = result.scalar_one_or_none()
    if not don:
        raise HTTPException(status_code=404, detail="Don introuvable")
    await db.delete(don)
    await db.commit()
