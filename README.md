# Jaguarundi ORM

Simple SQLite ORM for Python. Requires Python 3.6+.

**<Attention!>** This module was made by mad-skilled student. Never use it in production. I said "NEVER". :) **</Attention!>**

## Install
### Easy install

To install this script using pip (auto install, requirements will be installed automatically):
```
$ pip install git+https://github.com/ravique/jaduarundi-orm.git
```

### Manual install

Download [Jaguarundi ORM](https://github.com/ravique/jaduarundi-orm/archive/master.zip) manually.

### Prerequisites

You need to have Python 3.6+ installed in your system.

# Usage
## Configuration
You can configure Jaguarundi ORM in config.ini (must be in the same folder as your python script).  

**Config.ini Example**

```
[DB_SETTINGS]

db_name = default.db
path_to_db = path/to/your/db/

print_sql_requests = True
control_foreign_keys = True

```
If config.ini does not exist, Jaguarundi ORM will use default settings.

`db_name`: Name of your database. _Default: default.db_  
`path_to_db`: Absolute or relative path to your database. By default, Jaguarundi ORM operates with database in the same folder as your python script.  
`print_sql_requests`: if True, script will print raw sql requests to console. Usable for debug. _Default: False_  
`control_foreign_keys`: if True, preserves to add records to db with foreign key fields to non-existing records. _Default: True_

## Jaguarundi ORM Model reference
To create your first model, import base classes:  
 `from jaguarundi.models import Model, Field`
 
To create model with fields:
```
class Author(Model):
    author_name = Field(field_type='VARCHAR', is_null=True) 
```

Model has default field "id". If you want, you can override it in your model:
```
id = Field(field_type='INTEGER', is_null=False,
            pk=True, auto_increment=True)
```
### Foreign keys
Jaguarundi ORM supports foreign keys (connect by model id field only). 
To create a model with foreign key to model Author:  

```
class Book(Model):
    book_name = Field(field_type='VARCHAR', is_null=True)
    author = Field(field_type='INT', is_null=True, foreign_key=Author.get_fk())
```

**Note:** your models linked by foreign keys must have unique fields names!

### Field parameters

`field_type` – must be in [SQLite datatypes](https://www.sqlite.org/datatype3.html).  
`is_null` – specify whether it can be Null. _Default: False_  
`name` – you can specify custom field name. If not specified, object name will be used.  
`pk` – if True, field be a primary key. _Default: False_  
`auto_increment` – if True, field will get autoincrement. _Default: False_  
`foreign_key` generates Foreign Key link to other model (by id field). Usage: YourModel.get_fk()

## Supported commands
### Create and destroy
`YourModel.create_table()` – creates table in db. If db does not exist, creates db.
`YourModel.create_table()` – drops table.  
`YourModel.create(**params)` – inserts record into table.  
**Example:**  
```
Author.create(author_name="Samuel Beckett")
Book.create(book_name="En attendant Godot", author=1)
```

### Get from db
`YourModel.get(**params)` – returns an object from db, that corresponded to the passed parameters. If no object exist, returns None. If more than one records found, prints error. Parameter "only" can be used.  
**Example:** 
```
beckett = Author.get(author_name="Samuel Beckett")
print(beckett.__dict__)
...
{'id': 1, 'author_name': 'Samuel Beckett'}

```
  
`YourModel.all(**params)` – return list of all founded objects. Only parameter "only" can be used.   
**Example:** 
```
authors = Author.all()
print(authors)
...
[<__main__.Author object at 0x0000021196B78128>, ...]
```
  
`YourModel.all(**params)` – return list of objects, filered by params. If no objects exist, returns None. Parameter "only" can be used.  
**Example:** 
```
authors = Author.filer(author_name="Samuel Beckett")
print(authors)
...
[<__main__.Author object at 0x0000021196B78128>]
```
  
**Note:** if your model has foreign field to another model, you will get another model fields too (not recursive, only first generation of links). 

#### Only fields
If you want to get only necessary fields, use "only" parameter.   

**Note:** If your model has foreign keys to another, "only" parameter will work only for your model fields!
```
beckett = Author.get(author_name="Samuel Beckett", only=['author_name'])
print(beckett.__dict__)
...
{'author_name': 'Samuel Beckett'}

```
**Note:** if you want to get, modify, and than save your object to database, always add "id" into "only" list.

## Working with objects
After getting object ( .get() ) or list of objects ( .filter(), .all() ), you can work with them as with simple python objects.  
**Example:**
```
beckett.authors_name = "Knut Hamsun"
```  
  
`object.save()` – save object to database. Only existing columns will be rewrited.  
`object.update(**params)` – update columns in database. Only existing columns will be rewrited. Object updates too. 
**Example:**
```
beckett.update(author_name="Franz Kafka")
print(beckett.author_name)
...
Franz Kafka

kafka = Author.get(author_name="Franz Kafka")
print(kafka.author_name)
...
Franz Kafka
```


## Authors

* **Andrei Etmanov** - *Student of OTUS :)*

## License

This project is licensed under the MIT License – see the [LICENSE.md](LICENSE.md) file for details