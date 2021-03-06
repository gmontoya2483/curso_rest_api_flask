# Storing Resources in an SQL Database

[VOLVER A README.md](README.md)

## Índice

* [Comandos basicos de SQL](#comandos_basicos_de_sql)
* [Logging in and retrieving Users from database](#logging-in-and-retrieving-Users-from-database)
* [Signing up and escribir usuarios en la base de datos](#signing-up-and-escribir-usuarios-en-la-base-de-datos)
* [Obtener un item desde la base de datos](#obtener-un-item-desde-la-base-de-datos)
* [Escribir un item en la base de datos](#escribir-un-item-en-la-base-de-datos)
* [Borrar un item de la base de datos](#borrar-un-item-de-la-base-de-datos)
* [Refactor insert of items](#refactor-insert-of-items)
* [Implementar el metodo put para modificar items](#implementar-el-metodo-put-para-modificar-items)
* [Implementar el metodo GET obtner todos los items](#implementar-el-metodo-get-obtner-todos-los-items)
* [Configuraciones avanzadas de Flask-JWT](#configuraciones-avanzadas-de-flask-jwt)

## Comandos basicos de SQL

```python
    import sqlite3

    connection = sqlite3.connect('data.db')

    cursor = connection.cursor()

    create_table = "CREATE TABLE users (id int, username text, password text)"

    cursor.execute(create_table)

    user = (1, 'jose', 'asdf')
    insert_query = "INSERT INTO users VALUES (?, ?, ?)"
    cursor.execute(insert_query, user)


    users = [(2, 'rolf', 'asdf'), (3, 'anne', 'asdf')]
    cursor.executemany(insert_query,users)


    select_query = "SELECT * FROM users"
    for row in cursor.execute(select_query):
        print(row)


    connection.commit()
    connection.close()
```

[Video: Comandos basicos de SQL](https://www.udemy.com/rest-api-flask-and-python/learn/v4/t/lecture/5965476?start=0)

## Logging in and retrieving Users from database

1. Modificar ```user.py``` para agregar 2 metodos de clases que busquen en la base de datos el usuario por ```username``` y por ```_id```

    ```python
        import sqlite3
    ```

    ```python
        @classmethod
        def find_by_username(cls, username):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "SELECT * FROM users WHERE username=?"
            result = cursor.execute(query, (username,))
            row = result.fetchone()
            if row is not None:
                user = cls(*row)  # *row = row[0], row[1], row[2]
            else:
                user = None

            connection.close()
            return user
    ```

    ```python
        @classmethod
        def find_by_id(cls, _id):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "SELECT * FROM users WHERE id=?"
            result = cursor.execute(query, (_id,))
            row = result.fetchone()
            if row is not None:
                user = cls(*row)  # *row = row[0], row[1], row[2]
            else:
                user = None

            connection.close()
            return user
    ```

2. Modificar ```security.py``` para utilizar los m'etodos de la clase User

```python
    from user import User
    from werkzeug.security import safe_str_cmp

    def authenticate(username, password):
        user = User.find_by_username(username)
        if user and safe_str_cmp(user.password, password):
            return user


    def identity(payload):
        user_id = payload['identity']
        return User.find_by_id(user_id)
```

[Video: Logging in](https://www.udemy.com/rest-api-flask-and-python/learn/v4/t/lecture/5965500?start=0)

## Signing up and escribir usuarios en la base de datos

1. Crear el recurso ```UserRegister``` dentro del archivo ```user.py``` y agregarle el metodo ```post``

```python
    from flask_restful import Resource, reqparse
```

```python
    class UserRegister(Resource):

        parser = reqparse.RequestParser()
        parser.add_argument('username',
                type = str,
                required = True,
                help = "This field cannot be left blank!!"
        )

        parser.add_argument('password',
                type = str,
                required = True,
                help = "This field cannot be left blank!!"
        )


        def post(self):
            data = UserRegister.parser.parse_args()

            if User.find_by_username(data['username']):
            return {'message': "An user with name '{}' already exist".format(data['username'])}, 400

            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "INSERT INTO users VALUES (NULL, ?, ?)"
            cursor.execute(query, (data['username'], data['password'],))

            connection.commit()
            connection.close()

            return {"message": "User created"}, 201
```

2. Dentro de app.py importar UserRegistrer y agregar el recurso

```python
    from user import UserRegister
```

```python
    api.add_resource(UserRegister,'/register')
```

[Video: Signing up y escribir usuario en la base de datos](https://www.udemy.com/rest-api-flask-and-python/learn/v4/t/lecture/5965498?start=0)  
[Video: Evitando usuarion duplicados](https://www.udemy.com/rest-api-flask-and-python/learn/v4/t/lecture/5989182?start=0)

## Obtener un item desde la base de datos

```python
    @jwt_required()
    def get (self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item':{'name':row[0], 'price': row[1]}}, 200
        else:
            return {'message': 'Item not found'}, 404
```

[Video: Obtener un item desde la base de datos](https://www.udemy.com/rest-api-flask-and-python/learn/v4/t/lecture/5965486?start=0)

## Escribir un item en la base de datos

```python
    def post(self, name):
            if Item.find_by_name(name):
                return {'message': "An item with name '{}' already exist".format(name)}, 400

            data = Item.parser.parse_args()

            item = {'name': name, 'price': data['price']}

            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "INSERT INTO items VALUES (?, ?)"
            cursor.execute(query,(item['name'], item['price'],))

            connection.commit()
            connection.close()

            return item, 201
```

[Video: Escribir un item en la base de datos](https://www.udemy.com/rest-api-flask-and-python/learn/v4/t/lecture/5965494?start=0)

## Borrar un item de la base de datos

```python
   def delete(self, name):
        if Item.find_by_name(name) is None:
            return {'message': "An item with name '{}' does not exist".format(name)}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query,(name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}
```

[Video: Borrar un item de la base de datos](https://www.udemy.com/rest-api-flask-and-python/learn/v4/t/lecture/5988604?start=0)


## Refactor insert of items

```python
    @classmethod
    def insert_item(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query,(item['name'], item['price'],))

        connection.commit()
        connection.close()

```

```python
    def post(self, name):
        if Item.find_by_name(name):
            return {'message': "An item with name '{}' already exist".format(name)}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        try:
            Item.insert_item(item)
        except:
            return {'message': "An error occurred inserting the item."},500

        return item, 201
```

**html codes:**  
> 200 OK  
> 201 CREATED  
> 202 ACCEPTED  
> 404 NOT FOUND  
> 400 BAD REQUEST  
> 500 INTERNAL SERVER ERROR  

[Video: refactor insert of items](https://www.udemy.com/rest-api-flask-and-python/learn/v4/t/lecture/5988608?start=0)

## Implementar el metodo put para modificar items

```python
    @classmethod
    def update_item(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query,(item['price'], item['name'],))

        connection.commit()
        connection.close()
```

```python
    def put (self, name):
        data = Item.parser.parse_args()
        item = Item.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                Item.insert_item(updated_item)
            except:
                return {'message': "An error occurred inserting the item."},500
            return updated_item, 201
        else:
            try:
                Item.update_item(updated_item)
            except:
                return {'message': "An error occurred updating the item."},500
            return updated_item
```

[Video: implementar metodo PUT](https://www.udemy.com/rest-api-flask-and-python/learn/v4/t/lecture/5988614?start=0)

## Implementar el metodo GET obtner todos los items

```python
class ItemList(Resource):

    def get (self):
        list_of_items=[]

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * from items"
        result = cursor.execute(query)

        for row in result:
            item = {'name': row[0], 'price':row[1]}
            list_of_items.append(item)

        connection.close()
        return {'items':list_of_items}
```

[Video: Obterner todos los items](https://www.udemy.com/rest-api-flask-and-python/learn/v4/t/lecture/5989696?start=0)


## Configuraciones avanzadas de Flask-JWT

* Changing the authentication endpoint (by default, ``/auth``);
* Changing the token expiration time (by default, ``5 minutes``);
* Changing the authentication key name (by default, ``username``);
* Changing the authentication response body (by default, only contains ``access_token``); and
* Changing the error handlers.

Ver [el blog](http://tecladocode.com/blog/learn-python-advanced-configuration-of-flask-jwt/) (for online viewing) o el archivo ``flask-jwt-guide.pdf`` que se encuentr en la carpeta ``documentacion``.
