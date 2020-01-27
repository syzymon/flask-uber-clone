"""Add sequences

Revision ID: 1d37af335053
Revises: 982fc8c9327b
Create Date: 2020-01-27 17:10:52.682249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d37af335053'
down_revision = '982fc8c9327b'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("create sequence cars_id_seq start with 1 increment by 1 nocache nocycle")
    op.execute("create sequence drivers_id_seq start with 1 increment by 1 nocache nocycle")
    op.execute("create sequence jobs_id_seq start with 1 increment by 1 nocache nocycle")
    op.execute("create sequence finished_id_seq start with 1 increment by 1 nocache nocycle")
    op.execute("create sequence riders_id_seq start with 1 increment by 1 nocache nocycle")
    op.execute("create sequence routes_id_seq start with 1 increment by 1 nocache nocycle")
    op.execute("create sequence orders_id_seq start with 1 increment by 1 nocache nocycle")


def downgrade():
    pass
