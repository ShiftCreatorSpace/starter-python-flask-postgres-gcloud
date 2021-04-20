import os

from alembic import command
from alembic.config import Config

from MyAppRest.app import create_app
from MyAppRest.tests.test_config import TestConfig, TestDevConfig
from common.models.base import db

config = TestConfig if os.environ.get('TEST_USE_HOST') is None else TestDevConfig

app = create_app(config)
app.app_context().push()

client = app.test_client

db.drop_all()
with db.engine.connect().execution_options(autocommit=True) as conn:
    conn.execute('DROP TABLE IF EXISTS alembic_version;')
db.session.commit()

if os.environ.get('TEST_USE_HOST') is not None:
    alembicini_loc = "alembic.ini"
    if not os.path.isfile(alembicini_loc):
        alembicini_loc = "../../alembic.ini"

    alembic_cfg = Config(alembicini_loc)
    command.upgrade(alembic_cfg, "head")
else:
    db.create_all()
    db.session.commit()


def reset():
    # Clear table data
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()

    # Load devdb
    devdb_location = "devdb.sql"
    if not os.path.isfile(devdb_location):
        devdb_location = "../../devdb.sql"

    devdb_file = open(devdb_location)
    devdb_sql = devdb_file.read()
    devdb_file.close()

    with db.engine.connect().execution_options(autocommit=True) as conn:
        if db.session.bind.dialect.name == 'sqlite':
            conn.connection.connection.executescript(devdb_sql)
        else:
            conn.execute(devdb_sql)


reset()
