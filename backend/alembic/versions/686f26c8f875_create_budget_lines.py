"""create budget_lines

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
        "budget_lines",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("categorie", sa.String(length=100), nullable=False),
        sa.Column("montant_prevu", sa.Numeric(12, 2), nullable=False),
        sa.Column("montant_realise", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("periode", sa.String(length=7), nullable=False),
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
    op.create_index("ix_budget_lines_categorie", "budget_lines", ["categorie"])
    op.create_index("ix_budget_lines_periode", "budget_lines", ["periode"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_budget_lines_periode", table_name="budget_lines")
    op.drop_index("ix_budget_lines_categorie", table_name="budget_lines")
    op.drop_table("budget_lines")
