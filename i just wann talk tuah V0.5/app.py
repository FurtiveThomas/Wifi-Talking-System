from flask import Flask
from flask_socketio import SocketIO, emit
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def init_db():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, message TEXT)''')
    conn.commit()
    conn.close()

def add_message(username, message):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute("INSERT INTO messages (username, message) VALUES (?, ?)", (username, message))
    conn.commit()
    conn.close()

def get_messages():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute("SELECT username, message FROM messages ORDER BY id ASC")
    messages = c.fetchall()
    conn.close()
    return messages

@socketio.on('connect')
def handle_connect():
    messages = get_messages()
    for username, message in messages:
        emit('update_messages', {'username': username, 'message': message})

@socketio.on('new_message')
def handle_new_message(data):
    username = data['username']
    message = data['message']
    add_message(username, message)
    emit('update_messages', {'username': username, 'message': message}, broadcast=True)

if __name__ == '__main__':
    init_db()
    socketio.run(app, host='192.168.86.250', port=5000, debug=False)
