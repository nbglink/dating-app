from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial_users'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), primary_key=True),
        sa.Column('email', sa.String(length=320), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('gender', sa.String(length=16), nullable=True),
        sa.Column('birthdate', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('users')
