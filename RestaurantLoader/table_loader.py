import csv

import click

from MyAppRest.app import create_app
from MyAppRest.settings import DevConfig
from common.models import RestaurantDao, RestaurantTableDao
from common.models.base import db


@click.command()
@click.option('--restaurant_id', help='Restaurant id we are loading to',
              type=str, required=True)
@click.option('--table_csv', help='csv of tables (display_name)',
              type=click.File('rt'))
def load_menu(restaurant_id, table_csv):
    app = create_app(DevConfig)
    app.app_context().push()
    db.init_app(app)

    restaurant = RestaurantDao.get_by_id(restaurant_id)
    if restaurant is None:
        raise Exception('Restaurant id is not valid')

    tables = csv.reader(table_csv, delimiter='\t')

    next(tables)  # skip the first line
    for i, table in enumerate(tables):
        restaurant.tables.append(RestaurantTableDao(display_name=table[0], position=i))

    db.session.commit()


if __name__ == '__main__':
    load_menu()
