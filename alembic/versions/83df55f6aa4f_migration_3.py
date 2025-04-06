"""migration №3

Revision ID: 83df55f6aa4f
Revises: afee2357baa9
Create Date: 2025-04-06 15:09:25.960862

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "83df55f6aa4f"
down_revision: str | None = "afee2357baa9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("log", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "event",
                sa.Enum("created", "read", "deleted", name="event"),
                nullable=False,
            )
        )
        batch_op.alter_column(
            "id", existing_type=sa.NUMERIC(), type_=sa.UUID(), existing_nullable=False
        )
        batch_op.drop_column("status")

    with op.batch_alter_table("secret", schema=None) as batch_op:
        batch_op.alter_column(
            "id", existing_type=sa.NUMERIC(), type_=sa.UUID(), existing_nullable=False
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("secret", schema=None) as batch_op:
        batch_op.alter_column(
            "id", existing_type=sa.UUID(), type_=sa.NUMERIC(), existing_nullable=False
        )

    with op.batch_alter_table("log", schema=None) as batch_op:
        batch_op.add_column(sa.Column("status", sa.VARCHAR(length=7), nullable=False))
        batch_op.alter_column(
            "id", existing_type=sa.UUID(), type_=sa.NUMERIC(), existing_nullable=False
        )
        batch_op.drop_column("event")

    # ### end Alembic commands ###
