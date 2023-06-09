"""empty message

Revision ID: 658e6320e2c2
Revises: 6935e7004442
Create Date: 2023-06-05 08:38:10.709028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '658e6320e2c2'
down_revision = '6935e7004442'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('people')
    # ### end Alembic commands ###
