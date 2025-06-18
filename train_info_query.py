import tkinter as tk
from tkinter import ttk, messagebox
import pymysql as mysql
from datetime import datetime

# 数据库连接（根据实际情况修改配置）
db = mysql.connect(
    host="127.0.0.1",
    user="wj",
    password="20051005wj",
    database="gaotie"
)

class TrainInfoQueryWindow:
    def __init__(self, root, operation_window):
        self.root = root
        self.operation_window = operation_window
        self.query_window = tk.Toplevel(self.root)
        self.query_window.title("车讯查询")
        self.query_window.geometry("800x600")
        self.query_window.configure(bg="#f0f0f0")
        self.query_window.columnconfigure(0, weight=1)

        # 标题
        tk.Label(
            self.query_window,
            text="车讯查询",
            bg="#f0f0f0",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # 输入框框架
        input_frame = tk.Frame(self.query_window, bg="#f0f0f0")
        input_frame.pack(pady=10)

        # 出发地标签和输入框
        tk.Label(input_frame, text="出发地:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
        self.start_place_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.start_place_entry.grid(row=0, column=1, padx=10, pady=5)

        # 目的地标签和输入框
        tk.Label(input_frame, text="目的地:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
        self.end_place_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.end_place_entry.grid(row=1, column=1, padx=10, pady=5)

        # 查询按钮
        tk.Button(
            input_frame,
            text="查询",
            command=self.query_trains,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).grid(row=2, column=0, columnspan=2, pady=20)

        # 表格：展示查询结果
        self.tree = ttk.Treeview(
            self.query_window,
            columns=('车次号', '出发时间', '到达时间'),
            show='headings',
            selectmode='none'
        )
        # 配置表头
        self.tree.heading('车次号', text='车次号', anchor='center')
        self.tree.heading('出发时间', text='出发时间', anchor='center')
        self.tree.heading('到达时间', text='到达时间', anchor='center')
        # 配置列宽
        self.tree.column('车次号', width=150, anchor='center')
        self.tree.column('出发时间', width=200, anchor='center')
        self.tree.column('到达时间', width=200, anchor='center')

        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 返回按钮
        tk.Button(
            self.query_window,
            text="返回",
            command=self.go_back,
            bg="#f0f0f0",
            font=("Arial", 12)
        ).pack(pady=10)

    def query_trains(self):
        start_place = self.start_place_entry.get()
        end_place = self.end_place_entry.get()

        if not start_place or not end_place:
            messagebox.showinfo("提示", "请输入出发地和目的地")
            return

        try:
            with db.cursor() as cursor:
                # 查询符合条件的车次信息
                sql = "SELECT train_id, departure_time, arrive_time FROM Train WHERE start_place = %s AND end_place = %s"
                cursor.execute(sql, (start_place, end_place))
                trains = cursor.fetchall()

                # 清空表格
                for _ in self.tree.get_children():
                    self.tree.delete(_)

                if not trains:
                    # 无符合条件的车次，显示提示信息
                    self.tree.insert('', tk.END, values=('该线路暂未开通，敬请期待', '', ''))
                else:
                    # 逐行渲染查询结果
                    for train in trains:
                        train_id, departure_time, arrive_time = train
                        departure_time_str = departure_time.strftime("%Y-%m-%d %H:%M:%S")
                        arrive_time_str = arrive_time.strftime("%Y-%m-%d %H:%M:%S")
                        self.tree.insert(
                            '',
                            tk.END,
                            values=(train_id, departure_time_str, arrive_time_str)
                        )

        except mysql.Error as e:
            messagebox.showerror("数据库错误", f"查询失败: {str(e)}")
            db.rollback()
        except Exception as e:
            messagebox.showerror("错误", f"查询失败: {str(e)}")
            db.rollback()

    def go_back(self):
        """关闭当前窗口，返回上一级"""
        self.query_window.destroy()
        self.operation_window.deiconify()
