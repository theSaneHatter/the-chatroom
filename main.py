print(f'{__name__} running!')
from flask import Flask, render_template, jsonify, request
import time, random
from datetime import datetime
from flask_socketio import SocketIO, emit
import lib as lib

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/io/button', methods=['POST'])
def button_handler():
    print('button pressed')
    return jsonify({'message':'some shit'})

@app.route('/io/form', methods=['POST'])
def form_handler():
    #time.sleep(1)
    data = request.get_json()
    message = data.get('message')
    messageId = data.get('messageId')

    print(f'form submitted. Content: {message}')
    now = datetime.now()
    time_string = now.strftime("%H:%M:%S")
    ip = request.remote_addr
    username = lib.gen_username(ip)
    if len(message) > 420*10:
        print(f'@update: {ip} violated the limit')
        message = f'user [{username}] is spamming the chat. Here is his IP: [{ip}]'
    full_message = f'{time_string}:[{username}]:{message}'
    print(f'@debug:{time_string}:POSTing new message: >{full_message}< to all users, creater: >{ip}<')
    lib.log(message, ip=ip)
    socketio.emit('new_message', {'message':full_message, 'messageId': messageId, 'username':username})
    return jsonify({'response': full_message})

@app.route('/io/prefix')
def send_prefix():
    ip = request.remote_addr
    uid = lib.gen_username(ip)
    return uid


@app.route('/io/message-update', methods=['POST'])
def upadete_handler():
    time.sleep(5)
    data = request.get_json()
    time_string = now.strftime("%H:%M:%S")
    time.sleep(5)
    return jsonify({'response':f'here is a NEW message at {time_string}'})

@app.route('/hello',methods=['POST','GET'])
def hello():
    time.sleep(3)
    return jsonify({'response':'hello'})

@socketio.on('connect')
def handle_connect():
    ip = request.remote_addr
    msg = f'@debug:{lib.get_time()}:Client>{ip}<connected to socketio'
    lib.log(f'Client [ip=[]{ip}, sessionID={request.sid}] CONNECTED to socketio, sessionID')
    print(msg)

@socketio.on('disconnect')
def handle_disconnect():
    ip = request.remote_addr
    msg = f'@debug:{lib.get_time()}:Client >{ip}< disconnected from socket'
    lib.log(f'Client [ip=[{ip}], sessionID=[{request.sid}] DISCONECTED from socketio, sessionID')
    print(msg)

@socketio.on('event')
def handle_event(data):
    print(f'@debug:receved from client >{data}<')
    emit('new_data', {'message': 'message receved'}, broadcast=True) #broadcast=True if send to ALL connected clients


if __name__ == '__main__':
    lib.backup_logs()
    socketio.run(app, host='0.0.0.0',port=5000,debug=True, log_output=True)

'''
SETUP:
/etc/hosts: ip -- website eg ip resistance.local
/etc/nginx/sites-available/chat-room config
sudo systemctl reload nginx


'''
