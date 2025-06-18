import tkinter as tk
from tkinter import messagebox
import pymysql as mysql
from datetime import datetime, timedelta

# 数据库连接
db = mysql.connect(
    host="127.0.0.1",
    user="wj",
    password="20051005wj",
    database="gaotie"
)

class StatisticalReportWindow:
    def __init__(self, root, operation_window):
        self.root = root
        self.operation_window = operation_window
        self.report_window = tk.Toplevel(self.root)
        self.report_window.title("统计报表")
        self.report_window.geometry("500x300")

        self.report_window.configure(bg="#f0f0f0")
        self.report_window.columnconfigure(0, weight=1)
        self.report_window.rowconfigure(0, weight=1)

        # 创建一个框架来包含按钮
        button_frame = tk.Frame(self.report_window, bg="#f0f0f0")
        button_frame.pack(pady=50)

        tk.Button(button_frame, text="当天统计", command=lambda: self.generate_report('day'), bg="#4CAF50", fg="white", font=("Arial", 12)).pack(expand=True)
        tk.Button(button_frame, text="本周统计", command=lambda: self.generate_report('week'), bg="#4CAF50", fg="white", font=("Arial", 12)).pack(expand=True)
        tk.Button(button_frame, text="本月统计", command=lambda: self.generate_report('month'), bg="#4CAF50", fg="white", font=("Arial", 12)).pack(expand=True)

        tk.Button(self.report_window, text="返回", command=self.go_back).pack(expand=True)

    def generate_report(self, period):
        if period == 'day':
            start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        elif period == 'week':
            today = datetime.now()
            start_date = today - timedelta(days=today.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=6, hours=23, minutes=59, seconds=59, microseconds=999999)
        elif period == 'month':
            today = datetime.now()
            start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            next_month = today.replace(day=28) + timedelta(days=4)
            end_date = next_month - timedelta(days=next_month.day, hours=0, minutes=0, seconds=1, microseconds=0)

        try:
            cursor = db.cursor()

            # 统计总车次
            sql = "SELECT COUNT(DISTINCT train_id) FROM Train WHERE departure_time BETWEEN %s AND %s"
            cursor.execute(sql, (start_date, end_date))
            total_trains = cursor.fetchone()[0]

            # 统计旅客总数
            sql = "SELECT COUNT(*) FROM Ticket JOIN Train ON Ticket.train_id = Train.train_id WHERE Ticket.buy_time BETWEEN %s AND %s AND Ticket.status = '已支付'"
            cursor.execute(sql, (start_date, end_date))
            total_passengers = cursor.fetchone()[0]

            # 统计收入总数
            sql = "SELECT SUM(Ticket.ticket_price) FROM Ticket JOIN Train ON Ticket.train_id = Train.train_id WHERE Ticket.buy_time BETWEEN %s AND %s AND Ticket.status = '已支付'"
            cursor.execute(sql, (start_date, end_date))
            total_income = cursor.fetchone()[0]

            report = f"{period}统计报表：\n总车次: {total_trains}\n旅客总数: {total_passengers}\n收入总数: {total_income}"
            messagebox.showinfo("统计报表", report)
        except mysql.Error as e:
            messagebox.showerror("数据库错误", f"生成报表失败: {str(e)}")
            db.rollback()

    def go_back(self):
        self.report_window.destroy()
        self.operation_window.deiconify()