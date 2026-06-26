"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-06-26
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "donateurs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nom", sa.String(100), nullable=False),
        sa.Column("prenom", sa.String(100), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("telephone", sa.String(20), nullable=True),
        sa.Column("pays", sa.String(100), nullable=True),
        sa.Column("mot_de_passe", sa.String(255), nullable=False),
        sa.Column(
            "type_compte",
            sa.Enum("anonyme", "enregistre", name="typecompte"),
            nullable=False,
        ),
        sa.Column("date_inscription", sa.DateTime(timezone=True), nullable=False),
        sa.Column("est_actif", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_donateurs_email", "donateurs", ["email"], unique=True)
    op.create_index("ix_donateurs_id", "donateurs", ["id"])

    op.create_table(
        "campagnes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("titre", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("objectif", sa.Float(), nullable=False),
        sa.Column("montant_collecte", sa.Float(), nullable=False),
        sa.Column("date_debut", sa.DateTime(timezone=True), nullable=False),
        sa.Column("date_fin", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "statut",
            sa.Enum("active", "cloturee", "suspendue", name="statutcampagne"),
            nullable=False,
        ),
        sa.Column("cree_par", sa.String(100), nullable=False),
        sa.Column("date_creation", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_campagnes_id", "campagnes", ["id"])

    op.create_table(
        "dons",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("montant", sa.Float(), nullable=False),
        sa.Column("devise", sa.String(3), nullable=False),
        sa.Column("date", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "frequence",
            sa.Enum("ponctuel", "mensuel", "annuel", name="frequencedon"),
            nullable=False,
        ),
        sa.Column(
            "statut",
            sa.Enum("en_attente", "confirme", "annule", "echoue", name="statutdon"),
            nullable=False,
        ),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("donateur_id", sa.Integer(), nullable=False),
        sa.Column("campagne_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["donateur_id"], ["donateurs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["campagne_id"], ["campagnes.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_dons_id", "dons", ["id"])

    op.create_table(
        "paiements",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("reference", sa.String(100), nullable=False),
        sa.Column(
            "methode",
            sa.Enum("carte", "paypal", "virement", name="methodepaiement"),
            nullable=False,
        ),
        sa.Column("montant", sa.Float(), nullable=False),
        sa.Column(
            "statut",
            sa.Enum("initie", "valide", "echoue", "rembourse", name="statutpaiement"),
            nullable=False,
        ),
        sa.Column("date_transaction", sa.DateTime(timezone=True), nullable=False),
        sa.Column("don_id", sa.Integer(), nullable=False),
        sa.Column("code_pays", sa.String(3), nullable=True),
        sa.ForeignKeyConstraint(["don_id"], ["dons.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_paiements_id", "paiements", ["id"])
    op.create_index("ix_paiements_reference", "paiements", ["reference"], unique=True)

    op.create_table(
        "recus",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("numero", sa.String(50), nullable=False),
        sa.Column("date_emission", sa.DateTime(timezone=True), nullable=False),
        sa.Column("montant", sa.Float(), nullable=False),
        sa.Column("donateur_nom", sa.String(200), nullable=False),
        sa.Column("campagne_titre", sa.String(200), nullable=False),
        sa.Column("don_id", sa.Integer(), nullable=False),
        sa.Column("envoye", sa.Boolean(), nullable=False),
        sa.Column("pdf_url", sa.String(500), nullable=True),
        sa.ForeignKeyConstraint(["don_id"], ["dons.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_recus_id", "recus", ["id"])
    op.create_index("ix_recus_numero", "recus", ["numero"], unique=True)


def downgrade() -> None:
    op.drop_table("recus")
    op.drop_table("paiements")
    op.drop_table("dons")
    op.drop_table("campagnes")
    op.drop_table("donateurs")

    op.execute("DROP TYPE IF EXISTS statutrecu")
    op.execute("DROP TYPE IF EXISTS statutpaiement")
    op.execute("DROP TYPE IF EXISTS methodepaiement")
    op.execute("DROP TYPE IF EXISTS statutdon")
    op.execute("DROP TYPE IF EXISTS frequencedon")
    op.execute("DROP TYPE IF EXISTS statutcampagne")
    op.execute("DROP TYPE IF EXISTS typecompte")
