import sqlalchemy as sa
from sqlalchemy.orm import relationship
from db import Base

class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.BigInteger, primary_key=True, index=True)
    email = sa.Column(sa.String(255), unique=True, nullable=False, index=True)
    hashed_password = sa.Column(sa.String(255), nullable=False)
    name = sa.Column(sa.String(255))
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = sa.Column(sa.BigInteger, primary_key=True)
    user_id = sa.Column(sa.BigInteger, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token = sa.Column(sa.String(512), nullable=False, unique=True, index=True)
    revoked = sa.Column(sa.Boolean, nullable=False, server_default=sa.text("false"))
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
    expires_at = sa.Column(sa.DateTime(timezone=True), nullable=False)

    user = relationship("User", backref="refresh_tokens")

class Photo(Base):
    __tablename__ = "photos"

    id = sa.Column(sa.BigInteger, primary_key=True)
    user_id = sa.Column(sa.BigInteger, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    object_key = sa.Column(sa.String(512), nullable=False, index=True)
    content_type = sa.Column(sa.String(128), nullable=True)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)