from peewee import *

database = MySQLDatabase('lhsmachines', **{'host': 'db01.home.snowdenlabs.co.uk', 'port': 3306, 'user': 'machines', 'password': 'Password99'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class ModelBase(Model):
    class Meta:
        database = database

class Log(ModelBase):
    endtime = DateTimeField(null=True)
    machineuid = CharField(null=True)
    notes = CharField(null=True)
    starttime = DateTimeField(null=True)
    useruid = CharField(null=True)
    charge = FloatField()

    class Meta:
        table_name = 'log'

class Machine(ModelBase):
    id = PrimaryKeyField()
    creator = CharField()
    machineuid = CharField(unique=True)
    machinename = CharField()
    status = IntegerField(null=True)
    costperminute = FloatField()
    costminimum = FloatField()

    class Meta:
        table_name = 'machine'

class User(ModelBase):
    carduid = CharField(null=True)
    username = CharField(null=True)
    useruid = CharField(null=True, unique=True)
    valid = IntegerField(null=True)

    class Meta:
        table_name = 'user'

class Permission(ModelBase):
    caninduct = IntegerField(null=True)
    canuse = IntegerField(null=True)
    creator = CharField(null=True)
    machineuid = ForeignKeyField(column_name='machineuid', model=Machine, field='machineuid')
    useruid = ForeignKeyField(column_name='useruid', model=User, field='useruid')

    class Meta:
        table_name = 'permission'
