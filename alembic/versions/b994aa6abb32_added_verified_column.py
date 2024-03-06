"""added verified column

Revision ID: b994aa6abb32
Revises: 3f6fcd15779c
Create Date: 2024-03-06 01:19:40.281948

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b994aa6abb32'
down_revision = '3f6fcd15779c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('verified', sa.Boolean(), server_default='FALSE', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'verified')
    # ### end Alembic commands ###