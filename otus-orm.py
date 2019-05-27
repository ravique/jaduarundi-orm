from jaguarundi.models import Model, Field

# TODO: determine db


# Create your models here

class Colors(Model):
    col_name = Field(field_type='VARCHAR', is_null=True)
    color_type = Field(field_type='VARCHAR', is_null=True)


class Classes(Model):
    cl_name = Field(field_type='VARCHAR', is_null=True)
    class_type = Field(field_type='VARCHAR', is_null=True)


class Koalas(Model):
    id = Field(field_type='INTEGER', is_null=False, pk=True)
    name = Field(field_type='VARCHAR', is_null=True)
    sex = Field(field_type='CHAR', is_null=True)
    age = Field(field_type='INT', is_null=True, )
    color = Field(field_type='INT', is_null=True, foreign_key=Colors.get_fk())
    cl = Field(field_type='INT', is_null=True, foreign_key=Classes.get_fk())


Koalas.drop_table()
Colors.drop_table()
Classes.drop_table()

Classes.create_table()
Colors.create_table()
Koalas.create_table()


# Koalas().create(name='Serush', id=1)
#
Colors.create(col_name='gray', color_type='dark')
Colors.create(col_name='brown', color_type='dark')
Classes.create(cl_name='first', class_type='best')
Classes.create(cl_name='second', class_type='best2')
# Classes().create(cl_name='third', class_type='best3')

Koalas.create(name='Burush', age=10, color='1', cl='2')
Koalas.create(name='Burush2', age=20, color='1', cl='3')
Koalas.create(name='Serush', age=20, id=100)
#

serush = Koalas.get(id=100)


burush = Koalas.get(id=1, only=['name'])
burush.update(name='Jaguar', age=10, sex='Male')
burush.update(sex=None)

non = Koalas.filter(age=1000)

koalas = Koalas.all()
print('\n Burush:')
print(burush.__dict__)


print('\n Koalas:')
for o in koalas:
    print(o.__dict__)

# burush.age = 32768
# burush.save()




#
# burush = Koalas().get(id=2)
# print(burush.__dict__)

#
# print(burush.__dict__)
# # print(type(serush))
# print(burush.name)
