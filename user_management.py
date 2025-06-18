import tkinter as tk
from tkinter import messagebox, ttk  # 添加 ttk 模块的导入
import pymysql as mysql

# 数据库连接
db = mysql.connect(
    host="127.0.0.1",
    user="wj",
    password="20051005wj",
    database="gaotie"
)

class UserManagementWindow:
    def __init__(self, root, operation_window):
        self.root = root
        self.operation_window = operation_window
        self.management_window = tk.Toplevel(self.root)
        self.management_window.title("用户管理")
        self.management_window.geometry("800x600")

        self.management_window.configure(bg="#f0f0f0")
        self.management_window.columnconfigure(0, weight=1)
        self.management_window.rowconfigure(0, weight=1)

        # 创建一个框架来包含表格和按钮
        main_frame = tk.Frame(self.management_window, bg="#f0f0f0")
        main_frame.pack(pady=20)

        # 创建表格
        self.tree = ttk.Treeview(main_frame, columns=('user_id', 'name', 'password'), show='headings')
        self.tree.heading('user_id', text='用户ID')
        self.tree.heading('name', text='用户名')
        self.tree.heading('password', text='密码')
        self.tree.column('user_id', width=100)
        self.tree.column('name', width=200)
        self.tree.column('password', width=200)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 创建滚动条
        scrollbar = ttk.Scrollbar(main_frame, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # 填充表格
        self.populate_table()

        # 创建操作按钮框架
        button_frame = tk.Frame(self.management_window, bg="#f0f0f0")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="修改密码", command=self.update_password, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="删除用户", command=self.delete_user, bg="#FF5722", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="添加用户", command=self.add_user, bg="#2196F3", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(self.management_window, text="返回", command=self.go_back).pack(expand=True)

    def populate_table(self):
        # 清空表格
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            cursor = db.cursor()
            sql = "SELECT user_id, name, password FROM User WHERE role = 'user'"
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                self.tree.insert('', 'end', values=row)
        except mysql.Error as e:
            messagebox.showerror("数据库错误", f"获取用户信息失败: {str(e)}")

    def update_password(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("错误", "请选择要修改密码的用户！")
            return

        user_id = self.tree.item(selected_item, 'values')[0]
        new_password = tk.simpledialog.askstring("修改密码", "请输入新密码:")
        if new_password:
            try:
                cursor = db.cursor()
                sql = "UPDATE User SET password = %s WHERE user_id = %s"
                cursor.execute(sql, (new_password, user_id))
                db.commit()
                messagebox.showinfo("成功", "密码修改成功！")
                self.populate_table()
            except mysql.Error as e:
                messagebox.showerror("数据库错误", f"修改密码失败: {str(e)}")
                db.rollback()

    def delete_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("错误", "请选择要删除的用户！")
            return

        user_id = self.tree.item(selected_item, 'values')[0]
        confirm = messagebox.askyesno("确认删除", "确定要删除该用户吗？")
        if confirm:
            try:
                cursor = db.cursor()
                sql = "DELETE FROM User WHERE user_id = %s"
                cursor.execute(sql, (user_id,))
                db.commit()
                messagebox.showinfo("成功", "用户删除成功！")
                self.populate_table()
            except mysql.Error as e:
                messagebox.showerror("数据库错误", f"删除用户失败: {str(e)}")
                db.rollback()

    def add_user(self):
        new_name = tk.simpledialog.askstring("添加用户", "请输入用户名:")
        if new_name:
            new_password = tk.simpledialog.askstring("添加用户", "请输入密码:")
            if new_password:
                try:
                    cursor = db.cursor()
                    sql = "INSERT INTO User (name, password, role) VALUES (%s, %s, 'user')"
                    cursor.execute(sql, (new_name, new_password))
                    db.commit()
                    messagebox.showinfo("成功", "用户添加成功！")
                    self.populate_table()
                except mysql.Error as e:
                    messagebox.showerror("数据库错误", f"添加用户失败: {str(e)}")
                    db.rollback()

    def go_back(self):
        self.management_window.destroy()
        self.operation_window.deiconify()