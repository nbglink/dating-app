from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy import engine_from_config
from alembic import context
import os
import sys
from pathlib import Path

# ensure apps/api is on path
THIS_DIR = Path(__file__).resolve().parent
API_DIR = THIS_DIR.parent
if str(API_DIR) not in sys.path:
    sys.path.append(str(API_DIR))

from models import User  # noqa
from db import Base  # noqa

config = context.config
target_metadata = Base.metadata

def get_url():
    return os.getenv("DATABASE_URL", "postgresql+psycopg://dating:datingpass@localhost:5432/datingdb")

def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section) or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=get_url(),
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
