import json
from datetime import timedelta
from pathlib import Path
from typing import Any

import pandas as pd
from celery import Celery
from openpyxl import load_workbook
from sqlalchemy import create_engine

from app.celery.hash_xls import calculate_file_hash, read_hash, write_hash
from app.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

celery_app = Celery()

celery_app.conf.broker_url = "amqp://guest:guest@rabbitmq:5672//"
celery_app.conf.result_backend = "rpc://"
celery_app.conf.broker_connection_retry_on_startup = True

celery_app.conf.beat_schedule = {
    "pandas_update_database": {
        "task": "app.celery.tasks.pandas_update_database",
        "schedule": timedelta(seconds=15),
    },
}


def excel_to_json() -> tuple[dict[str, dict[Any, Any]], dict[str, dict[Any, Any]], dict[str, dict[Any, Any]]]:
    wb = load_workbook(Path("./app/admin/Menu.xlsx"))
    sheet = wb.active

    menu_json: dict[str, dict] = {"id": {}, "title": {}, "description": {}}
    submenu_json: dict[str, dict] = {"id": {}, "menu_id": {}, "title": {}, "description": {}}
    dish_json: dict[str, dict] = {"id": {}, "submenu_id": {}, "title": {}, "description": {}, "price": {}}

    menu_count, sub_count, dish_count = 0, 0, 0

    current_menu_id = ""
    current_sub_id = ""

    for row in sheet.iter_rows(values_only=True):
        if row[0] is not None and row[1] is not None:
            current_menu_id = row[0]
            menu_json["id"][menu_count] = row[0]
            menu_json["title"][menu_count] = row[1]
            menu_json["description"][menu_count] = row[2]
            menu_count += 1

        if row[0] is None and row[1] is not None:
            current_sub_id = row[1]
            submenu_json["id"][sub_count] = row[1]
            submenu_json["menu_id"][sub_count] = current_menu_id
            submenu_json["title"][sub_count] = row[2]
            submenu_json["description"][sub_count] = row[3]
            sub_count += 1

        if row[0] is None and row[1] is None:
            dish_json["id"][dish_count] = row[2]
            dish_json["submenu_id"][dish_count] = current_sub_id
            dish_json["title"][dish_count] = row[3]
            dish_json["description"][dish_count] = row[4]
            if len(row) > 6 and row[6] is not None:
                new_price = float(row[5]) * (100 - int(row[6])) / 100
                dish_json["price"][dish_count] = new_price
            else:
                dish_json["price"][dish_count] = row[5]
            dish_count += 1
    return menu_json, submenu_json, dish_json


@celery_app.task
def pandas_update_database() -> None:
    new_hash = calculate_file_hash()
    if not Path.exists(Path("./app/admin/hash")):
        write_hash(new_hash)
    old_hash = read_hash()

    if old_hash != new_hash:
        menus_data, submenus_data, dishes_data = excel_to_json()

        menu_df = pd.read_json(json.dumps(menus_data))
        menu_df.to_sql("menus", engine, if_exists="replace", index=False)

        submenu_df = pd.read_json(json.dumps(menus_data))
        submenu_df.to_sql("submenus", engine, if_exists="replace", index=False)

        dish_df = pd.read_json(json.dumps(menus_data))
        dish_df.to_sql("dishes", engine, if_exists="replace", index=False)

        write_hash(new_hash)
