import pymysql as mysql
import yaml

db = mysql.connect(
    host="127.0.0.1",
    user="wj",
    password="20051005wj",
    database="gaotie"
)

def  create_table():
    cursor = db.cursor()

    #user_id 自增主键，id_card 唯一约束确保用户身份唯一
    sql_create_table_User = """ create table User(
        user_id int primary key auto_increment,
        name varchar(50) not null,
        gender char(2) not null,
        age int not null,
        id_card varchar(18) unique not null,
        password varchar(100) not null,
        role varchar(20) not null
    )"""

    #train_id 采用 “字母 + 数字” 组合（如 G1234），departure_time 与 arrival_time 精确到时分
    sql_create_table_Train = """ create table Train(
        train_id varchar(20) primary key,
        start_place varchar(50) not null,
        end_place varchar(50) not null,
        departure_time datetime not null,
        arrive_time datetime not null,
        price decimal(10,2) not null,
        run_date date not null,
        seat_total int not null
    )"""

    #ticket_id 自增主键，status 取值为 “已支付”“未支付”“已退票”，外键约束关联 User 表 user_id 和 Train 表 train_id
    sql_create_table_Ticket = """  create table Ticket(
        ticket_id int primary key auto_increment,
        user_id int not null,
        train_id varchar(20),
        buy_time datetime not null,
        seat_number varchar(20),
        ticket_price decimal(10,2) not null,
        status varchar(20) not null,
        foreign key (user_id) references User(user_id),
        foreign key (train_id) references Train(train_id)
    )"""

    #创建数据库表
    try:
        cursor.execute(sql_create_table_User)
        cursor.execute(sql_create_table_Train)
        cursor.execute(sql_create_table_Ticket)
        db.commit()
        print("创建数据库表成功！")
    except Exception as e:
        print("创建数据库表失败！", e)
        db.rollback()

if __name__ == '__main__':
    create_table()