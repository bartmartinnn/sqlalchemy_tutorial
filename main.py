from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)

with engine.connect() as conn:
    conn.execute(text('create table some_table (x int, y int)'))
    conn.execute(text('insert into some_table (x, y) values (:x, :y)'),
                    [{'x': 1, 'y': 2}, {'x': 3, 'y': 4}])
    result = conn.execute(text('select * from some_table'))
    print(result.all())
    conn.commit()  

'begin once'
with engine.begin() as conn:
    conn.execute(text('insert into some_table (x, y) values (:x, :y)'),
                    [{'x': 1, 'y': 2}, {'x': 3, 'y': 4}])
    result = conn.execute(text('select * from some_table'))
    print('tuple assignment')
    for x, y in result:
        print(f'x: {x}, y: {y}')
    
    result = conn.execute(text('select x, y from some_table'))
    print('attribute access')
    for row in result:
        print(f'x: {row.x}, y: {row.y}')
    
    result = conn.execute(text('select x, y from some_table'))
    print('dictionary access')
    for dict_row in result.mappings():
        print(f'x: {dict_row['x']}, y: {dict_row['y']}')
    
    with engine.connect() as conn:
        print('parameterized query')
        result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
        for row in result:
            print(f"x: {row.x}  y: {row.y}")
    
    print('USING SESSION')
    stmt = text('select x, y from some_table where y > :y order by x, y')
    with Session(engine) as session:
        result = session.execute(stmt, {'y': 2})
        for row in result:
            print(f'x: {row.x}, y: {row.y}')

    print('UPDATE SESSION')
    stmt = text('update some_table set y=:y where x=:x')
    with Session(engine) as session:
        result = session.execute(stmt, {'x': 3, 'y': 13})
        session.commit()
        result_updated = session.execute(text('select * from some_table'))
        for row in result_updated:
            print(f'x: {row.x}, y: {row.y}')