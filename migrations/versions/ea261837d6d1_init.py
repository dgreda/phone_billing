# flake8: noqa

"""init

Revision ID: ea261837d6d1
Revises: 
Create Date: 2022-07-29 21:56:48.993687

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "ea261837d6d1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("number", sa.BigInteger(), nullable=False),
        sa.Column("country_code", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "invoice",
        sa.Column("identifier", sa.String(), nullable=False),
        sa.Column("billing_month", sa.Integer(), nullable=False),
        sa.Column("billing_year", sa.Integer(), nullable=False),
        sa.Column("total_minutes", sa.Integer(), nullable=False),
        sa.Column("total_charges", sa.Float(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("identifier"),
    )
    op.create_table(
        "call",
        sa.Column("recipient_number", sa.BigInteger(), nullable=False),
        sa.Column(
            "start_datetime_iso_8601",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "end_datetime_iso_8601", sa.DateTime(timezone=True), nullable=False
        ),
        sa.Column("recipient_country_code", sa.Integer(), nullable=False),
        sa.Column("duration_in_minutes", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("invoice_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["invoice_id"],
            ["invoice.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("call")
    op.drop_table("invoice")
    op.drop_table("user")
    # ### end Alembic commands ###
