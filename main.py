from gui.app import FileTransferGUI
from utils.logger import logger

"""
局域网文件传输工具主程序入口
"""

if __name__ == "__main__":
    try:
        logger.info("程序启动")
        # 创建并运行GUI应用
        app = FileTransferGUI()
        app.mainloop()
    except Exception as e:
        logger.error(f"程序运行出错: {e}")
        # 显示错误信息
        from tkinter import messagebox
        messagebox.showerror("错误", f"程序运行出错: {str(e)}")
    finally:
        logger.info("程序退出")