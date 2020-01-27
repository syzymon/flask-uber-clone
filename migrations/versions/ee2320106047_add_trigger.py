"""Add trigger

Revision ID: ee2320106047
Revises: 1d37af335053
Create Date: 2020-01-27 17:45:20.867555

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee2320106047'
down_revision = '1d37af335053'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute("""
CREATE OR REPLACE TRIGGER drivers_update_rating
    AFTER INSERT OR UPDATE ON finished
    FOR EACH ROW
BEGIN
    If :NEW.rating IS NOT NULL then
        UPDATE drivers 
        SET drivers.rating = (drivers.rating * experience + :NEW.rating) / (experience + 1),
            experience = experience + 1
        WHERE drivers.id = :NEW.driver_id;
    END IF;
END;
    """)


def downgrade():
    op.execute("DROP TRIGGER drivers_update_rating")
    pass
