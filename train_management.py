import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import pymysql as mysql

# 数据库连接函数
def get_db_connection():
    return mysql.connect(
        host="127.0.0.1",
        user="wj",
        password="20051005wj",
        database="gaotie"
    )

class TrainManagementWindow:
    def __init__(self, root, operation_window):
        self.root = root
        self.operation_window = operation_window
        self.management_window = tk.Toplevel(self.root)
        self.management_window.title("车次管理")
        self.management_window.geometry("1000x600")

        self.management_window.configure(bg="#f0f0f0")
        self.management_window.columnconfigure(0, weight=1)
        self.management_window.rowconfigure(0, weight=1)

        # 创建主框架，包含表格和按钮
        main_frame = tk.Frame(self.management_window, bg="#f0f0f0")
        main_frame.pack(pady=20)

        # 表格：显示车次关键信息，与 train 表字段对应
        self.tree = ttk.Treeview(
            main_frame,
            columns=(
                'train_id', 'start_place', 
                'end_place', 'departure_time', 
                'arrive_time', 'price', 
                'run_date', 'seat_total'
            ),
            show='headings',
            selectmode='browse'  # 单选模式，方便选择删除
        )
        # 配置表头与宽度，根据实际展示需求调整
        self.tree.heading('train_id', text='车次ID')
        self.tree.heading('start_place', text='出发地')
        self.tree.heading('end_place', text='目的地')
        self.tree.heading('departure_time', text='出发时间')
        self.tree.heading('arrive_time', text='到达时间')
        self.tree.heading('price', text='票价')
        self.tree.heading('run_date', text='运行日期')
        self.tree.heading('seat_total', text='总座位数')

        self.tree.column('train_id', width=80)
        self.tree.column('start_place', width=100)
        self.tree.column('end_place', width=100)
        self.tree.column('departure_time', width=150)
        self.tree.column('arrive_time', width=150)
        self.tree.column('price', width=80)
        self.tree.column('run_date', width=120)
        self.tree.column('seat_total', width=80)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 滚动条
        scrollbar = ttk.Scrollbar(main_frame, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # 填充表格数据
        self.populate_table()

        # 操作按钮框架
        button_frame = tk.Frame(self.management_window, bg="#f0f0f0")
        button_frame.pack(pady=20)

        tk.Button(
            button_frame, 
            text="删除车次", 
            command=self.delete_train, 
            bg="#FF5722", 
            fg="white", 
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame, 
            text="添加车次", 
            command=self.add_train, 
            bg="#2196F3", 
            fg="white", 
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            self.management_window, 
            text="返回", 
            command=self.go_back
        ).pack(expand=True)

    def populate_table(self):
        """从数据库查询车次数据，填充到表格"""
        # 清空原有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            db = get_db_connection()
            cursor = db.cursor()
            # 查询所有车次字段，与表格列对应
            sql = """
                SELECT 
                    train_id, start_place, end_place, 
                    departure_time, arrive_time, price, 
                    run_date, seat_total 
                FROM train
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                self.tree.insert('', 'end', values=row)
        except mysql.Error as e:
            messagebox.showerror("数据库错误", f"获取车次信息失败: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    def delete_train(self):
        """删除选中的车次"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("错误", "请选择要删除的车次！")
            return
        
        # 获取选中车次的 train_id
        train_id = self.tree.item(selected_item, 'values')[0]
        confirm = messagebox.askyesno("确认删除", "确定要删除该车次吗？删除后相关数据将无法恢复！")
        if confirm:
            try:
                db = get_db_connection()
                cursor = db.cursor()
                sql = "DELETE FROM train WHERE train_id = %s"
                cursor.execute(sql, (train_id,))
                db.commit()
                messagebox.showinfo("成功", "车次删除成功！")
                # 重新加载表格数据
                self.populate_table()
            except mysql.Error as e:
                messagebox.showerror("数据库错误", f"删除车次失败: {str(e)}")
                db.rollback()
            finally:
                if 'db' in locals():
                    db.close()

    def add_train(self):
        """添加新车次，弹出对话框录入信息"""
        # 弹出对话框，依次录入字段值
        train_id = simpledialog.askstring("添加车次", "请输入车次ID（如 C1234）:")
        if not train_id:
            return
        
        start_place = simpledialog.askstring("添加车次", "请输入出发地:")
        if not start_place:
            return
        
        end_place = simpledialog.askstring("添加车次", "请输入目的地:")
        if not end_place:
            return
        
        # 处理日期时间格式，需与数据库 datetime 类型匹配（YYYY-MM-DD HH:MM:SS）
        departure_time = simpledialog.askstring(
            "添加车次", 
            "请输入出发时间（格式：YYYY-MM-DD HH:MM:SS，如 2025-09-17 08:00:00）:"
        )
        if not departure_time:
            return
        
        arrive_time = simpledialog.askstring(
            "添加车次", 
            "请输入到达时间（格式：YYYY-MM-DD HH:MM:SS，如 2025-09-17 10:00:00）:"
        )
        if not arrive_time:
            return
        
        # 票价：需为数字，可转 decimal(10,2)
        price_str = simpledialog.askstring("添加车次", "请输入票价（如 185.06）:")
        if not price_str:
            return
        try:
            price = float(price_str)
        except ValueError:
            messagebox.showerror("错误", "票价需为有效数字！")
            return
        
        # 运行日期：格式 YYYY-MM-DD
        run_date = simpledialog.askstring(
            "添加车次", 
            "请输入运行日期（格式：YYYY-MM-DD，如 2025-09-17）:"
        )
        if not run_date:
            return
        
        # 总座位数：需为整数
        seat_total_str = simpledialog.askstring("添加车次", "请输入总座位数（如 176）:")
        if not seat_total_str:
            return
        try:
            seat_total = int(seat_total_str)
        except ValueError:
            messagebox.showerror("错误", "总座位数需为有效整数！")
            return
        
        # 拼接 SQL 插入语句，与 train 表字段对应
        try:
            db = get_db_connection()
            cursor = db.cursor()
            sql = """
                INSERT INTO train (
                    train_id, start_place, end_place, 
                    departure_time, arrive_time, price, 
                    run_date, seat_total
                ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                sql, 
                (
                    train_id, start_place, end_place, 
                    departure_time, arrive_time, price, 
                    run_date, seat_total
                )
            )
            db.commit()
            messagebox.showinfo("成功", "车次添加成功！")
            # 重新加载表格数据
            self.populate_table()
        except mysql.Error as e:
            messagebox.showerror("数据库错误", f"添加车次失败: {str(e)}")
            db.rollback()
        finally:
            if 'db' in locals():
                db.close()

    def go_back(self):
        """关闭当前窗口，返回上一级操作界面"""
        self.management_window.destroy()
        self.operation_window.deiconify()