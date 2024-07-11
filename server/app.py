from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

# Create Flask app
app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Enable CORS
CORS(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize SQLAlchemy
db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    """Handle GET and POST requests for messages."""
    if request.method == 'GET':
        # Retrieve all messages from the database and serialize them
        messages = Message.query.order_by(Message.created_at.asc()).all()
        msg_dicts = [message.to_dict() for message in messages]
        return jsonify(msg_dicts)
    elif request.method == 'POST':
        # Create a new message and add it to the database
        json_data = request.get_json()
        new_message = Message(
            body=json_data.get('body'),
            username=json_data.get('username')
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    """Handle PATCH and DELETE requests for messages by ID."""
    message = Message.query.filter(Message.id == id).first()

    if message is None:
        # If message is not found, return 404 error
        return {'error': 'message not found'}, 404

    if request.method == 'PATCH':
        # Update message if PATCH request
        json_data = request.get_json()
        if 'body' in json_data:
            message.body = json_data.get('body')
        db.session.add(message)
        db.session.commit()
        return jsonify(message.to_dict()), 200
    elif request.method == 'DELETE':
        # Delete message if DELETE request
        db.session.delete(message)
        db.session.commit()
        return {'delete': 'message been deleted'}