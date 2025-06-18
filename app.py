import tkinter as tk
from login import LoginWindow

if __name__ == '__main__':
    root = tk.Tk()
    root.title("高铁票务系统")
    # 计算窗口居中位置
    window_width = 1000  # 可根据实际调整窗口宽度
    window_height = 800  # 可根据实际调整窗口高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    root.configure(bg="#f0f0f0")  # 设置背景颜色

    # 创建登录窗口
    login_window = LoginWindow(root)

    root.mainloop()