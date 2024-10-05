from peewee import *


db = SqliteDatabase('database.db')


class BaseModel(Model):
    id = PrimaryKeyField()

    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField()


def main():
    db.connect()
    db.drop_tables([User])
    db.create_tables([User])


if __name__ == "__main__":
    main()
