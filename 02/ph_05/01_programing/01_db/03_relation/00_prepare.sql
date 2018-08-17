CREATE database store_db DEFAULT CHARACTER SET utf8;

--商品
INSERT INTO product_tb (
product_name ,
price  ,
detail
) VALUES
('りんご',120 ,'とてもおいしいりんごです。'),
('みかん',100 ,'とてもおいしいみかんです。'),
('もも',200 ,'とてもおいしいももです。'),
('ぶどう',250,'とてもおいしいぶどうです。'),
('さくらんぼ',300,'とてもおいしいさくらんぼです。');

--注文
CREATE TABLE order_tb (
order_id int not null auto_increment primary key,
order_date datetime not null,
customer_id int not null
);

INSERT INTO order_tb (
order_date,
customer_id
)
VALUES
('2014/8/1',2),
('2014/7/1',2),
('2014/7/1',3),
('2014/6/1',1),
('2014/5/1',2);

--注文明細
CREATE TABLE order_detail_tb (
order_detail_id int not null auto_increment primary key,
order_id int not null ,
product_id int not null,
product_count int not null
);

INSERT INTO order_detail_tb (
order_id,
product_id,
product_count
)
VALUES
(1,5,1),
(1,4,2),
(1,2,10),
(2,1,3),
(2,2,4),
(3,1,2),
(3,3,4),
(3,4,3),
(3,5,2),
(4,2,3),
(4,1,5),
(5,5,7);

--顧客
CREATE TABLE customer_tb (
customer_id int not null auto_increment primary key,
customer_name varchar(20) not null ,
customer_age int not null,
address varchar(200) not null
);

INSERT INTO customer_tb (
customer_name,
customer_age,
address
) VALUES
('松本賀生',34,'千葉県'),
('山田太郎',23,'東京都'),
('鈴木次郎',31,'神奈川');