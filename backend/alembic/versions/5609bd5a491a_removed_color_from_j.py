"""removed color from journals

Revision ID: 5609bd5a491a
Revises: 56f2aeb28bd4
Create Date: 2013-10-27 15:12:04.295524

"""

# revision identifiers, used by Alembic.
revision = '5609bd5a491a'
down_revision = '56f2aeb28bd4'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('journals', u'color')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('journals', sa.Column(u'color', mysql.VARCHAR(length=7), nullable=True))
    ### end Alembic commands ###
