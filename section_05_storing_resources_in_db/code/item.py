import sqlite3
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type = float,
            required = True,
            help = "This field cannot be left blank!!"
    )
    
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

    def post(self, name):
        if next(filter(lambda item: item['name'] == name, items), None) is not None:
            return {'message': "An item with name '{}' already exist".format(name)}, 400
        
        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda item: item['name'] != name, items))
        return {'message': 'Item deleted'}
    
    def put (self, name):

        data = Item.parser.parse_args()

        item = next(filter(lambda item: item['name'] == name, items), None)

        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get (self):
        return {'items': items}