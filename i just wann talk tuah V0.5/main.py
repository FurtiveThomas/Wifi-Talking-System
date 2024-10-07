import subprocess
import threading
import time
import tkinter as tk
from tkinter import scrolledtext
import socketio

# Initialize the SocketIO client globally
sio = socketio.Client()

# Function to install dependencies
def install_dependencies():
    try:
        subprocess.check_call(['pip', 'install', 'flask', 'flask-socketio', 'python-socketio-client'])
    except subprocess.CalledProcessError:
        print("Error installing dependencies. Ensure you have pip and necessary privileges.")

# Function to run the Flask server
def run_server():
    try:
        subprocess.Popen(['python', 'app.py'])
    except Exception as e:
        print(f"Error starting the server: {e}")

# Function to connect to the server
def connect_to_server():
    sio.connect('http://192.168.86.250:5000')  # Updated connection URL

# Function to send a message
def send_message():
    username = entry_username.get()
    message = entry_message.get()
    if username and message:
        sio.emit('new_message', {'username': username, 'message': message})
        entry_message.delete(0, tk.END)  # Clear the message field

# Function to display received messages
@sio.on('update_messages')
def update_messages(data):
    username = data['username']
    message = data['message']
    message_board.configure(state='normal')
    message_board.insert(tk.END, f"{username}: {message}\n")
    message_board.configure(state='disabled')
    message_board.yview(tk.END)  # Scroll to the latest message

# Create the Tkinter GUI
def create_gui():
    window = tk.Tk()
    window.title("Messaging App")

    # Username label and entry
    tk.Label(window, text="Username:").pack()
    global entry_username
    entry_username = tk.Entry(window, width=50)
    entry_username.pack()

    # Message board
    global message_board
    message_board = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=50, height=20)
    message_board.pack()
    message_board.configure(state='disabled')

    # Message entry and send button
    tk.Label(window, text="Message:").pack()
    global entry_message
    entry_message = tk.Entry(window, width=50)
    entry_message.pack()

    send_button = tk.Button(window, text="Send", command=send_message)
    send_button.pack()

    return window

# Function to launch the Tkinter client
def run_client():
    window = create_gui()
    connect_to_server()  # Connect to the server
    window.mainloop()

# Main function to install dependencies, run the server, and start the client
if __name__ == '__main__':
    # Step 1: Install dependencies
    print("Installing dependencies...")
    install_dependencies()

    # Step 2: Run the Flask server in a background thread
    print("Starting server...")
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    # Step 3: Wait for the server to start
    time.sleep(2)  # Add a small delay to give the server time to start

    # Step 4: Run the Tkinter client
    print("Starting client...")
    run_client()
