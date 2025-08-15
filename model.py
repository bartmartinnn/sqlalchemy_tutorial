from sqlalchemy import MetaData, Table, Column, Integer, String

metadata_obj = MetaData()

user_table = Table(
    'user_account',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('fullname', String)
)

