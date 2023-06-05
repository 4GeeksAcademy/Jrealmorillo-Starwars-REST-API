"""empty message

Revision ID: 01494e236f98
Revises: 648c82eb0086
Create Date: 2023-06-05 08:17:47.195580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01494e236f98'
down_revision = '648c82eb0086'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=120), nullable=False))
        batch_op.create_unique_constraint(None, ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('name')

    # ### end Alembic commands ###