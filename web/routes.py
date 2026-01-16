from flask import render_template, request, jsonify, send_from_directory
from web import app
from utils.file_utils import file_utils
from utils.user_cache import user_cache
from utils.logger import logger
import os

@app.route('/')
def index():
    """
    首页路由
    
    Returns:
        str: 首页HTML模板
    """
    return render_template('index.html')

@app.route('/api/files')
def get_files():
    """
    获取文件列表API
    
    Returns:
        json: 文件列表
    """
    files = file_utils.get_file_list()
    return jsonify({"files": files})

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    文件上传路由
    
    Returns:
        json: 上传结果
    """
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "没有文件上传"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "message": "没有选择文件"}), 400
        
        success, filename = file_utils.save_file(file, file.filename)
        if success:
            from web.socket_events import socketio
            socketio.emit('file_list_update', {"files": file_utils.get_file_list()})
            return jsonify({"success": True, "message": "文件上传成功", "filename": filename})
        else:
            return jsonify({"success": False, "message": "文件上传失败"}), 500
    except Exception as e:
        logger.error(f"文件上传失败: {e}")
        return jsonify({"success": False, "message": f"文件上传失败: {str(e)}"}), 500

@app.route('/download/<path:filename>')
def download_file(filename):
    """
    文件下载路由
    
    Args:
        filename: 文件名
    
    Returns:
        file: 文件流
    """
    try:
        import urllib.parse
        # 解码URL中的文件名
        filename = urllib.parse.unquote(filename)
        
        # 使用绝对路径确保文件能被正确找到
        upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', app.config['UPLOAD_FOLDER'])
        
        logger.info(f"尝试下载文件: {filename}，路径: {upload_dir}")
        
        return send_from_directory(upload_dir, filename, as_attachment=True)
    except FileNotFoundError:
        logger.error(f"文件下载失败: 文件 {filename} 不存在")
        return jsonify({"success": False, "message": "文件不存在"}), 404
    except Exception as e:
        logger.error(f"文件下载失败: {e}")
        return jsonify({"success": False, "message": f"下载失败: {str(e)}"}), 500

@app.route('/api/users')
def get_users():
    """
    获取用户列表API
    
    Returns:
        json: 用户列表
    """
    users = user_cache.get_all_users()
    return jsonify({"users": users})

@app.route('/api/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    更新用户信息API
    
    Args:
        user_id: 用户ID
    
    Returns:
        json: 更新结果
    """
    try:
        data = request.get_json()
        username = data.get('username')
        if not username:
            return jsonify({"success": False, "message": "用户名不能为空"}), 400
        
        user = user_cache.update_user(user_id, {"username": username})
        if user:
            from web.socket_events import socketio
            socketio.emit('user_list_update', {"users": user_cache.get_all_users()}, broadcast=True)
            return jsonify({"success": True, "user": user})
        else:
            return jsonify({"success": False, "message": "用户不存在"}), 404
    except Exception as e:
        logger.error(f"更新用户信息失败: {e}")
        return jsonify({"success": False, "message": "更新失败"}), 500

@app.route('/delete/<path:filename>', methods=['DELETE'])
def delete_file(filename):
    """
    删除单个文件
    
    Args:
        filename: 文件名
    
    Returns:
        json: 删除结果
    """
    try:
        import urllib.parse
        filename = urllib.parse.unquote(filename)
        
        success = file_utils.delete_file(filename)
        if success:
            from web.socket_events import socketio
            socketio.emit('file_list_update', {"files": file_utils.get_file_list()})
            return jsonify({"success": True, "message": "文件删除成功"})
        else:
            return jsonify({"success": False, "message": "文件删除失败"}), 500
    except Exception as e:
        logger.error(f"文件删除失败: {e}")
        return jsonify({"success": False, "message": f"文件删除失败: {str(e)}"}), 500

@app.route('/batch-delete', methods=['POST'])
def batch_delete_files():
    """
    批量删除文件
    
    Returns:
        json: 删除结果
    """
    try:
        data = request.get_json()
        filenames = data.get('filenames', [])
        
        if not filenames:
            return jsonify({"success": False, "message": "没有选择要删除的文件"}), 400
        
        success_count = 0
        for filename in filenames:
            if file_utils.delete_file(filename):
                success_count += 1
        
        from web.socket_events import socketio
        socketio.emit('file_list_update', {"files": file_utils.get_file_list()})
        
        return jsonify({"success": True, "message": f"成功删除 {success_count} 个文件", "deleted_count": success_count})
    except Exception as e:
        logger.error(f"批量删除文件失败: {e}")
        return jsonify({"success": False, "message": f"批量删除文件失败: {str(e)}"}), 500
