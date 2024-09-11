"""
database schema, it's structure of tables, columns and so on
"""

import databases
import sqlalchemy

# reads the config file and gets the appropriate config setup and environment
from main.config import config


# info about db
metadata = sqlalchemy.MetaData()

# db schemas / table name, metadata object, columns
post_table = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String)
)

comment_table = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column("post_id", sqlalchemy.ForeignKey("posts.id"), nullable=False)
)

# connect to specific type od db (sqlite in this case)
engine = sqlalchemy.create_engine(
    # multithread for sqlite
    config.DATABASE_URL, connect_args={"Check_same_thread": False}
)

# use metadata object to create all the tables, then uses metadata module to create metadata object
metadata.create_all(engine)
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK
)
