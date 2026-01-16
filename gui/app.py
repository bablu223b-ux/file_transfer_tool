import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import webbrowser
import socket
import json
import os
import logging
from PIL import Image, ImageTk
import qrcode
from web import app, socketio
from utils.logger import logger

class FileTransferGUI(tk.Tk):
    """
    文件传输工具GUI类
    """
    
    def __init__(self):
        """
        初始化GUI窗口
        """
        super().__init__()
        
        # 读取配置文件
        self.config = self._load_config()
        
        # 初始化变量
        self.server_running = False
        self.server_thread = None
        self.qr_image = None
        
        # 设置窗口属性
        self.title("局域网文件传输工具")
        self.geometry("800x600")
        self.resizable(True, True)
        
        # 创建界面组件
        self._create_widgets()
        
        # 日志重定向
        self._setup_logging()
    
    def _load_config(self):
        """
        加载配置文件
        
        Returns:
            dict: 配置信息
        """
        try:
            with open("config.json", "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            # 返回默认配置
            return {
                "server_port": 5000,
                "upload_dir": "static/uploads",
                "user_cache_file": "users.json",
                "log_level": "INFO",
                "auto_open_browser": True,
                "max_file_size": 104857600
            }
    
    def _create_widgets(self):
        """
        创建GUI组件
        """
        # 主框架
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 顶部控制区
        control_frame = ttk.LabelFrame(main_frame, text="服务控制", padding="10")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 启动/停止按钮
        self.start_btn = ttk.Button(control_frame, text="启动服务", command=self._toggle_server)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 状态显示
        self.status_var = tk.StringVar(value="服务未启动")
        status_label = ttk.Label(control_frame, textvariable=self.status_var, font=("Arial", 12))
        status_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # 服务URL显示
        url_frame = ttk.Frame(control_frame)
        url_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        url_label = ttk.Label(url_frame, text="服务URL:")
        url_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, state="readonly", font=("Arial", 10))
        url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 二维码和日志区
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 二维码显示区
        qr_frame = ttk.LabelFrame(content_frame, text="二维码", padding="10")
        qr_frame.pack(side=tk.LEFT, fill=tk.Y, pady=(0, 10), padx=(0, 10))
        
        self.qr_canvas = tk.Canvas(qr_frame, width=200, height=200, bg="white")
        self.qr_canvas.pack()
        
        # 日志显示区
        log_frame = ttk.LabelFrame(content_frame, text="运行日志", padding="10")
        log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, font=("Arial", 10))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.configure(state="disabled")
    
    def _setup_logging(self):
        """
        设置日志重定向，将日志显示到GUI文本框中
        """
        # 创建自定义日志处理器
        import logging
        from logging.handlers import QueueHandler
        import queue
        
        self.log_queue = queue.Queue()
        queue_handler = QueueHandler(self.log_queue)
        
        # 获取根日志记录器
        root_logger = logging.getLogger()
        root_logger.addHandler(queue_handler)
        
        # 启动日志处理线程
        self.log_thread = threading.Thread(target=self._process_log_queue, daemon=True)
        self.log_thread.start()
    
    def _process_log_queue(self):
        """
        处理日志队列，将日志显示到文本框中
        """
        while True:
            try:
                record = self.log_queue.get()
                if record is None:  # 终止信号
                    break
                msg = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s").format(record)
                self._add_log(msg)
                self.log_queue.task_done()
            except Exception as e:
                logger.error(f"处理日志队列失败: {e}")
    
    def _add_log(self, message):
        """
        向日志文本框添加日志
        
        Args:
            message: 日志消息
        """
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)  # 滚动到底部
        self.log_text.configure(state="disabled")
    
    def _get_local_ip(self):
        """
        获取本地IP地址
        
        Returns:
            str: 本地IP地址
        """
        try:
            # 创建socket连接，不实际连接任何主机
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            logger.error(f"获取本地IP地址失败: {e}")
            return "127.0.0.1"
    
    def _generate_qr_code(self, url):
        """
        生成二维码
        
        Args:
            url: 要生成二维码的URL
        """
        try:
            # 生成二维码
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # 调整大小
            img = img.resize((200, 200), Image.LANCZOS)
            
            # 转换为PhotoImage
            self.qr_image = ImageTk.PhotoImage(img)
            
            # 显示二维码
            self.qr_canvas.delete("all")
            self.qr_canvas.create_image(0, 0, anchor=tk.NW, image=self.qr_image)
        except Exception as e:
            logger.error(f"生成二维码失败: {e}")
    
    def _start_server(self):
        """
        启动Web服务
        """
        try:
            # 获取本地IP地址
            local_ip = self._get_local_ip()
            self.server_url = f"http://{local_ip}:{self.config['server_port']}"
            
            # 生成二维码
            self._generate_qr_code(self.server_url)
            
            # 更新UI
            self.url_var.set(self.server_url)
            self.status_var.set("服务运行中")
            self.start_btn.config(text="停止服务")
            self.server_running = True
            
            logger.info(f"服务已启动，URL: {self.server_url}")
            
            # 自动打开浏览器
            if self.config["auto_open_browser"]:
                webbrowser.open(self.server_url)
            
            # 启动Flask-SocketIO服务器
            socketio.run(app, host="0.0.0.0", port=self.config["server_port"], debug=False, use_reloader=False)
        except Exception as e:
            logger.error(f"启动服务失败: {e}")
            self._stop_server()
    
    def _stop_server(self):
        """
        停止Web服务
        """
        try:
            self.server_running = False
            self.status_var.set("服务已停止")
            self.start_btn.config(text="启动服务")
            self.url_var.set("")
            
            # 清除二维码
            self.qr_canvas.delete("all")
            
            logger.info("服务已停止")
            
            # 终止服务器线程
            if hasattr(self, 'server_thread') and self.server_thread.is_alive():
                # 由于Flask-SocketIO的run()方法是阻塞的，我们需要强制终止线程
                # 这不是最佳实践，但对于我们的简单应用来说是可行的
                import os
                import signal
                os.kill(os.getpid(), signal.SIGTERM)
        except Exception as e:
            logger.error(f"停止服务失败: {e}")
    
    def _toggle_server(self):
        """
        切换服务状态（启动/停止）
        """
        if not self.server_running:
            # 启动服务
            self.server_thread = threading.Thread(target=self._start_server, daemon=True)
            self.server_thread.start()
        else:
            # 停止服务
            self._stop_server()
    
    def on_closing(self):
        """
        窗口关闭事件处理
        """
        if self.server_running:
            self._stop_server()
        self.destroy()

if __name__ == "__main__":
    app = FileTransferGUI()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()