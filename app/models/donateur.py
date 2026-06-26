import enum
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class TypeCompte(str, enum.Enum):
    anonyme = "anonyme"
    enregistre = "enregistre"


class Donateur(Base):
    __tablename__ = "donateurs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    prenom: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    telephone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    pays: Mapped[str | None] = mapped_column(String(100), nullable=True)
    mot_de_passe: Mapped[str] = mapped_column(String(255), nullable=False)
    type_compte: Mapped[TypeCompte] = mapped_column(Enum(TypeCompte), default=TypeCompte.enregistre)
    date_inscription: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    est_actif: Mapped[bool] = mapped_column(Boolean, default=True)

    dons: Mapped[list["Don"]] = relationship("Don", back_populates="donateur", cascade="all, delete-orphan")
