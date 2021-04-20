import os
import sys
from logging.config import fileConfig

from flask import current_app, has_request_context, has_app_context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
from common.models.base import Base, db

config = context.config

# Interpret the modifier file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = db.Model.metadata


# other values from the modifier, defined by the needs of env.py,
# can be acquired:
# my_important_option = modifier.get_main_option("my_important_option")
# ... etc.

def get_db_conn_str():
    if has_app_context() and current_app.config['SQLALCHEMY_DATABASE_URI'] is not None:
        return current_app.config['SQLALCHEMY_DATABASE_URI']

    postgres_user = os.environ.get('POSTGRES_USER', 'serviceclient')
    postgres_password = os.environ.get('POSTGRES_PASSWORD', 'password')
    postgres_host = os.environ.get('POSTGRES_HOST', 'localhost')
    postgres_port = os.environ.get('POSTGRES_PORT', 5433)
    postgres_database = os.environ.get('POSTGRES_DB', 'chimedb')

    url = f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/' \
          f'{postgres_database}'

    return url


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=get_db_conn_str(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    config_section = config.get_section(config.config_ini_section)
    config_section["sqlalchemy.url"] = get_db_conn_str()

    connectable = engine_from_config(
        config_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
