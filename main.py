from sqlalchemy import create_engine, text
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