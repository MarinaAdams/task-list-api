"""Migration: added one-to-many relationship between goals and tasks.
q


Revision ID: 8cf3c04ce4b6
Revises: 61d7672dd37e
Create Date: 2025-05-11 01:44:57.765674

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8cf3c04ce4b6"
down_revision = "61d7672dd37e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("task", schema=None) as batch_op:
        batch_op.add_column(sa.Column("goal_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, "goal", ["goal_id"], ["id"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("task", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.drop_column("goal_id")

    # ### end Alembic commands ###
