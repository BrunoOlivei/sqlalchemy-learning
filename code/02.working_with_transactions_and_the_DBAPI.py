# THE ENGINE

from sqlalchemy import create_engine

dialect = 'sqlite'  # The database engine
driver = ''  # The database driver DBAPI

echo = True  # Log SQL calls

engine = create_engine('sqlite:///:memory:', echo=True)

"""
The Engine, when first returned by create_engine(), has not actually tried to
connect to the database yet; that happens only the first time it is asked to
perform a task against the database. This is a software design pattern known
as lazy initialization.
"""

############################################################################

# Working with transactions and the DBAPI

"""
Ao utilizar o ORM, o Motor é gerenciado por outro objeto denominado Sessão.
A Sessão no SQLAlchemy moderno enfatiza um padrão de execução transacional
e SQL que é amplamente idêntico ao da Conexão discutida abaixo
"""

"""
Ao trabalhar diretamente com o Core, o objeto Connection é como é feita toda a
interação com o banco de dados. Como a Conexão representa um recurso aberto no
banco de dados, queremos sempre limitar o escopo de nosso uso deste objeto a
um contexto específico, e a melhor maneira de fazer isso é usando o formulário
do gerenciador de contexto Python, também conhecido como instrução with.
"""

from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())


# Committing Changes

with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
    )
    conn.commit()


"""
Há também outro estilo de confirmação de dados, que consiste em declarar
antecipadamente nosso bloco “conectar” como um bloco de transação. Para este
modo de operação, usamos o método Engine.begin() para adquirir a conexão, ao
invés do método Engine.connect(). Este método irá gerenciar o escopo da
Conexão e também incluir tudo dentro de uma transação com COMMIT no final,
assumindo um bloco bem-sucedido, ou ROLLBACK em caso de aumento de exceção.
Este estilo pode ser referido como começar uma vez:
"""

with engine.begin() as conn:
    conn.execute(text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
                 [{"x": 6, "y": 8}, {"x": 9, "y": 10}])


# Fetching Rows

# with engine.connect() as conn:
#     result = conn.execute(text("SELECT x, y FROM some_table"))
#     for row in result:
#         print("x: {x}  y: {y}".format(x=row.x, y=row.y))


# with engine.connect() as conn:
#     result = conn.execute(text("SELECT x, y FROM some_table"))
#     for row in result:
#         print(row)

# with engine.connect() as conn:
#     result = conn.execute(text("SELECT x, y FROM some_table"))
#     for x, y in result:
#         print(x)
#         print(y)

# with engine.connect() as conn:
#     result = conn.execute(text("SELECT x, y FROM some_table"))
#     for row in result:
#         print(row.x)
#         print(row.y)

# with engine.connect() as conn:
#     result = conn.execute(text("SELECT x, y FROM some_table"))
#     for dict_row in result.mappings():
#         print(dict_row["x"])
#         print(dict_row["y"])


# Sending Parameters

# with engine.connect() as conn:
#     result = conn.execute(text("SELECT X, Y FROM some_table WHERE y > :y"),
#                           {"y": 2})
#     for row in result:
#         print(f'x: {row.x}  y: {row.y}')


# Sending Multiple Parameters

with engine.connect() as conn:
    conn.execute(text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
                 [{"x": 11, "y": 12}, {"x": 13, "y": 14}])
    conn.commit()


# Executing with an ORM Session

from sqlalchemy.orm import Session

stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
with Session(engine) as session:
    result = session.execute(stmt, {"y": 6})
    for row in result:
        print(f'x: {row.x}  y: {row.y}')


with Session(engine) as session:
    result = session.execute(
        text("UPDATE some_table SET y=:y WHERE x=:x"),
        [{"x": 9, "y": 11}, {"x": 13, "y": 15}]
    )
    session.commit()
