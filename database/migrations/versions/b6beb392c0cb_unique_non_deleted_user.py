"""unique_non_deleted_user

Revision ID: b6beb392c0cb
Revises: c23f9ef464c9
Create Date: 2023-08-20 22:47:07.898149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6beb392c0cb'
down_revision = 'c23f9ef464c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_unique_emails_not_deleted_combo', table_name='users')
    op.create_index('ix_unique_non_deleted_user', 'users', ['name', 'email', 'is_deleted'], unique=True, postgresql_where=sa.text('NOT is_deleted'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_unique_non_deleted_user', table_name='users', postgresql_where=sa.text('NOT is_deleted'))
    op.create_index('ix_unique_emails_not_deleted_combo', 'users', ['email', 'is_deleted'], unique=False)
    # ### end Alembic commands ###
