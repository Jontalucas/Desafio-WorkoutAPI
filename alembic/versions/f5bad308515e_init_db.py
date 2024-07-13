"""init_db

Revision ID: f5bad308515e
Revises: 
Create Date: 2024-07-13 01:51:56.181227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5bad308515e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categoria',
    sa.Column('pk_id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=10), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('pk_id'),
    sa.UniqueConstraint('nome')
    )
    op.create_table('centro_treinamento',
    sa.Column('pk_id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=20), nullable=False),
    sa.Column('endereco', sa.String(length=60), nullable=False),
    sa.Column('proprietario', sa.String(length=30), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('pk_id')
    )
    op.create_table('atletas',
    sa.Column('pk_id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=50), nullable=False),
    sa.Column('cpf', sa.String(length=11), nullable=False),
    sa.Column('idade', sa.Integer(), nullable=False),
    sa.Column('peso', sa.Float(), nullable=False),
    sa.Column('altura', sa.Float(), nullable=False),
    sa.Column('sexo', sa.String(length=1), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('categoria_id', sa.Integer(), nullable=False),
    sa.Column('centro_treinamento_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['categoria_id'], ['categoria.pk_id'], ),
    sa.ForeignKeyConstraint(['centro_treinamento_id'], ['centro_treinamento.pk_id'], ),
    sa.PrimaryKeyConstraint('pk_id'),
    sa.UniqueConstraint('cpf')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('atletas')
    op.drop_table('centro_treinamento')
    op.drop_table('categoria')
    # ### end Alembic commands ###