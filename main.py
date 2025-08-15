from sqlalchemy import create_engine, text
engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)

with engine.connect() as conn:
    conn.execute(text('create table some_table (x int, y int)'))
    conn.execute(text('insert into some_table (x, y) values (:x, :y)'),
                    [{'x': 1, 'y': 2}, {'x': 3, 'y': 4}])
    result = conn.execute(text('select * from some_table'))
    print(result.all())
    conn.commit()  