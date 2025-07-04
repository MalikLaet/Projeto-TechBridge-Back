"""create cursos table

Revision ID: 77038036c823
Revises: daa662ddbe05
Create Date: 2025-06-18 12:59:49.745217

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77038036c823'
down_revision: Union[str, None] = 'daa662ddbe05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cursos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('descricao', sa.String(), nullable=False),
    sa.Column('youtube_link', sa.String(), nullable=False),
    sa.Column('empresa_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['empresa_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cursos_id'), 'cursos', ['id'], unique=False)
    op.drop_column('users', 'created_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('created_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False))
    op.drop_index(op.f('ix_cursos_id'), table_name='cursos')
    op.drop_table('cursos')
    # ### end Alembic commands ###
