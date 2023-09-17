import peewee
from .db_options import DbOptions


class DbInitializer:
    @staticmethod
    def initialize_database_proxy(
        db_options: DbOptions,
        database_proxy: peewee.DatabaseProxy,
        models: list[peewee.Model],
    ) -> None:
        database = DbInitializer._create_database(db_options)
        database_proxy.initialize(database)
        with database_proxy:
            database_proxy.create_tables(models, safe=True)

    @staticmethod
    def _create_database(db_options: DbOptions) -> peewee.Database:
        if db_options.has_all_data():
            print("MySQL db")
            return peewee.MySQLDatabase(
                db_options.database,
                user=db_options.user,
                password=db_options.password,
                host=db_options.host,
                port=db_options.port,
                autoconnect=False,
            )
        else:
            print("SQL lite db")
            return peewee.SqliteDatabase("gloomhaven.db", autoconnect=False)
