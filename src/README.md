# The REST API app for small restaurants

## Stack

- [FastAPI](https://fastapi.tiangolo.com/)  
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20)
- [PyJWT](https://pyjwt.readthedocs.io/en/latest/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [WebSocket](https://en.wikipedia.org/wiki/WebSocket)
- [PassLib](https://pypi.org/project/passlib/)


## Description

It's small app for restaurants. 
It's main purpose is to manage orders.\
\
WebSocket is used for real-time communication with waiter and kitchen.
\
In app used JWT for authentication.\
Used async session of SQLAlchemy for CRUD operations.