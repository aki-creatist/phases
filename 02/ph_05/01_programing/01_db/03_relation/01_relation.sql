--注文と顧客のリレーション
SELECT
ord.order_id,
cus.customer_name
FROM
order_tb ord
JOIN
customer_tb cus
ON
ord.customer_id = cus.customer_id;

--order_tbとorder_detail_tbとproduct_tbの結合
SELECT
ord.order_id,
pro.product_id,
pro.price,
order_detail.product_count,
pro.price *  order_detail.product_count AS sales
FROM
order_tb ord
JOIN
order_detail_tb order_detail
ON
ord.order_id = order_detail.order_id
JOIN
product_tb pro
ON
order_detail.product_id = pro.product_id

--集計
SELECT
ord.order_id,
SUM(order_detail.product_count),
SUM(pro.price *  order_detail.product_count )AS sales
FROM
order_tb ord
JOIN
order_detail_tb order_detail
ON
ord.order_id = order_detail.order_id
JOIN
product_tb pro
ON
order_detail.product_id = pro.product_id
GROUP BY
order_id
ORDER BY
sales desc;

--全員の明細
SELECT
cus.customer_name  ,
ord.order_id ,
pro.product_name ,
pro.price,
detail.product_count ,
pro.price * detail.product_count AS total
FROM
customer_tb cus
JOIN
order_tb ord
ON
cus.customer_id = ord.customer_id
JOIN
order_detail_tb detail
ON
ord.order_id = detail.order_id
JOIN
product_tb pro
on
detail.product_id = pro.product_id
ORDER BY
cus.customer_id desc

--客別売上リスト
SELECT
cus.customer_name  ,
SUM( pro.price * detail.product_count  ) AS sales
FROM
customer_tb cus
JOIN
order_tb ord
ON
cus.customer_id = ord.customer_id
JOIN
order_detail_tb detail
ON
ord.order_id = detail.order_id
JOIN
product_tb pro
ON
detail.product_id = pro.product_id
GROUP BY
cus.customer_id
ORDER BY
sales desc;