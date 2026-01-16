import os
import shutil
from datetime import datetime
from .logger import logger

class FileUtils:
    """
    文件处理工具类，用于处理文件的上传、下载和管理
    """
    
    def __init__(self, upload_dir="static/uploads"):
        """
        初始化文件处理工具
        
        Args:
            upload_dir: 上传文件存储目录
        """
        # 使用绝对路径，确保在不同环境下都能正确找到目录
        self.upload_dir = os.path.abspath(upload_dir)
        # 确保上传目录存在
        os.makedirs(self.upload_dir, exist_ok=True)
    
    def get_file_list(self):
        """
        获取文件列表
        
        Returns:
            list: 文件信息列表，包含文件名、大小、修改时间等
        """
        file_list = []
        try:
            for filename in os.listdir(self.upload_dir):
                file_path = os.path.join(self.upload_dir, filename)
                if os.path.isfile(file_path):
                    file_stats = os.stat(file_path)
                    file_list.append({
                        "filename": filename,
                        "size": file_stats.st_size,
                        "mtime": datetime.fromtimestamp(file_stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                        "url": f"/download/{filename}"
                    })
            # 按修改时间倒序排序
            file_list.sort(key=lambda x: x["mtime"], reverse=True)
        except Exception as e:
            logger.error(f"获取文件列表失败: {e}")
        return file_list
    
    def save_file(self, file_obj, filename):
        """
        保存上传的文件
        
        Args:
            file_obj: 文件对象，可以是Flask的FileStorage对象或BytesIO对象
            filename: 文件名
        
        Returns:
            bool: 保存成功返回True，否则返回False
        """
        try:
            file_path = os.path.join(self.upload_dir, filename)
            # 确保文件名唯一
            base_name, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(file_path):
                filename = f"{base_name}_{counter}{ext}"
                file_path = os.path.join(self.upload_dir, filename)
                counter += 1
            
            # 保存文件
            with open(file_path, "wb") as f:
                if hasattr(file_obj, 'save'):
                    # Flask FileStorage对象
                    file_obj.save(f)
                else:
                    # BytesIO或其他文件对象
                    f.write(file_obj.getvalue())
            logger.info(f"文件保存成功: {filename}")
            return True, filename
        except Exception as e:
            logger.error(f"文件保存失败: {e}")
            return False, filename
    
    def delete_file(self, filename):
        """
        删除文件
        
        Args:
            filename: 文件名
        
        Returns:
            bool: 删除成功返回True，否则返回False
        """
        try:
            file_path = os.path.join(self.upload_dir, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"文件删除成功: {filename}")
                return True
            return False
        except Exception as e:
            logger.error(f"文件删除失败: {e}")
            return False
    
    def get_file_path(self, filename):
        """
        获取文件路径
        
        Args:
            filename: 文件名
        
        Returns:
            str or None: 文件路径或None
        """
        file_path = os.path.join(self.upload_dir, filename)
        if os.path.exists(file_path):
            return file_path
        return None
    
    def clear_upload_dir(self):
        """
        清空上传目录
        
        Returns:
            bool: 清空成功返回True，否则返回False
        """
        try:
            for filename in os.listdir(self.upload_dir):
                file_path = os.path.join(self.upload_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            logger.info("上传目录清空成功")
            return True
        except Exception as e:
            logger.error(f"上传目录清空失败: {e}")
            return False

# 创建全局文件工具实例
file_utils = FileUtils()