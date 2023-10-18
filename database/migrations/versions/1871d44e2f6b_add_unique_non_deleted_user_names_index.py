"""add_unique_non_deleted_user_names_index

Revision ID: 1871d44e2f6b
Revises: ae53f60cf5c7
Create Date: 2023-08-20 23:09:15.518659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1871d44e2f6b'
down_revision = 'ae53f60cf5c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_unique_non_deleted_user', table_name='users')
    op.create_index('ix_unique_non_deleted_user_names', 'users', ['name', 'is_deleted'], unique=True, postgresql_where=sa.text('NOT is_deleted'))
    op.create_index('ix_unique_non_deleted_users_by_email', 'users', ['email', 'is_deleted'], unique=True, postgresql_where=sa.text('NOT is_deleted'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_unique_non_deleted_users_by_email', table_name='users', postgresql_where=sa.text('NOT is_deleted'))
    op.drop_index('ix_unique_non_deleted_user_names', table_name='users', postgresql_where=sa.text('NOT is_deleted'))
    op.create_index('ix_unique_non_deleted_user', 'users', ['name', 'email', 'is_deleted'], unique=False)
    # ### end Alembic commands ###
