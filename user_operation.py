import tkinter as tk
from ticket_booking import TicketBookingWindow

class UserOperationsWindow:
    def __init__(self, root,user_id):
        self.root = root  # 接收登录界面的根窗口
        self.user_id = user_id
        self.user_window = tk.Toplevel(self.root)  # 使用 Toplevel 创建新窗口
        self.user_window.title("用户操作界面")
        self.user_window.geometry("500x300")

        self.user_window.configure(bg="#f0f0f0")  # 设置背景颜色
        self.user_window.columnconfigure(0, weight=1)
        self.user_window.rowconfigure(0, weight=1)

        # 创建一个框架来包含按钮
        button_frame = tk.Frame(self.user_window, bg="#f0f0f0")
        button_frame.pack(pady=50)

        tk.Button(button_frame, text="车票预定", command=self.show_ticket_booking, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(expand=True)
        tk.Button(button_frame, text="车票退订", command=self.show_ticket_cancellation, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(expand=True)       
        tk.Button(button_frame, text="车讯查询", command=self.show_train_info_query, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(expand=True) 
        tk.Button(self.user_window, text="返回", command=self.go_back).pack(expand=True)

    def show_ticket_booking(self):
        self.user_window.withdraw()
        TicketBookingWindow(self.root, self.user_window,self.user_id)  # 传入当前的用户操作窗口

    def show_ticket_cancellation(self):
        self.user_window.withdraw()
        from ticket_cancellation import TicketCancellationWindow
        TicketCancellationWindow(self.root, self.user_window, self.user_id)  # 传入 user_id

    def show_train_info_query(self):
        self.user_window.withdraw()
        from train_info_query import TrainInfoQueryWindow
        TrainInfoQueryWindow(self.root, self.user_window)  # 调用车讯查询窗口

    def go_back(self):
        self.user_window.destroy()
        self.root.deiconify()  # 重新显示登录界面