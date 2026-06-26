from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Recu(Base):
    __tablename__ = "recus"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    numero: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    date_emission: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    montant: Mapped[float] = mapped_column(Float, nullable=False)
    donateur_nom: Mapped[str] = mapped_column(String(200), nullable=False)
    campagne_titre: Mapped[str] = mapped_column(String(200), nullable=False)
    don_id: Mapped[int] = mapped_column(Integer, ForeignKey("dons.id"), unique=True, nullable=False)
    envoye: Mapped[bool] = mapped_column(Boolean, default=False)
    pdf_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    don: Mapped["Don"] = relationship("Don", back_populates="recu")
