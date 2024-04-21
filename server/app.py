from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)



@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        message_list = [message.to_dict() for message in Message.query.order_by(Message.created_at.asc()).all()]

        return make_response(message_list, 200)
    
    elif request.method == 'POST':
        new_message = Message(
            body = request.json.get('body'),
            username = request.json.get('username')
        )
        db.session.add(new_message)
        db.session.commit()

        return make_response(new_message.to_dict(), 200)


@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()

    if request.method == 'DELETE':
        
        db.session.delete(message)
        db.session.commit()
        return make_response(f'message {message} deleted successfuly!', 200)
    
    elif request.method == 'PATCH':
        for key in request.json:
            setattr(message, key, request.json.get(key))
            db.session.add(message)
            db.session.commit()
        return make_response(message.to_dict(), 201)




if __name__ == '__main__':
    app.run(port=5555)