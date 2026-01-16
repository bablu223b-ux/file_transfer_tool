from flask import Flask
from flask_socketio import SocketIO
import os

# 创建Flask应用实例
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# 创建SocketIO实例
socketio = SocketIO(app)

# 导入路由和事件处理
from web import routes
from web import socket_events
