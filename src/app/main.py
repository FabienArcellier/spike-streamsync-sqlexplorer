from typing import Dict

import pandas
import streamsync as ss
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

engine = sa.create_engine("postgresql://admin:admin@localhost/Adventureworks")
Session = sessionmaker(engine)


def pick_table(state, payload):
    schema, table = payload.split(".")
    state['table'] = payload
    state['table_content'] = pandas.read_sql_table(table, engine, schema=schema)

# Initialise the state

def _list_tables() -> Dict[str, str]:
    inspector = sa.inspect(engine)
    schemas = inspector.get_schema_names()
    all_tables = {}
    for schema in schemas:
        tables = inspector.get_table_names(schema=schema)
        for table in tables:
            all_tables[f"{schema}.{table}"] = f"{schema}.{table}"

    return all_tables


def _first_table() -> str:
    table = list(_list_tables().keys())[0]
    return table


def _first_table_content() -> pandas.DataFrame:
    table = _first_table()
    schema, table = table.split(".")
    return pandas.read_sql_table(table, engine, schema=schema)

initial_state = ss.init_state({
    "sqlalchemy_version": sa.__version__,
    "tables": _list_tables(),
    "table": _first_table(),
    "table_content": _first_table_content(),
})


