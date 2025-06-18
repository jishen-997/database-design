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

class TicketCancellationWindow:
    def __init__(self, root, operation_window, user_id):
        self.root = root
        self.operation_window = operation_window
        self.user_id = user_id  # 接收登录用户的user_id
        self.cancellation_window = tk.Toplevel(self.root)
        self.cancellation_window.title("车票退订")
        self.cancellation_window.geometry("1200x500")
        self.cancellation_window.configure(bg="#f0f0f0")
        self.cancellation_window.columnconfigure(0, weight=1)

        # 标题
        tk.Label(
            self.cancellation_window,
            text="我的车票",
            bg="#f0f0f0",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # 表格：展示车票
        self.tree = ttk.Treeview(
            self.cancellation_window,
            columns=('车次', '座位号', '票价', '状态', '购票时间', '区间', '出发时间'),
            show='headings',
            selectmode='none'  # 禁止默认行选中
        )
        # 配置表头
        self.tree.heading('车次', text='车次', anchor='center')
        self.tree.heading('座位号', text='座位号', anchor='center')
        self.tree.heading('票价', text='票价', anchor='center')
        self.tree.heading('状态', text='状态', anchor='center')
        self.tree.heading('购票时间', text='购票时间', anchor='center')
        self.tree.heading('区间', text='出发地-目的地', anchor='center')
        self.tree.heading('出发时间', text='出发时间', anchor='center')
        # 配置列宽
        self.tree.column('车次', width=100, anchor='center')
        self.tree.column('座位号', width=80, anchor='center')
        self.tree.column('票价', width=80, anchor='center')
        self.tree.column('状态', width=80, anchor='center')
        self.tree.column('购票时间', width=150, anchor='center')
        self.tree.column('区间', width=150, anchor='center')
        self.tree.column('出发时间', width=150, anchor='center')

        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 加载车票数据
        self.load_tickets()

        # 输入车次号的标签和输入框
        tk.Label(self.cancellation_window, text="请输入要退订的车次号:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
        self.train_id_entry = tk.Entry(self.cancellation_window, font=("Arial", 12))
        self.train_id_entry.pack(pady=5)

        # 按钮区
        btn_frame = tk.Frame(self.cancellation_window, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        # 退订按钮
        tk.Button(
            btn_frame,
            text="退订",
            command=self.cancel_tickets,
            bg="#f44336",
            fg="white",
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=40)

        # 返回按钮
        tk.Button(
            btn_frame,
            text="返回",
            command=self.go_back,
            bg="#f0f0f0",
            font=("Arial", 12)
        ).pack(side=tk.RIGHT, padx=40)

    def load_tickets(self):
        """从数据库加载当前用户的车票，渲染到表格"""
        try:
            with db.cursor() as cursor:
                # 联表查询用户未退票的车票
                sql = """
                SELECT t.ticket_id, t.train_id, t.seat_number, t.ticket_price, t.status, 
                       t.buy_time, tr.start_place, tr.end_place, tr.departure_time
                FROM Ticket t
                JOIN Train tr ON t.train_id = tr.train_id
                WHERE t.user_id = %s AND t.status != '已退票'
                """
                cursor.execute(sql, (self.user_id,))
                tickets = cursor.fetchall()

                # 清空表格
                for _ in self.tree.get_children():
                    self.tree.delete(_)

                if not tickets:
                    # 无车票时插入提示行
                    self.tree.insert('', tk.END, values=('','','','无车票记录','','',''))
                    return

                # 逐行渲染车票
                for ticket in tickets:
                    # 确保查询结果有9个字段
                    if len(ticket) != 9:
                        messagebox.showwarning("数据异常", "车票记录字段数量不符，跳过该条")
                        continue

                    (ticket_id, train_id, seat_number, price, status, 
                     buy_time, start_place, end_place, departure_time) = ticket

                    # 格式化时间
                    buy_time_str = buy_time.strftime("%Y-%m-%d %H:%M:%S")
                    departure_time_str = departure_time.strftime("%Y-%m-%d %H:%M:%S")
                    # 格式化票价
                    price_str = f"¥{price:.2f}"
                    # 拼接区间
                    interval = f"{start_place}-{end_place}"

                    # 插入表格行
                    self.tree.insert(
                        '', 
                        tk.END, 
                        values=(train_id, seat_number, price_str, status, 
                                buy_time_str, interval, departure_time_str)
                    )

        except mysql.Error as e:
            messagebox.showerror("数据库错误", f"加载车票信息失败: {str(e)}")
            db.rollback()
        except Exception as e:
            messagebox.showerror("错误", f"加载车票信息失败: {str(e)}")
            db.rollback()

    def cancel_tickets(self):
        """退订用户输入车次号对应的车票：更新状态 + 恢复座位"""
        train_id = self.train_id_entry.get()
        if not train_id:
            messagebox.showinfo("提示", "请输入要退订的车次号")
            return

        if not messagebox.askyesno("确认", f"确定退订车次号为 {train_id} 的车票？"):
            return

        try:
            with db.cursor() as cursor:
                # 1. 查询该用户该车次下的车票
                sql = "SELECT ticket_id, train_id FROM Ticket WHERE user_id = %s AND train_id = %s AND status != '已退票'"
                cursor.execute(sql, (self.user_id, train_id))
                tickets = cursor.fetchall()

                if not tickets:
                    messagebox.showinfo("提示", f"未找到车次号为 {train_id} 的未退票车票")
                    return

                for ticket_id, train_id in tickets:
                    # 2. 更新车票状态为“已退票”
                    sql = "UPDATE Ticket SET status = '已退票' WHERE ticket_id = %s"
                    cursor.execute(sql, (ticket_id,))

                db.commit()
                messagebox.showinfo("成功", "退订完成！")
                self.load_tickets()  # 刷新列表
                self.train_id_entry.delete(0, tk.END)  # 清空输入框

        except mysql.Error as e:
            messagebox.showerror("数据库错误", f"退订失败: {str(e)}")
            db.rollback()
        except Exception as e:
            messagebox.showerror("错误", f"退订失败: {str(e)}")
            db.rollback()

    def go_back(self):
        """关闭当前窗口，返回上一级"""
        self.cancellation_window.destroy()
        self.operation_window.deiconify()