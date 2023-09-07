from typing import List, Optional

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine, insert, select, func
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, \
    relationship
# from sqlalchemy import select, bindparam

engine = create_engine('sqlite:///:memory:', echo=True)

metadata_obj = MetaData()


user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String, nullable=False),
)

metadata_obj.create_all(engine)


insert_stmt = insert(user_table).values(name='spongebob',
                                        fullname='Spongebob Squarepants')

# print(stmt)
# print(insert_stmt.compile().params)

with engine.connect() as conn:
    result = conn.execute(insert_stmt)
    conn.commit()

# print(compiled.params)

# scalar_subq = (
#     select(user_table.c.id).
#     where(user_table.c.name == bindparam('username'))
#     .scalar_subquery()
# )
# with engine.connect() as conn:
#     result = conn.execute(
#         insert(address_table).values(
#             user_id=scalar_subq,
#             ),
#         [
#             {
#                 'username': 'spongebob',
#                 'email_address': 'spongebob@sqlalchemy.org'
#             },
#             {
#                 'username': 'sandy',
#                 'email_address': 'sandy@sqlalchemy.org'
#             },
#             {
#                 'username': 'sandy',
#                 'email_address': 'sandy@squirrelpower.org'
#             },
#         ],
#     )

#     conn.commit()

# print(insert(user_table).values().compile(engine))

insert_stmt = insert(address_table).returning(
    address_table.c.id, address_table.c.email_address
)
# print(insert_stmt)

# select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
# insert_stmt = insert(address_table).from_select(
#     ["user_id", "email_address"], select_stmt
# )
# print(insert_stmt.returning(address_table.c.id,
#                             address_table.c.email_address))

# with Session(engine) as session:
#     row = session.execute(select(user_table)).first()
#     print(row[0])


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str] = mapped_column(String)

    addresses: Mapped[List["Address"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r},\
              fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email_address: Mapped[str] = mapped_column(String, nullable=False)

    user_id: Mapped[int] = mapped_column(Integer,
                                         ForeignKey("user_account.id"))
    user: Mapped[Optional[User]] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


insert_stmt = insert(User).values(name='spongebob',
                                  fullname='Spongebob Squarepants')

with Session(engine) as session:
    row = session.execute(select(User)).first()
    print("Print from User table:")
    print(row)


with Session(engine) as session:
    user = session.scalars(select(User)).first()
    print("Print from User table:")
    print(user)


print(
    func.unnest(
        func.percentile_disc([0.25, 0.5, 0.75, 1]).within_group(
            user_table.c.name
        )
    )
)
