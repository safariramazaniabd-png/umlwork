import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class StatutCampagne(str, enum.Enum):
    active = "active"
    cloturee = "cloturee"
    suspendue = "suspendue"


class Campagne(Base):
    __tablename__ = "campagnes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    titre: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    objectif: Mapped[float] = mapped_column(Float, nullable=False)
    montant_collecte: Mapped[float] = mapped_column(Float, default=0.0)
    date_debut: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    date_fin: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    statut: Mapped[StatutCampagne] = mapped_column(Enum(StatutCampagne), default=StatutCampagne.active)
    cree_par: Mapped[str] = mapped_column(String(100), nullable=False)
    date_creation: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    dons: Mapped[list["Don"]] = relationship("Don", back_populates="campagne", cascade="all, delete-orphan")
