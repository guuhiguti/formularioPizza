from peewee import Model, CharField, TextField, DateTimeField, FloatField
from database.database import db
import datetime

class Pedidos(Model):
    nome = CharField()
    whatsapp = CharField()
    retirada = CharField()
    detalhe_retirada = TextField(null=True)
    pizzas = TextField()
    total = FloatField()
    data = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db