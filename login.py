import tkinter as tk
from tkinter import messagebox
import pymysql as mysql
from register import RegisterWindow
from change_password import ChangePasswordWindow

# 数据库连接
db = mysql.connect(
    host="127.0.0.1",
    user="wj",
    password="20051005wj",
    database="gaotie"
)

class LoginWindow:
    def __init__(self, root):
        self.root = root
        window_width = 400  # 可根据实际调整窗口宽度
        window_height = 350  # 可根据实际调整窗口高度
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)
        for i in range(5):
            self.root.rowconfigure(i, weight=1)
        self.root.configure(bg="#f0f0f0")  # 设置背景颜色

        # 创建一个框架来包含登录表单
        form_frame = tk.Frame(self.root, bg="#f0f0f0")
        form_frame.grid(row=0, column=0, columnspan=2, padx=50, pady=50, sticky="nsew")

        tk.Label(form_frame, text="用户名:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_name = tk.Entry(form_frame, font=("Arial", 12))
        self.entry_name.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(form_frame, text="密码:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_password = tk.Entry(form_frame, show='*', font=("Arial", 12))
        self.entry_password.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Button(form_frame, text="登录", command=self.login, bg="#4CAF50", fg="white", font=("Arial", 12)).grid(row=2, column=0, columnspan=2, pady=20)

        tk.Button(form_frame, text="用户注册", command=self.show_register, bg="#2196F3", fg="white", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5)
        tk.Button(form_frame, text="修改密码", command=self.show_change_password, bg="#FF9800", fg="white", font=("Arial", 12)).grid(row=3, column=1, padx=10, pady=5)

    def login(self):
        name = self.entry_name.get()
        password = self.entry_password.get()
        cursor = db.cursor()
        # 修改查询语句，仅使用用户名和密码进行验证
        sql = "SELECT user_id, role FROM User WHERE name = %s AND password = %s"
        cursor.execute(sql, (name, password))
        result = cursor.fetchone()
        if result:
            user_id, role = result
            self.root.withdraw()  # 隐藏登录界面
            if role == 'admin':
                from administrator_operation import AdminOperationsWindow
                AdminOperationsWindow(self.root, user_id)
            else:
                from user_operation import UserOperationsWindow
                UserOperationsWindow(self.root, user_id)
        else:
            messagebox.showerror("登录失败", "用户名或密码错误！")

    def show_register(self):
        self.root.withdraw()
        RegisterWindow(self.root)

    def show_change_password(self):
        self.root.withdraw()
        ChangePasswordWindow(self.root)