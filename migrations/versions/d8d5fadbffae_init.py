"""init

Revision ID: d8d5fadbffae
Revises: 
Create Date: 2022-09-17 23:25:52.195467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8d5fadbffae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'car',
        sa.Column('id', sa.String(6), primary_key=True),
        sa.Column('model', sa.String, nullable=False),
        sa.Column('owner', sa.String, nullable=False),
        sa.Column('mileage', sa.Integer, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('car')
