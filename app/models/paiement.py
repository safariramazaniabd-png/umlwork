import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class MethodePaiement(str, enum.Enum):
    carte = "carte"
    paypal = "paypal"
    virement = "virement"


class StatutPaiement(str, enum.Enum):
    initie = "initie"
    valide = "valide"
    echoue = "echoue"
    rembourse = "rembourse"


class Paiement(Base):
    __tablename__ = "paiements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    reference: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    methode: Mapped[MethodePaiement] = mapped_column(Enum(MethodePaiement), nullable=False)
    montant: Mapped[float] = mapped_column(Float, nullable=False)
    statut: Mapped[StatutPaiement] = mapped_column(Enum(StatutPaiement), default=StatutPaiement.initie)
    date_transaction: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    don_id: Mapped[int] = mapped_column(Integer, ForeignKey("dons.id"), unique=True, nullable=False)
    code_pays: Mapped[str | None] = mapped_column(String(3), nullable=True)

    don: Mapped["Don"] = relationship("Don", back_populates="paiement")
