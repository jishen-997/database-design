import tkinter as tk
from train_scheduling import TrainSchedulingWindow
from statistical_report import StatisticalReportWindow
from user_management import UserManagementWindow
from train_management import TrainManagementWindow  # 导入用户管理窗口类

class AdminOperationsWindow:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.admin_window = tk.Toplevel(self.root)
        self.admin_window.title("管理员操作界面")
        self.admin_window.geometry("500x300")

        self.admin_window.configure(bg="#f0f0f0")
        self.admin_window.columnconfigure(0, weight=1)
        self.admin_window.rowconfigure(0, weight=1)

        # 创建一个框架来包含按钮
        button_frame = tk.Frame(self.admin_window, bg="#f0f0f0")
        button_frame.pack(pady=50)

        tk.Button(button_frame, text="车次调度", command=self.show_train_scheduling, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(expand=True)
        tk.Button(button_frame, text="统计报表", command=self.show_statistical_report, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(expand=True)
        tk.Button(button_frame, text="用户管理", command=self.show_user_management, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(expand=True)  # 添加用户管理按钮
        tk.Button(button_frame, text="车次管理", command=self.show_train_maganement, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(expand=True)
        tk.Button(self.admin_window, text="返回", command=self.go_back).pack(expand=True)

    def show_train_scheduling(self):
        self.admin_window.withdraw()
        TrainSchedulingWindow(self.root, self.admin_window)

    def show_statistical_report(self):
        self.admin_window.withdraw()
        StatisticalReportWindow(self.root, self.admin_window)

    def show_user_management(self):
        self.admin_window.withdraw()
        UserManagementWindow(self.root, self.admin_window)  # 显示用户管理窗口
    
    def show_train_maganement(self):
        self.admin_window.withdraw()
        TrainManagementWindow(self.root, self.admin_window)

    def go_back(self):
        self.admin_window.destroy()
        self.root.deiconify()  # 重新显示登录界面