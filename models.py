from peewee import *
import peewee_async

database = PostgresqlDatabase('testdb2', user='postgres', password='postgres', host='db', port=5432)

class BaseModel(Model):
    class Meta:
        database = database

class ApiUser(BaseModel):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()

class Location(BaseModel):
    name = CharField()

class Device(BaseModel):
    name = CharField()
    type = CharField()
    login = CharField()
    password = CharField()
    location = ForeignKeyField(Location, backref='devices')
    api_user = ForeignKeyField(ApiUser, backref='devices')

# Створення таблиць під час ініціалізації
if __name__ == "__main__":
    database.connect()
    database.create_tables([ApiUser, Location, Device])
    database.close()
