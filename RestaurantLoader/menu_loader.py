import csv

import click
from flask import Flask
from sqlalchemy import and_
from sqlalchemy.orm import aliased

from MyAppRest.app import create_app
from MyAppRest.settings import DevConfig
from common.models import RestaurantDao, RestaurantMenuDao, RestaurantItemModifierDao, RestaurantItemModifierOptionDao, RestaurantMenuCategoryDao, RestaurantItemDao, \
    RestaurantMenuCategoryItemAssociationDao, RestaurantItemModifierAssociationDao
from common.models.base import db


@click.command()
@click.option('--restaurant_id', help='Restaurant id we are loading to',
              type=str, required=True)
@click.option('--restaurant_menu_id', help='RestaurantMenu id we are loading to',
              type=str, required=True)
@click.option('--item_modifier_csv', help='csv of item modifiers (item_modifier_name, description, item_modifier_type)',
              type=click.File('rt'))
@click.option('--item_modifier_option_csv',
              help='csv of item modifier options with mapping to item_modifier (item_modifier_option_name, item_modifier_name, '
                   'item_modifier_option_price)',
              type=click.File('rt'))
@click.option('--menu_category_csv',
              help='csv of menu categories (category_name, subcategory_name)', type=click.File('rt'))
@click.option('--restaurant_items_csv',
              help='csv of menu items (name, description, price, category, subcategory, item_modifier_1_name, '
                   'item_modifier_2_name, item_modifier_3_name)', type=click.File('rt'))
def load_menu(menu_id, restaurant_id, item_modifier_csv, item_modifier_option_csv, menu_category_csv, restaurant_items_csv):
    app = create_app(DevConfig)
    app.app_context().push()
    db.init_app(app)

    menu = db.session.query(RestaurantMenuDao).get((menu_id, restaurant_id))
    if menu is None:
        raise Exception('RestaurantMenu id is not valid')

    restaurant = RestaurantDao.get_by_id(restaurant_id)
    if restaurant is None:
        raise Exception('Restaurant id is not valid')

    if item_modifier_csv is not None:
        item_modifiers = csv.reader(item_modifier_csv, delimiter='\t')

        next(item_modifiers)  # skip the first line
        for item_modifier in item_modifiers:
            restaurant.item_modifiers.append(RestaurantItemModifierDao(name=item_modifier[0], type=item_modifier[2]))

        # db.session.commit()

    if item_modifier_option_csv is not None:
        item_modifier_options = csv.reader(item_modifier_option_csv, delimiter='\t')

        next(item_modifier_options)  # skip the first line
        for item_modifier_option in item_modifier_options:
            item_modifier_names = item_modifier_option[1].split(';')

            for item_modifier_name in item_modifier_names:
                item_modifier = db.session.query(RestaurantItemModifierDao).filter(
                    and_(RestaurantItemModifierDao.restaurant == menu.restaurant,
                         RestaurantItemModifierDao.name == item_modifier_name.strip())) \
                    .first()

                if item_modifier is None:
                    raise Exception(f'Missing item modifier name {item_modifier_name.strip()}')

                item_modifier_opt = RestaurantItemModifierOptionDao(label=item_modifier_option[0],
                                                                    price=item_modifier_option[2] if len(
                                                              item_modifier_option[2]) > 0 else 0,
                                                                    restaurant_item_modifier_id=item_modifier.id)
                item_modifier_opt.restaurant = restaurant
                db.session.add(item_modifier_opt)
        # db.session.commit()

    if menu_category_csv is not None:
        menu_categories_csv = csv.reader(menu_category_csv, delimiter='\t')

        i = 0
        next(menu_categories_csv)  # skip the first line
        for menu_category in menu_categories_csv:
            parent_category = db.session.query(RestaurantMenuCategoryDao) \
                .filter(and_(RestaurantMenuCategoryDao.restaurant_menu_id == menu.id, RestaurantMenuCategoryDao.restaurant_id == restaurant_id,
                             RestaurantMenuCategoryDao.name == menu_category[0])).first()

            if parent_category is None:
                parent_category = RestaurantMenuCategoryDao(name=menu_category[0], position=i, restaurant_id=restaurant_id)
                menu.categories.append(parent_category)

            if menu_category[1] is not None and len(menu_category[1]) > 0:
                child_category = db.session.query(RestaurantMenuCategoryDao) \
                    .filter(and_(RestaurantMenuCategoryDao.parent_category_id == parent_category.id,
                                 RestaurantMenuCategoryDao.restaurant_id == restaurant_id,
                                 RestaurantMenuCategoryDao.name == menu_category[1])).first()

                if child_category is None:
                    parent_category.child_categories.append(RestaurantMenuCategoryDao(name=menu_category[1],
                                                                                      restaurant_id=restaurant_id,
                                                                                      position=i,
                                                                                      restaurant_menu_id=parent_category.restaurant_menu_id))
            i = i + 1

        # db.session.commit()

    if restaurant_items_csv is not None:
        restaurant_items_csv = csv.reader(restaurant_items_csv, delimiter='\t')

        i = 0
        next(restaurant_items_csv)  # skip the first line
        for restaurant_item in restaurant_items_csv:
            item = RestaurantItemDao(name=restaurant_item[0], description=restaurant_item[1], price=restaurant_item[2],
                                     restaurant_id=menu.restaurant_id,
                                     featured=int(restaurant_item[3] if len(restaurant_item[3]) > 0 else 0))
            db.session.add(item)

            if restaurant_item[5] is not None and len(restaurant_item[5]) > 0:  # subcategory
                # TODO: if duplicates between category names and sub category names this won't work
                parent_cat = aliased(RestaurantMenuCategoryDao)
                child_cat = aliased(RestaurantMenuCategoryDao)

                category = db.session.query(child_cat).join(parent_cat, child_cat.parent_category) \
                    .filter(and_(parent_cat.name == restaurant_item[4],
                                 child_cat.restaurant_id == restaurant_id,
                                 child_cat.name == restaurant_item[5])).first()
            else:  # category
                category = db.session.query(RestaurantMenuCategoryDao) \
                    .filter(and_(RestaurantMenuCategoryDao.parent_category_id == None,
                                 RestaurantMenuCategoryDao.restaurant_id == restaurant_id,
                                 RestaurantMenuCategoryDao.name == restaurant_item[4])).first()

            if category is None:
                raise Exception(f'Missing category name {restaurant_item[5]}, {restaurant_item[4]}')

            item_assoc = RestaurantMenuCategoryItemAssociationDao(restaurant_item_id=item.id, restaurant_id=restaurant_id,
                                                                  restaurant_menu_category_id=category.id, position=i)
            category.items_assoc.append(item_assoc)

            k = 0
            for j in range(1):
                modifier_name = restaurant_item[6 + j * 2]
                required = restaurant_item[6 + j * 2 + 1]

                if modifier_name is not None and len(modifier_name) > 0:
                    item_modifier = db.session.query(RestaurantItemModifierDao).filter(
                        and_(RestaurantItemModifierDao.restaurant == menu.restaurant,
                             RestaurantItemModifierDao.name == modifier_name.strip())).first()
                    if item_modifier is None:
                        raise Exception(f'Missing item_modifier name {modifier_name.strip()}')

                    item_assoc = RestaurantItemModifierAssociationDao(restaurant_item_id=item.id, restaurant_item_modifier_id=item.id,
                                                                      position=k, required=int(required),
                                                                      restaurant_id=restaurant_id)
                    item_modifier.items_assoc.append(item_assoc)
                    k += 1

            i += 1

        # db.session.commit()

    db.session.commit()


if __name__ == '__main__':
    load_menu()
