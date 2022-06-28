"""create tebles

Revision ID: ce09fc723e4b
Revises: 
Create Date: 2022-06-26 18:53:53.936897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce09fc723e4b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
                    sa.Column('email', sa.String(length=40), nullable=True),
                    sa.Column('name', sa.String(length=100), nullable=True),
                    sa.Column('hashed_password', sa.String(), nullable=True),
                    sa.Column('removed', sa.Boolean(), default=False, nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('user_balance',
                    sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
                    sa.Column('balance', sa.Float(), default=0, nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('removed', sa.Boolean(), default=False, nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    pass
