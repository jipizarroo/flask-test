import os
from flask import Flask, render_template, jsonify, request
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, Contact, Todo

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')   #RUTA DE BASE DE DATOS
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db.init_app(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
CORS(app)


@app.route('/')
def home(): 
    return render_template('index.html', name="home")

@app.route( '/api/contacts', methods=['GET', 'POST'])
@app.route('/api/contacts/<int:id>', methods=['GET', 'PUT','DELETE'])

def contacts(id = None):
    if request.method == 'GET':
        if id is not None:
            contact = Contact.query.get(id)
            if contact:
                return jsonify(contact.serialize()), 200
            else:
                return jsonify({"msg": "Not Found"}), 404
        else:
            contacts = Contact.query.all()
            contacts = list(map(lambda contact: contact.serialize(), contacts))
            return jsonify(contacts), 200

    if request.method == 'POST':
        if not request.json.get('name'):
            return jsonify({"name": "is required"}), 422
        if not request.json.get('phone'):
            return jsonify({"phone": "is required"}), 422

        contact = Contact()
        contact.name = request.json.get('name')
        contact.phone = request.json.get('phone')

        db.session.add(contact)
        db.session.commit()
        return jsonify(contact.serialize()), 201

    if request.method == 'PUT':
        contact = Contact.query.get(id)
        if not contact:
            return jsonify({"msg": "Not Found"}), 404
        
        if not request.json.get('name'):
            return jsonify({"name": "is required"}), 422
        if not request.json.get('phone'):
            return jsonify({"phone": "is required"}), 422

        contact.name = request.json.get('name')
        contact.phone = request.json.get('phone')

        db.session.commit()
        return jsonify(contact.serialize()), 201


    if request.method == 'DELETE':

        contact = Contact.query.get(id)
        if not contact:
            return jsonify({"msg": "Not Found"}), 404

        db.session.delete(contact)
        return jsonify({"msg": "Contact Deleted"}), 200  


@app.route( '/api/todos', methods=['GET', 'POST'])
@app.route('/api/todos/<int:id>', methods=['GET', 'PUT','DELETE'])

def todos(id = None):
    if request.method == 'GET':
        if id is not None:
            todo = Todo.query.get(id)
            if todo:
                return jsonify(todo.serialize()), 200
            else:
                return jsonify({"msg": "Not Found"}), 404
        else:
            todos = Todo.query.all()
            todos = list(map(lambda todo: todo.serialize(), todos))
            return jsonify(todos), 200

    if request.method == 'POST':
        if not request.json.get('label'):
            return jsonify({"label": "is required"}), 422
        if not request.json.get('done'):
            return jsonify({"done": "is required"}), 422

        todo = Todo()
        todo.label = request.json.get('label')
        todo.done = request.json.get('done')

        db.session.add(todo)
        db.session.commit()
        return jsonify(todo.serialize()), 201

    if request.method == 'PUT':
        todo = Todo.query.get(id)
        if not todo:
            return jsonify({"msg": "Not Found"}), 404
        
        if not request.json.get('label'):
            return jsonify({"label": "is required"}), 422
        if not request.json.get('done'):
            return jsonify({"done": "is required"}), 422

        todo.label = request.json.get('label')
        todo.done = request.json.get('done')

        db.session.commit()
        return jsonify(todo.serialize()), 201


    if request.method == 'DELETE':

        todo = Todo.query.get(id)
        if not todo:
            return jsonify({"msg": "Not Found"}), 404

        db.session.delete(todo)
        return jsonify({"msg": "Todo Deleted"}), 200        



if __name__ == "__main__":
    manager.run()
