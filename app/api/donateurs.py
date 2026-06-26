from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.hash import bcrypt

from app.database import get_db
from app.models.donateur import Donateur
from app.schemas.donateur import DonateurCreate, DonateurResponse, DonateurUpdate, DonateurList

router = APIRouter()


@router.post("/", response_model=DonateurResponse, status_code=status.HTTP_201_CREATED)
async def create_donateur(data: DonateurCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Donateur).where(Donateur.email == data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    donateur = Donateur(
        nom=data.nom,
        prenom=data.prenom,
        email=data.email,
        telephone=data.telephone,
        pays=data.pays,
        mot_de_passe=bcrypt.hash(data.mot_de_passe),
        type_compte=data.type_compte,
    )
    db.add(donateur)
    await db.commit()
    await db.refresh(donateur)
    return donateur


@router.get("/", response_model=DonateurList)
async def list_donateurs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    count_q = select(func.count(Donateur.id))
    total = (await db.execute(count_q)).scalar()
    result = await db.execute(select(Donateur).offset(skip).limit(limit))
    items = result.scalars().all()
    return DonateurList(items=items, total=total)


@router.get("/{donateur_id}", response_model=DonateurResponse)
async def get_donateur(donateur_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Donateur).where(Donateur.id == donateur_id))
    donateur = result.scalar_one_or_none()
    if not donateur:
        raise HTTPException(status_code=404, detail="Donateur introuvable")
    return donateur


@router.patch("/{donateur_id}", response_model=DonateurResponse)
async def update_donateur(
    donateur_id: int,
    data: DonateurUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Donateur).where(Donateur.id == donateur_id))
    donateur = result.scalar_one_or_none()
    if not donateur:
        raise HTTPException(status_code=404, detail="Donateur introuvable")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(donateur, key, value)

    await db.commit()
    await db.refresh(donateur)
    return donateur


@router.delete("/{donateur_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_donateur(donateur_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Donateur).where(Donateur.id == donateur_id))
    donateur = result.scalar_one_or_none()
    if not donateur:
        raise HTTPException(status_code=404, detail="Donateur introuvable")
    await db.delete(donateur)
    await db.commit()
