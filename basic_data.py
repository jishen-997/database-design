import pymysql as mysql
import random
from datetime import datetime, timedelta
import datetime
# 数据库连接配置
db = mysql.connect(
    host="127.0.0.1",
    user="wj",
    password="20051005wj",
    database="gaotie"
)

# 定义用户数据列表，包含 10 个普通用户和 3 个管理员
users_data = [
    # 普通用户
    ("张三", "男", 25, "110101199801011234", "123456", "user"),
    ("李四", "女", 30, "120101199302022345", "123456", "user"),
    ("王五", "男", 22, "130101200103033456", "123456", "user"),
    ("赵六", "女", 28, "140101199504044567", "123456", "user"),
    ("孙七", "男", 32, "150101199105055678", "123456", "user"),
    ("周八", "女", 26, "160101199706066789", "123456", "user"),
    ("吴九", "男", 29, "170101199407077890", "123456", "user"),
    ("郑十", "女", 23, "180101200008088901", "123456", "user"),
    ("王十一", "男", 31, "190101199209099012", "123456", "user"),
    ("李十二", "女", 27, "200101199610100123", "123456", "user"),
    # 管理员
    ("管理员1", "男", 40, "210101198311111230", "123456", "admin"),
    ("管理员2", "女", 45, "220101197812122340", "123456", "admin"),
    ("管理员3", "男", 38, "230101198501133450", "123456", "admin")
]

# 定义车次数据列表，包含 20 趟车次
trains_data = [
    ("G1234", "海口", "三亚", "2025-10-01 08:00:00", "2025-10-01 10:30:00", 180.00, "2025-10-01", 200),
    ("D2345", "三亚", "儋州", "2025-10-02 09:30:00", "2025-10-02 12:15:00", 120.00, "2025-10-02", 180),
    ("C3456", "儋州", "文昌", "2025-10-03 10:15:00", "2025-10-03 11:30:00", 50.00, "2025-10-03", 150),
    ("G4567", "文昌", "琼海", "2025-10-04 13:00:00", "2025-10-04 14:15:00", 60.00, "2025-10-04", 220),
    ("D5678", "琼海", "万宁", "2025-10-05 14:45:00", "2025-10-05 16:00:00", 40.00, "2025-10-05", 160),
    ("G6789", "万宁", "东方", "2025-10-06 07:30:00", "2025-10-06 09:45:00", 100.00, "2025-10-06", 210),
    ("D7890", "东方", "五指山", "2025-10-07 09:15:00", "2025-10-07 11:00:00", 80.00, "2025-10-07", 170),
    ("C8901", "五指山", "澄迈", "2025-10-08 11:00:00", "2025-10-08 12:30:00", 70.00, "2025-10-08", 190),
    ("G9012", "澄迈", "临高", "2025-10-09 12:45:00", "2025-10-09 14:00:00", 65.00, "2025-10-09", 200),
    ("D0123", "临高", "海口", "2025-10-10 14:30:00", "2025-10-10 16:45:00", 90.00, "2025-10-10", 230),
    ("G1357", "海口", "万宁", "2025-10-11 08:30:00", "2025-10-11 11:45:00", 150.00, "2025-10-11", 240),
    ("D2468", "万宁", "三亚", "2025-10-12 09:45:00", "2025-10-12 12:30:00", 130.00, "2025-10-12", 210),
    ("C3690", "三亚", "儋州", "2025-10-13 11:15:00", "2025-10-13 13:00:00", 75.00, "2025-10-13", 160),
    ("G4826", "儋州", "文昌", "2025-10-14 13:30:00", "2025-10-14 15:15:00", 60.00, "2025-10-14", 220),
    ("D5731", "文昌", "琼海", "2025-10-15 15:00:00", "2025-10-15 16:15:00", 45.00, "2025-10-15", 170),
    ("G6842", "琼海", "东方", "2025-10-16 07:45:00", "2025-10-16 10:00:00", 120.00, "2025-10-16", 230),
    ("D7953", "东方", "五指山", "2025-10-17 09:30:00", "2025-10-17 11:15:00", 85.00, "2025-10-17", 180),
    ("C8064", "五指山", "澄迈", "2025-10-18 11:30:00", "2025-10-18 13:00:00", 70.00, "2025-10-18", 200),
    ("G9175", "澄迈", "临高", "2025-10-19 13:00:00", "2025-10-19 14:15:00", 60.00, "2025-10-19", 210),
    ("D0286", "临高", "海口", "2025-10-20 14:45:00", "2025-10-20 17:00:00", 110.00, "2025-10-20", 230)
]
hainan_cities = ["海口", "三亚", "儋州", "文昌", "琼海", "万宁", "东方", "五指山", "澄迈", "临高"]
# 生成200条海南省内车次数据
new_trains_data = []
start_date = datetime.datetime(2025, 6, 12)
existing_train_ids = [train[0] for train in trains_data]  # 获取现有的车次ID

for i in range(200):
    # 生成唯一车次ID（G/D/C开头+4位数字）
    while True:
        train_type = random.choice(["G", "D", "C"])
        train_id = f"{train_type}{random.randint(1000, 9999)}"
        if train_id not in existing_train_ids:
            existing_train_ids.append(train_id)
            break
    
    # 随机选择海南省内出发地和目的地（不重复）
    start_place = random.choice(hainan_cities)
    end_place = random.choice([city for city in hainan_cities if city != start_place])
    
    # 生成运行日期（未来1年内）和时间
    run_date = start_date + datetime.timedelta(days=random.randint(0, 365))
    departure_hour = random.randint(6, 20)
    departure_minute = random.choice([0, 15, 30, 45])
    departure_time = run_date.replace(hour=departure_hour, minute=departure_minute)
    travel_hours = random.randint(1, 4)  # 海南省内行程时间缩短为1-4小时
    arrive_time = departure_time + datetime.timedelta(hours=travel_hours)
    
    # 调整票价（原票价范围100-1000调整为30-200，更符合省内短途票价）
    price = round(random.uniform(30, 200), 2)
    seat_total = random.randint(100, 300)  # 座位数保持不变
    
    new_trains_data.append((
        train_id,
        start_place,
        end_place,
        departure_time.strftime("%Y-%m-%d %H:%M:%S"),
        arrive_time.strftime("%Y-%m-%d %H:%M:%S"),
        price,
        run_date.strftime("%Y-%m-%d"),
        seat_total
    ))

# 合并数据
trains_data.extend(new_trains_data)

# 插入用户数据
def insert_users():
    cursor = db.cursor()
    sql = "INSERT INTO User (name, gender, age, id_card, password, role) VALUES (%s, %s, %s, %s, %s, %s)"
    try:
        cursor.executemany(sql, users_data)
        db.commit()
        print("插入用户数据成功！")
    except Exception as e:
        print("插入用户数据失败！", e)
        db.rollback()

# 插入车次数据
def insert_trains():
    cursor = db.cursor()
    sql = "INSERT INTO Train (train_id, start_place, end_place, departure_time, arrive_time, price, run_date, seat_total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        cursor.executemany(sql, trains_data)
        db.commit()
        print("插入车次数据成功！")
    except Exception as e:
        print("插入车次数据失败！", e)
        db.rollback()

if __name__ == '__main__':
    # insert_users()
    insert_trains()
    print("数据插入完成！")