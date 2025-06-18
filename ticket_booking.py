import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import pymysql as mysql
from datetime import datetime


# 数据库连接
db = mysql.connect(
    host="127.0.0.1",
    user="wj",
    password="20051005wj",
    database="gaotie"
)


class TicketBookingWindow:
    def __init__(self, root, operation_window,user_id):
        self.root = root
        self.user_id = user_id
        self.operation_window = operation_window
        self.booking_window = tk.Toplevel(self.root)
        self.booking_window.title("车票预定")
        self.booking_window.geometry("600x350")
        self.booking_window.configure(bg="#f0f0f0")
        self.booking_window.columnconfigure(0, weight=1)
        self.booking_window.columnconfigure(1, weight=3)

        # 出发地选择
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT start_place FROM Train")
        start_places = [row[0] for row in cursor.fetchall()]
        tk.Label(self.booking_window, text="出发地:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=10,
                                                                                            pady=5, sticky="e")
        self.combo_start_place = ttk.Combobox(self.booking_window, values=start_places, font=("Arial", 12))
        self.combo_start_place.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # 目的地选择
        tk.Label(self.booking_window, text="目的地:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, padx=10,
                                                                                             pady=5, sticky="e")
        self.combo_end_place = ttk.Combobox(self.booking_window, font=("Arial", 12))
        self.combo_end_place.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # 出发时间选择
        tk.Label(self.booking_window, text="出发时间:", bg="#f0f0f0", font=("Arial", 12)).grid(row=2, column=0, padx=10,
                                                                                              pady=5, sticky="e")
        self.combo_departure_time = ttk.Combobox(self.booking_window, font=("Arial", 12))
        self.combo_departure_time.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # 票价显示
        tk.Label(self.booking_window, text="票价:", bg="#f0f0f0", font=("Arial", 12)).grid(row=3, column=0, padx=10,
                                                                                           pady=5, sticky="e")
        self.label_price = tk.Label(self.booking_window, text="", bg="#f0f0f0", font=("Arial", 12))
        self.label_price.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # 票型选择（单人/团体）
        tk.Label(self.booking_window, text="票型选择:", bg="#f0f0f0", font=("Arial", 12)).grid(row=4, column=0, padx=10,
                                                                                             pady=5, sticky="e")
        self.ticket_type = tk.StringVar(value="single")
        tk.Radiobutton(self.booking_window, text="单人", variable=self.ticket_type, value="single", bg="#f0f0f0",
                       font=("Arial", 12)).grid(row=4, column=1, sticky="w")
        tk.Radiobutton(self.booking_window, text="团体", variable=self.ticket_type, value="group", bg="#f0f0f0",
                       font=("Arial", 12)).grid(row=4, column=1, sticky="e")

        # 绑定事件
        self.combo_start_place.bind("<<ComboboxSelected>>", self.update_end_places)
        self.combo_end_place.bind("<<ComboboxSelected>>", self.update_departure_times)
        self.combo_departure_time.bind("<<ComboboxSelected>>", self.update_price)

        # 创建按钮框架
        button_frame = tk.Frame(self.booking_window, bg="#f0f0f0")
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)

        # 预定按钮（靠左）
        tk.Button(button_frame, text="预定", command=self.book_tickets, bg="#4CAF50", fg="white",
                  font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        # 返回按钮（靠右）
        tk.Button(button_frame, text="返回", command=self.go_back, bg="#f0f0f0", font=("Arial", 12)).pack(side=tk.RIGHT,
                                                                                                           padx=10)

    def update_end_places(self, event):
        start_place = self.combo_start_place.get()
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT end_place FROM Train WHERE start_place = %s", (start_place,))
        end_places = [row[0] for row in cursor.fetchall()]
        self.combo_end_place['values'] = end_places
        self.combo_end_place.set('')

    def update_departure_times(self, event):
        start_place = self.combo_start_place.get()
        end_place = self.combo_end_place.get()
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT departure_time FROM Train WHERE start_place = %s AND end_place = %s",
                       (start_place, end_place))
        departure_times = [str(row[0]) for row in cursor.fetchall()]
        self.combo_departure_time['values'] = departure_times
        self.combo_departure_time.set('')

    def update_price(self, event):
        start_place = self.combo_start_place.get()
        end_place = self.combo_end_place.get()
        departure_time_str = self.combo_departure_time.get()
        if start_place and end_place and departure_time_str:
            departure_time = datetime.strptime(departure_time_str, '%Y-%m-%d %H:%M:%S')
            cursor = db.cursor()
            cursor.execute(
                "SELECT price FROM Train WHERE start_place = %s AND end_place = %s AND departure_time = %s",
                (start_place, end_place, departure_time))
            result = cursor.fetchone()
            if result:
                price = result[0]
                self.label_price.config(text=f"{price} 元")

    def book_tickets(self):
        start_place = self.combo_start_place.get()
        end_place = self.combo_end_place.get()
        departure_time_str = self.combo_departure_time.get()
        price_str = self.label_price.cget("text").replace(" 元", "")

        if not all([start_place, end_place, departure_time_str, price_str]):
            messagebox.showerror("预订失败", "请选择完整的车次信息！")
            return

        price = float(price_str)
        departure_time = datetime.strptime(departure_time_str, '%Y-%m-%d %H:%M:%S')

        # 查询车次ID
        cursor = db.cursor()
        cursor.execute(
            "SELECT train_id, seat_total FROM Train WHERE start_place = %s AND end_place = %s AND departure_time = %s",
            (start_place, end_place, departure_time))
        train_info = cursor.fetchone()

        if not train_info:
            messagebox.showerror("预订失败", "未找到该车次信息！")
            return

        train_id, seat_total = train_info

        if self.ticket_type.get() == "single":
            # 单人票预订：需要输入用户名并验证
            user_name = simpledialog.askstring("单人购票", "请输入您的姓名：")
            if not user_name:
                messagebox.showerror("预订失败", "姓名不能为空！")
                return

            # 检查用户是否存在于 User 表中
            cursor.execute("SELECT user_id FROM User WHERE name = %s", (user_name,))
            user_result = cursor.fetchone()
            if not user_result:
                messagebox.showerror("预订失败", f"用户 {user_name} 不存在，请先注册！")
                return

            user_id = user_result[0]
            self._book_single_ticket(user_id, train_id, price, seat_total)
        else:
            # 团体票预订逻辑
            self._book_group_tickets(train_id, price, seat_total)

    def _book_single_ticket(self, user_id, train_id, price, seat_total):
    # 生成默认座位号（实际应用中应查询可用座位）
        seat_number = f"A{seat_total}"  # 简单示例，实际应分配可用座位

        cursor = db.cursor()
        try:
            buy_time = datetime.now()
            # 开启事务
            db.begin()
        
            # 插入车票记录
            sql_insert = "INSERT INTO Ticket (user_id, train_id, buy_time, seat_number, ticket_price, status) " \
                        "VALUES (%s, %s, %s, %s, %s, '已支付')"
            cursor.execute(sql_insert, (user_id, train_id, buy_time, seat_number, price))
        
            # 提交事务
            db.commit()
            messagebox.showinfo("预订成功", f"单人票预订成功！\n车次: {train_id}\n座位号: {seat_number}")
        except Exception as e:
            # 事务回滚
            db.rollback()
            messagebox.showerror("预订失败", f"单人票预订失败: {str(e)}")
        finally:
            cursor.close()

    def _book_group_tickets(self, train_id, price, seat_total):
        """处理团体票预订"""
        # 获取团体成员姓名（通过对话框输入，多个姓名用逗号分隔）
        names_str = simpledialog.askstring("团体票预订", "请输入团体成员姓名（用逗号分隔）:")
        if not names_str:
            return
        
        member_names = [name.strip() for name in names_str.split(",") if name.strip()]
        if not member_names:
            messagebox.showerror("团体票预订", "请输入有效的成员姓名！")
            return
        
        cursor = db.cursor()
        valid_users = []
        invalid_names = []
        
        # 验证成员是否存在于用户表
        for name in member_names:
            cursor.execute("SELECT user_id FROM User WHERE name = %s", (name,))
            result = cursor.fetchone()
            if result:
                valid_users.append(result[0])
            else:
                invalid_names.append(name)
        
        if invalid_names:
            messagebox.showwarning("团体票预订", f"以下成员不存在于系统中:\n{', '.join(invalid_names)}\n仅为存在的成员预订车票。")
        
        if not valid_users:
            messagebox.showerror("团体票预订", "没有找到有效的成员，预订失败！")
            return
        
        # 检查剩余座位是否足够
        if len(valid_users) > seat_total:
            messagebox.showerror("团体票预订", f"剩余座位不足，仅{seat_total}个座位可用，无法预订{len(valid_users)}张票！")
            return
        
        # 批量插入车票记录
        try:
            buy_time = datetime.now()
            for user_id in valid_users:
                # 生成默认座位号（实际应用中应分配连续座位）
                seat_number = f"A{seat_total - len(valid_users) + valid_users.index(user_id) + 1}"
                sql = "INSERT INTO Ticket (user_id, train_id, buy_time, seat_number, ticket_price, status) " \
                      "VALUES (%s, %s, %s, %s, %s, '已支付')"
                cursor.execute(sql, (user_id, train_id, buy_time, seat_number, price))
            
            # 更新剩余座位
            new_seat_total = seat_total - len(valid_users)
            cursor.execute("UPDATE Train SET seat_total = %s WHERE train_id = %s", (new_seat_total, train_id))
            db.commit()
            
            messagebox.showinfo("团体票预订成功", f"成功为{len(valid_users)}位成员预订车票！\n车次: {train_id}")
        except Exception as e:
            messagebox.showerror("团体票预订失败", f"团体票预订失败: {str(e)}")
            db.rollback()

    def go_back(self):
        self.booking_window.destroy()
        self.operation_window.deiconify()