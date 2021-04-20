import os

import click
from alembic import command
from alembic.config import Config
from sqlalchemy_utils import drop_database, create_database

from MyAppRest.settings import DevConfig, ProdConfig
from common.models.base import db
from MyAppRest.app import create_app


class ProdMigrateConfig(ProdConfig):
    """Production migration configuration."""

    SQLALCHEMY_DATABASE_URI = ""


@click.command()
@click.option('--migrate', help='Migrate database', is_flag=True)
@click.option('--PROD', help='Production environment', is_flag=True)
@click.option('--drop', help='Drop database', is_flag=True)
@click.option('--create', help='Create database', is_flag=True)
@click.option('--dummy', help='Insert dummy data', is_flag=True)
def recreate(drop, create, dummy, migrate, prod):
    app = create_app(ProdMigrateConfig if prod else DevConfig)
    app.app_context().push()

    alembic_cfg = Config("alembic.ini")

    if migrate:
        command.upgrade(alembic_cfg, "head")

    if prod:
        return  # Prod safety catch so stuff doesn't get deleted

    if drop:
        db.drop_all()
        with db.engine.connect().execution_options(autocommit=True) as conn:
            conn.execute('DROP TABLE IF EXISTS alembic_version;')

    if create:
        db.create_all()
        command.stamp(alembic_cfg, "head")

    if dummy:
        devdb_sql = open("devdb.sql").read()

        with db.engine.connect().execution_options(autocommit=True) as conn:
            conn.execute(devdb_sql)


if __name__ == '__main__':
    recreate()
