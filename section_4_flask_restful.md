# Flask-RESTful

## Crear un entorno virtual

Un entorno virtual nos da una instalacion limpia de Python. Esto nos permite hacer que los proyectos no compartan librerias. Podemos tener dos o mas proyectos corriendo la misma libreria pero diferentes versiones.

> Para saber que librerias tenemos instaladas y las versiones, ejecutar el siguiente comando: ```pip freeze```

1. Instalar la herramienta ```virtualenv``` ejecutando el siguiente comando:

    ```pip install virtualenv```

2. Crear el entorno virtual ejecuanto el siguiente comando dentro de la carpeta donde queremos crearlo:

    ```virtualenv --python "C:\Users\Gabriel\AppData\Local\Programs\Python\Python36-32\python.exe" venv```

    Output:

    ```
    Using base prefix 'C:\\Users\\Gabriel\\AppData\\Local\\Programs\\Python\\Python36-32'
    New python executable in C:\Users\Gabriel\Documents\Projects\curso_rest_api_flask\section_04_Flask_Restful\venv\Scripts\python.exe
    Installing setuptools, pip, wheel...done.
    Running virtualenv with interpreter C:\Users\Gabriel\AppData\Local\Programs\Python\Python36-32\python.exe
    ```
    > Estas instrucciones son validas solo para Windows10, para otros entornos Mac, Linux ver las referencias en el video.

    Este comando nos crea una carpeta llamada venv dentro del directorio donde nos encontramos.

3. Activar el entorno virtual ejecutando el siguiente comando:  

    ```.\venv\Scripts\activate.bat```

    > Estas instrucciones son validas solo para Windows10, para otros entornos Mac, Linux ver las referencias en el video.

4. Para salir del entorno virtual ejecuar el siguiente comando: ```deactivate```

## Instalar la libreria Flask-Restful

Para instalar esta libreria ejecutar el comando ```pip install Flask-RESTful```. Al instalar esta libreria tambien instsala la libreria de Flask.

```
(venv) pip freeze
    click==6.7
    Flask==0.12.2
    itsdangerous==0.24
    Jinja2==2.10
    MarkupSafe==1.0
    SQLAlchemy==1.2.2
    virtualenv==15.1.0
    Werkzeug==0.14.1
```

>Nota: Si estamos dentro del entorno virtual la libreria va a ser cargada solo para el entorno virtual. Por otro lado si estamos fuera del entorno virtual esta libreria no va a ser accesible por el mismo.

[Video: Virtualenvs and setting up Flask-RESTful](https://www.udemy.com/rest-api-flask-and-python/learn/v4/t/lecture/5960148?start=0)

## Primera aplicacion Flask-RESTful

> Crear la carpeta donde se va a alojar el código desde la consola estando dentro del entorno virtual. Crear dentro de esta carpeta el archivo ```app.py```.

Importar las clases ```Resource``` y ```Api``` del modulo ```flask_restful```. Además importar la clase ```Flask``` del modulo ```flask```

```python
    from flask import Flask
    from flask_restful import Resource, Api
```

* RESTful api basica con un recurso y meodo ```GET```:  

```python
    from flask import Flask
    from flask_restful import Resource, Api

    app = Flask (__name__)
    api = Api(app)

    class Student(Resource):
        def get (self, name):
            return {'student':name}

    api.add_resource(Student, '/student/<string:name>')

    app.run(port=5000)
```

* Ejecutar el archivo ```app.py``` desde el entorno virtual:  

    ```python app.py```

[Video: primera aplicacion Flask-RESTful](https://www.udemy.com/rest-api-flask-and-python/learn/v4/t/lecture/5960152?start=0)

## Crear el recurso Item

```python
    items = []

    class Item(Resource):
        def get (self, name):
            for item in items:
                if item['name'] == name:
                    return item
            return {'item': None}, 404

        def post(self, name):
            item = {'name': name, 'price': 12.00}
            items.append(item)
            return item, 201

    api.add_resource(Item, '/item/<string:name>')
```

> **html codes:**  
> 200 OK  
> 201 CREATED  
> 202 ACCEPTED  
> 404 NOT FOUND  

[Video: Crear el recurso Item](https://www.udemy.com/rest-api-flask-and-python/learn/v4/t/lecture/5960156?start=0)