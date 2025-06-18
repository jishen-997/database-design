import tkinter as tk
from tkinter import messagebox
import pymysql as mysql

# 数据库连接
db = mysql.connect(
    host="127.0.0.1",
    user="wj",
    password="20051005wj",
    database="gaotie"
)

class RegisterWindow:
    def __init__(self, root):
        self.root = root
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("用户注册")
        self.new_window.geometry("500x400")

        self.new_window.configure(bg="#f0f0f0")  # 设置背景颜色
        self.new_window.columnconfigure(0, weight=1)
        self.new_window.columnconfigure(1, weight=1)

        # 创建一个框架来包含注册表单
        form_frame = tk.Frame(self.new_window, bg="#f0f0f0")
        form_frame.grid(row=0, column=0, columnspan=2, padx=50, pady=50, sticky="nsew")

        tk.Label(form_frame, text="姓名:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_new_name = tk.Entry(form_frame, font=("Arial", 12))
        self.entry_new_name.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(form_frame, text="性别:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_new_gender = tk.Entry(form_frame, font=("Arial", 12))
        self.entry_new_gender.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(form_frame, text="年龄:", bg="#f0f0f0", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_new_age = tk.Entry(form_frame, font=("Arial", 12))
        self.entry_new_age.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        tk.Label(form_frame, text="身份证号:", bg="#f0f0f0", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entry_new_id_card = tk.Entry(form_frame, font=("Arial", 12))
        self.entry_new_id_card.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        tk.Label(form_frame, text="密码:", bg="#f0f0f0", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.entry_new_password = tk.Entry(form_frame, show='*', font=("Arial", 12))
        self.entry_new_password.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # 添加角色显示标签
        self.role_label = tk.Label(form_frame, text="角色: 用户", bg="#f0f0f0", font=("Arial", 12))
        self.role_label.grid(row=5, column=0, columnspan=2, pady=5)

        # 绑定姓名输入框变化事件
        self.entry_new_name.bind('<KeyRelease>', self.update_role_display)

        button_frame = tk.Frame(self.new_window, bg="#f0f0f0")
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)

        tk.Button(button_frame, text="注册", command=self.save_register, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="返回", command=self.go_back, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)

    def update_role_display(self, event=None):
        """根据姓名首字母更新角色显示"""
        name = self.entry_new_name.get().strip()
        if name and name[0].lower() == 'a':
            self.role_label.config(text="角色: 管理员")
        else:
            self.role_label.config(text="角色: 用户")

    def save_register(self):
        name = self.entry_new_name.get()
        gender = self.entry_new_gender.get()
        age = self.entry_new_age.get()
        id_card = self.entry_new_id_card.get()
        password = self.entry_new_password.get()

        # 根据姓名首字母确定角色
        if name and name[0].lower() == 'a':
            role = 'admin'
        else:
            role = 'user'

        cursor = db.cursor()
        try:
            sql = "INSERT INTO User (name, gender, age, id_card, password, role) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (name, gender, age, id_card, password, role))
            db.commit()
            messagebox.showinfo("注册成功", f"用户注册成功！\n角色: {role}")
            self.new_window.destroy()
            self.root.deiconify()
        except Exception as e:
            messagebox.showerror("注册失败", str(e))
            db.rollback()

    def go_back(self):
        self.new_window.destroy()
        self.root.deiconify()