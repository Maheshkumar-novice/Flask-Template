"""user_email_is_deleted_unique

Revision ID: c23f9ef464c9
Revises: 4d6a996b575f
Create Date: 2023-08-20 22:41:15.903329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c23f9ef464c9'
down_revision = '4d6a996b575f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_user_emails', 'users', type_='unique')
    op.create_index('ix_unique_emails_not_deleted_combo', 'users', ['email', 'is_deleted'], unique=True, postgresql_where=sa.text('NOT is_deleted'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_unique_emails_not_deleted_combo', table_name='users', postgresql_where=sa.text('NOT is_deleted'))
    op.create_unique_constraint('unique_user_emails', 'users', ['email'])
    # ### end Alembic commands ###