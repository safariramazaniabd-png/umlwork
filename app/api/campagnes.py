from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.campagne import Campagne, StatutCampagne
from app.schemas.campagne import CampagneCreate, CampagneResponse, CampagneUpdate, CampagneList

router = APIRouter()


@router.post("/", response_model=CampagneResponse, status_code=status.HTTP_201_CREATED)
async def create_campagne(data: CampagneCreate, db: AsyncSession = Depends(get_db)):
    campagne = Campagne(
        titre=data.titre,
        description=data.description,
        objectif=data.objectif,
        date_debut=data.date_debut,
        date_fin=data.date_fin,
        cree_par="admin",
    )
    db.add(campagne)
    await db.commit()
    await db.refresh(campagne)
    campagne.progression = (campagne.montant_collecte / campagne.objectif * 100) if campagne.objectif > 0 else 0.0
    return campagne


@router.get("/", response_model=CampagneList)
async def list_campagnes(
    skip: int = 0,
    limit: int = 100,
    statut: StatutCampagne | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Campagne)
    if statut:
        query = query.where(Campagne.statut == statut)
    count_q = select(func.count(Campagne.id))
    if statut:
        count_q = count_q.where(Campagne.statut == statut)
    total = (await db.execute(count_q)).scalar()
    result = await db.execute(query.offset(skip).limit(limit))
    items = result.scalars().all()
    for c in items:
        c.progression = (c.montant_collecte / c.objectif * 100) if c.objectif > 0 else 0.0
    return CampagneList(items=items, total=total)


@router.get("/{campagne_id}", response_model=CampagneResponse)
async def get_campagne(campagne_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Campagne).where(Campagne.id == campagne_id))
    campagne = result.scalar_one_or_none()
    if not campagne:
        raise HTTPException(status_code=404, detail="Campagne introuvable")
    campagne.progression = (campagne.montant_collecte / campagne.objectif * 100) if campagne.objectif > 0 else 0.0
    return campagne


@router.patch("/{campagne_id}", response_model=CampagneResponse)
async def update_campagne(
    campagne_id: int,
    data: CampagneUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Campagne).where(Campagne.id == campagne_id))
    campagne = result.scalar_one_or_none()
    if not campagne:
        raise HTTPException(status_code=404, detail="Campagne introuvable")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(campagne, key, value)

    await db.commit()
    await db.refresh(campagne)
    campagne.progression = (campagne.montant_collecte / campagne.objectif * 100) if campagne.objectif > 0 else 0.0
    return campagne


@router.delete("/{campagne_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campagne(campagne_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Campagne).where(Campagne.id == campagne_id))
    campagne = result.scalar_one_or_none()
    if not campagne:
        raise HTTPException(status_code=404, detail="Campagne introuvable")
    await db.delete(campagne)
    await db.commit()
