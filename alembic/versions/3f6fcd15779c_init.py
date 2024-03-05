"""init

Revision ID: 3f6fcd15779c
Revises: 
Create Date: 2024-03-05 01:56:16.195840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f6fcd15779c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('bio', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('gender', sa.Enum('male', 'female', 'other', name='gender'), nullable=True),
    sa.Column('pronouns', sa.String(), nullable=True),
    sa.Column('profile_image', sa.String(), nullable=True),
    sa.Column('role', sa.Enum('student', 'teacher', 'admin', name='role'), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('admin',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('contact', sa.String(), nullable=True),
    sa.Column('office', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id', 'user_id')
    )
    op.create_table('student',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('department', sa.Enum('science', 'management', 'arts', 'engineering', 'nursing', 'medicine', 'law', 'creative_studies', name='department'), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('degree', sa.Enum('bsc', 'ba', name='degree'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id', 'user_id')
    )
    op.create_table('teacher',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('faculty', sa.String(), nullable=True),
    sa.Column('office', sa.String(), nullable=True),
    sa.Column('contact', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teacher')
    op.drop_table('student')
    op.drop_table('admin')
    op.drop_table('user')
    # ### end Alembic commands ###