"""Add location fields to Order model

Revision ID: bd13d0f8a703
Revises: 
Create Date: 2024-06-08 16:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd13d0f8a703'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Добавляем новые колонки в таблицу order
    op.add_column('order', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('order', sa.Column('longitude', sa.Float(), nullable=True))
    op.add_column('order', sa.Column('address', sa.String(length=256), nullable=True))


def downgrade():
    # Удаляем добавленные колонки
    op.drop_column('order', 'address')
    op.drop_column('order', 'longitude')
    op.drop_column('order', 'latitude')
