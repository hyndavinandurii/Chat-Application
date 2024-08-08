from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio = SocketIO(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200))
    likes = db.Column(db.Integer, default=0)

@app.route('/')
def index():
    messages = Message.query.all()
    return render_template('index.html', messages=messages)

@app.route('/post_message', methods=['POST'])
def post_message():
    username = request.form.get('username')
    message_text = request.form.get('message')
    image_url = request.form.get('image_url')
    new_message = Message(username=username, message=message_text, image_url=image_url)
    db.session.add(new_message)
    db.session.commit()
    socketio.emit('new_message', {'username': username, 'message': message_text, 'image_url': image_url})
    return redirect(url_for('index'))

@app.route('/like/<int:message_id>', methods=['POST'])
def like(message_id):
    message = Message.query.get(message_id)
    if message:
        message.likes += 1
        db.session.commit()
        socketio.emit('update_likes', {'message_id': message_id, 'likes': message.likes})
    return redirect(url_for('index'))

if __name__ == '__main__':
    socketio.run(app, debug=True)
