import tkinter as tk
from tkinter import messagebox, simpledialog
import pymysql as mysql

# 数据库连接
db = mysql.connect(
    host="127.0.0.1",
    user="wj",
    password="20051005wj",
    database="gaotie"
)

class ChangePasswordWindow:
    def __init__(self, root):
        self.root = root
        self.change_window = tk.Toplevel(self.root)
        self.change_window.title("修改密码")
        self.change_window.geometry("500x300")

        self.change_window.configure(bg="#f0f0f0")  # 设置背景颜色

        # 创建一个框架来包含修改密码表单
        form_frame = tk.Frame(self.change_window, bg="#f0f0f0")
        form_frame.pack(padx=50, pady=50)

        tk.Label(form_frame, text="用户名:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_name = tk.Entry(form_frame, font=("Arial", 12))
        self.entry_name.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(form_frame, text="身份证号:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_id_card = tk.Entry(form_frame, font=("Arial", 12))
        self.entry_id_card.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(form_frame, text="旧密码:", bg="#f0f0f0", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_old_password = tk.Entry(form_frame, show='*', font=("Arial", 12))
        self.entry_old_password.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        button_frame = tk.Frame(form_frame, bg="#f0f0f0")
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        tk.Button(button_frame, text="确认修改", command=self.change_password, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="返回", command=self.go_back, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)

    def change_password(self):
        name = self.entry_name.get()
        id_card = self.entry_id_card.get()
        old_password = self.entry_old_password.get()
        cursor = db.cursor()
        sql = "SELECT user_id FROM User WHERE name = %s AND id_card = %s AND password = %s"
        cursor.execute(sql, (name, id_card, old_password))
        result = cursor.fetchone()
        if result:
            new_password = simpledialog.askstring("修改密码", "请输入新密码:")
            if new_password:
                user_id = result[0]
                try:
                    sql = "UPDATE User SET password = %s WHERE user_id = %s"
                    cursor.execute(sql, (new_password, user_id))
                    db.commit()
                    messagebox.showinfo("修改成功", "密码修改成功！")
                    self.change_window.destroy()
                    self.root.deiconify()
                except Exception as e:
                    messagebox.showerror("修改失败", str(e))
                    db.rollback()
        else:
            messagebox.showerror("验证失败", "用户名、身份证号或密码错误！")

    def go_back(self):
        self.change_window.destroy()
        self.root.deiconify()