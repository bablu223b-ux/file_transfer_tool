from flask import request
import flask_socketio
from web import socketio
from utils.user_cache import user_cache
from utils.file_utils import file_utils
from utils.logger import logger
from datetime import datetime

# 在线用户字典，key为socket_id，value为user_id
online_users = {}

@socketio.on('connect')
def handle_connect():
    """
    处理用户连接事件
    """
    logger.info(f"用户连接: {request.sid}")
    
@socketio.on('disconnect')
def handle_disconnect():
    """
    处理用户断开事件
    """
    if request.sid in online_users:
        user_id = online_users[request.sid]
        del online_users[request.sid]
        # 移除在线用户连接，使用socket_id跟踪
        user_cache.remove_online_user(user_id, request.sid)
        logger.info(f"用户断开: {request.sid}, user_id: {user_id}")
        # 更新用户最后在线时间
        user_cache.update_user_last_seen(user_id)
        # 广播用户列表更新，只发送在线用户
        online_users_list = user_cache.get_online_users()
        serialized_users = []
        for u in online_users_list:
            serialized_users.append({
                "user_id": u['user_id'],
                "username": u['username'],
                "ip_address": u['ip_address'],
                "device_info": u.get('device_info', ''),
                "last_seen": u.get('last_seen', '')
            })
        socketio.emit('user_list_update', {"users": serialized_users})

@socketio.on('user_login')
def handle_user_login(data):
    """
    处理用户登录事件
    
    Args:
        data: 包含用户信息的数据
    """
    ip_address = request.remote_addr
    device_info = data.get('device_info', '')
    
    # 创建或获取用户
    user = user_cache.create_user(ip_address, device_info)
    online_users[request.sid] = user['user_id']
    # 添加到在线用户列表，传递socket_id
    user_cache.add_online_user(user['user_id'], request.sid)
    
    logger.info(f"用户登录: {user['username']} ({ip_address})")
    
    # 确保user对象是可序列化的，只包含前端需要的数据
    user_data = {
        "user_id": user['user_id'],
        "username": user['username'],
        "ip_address": user['ip_address'],
        "device_info": user.get('device_info', ''),
        "last_seen": user.get('last_seen', '')
    }
    
    # 返回用户信息
    socketio.emit('login_success', user_data)
    
    # 发送当前文件列表给当前用户
    file_list = file_utils.get_file_list()
    socketio.emit('file_list_update', {"files": file_list})
    
    # 广播用户列表更新给所有用户，只发送在线用户
    online_users_list = user_cache.get_online_users()
    # 确保每个用户对象都是可序列化的
    serialized_users = []
    for u in online_users_list:
        serialized_users.append({
            "user_id": u['user_id'],
            "username": u['username'],
            "ip_address": u['ip_address'],
            "device_info": u.get('device_info', ''),
            "last_seen": u.get('last_seen', '')
        })
    socketio.emit('user_list_update', {"users": serialized_users})

@socketio.on('send_message')
def handle_send_message(data):
    """
    处理发送消息事件
    
    Args:
        data: 包含消息内容的数据
    """
    if request.sid in online_users:
        user_id = online_users[request.sid]
        # 获取用户信息
        user = None
        for u in user_cache.get_all_users():
            if u['user_id'] == user_id:
                user = u
                break
        
        if user:
            message = data.get('message', '')
            is_image = data.get('is_image', False)
            if message:
                # 构建消息数据
                msg_data = {
                    "user_id": user_id,
                    "username": user['username'],
                    "message": message,
                    "is_image": is_image,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                # 广播消息给所有用户
                socketio.emit('new_message', msg_data)
                if is_image:
                    logger.info(f"图片消息发送: {user['username']}")
                else:
                    logger.info(f"消息发送: {user['username']}: {message}")

@socketio.on('update_username')
def handle_update_username(data):
    """
    处理更新用户名事件
    
    Args:
        data: 包含新用户名的数据
    """
    if request.sid in online_users:
        user_id = online_users[request.sid]
        new_username = data.get('username', '')
        if new_username:
            # 更新用户名
            user = user_cache.update_user(user_id, {"username": new_username})
            if user:
                # 确保user对象是可序列化的
                user_data = {
                    "user_id": user['user_id'],
                    "username": user['username'],
                    "ip_address": user['ip_address'],
                    "device_info": user.get('device_info', ''),
                    "last_seen": user.get('last_seen', '')
                }
                
                # 广播用户列表更新给所有用户
                online_users_list = user_cache.get_online_users()
                serialized_users = []
                for u in online_users_list:
                    serialized_users.append({
                        "user_id": u['user_id'],
                        "username": u['username'],
                        "ip_address": u['ip_address'],
                        "device_info": u.get('device_info', ''),
                        "last_seen": u.get('last_seen', '')
                    })
                socketio.emit('user_list_update', {"users": serialized_users})
                
                # 返回更新后的用户信息给当前用户
                socketio.emit('username_updated', user_data)
                logger.info(f"用户名更新: {user['username']}")
