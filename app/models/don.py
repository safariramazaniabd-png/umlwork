import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class FrequenceDon(str, enum.Enum):
    ponctuel = "ponctuel"
    mensuel = "mensuel"
    annuel = "annuel"


class StatutDon(str, enum.Enum):
    en_attente = "en_attente"
    confirme = "confirme"
    annule = "annule"
    echoue = "echoue"


class Don(Base):
    __tablename__ = "dons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    montant: Mapped[float] = mapped_column(Float, nullable=False)
    devise: Mapped[str] = mapped_column(String(3), default="EUR")
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    frequence: Mapped[FrequenceDon] = mapped_column(Enum(FrequenceDon), default=FrequenceDon.ponctuel)
    statut: Mapped[StatutDon] = mapped_column(Enum(StatutDon), default=StatutDon.en_attente)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    donateur_id: Mapped[int] = mapped_column(Integer, ForeignKey("donateurs.id"), nullable=False)
    campagne_id: Mapped[int] = mapped_column(Integer, ForeignKey("campagnes.id"), nullable=False)

    donateur: Mapped["Donateur"] = relationship("Donateur", back_populates="dons")
    campagne: Mapped["Campagne"] = relationship("Campagne", back_populates="dons")
    paiement: Mapped["Paiement"] = relationship("Paiement", back_populates="don", uselist=False, cascade="all, delete-orphan")
    recu: Mapped["Recu | None"] = relationship("Recu", back_populates="don", uselist=False, cascade="all, delete-orphan")
