"""create centres_cout and budget_lines

Revision ID: 686f26c8f875
Revises:
Create Date: 2026-08-12 10:47:19.975591

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '686f26c8f875'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "centres_cout",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nom", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_centres_cout_nom", "centres_cout", ["nom"], unique=True)

    op.create_table(
        "budget_lines",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "centre_cout_id",
            sa.Integer(),
            sa.ForeignKey("centres_cout.id"),
            nullable=False,
        ),
        sa.Column("exercice", sa.Integer(), nullable=False),
        sa.Column("periode", sa.String(length=7), nullable=False),
        sa.Column("montant_prevu", sa.Numeric(12, 2), nullable=False),
        sa.Column("montant_reestime", sa.Numeric(12, 2), nullable=True),
        sa.Column("montant_realise", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_budget_lines_centre_cout_id", "budget_lines", ["centre_cout_id"])
    op.create_index("ix_budget_lines_exercice", "budget_lines", ["exercice"])
    op.create_index("ix_budget_lines_periode", "budget_lines", ["periode"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_budget_lines_periode", table_name="budget_lines")
    op.drop_index("ix_budget_lines_exercice", table_name="budget_lines")
    op.drop_index("ix_budget_lines_centre_cout_id", table_name="budget_lines")
    op.drop_table("budget_lines")
    op.drop_index("ix_centres_cout_nom", table_name="centres_cout")
    op.drop_table("centres_cout")
