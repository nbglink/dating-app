from alembic import op
import sqlalchemy as sa

revision = '0003_photos'
down_revision = '0002_refresh_tokens'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'photos',
        sa.Column('id', sa.BigInteger(), primary_key=True),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('object_key', sa.String(length=512), nullable=False, index=True),
        sa.Column('content_type', sa.String(length=128), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    )

def downgrade():
    op.drop_table('photos')
