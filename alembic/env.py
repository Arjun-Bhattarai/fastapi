import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Add project root to path FIRST before any app imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load .env BEFORE importing app modules
load_dotenv()

# Alembic Config object
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import Base and ALL models
from app.database.db import Base
from app.models import *
from app.database.schema.user_schema import UserSchema  # imports everything from __init__.py
target_metadata = Base.metadata

# Get DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")


def run_migrations_offline() -> None:
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        {"sqlalchemy.url": DATABASE_URL},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
