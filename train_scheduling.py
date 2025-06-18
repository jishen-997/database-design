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

class TrainSchedulingWindow:
    def __init__(self, root, operation_window):
        self.root = root
        self.operation_window = operation_window
        self.scheduling_window = tk.Toplevel(self.root)
        self.scheduling_window.title("车次调度")
        self.scheduling_window.geometry("500x300")

        self.scheduling_window.configure(bg="#f0f0f0")
        self.scheduling_window.columnconfigure(0, weight=1)
        self.scheduling_window.rowconfigure(0, weight=1)

        # 创建一个框架来包含输入框和按钮
        input_frame = tk.Frame(self.scheduling_window, bg="#f0f0f0")
        input_frame.pack(pady=20)

        tk.Label(input_frame, text="车次号:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_train_id = tk.Entry(input_frame, font=("Arial", 12))
        self.entry_train_id.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(input_frame, text="新票价:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_new_price = tk.Entry(input_frame, font=("Arial", 12))
        self.entry_new_price.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Button(input_frame, text="更新票价", command=self.update_price, bg="#4CAF50", fg="white", font=("Arial", 12)).grid(row=2, column=0, columnspan=2, pady=20)

        tk.Button(self.scheduling_window, text="返回", command=self.go_back).pack(expand=True)

    def update_price(self):
        train_id = self.entry_train_id.get()
        new_price = self.entry_new_price.get()

        if not train_id or not new_price:
            messagebox.showerror("错误", "请输入车次号和新票价！")
            return

        try:
            new_price = float(new_price)
            cursor = db.cursor()
            sql = "UPDATE Train SET price = %s WHERE train_id = %s"
            cursor.execute(sql, (new_price, train_id))
            db.commit()
            messagebox.showinfo("成功", "票价更新成功！")
        except ValueError:
            messagebox.showerror("错误", "新票价必须是数字！")
        except mysql.Error as e:
            messagebox.showerror("数据库错误", f"更新票价失败: {str(e)}")
            db.rollback()

    def go_back(self):
        self.scheduling_window.destroy()
        self.operation_window.deiconify()