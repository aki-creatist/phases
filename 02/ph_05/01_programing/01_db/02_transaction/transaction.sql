--トランザクション処理 在庫管理
use information_schema;

SELECT
table_name, engine
FROM
tables
WHERE table_name IN ('product_tb', 'order_tb','order_detail_tb','customer_tb');

--在庫情報を保持
UPDATE product_tb SET stock = 10;


--りんご2コを買う場合
--プロセスに整合性を持たせる
----プロセス1 在庫を減らす
----プロセス2 カートの中に入れる
use store_db;
SET AUTOCOMMIT=0;

--プロセス1 在庫を減らす
START TRANSACTION;
UPDATE product_tb SET stock = stock - 2 WHERE product_id  = 1;

--プロセス2 カートの中に入れる
INSERT INTO order_tb (
order_date,
customer_id
)
VALUES
('2014/10/1',1);

--元に戻せる
ROLLBACK;

--反映されていないことを確認
SELECT * FROM order_tb;
SELECT * FROM product_tb;
SELECT * FROM order_detail_tb;

--データ挿入
INSERT INTO order_detail_tb (
order_id,
product_id,
product_count
) VALUES (
LAST_INSERT_ID() ,1,2);

--処理の確定
COMMIT;

--COMMIT後は ROLLBACKしても戻らない
ROLLBACK;