-- sql 不区分大小写，分号结束
SHOW DATABASES;
CREATE DATABASE sqllearning;
USE sqllearning;

SELECT prod_name FROM prod_info;

UPDATE
DROP
CREATE DATABASE
INSERT INTO

SHOW DATABASES;
CREATE DATABASE sqllearning;
USE sqllearning;

SELECT sale_price FROM milk_tea;
SELECT prod_id, prod_name, net_w AS net_weight, pro_date, valid_month, in_price, sale_price FROM milk_tea;

SELECT * FROM milk_tea;
SELECT m.prod_name FROM milk_tea AS m;
SELECT m.pro_date, m.sale_price, m.net_w FROM milk_tea AS m;

SELECT m.prod_name FROM milk_tea AS m;

SELECT m.pro_date, m.sale_price, m.net_w FROM milk_tea AS m;

SELECT prod_id, prod_name, net_w AS net_weight, pro_date, valid_month, in_price, sale_price, 0.9 AS discount FROM milk_tea;
SELECT prod_id, prod_name, net_w AS net_weight, pro_date, valid_month, in_price, sale_price, '零食' AS class FROM milk_tea;

SELECT prod_id, prod_name, net_w AS net_weight, pro_date, valid_month, in_price, sale_price, m.sale_price-m.in_price AS profit, 0.9 AS discount, m.sale_price*0.9 AS new_sale FROM milk_tea AS m;

-- 拼接
SELECT m.*, CONCAT(prod_name, '（', net_w, '）') AS '产品信息' FROM milk_tea AS m;

SELECT CONCAT(prod_name, '是', net_w) AS '产品信息' FROM milk_tea;
SELECT m.*, CONCAT(m.prod_name, '是', m.net_w, '单价是', m.sale_price) AS '产品信息' FROM milk_tea AS m;
SELECT  m.*, CONCAT_WS('是', m.prod_name, m.net_w, m.sale_price) AS '产品信息' FROM milk_tea AS m;
SELECT  m.*, CONCAT_WS(' + ', m.prod_name, m.net_w, m.sale_price) AS '产品信息' FROM milk_tea AS m;

SELECT 6;
SELECT CONCAT('SQL', '训练营');
SELECT 15 * 15;
SELECT CONCAT_WS('+', 1, 2, 3, 4);

-- 内容去重
SELECT DISTINCT m.valid_month FROM milk_tea AS m;
SELECT DISTINCT m.sale_price FROM milk_tea AS m;
SELECT DISTINCT m.net_w FROM milk_tea AS m;

-- 结果排序：排序是对整张表进行的，SELECT 只是展示出来。ORDER BY 一定是查询语句的最后一条语句，紧跟；。
SELECT m.prod_id, m.prod_name FROM milk_tea AS m ORDER BY m.pro_date;
SELECT m.* FROM milk_tea AS m ORDER BY m.valid_month;
SELECT m.* FROM milk_tea AS m ORDER BY m.sale_price DESC;
SELECT m.* FROM milk_tea AS m ORDER BY m.pro_date;
SELECT m.* FROM milk_tea AS m ORDER BY m.prod_name;
SELECT m.* FROM milk_tea AS m ORDER BY CONVERT(prod_name USING gbk);

SELECT m.* FROM milk_tea AS m ORDER BY m.valid_month, m.sale_price;
SELECT m.* FROM milk_tea AS m ORDER BY m.valid_month, m.sale_price DESC;
SELECT m.* FROM milk_tea AS m ORDER BY m.valid_month DESC, m.sale_price DESC;

SELECT m.* FROM milk_tea AS m ORDER BY 5, 7;  -- 不建议

-- 过滤子句：from之后 order by 之前

/*
数据类型及其操作
varhcar 文本型
data
decimal
int*/

SELECT ABS(2);
SELECT ABS(-3);
SELECT SQRT(4);
SELECT SQRT(25);
SELECT EXP(2);
SELECT PI();
SELECT PI() + 3;

SELECT LENGTH('你好');
SELECT LENGTH('hello');
SELECT LENGTH('1234');
SELECT CHARACTER_LENGTH('你好');
SELECT CHARACTER_LENGTH('hello');
SELECT CHARACTER_LENGTH('1234');
SELECT LENGTH(RTRIM(' hello  '));
SELECT LENGTH(LTRIM(' hello  '));
SELECT UPPER('aBc');
SELECT LOWER('AbC');
SELECT UPPER(LTRIM(' hello'));

SELECT NOW();
SELECT YEAR(NOW()) ;
SELECT MONTH(NOW());
SELECT DAY(NOW());
SELECT MONTHNAME(NOW());
SELECT DAYNAME(NOW());
SELECT HOUR(NOW());
SELECT MINUTE(NOW());
SELECT SECOND(NOW());
SELECT CURRENT_DATE();
SELECT CURRENT_TIME;
SELECT UPPER(t.id_char) FROM test_sjlx AS t;
SELECT LENGTH(t.id_char) FROM test_sjlx AS t;
SELECT CHAR_LENGTH(t.id_char) FROM test_sjlx AS t;
SELECT CHAR_LENGTH(t.id_char) AS id_char_length FROM test_sjlx AS t;

-- 单表查询最后一节：聚合函数
-- 最好不要在一个语句里面写多个count会出问题，写了distinct稍微好点。
SELECT SUM(m.sale_price - m.in_price) FROM milk_tea AS m  -- 31.5

--聚合和四则运算需要注意空值。四则运算：空值运算会计作空值。Sum：忽略空值。
SELECT m.net_w, SUM(m.sale_price) FROM milk_tea AS m WHERE m.net_w in ('100g','150g') GROUP BY m.net_w;
-- 先过滤再group by

--聚合函数 COUNT SUM AVG MAX MIN
SELECT COUNT(*) FROM milk_tea AS m
SELECT COUNT(1) FROM milk_tea AS m
SELECT COUNT(m.prod_name) FROM milk_tea AS m
SELECT COUNT(m.pro_date) FROM milk_tea AS m
SELECT COUNT(DISTINCT m.sale_price), COUNT(DISTINCT m.pro_date) FROM milk_tea AS m
SELECT DISTINCT m.sale_price FROM milk_tea AS m
SELECT SUM(m.in_price) * 1.1 FROM milk_tea AS m  -- 86.35
SELECT SUM(m.in_price * 1.1) FROM milk_tea AS m  -- 86.35
SELECT SUM(m.sale_price) FROM milk_tea AS m  -- 94.5
SELECT SUM(m.in_price) FROM milk_tea AS m  -- 78.5
SELECT SUM(m.sale_price - m.in_price) FROM milk_tea AS m  -- 31.5
SELECT SUM(m.sale_price) - SUM(m.in_price) FROM milk_tea AS m  -- 16
SELECT SUM(IFNULL(m.sale_price, 0) - m.in_price) FROM milk_tea AS m  -- 16
SELECT AVG(m.sale_price) FROM milk_tea AS m  -- 13.5
SELECT SUM(m.sale_price) / COUNT(m.sale_price) FROM milk_tea AS m  -- 13.5 COUNT(列名)相当于排除了非null行
SELECT SUM(m.sale_price) / COUNT(1) FROM milk_tea AS m  -- 11.8125 COUNT(整行名)不会排除非null行


SELECT MAX(m.sale_price) FROM milk_tea AS m;
SELECT MIN(m.sale_price) FROM milk_tea AS m;
SELECT COUNT(m.sale_price), SUM(m.sale_price), AVG(m.sale_price), MIN(m.sale_price), MAX(m.sale_price), MIN(m.in_price) FROM milk_tea AS m;


SELECT SUM(m.sale_price) FROM milk_tea AS m WHERE m.net_w = '100g';
SELECT SUM(m.sale_price) FROM milk_tea AS m WHERE m.net_w = '150g';
SELECT m.net_w, SUM(m.sale_price) FROM milk_tea AS m WHERE m.net_w in ('100g','150g') GROUP BY m.net_w;
SELECT m.net_w, SUM(m.sale_price) FROM milk_tea AS m WHERE m.net_w = '100g' or m.net_w = '150g' GROUP BY m.net_w;
SELECT m.net_w, COUNT(m.sale_price) FROM milk_tea AS m WHERE m.net_w in ('100g','150g') GROUP BY m.net_w;

SELECT m.net_w, SUM(m.sale_price) FROM milk_tea AS m GROUP BY m.net_w;

SELECT m.net_w, SUM(m.sale_price) FROM milk_tea AS m GROUP BY m.net_w HAVING SUM(m.sale_price) > 20;
SELECT m.net_w, SUM(m.sale_price) FROM milk_tea AS m GROUP BY m.net_w HAVING m.net_w IN ('100g', '200g');   -- 不推荐，因为group by(分组)之前的where已经可以完成这个操作。

SELECT * FROM prod_info as p;
SELECT p.class, COUNT(1) FROM prod_info as p GROUP BY p.class;
SELECT p.class, SUM(p.sale_price) FROM prod_info as p GROUP BY p.class;
SELECT p.class, AVG(p.sale_price) FROM prod_info as p GROUP BY p.class;

SELECT p.class, COUNT(1) FROM prod_info as p GROUP BY p.class HAVING COUNT(1) > 4;
SELECT p.class, COUNT(1) FROM prod_info as p WHERE p.class in ('日用品', '饮料') GROUP BY p.class;
SELECT COUNT(1) FROM prod_info as p WHERE p.class = '零食' and p.sale_price > 10;
SELECT p.class, COUNT(1) FROM prod_info as p WHERE p.sale_price > 10 GROUP BY p.class;


-- 多表查询：
-- 标量子查询：
SELECT m.sale_price FROM milk_tea AS m WHERE m.prod_name = '奶茶';  -- 15

SELECT * 
FROM milk_tea AS m1 
WHERE m1.sale_price >(
											SELECT m.sale_price 
											FROM milk_tea AS m 
											WHERE m.prod_name = '奶茶');

SELECT m1.*, 15 FROM milk_tea AS m1;
SELECT m1.*, (SELECT m.sale_price FROM milk_tea AS m WHERE m.prod_name = '奶茶') FROM milk_tea AS m1;

SELECT p.class, AVG(p.sale_price) FROM prod_info as p GROUP BY p.class HAVING AVG(p.sale_price) > 15;

SELECT p.class, AVG(p.sale_price) 
		FROM prod_info as p 
				GROUP BY p.class 
						HAVING AVG(p.sale_price) > (SELECT m.sale_price FROM milk_tea AS m WHERE m.prod_name = '奶茶');
-- 关联子查询：

SELECT AVG(p1.sale_price) FROM prod_info as p1 WHERE p1.class = '日用品';
SELECT * FROM prod_info as p WHERE p.class = '日用品' AND p.sale_price > (SELECT AVG(p1.sale_price) FROM prod_info as p1 WHERE p1.class = '日用品') ;


SELECT * FROM prod_info as p WHERE p.sale_price > (SELECT AVG(p1.sale_price) FROM prod_info as p1 WHERE p1.class = p.class);

SELECT m.prod_name FROM milk_tea AS m WHERE m.sale_price = 15;
SELECT * FROM milk_tea AS m WHERE m.prod_name IN ('奶茶', '薯片', '薯条');

SELECT * 
FROM milk_tea AS m 
WHERE m.prod_name IN (
											SELECT m1.prod_name 
											FROM milk_tea AS m1
											WHERE m1.sale_price = 15);

SELECT p.prod_name, p.type, p.sale_price FROM prod_info as p WHERE p.prod_name = '抽纸';

SELECT p1.type 
FROM (
			SELECT p.prod_name, p.type, p.sale_price 
			FROM prod_info as p 
			WHERE p.prod_name = '抽纸') AS p1 
WHERE p1.sale_price > 26;

-- 关联
SELECT * FROM prod_info AS p;
SELECT * FROM supplier_info AS s;

SELECT p.prod_name, p.sale_price, s.supplier_name
FROM prod_info AS p, supplier_info AS s
WHERE p.supplier_id = s.supplier_id;

SELECT * FROM prod_info AS p;
SELECT * FROM order_list AS l;
SELECT l.prod_id FROM order_list AS l WHERE l.order_id = '20190401001';
SELECT * FROM prod_info AS p WHERE p.prod_id IN (SELECT l.prod_id FROM order_list AS l WHERE l.order_id = '20190401001');

-- 内联结(只是换了个写法)
SELECT p.*, l.*
FROM prod_info AS p, order_list AS l
WHERE p.prod_id = l.prod_id
AND l.order_id ='20190401001'; 

SELECT p.*, l.*
FROM prod_info AS p INNER JOIN order_list AS l
ON p.prod_id = l.prod_id
AND l.order_id ='20190401001'; 

-- 外联结（保留左边，右边，全部字段）
SELECT * FROM cust_info AS c;
SELECT * FROM order_list AS l WHERE l.date = '2019-04-07';
SELECT * FROM order_list AS l WHERE l.order_id LIKE '20190407%';

SELECT c.*, l.*
FROM cust_info AS c LEFT JOIN order_list AS l
ON c.cust_id = l.cust_id
AND l.order_id LIKE '20190401%';


SELECT c.*, l.*
FROM cust_info AS c LEFT JOIN order_list AS l
ON c.cust_id = l.cust_id
AND l.order_id LIKE '20190401%';

-- 联结后聚合
SELECT c2.cust_id, COUNT(c2.prod_id)
FROM (SELECT c.cust_id, c.cust_name, l.prod_id, l.prodname, l.order_id
			FROM cust_info AS c LEFT JOIN order_list AS l
			ON c.cust_id = l.cust_id
			AND l.order_id LIKE '20190401%') c2
GROUP BY c2.cust_id;


SELECT c.cust_id, COUNT(l.prod_id)
FROM cust_info AS c LEFT JOIN order_list AS l
ON c.cust_id = l.cust_id
AND l.order_id LIKE '20190401%'
GROUP BY c.cust_id;

UNION，UNION ALL：
SELECT * FROM order_list AS l WHERE l.order_id LIKE '20190407%'
UNION
SELECT * FROM order_list AS l WHERE l.order_id LIKE '20190407%';


SELECT * FROM order_list AS l WHERE l.order_id LIKE '20190407%'
UNION ALL
SELECT * FROM order_list AS l WHERE l.order_id LIKE '20190407%';


-- 增删改：在这类操作前都要select from 检查一下要改变的东西。
SELECT * FROM prod_info2 AS p2 ORDER BY p2.prod_id DESC;

INSERT INTO prod_info2 VALUES('T00001', '测试商品', 'test', 'test', 'test', 10, 20, 'NJ0001');

INSERT INTO prod_info2(prod_id, prod_name, brand, type, class, cost, supplier_id) 
VALUES('T00002', '测试商品', 'test', 'test', 'test', 10, 'NJ0001');

INSERT INTO prod_info2(prod_id, prod_name, type, brand, class, cost, supplier_id) 
VALUES('T00003', '测试商品', 'test_t', 'test_b', 'test', 10, 'NJ0001');

SELECT * FROM prod_info AS p WHERE p.prod_id = '10001';

INSERT INTO prod_info2
SELECT CONCAT('T', p.prod_id), p.prod_name, p.type, p.brand, p.class, p.cost, p.sale_price, p.supplier_id 
FROM prod_info AS p 
WHERE p.prod_id = '10001';

INSERT INTO prod_info2(prod_id, prod_name, type, brand, class, cost, supplier_id) 
SELECT CONCAT('T', p.prod_id), p.prod_name, p.type, p.brand, p.class, p.cost, p.supplier_id 
FROM prod_info AS p 
WHERE p.prod_id = '10002';

INSERT INTO prod_info2(prod_id, prod_name,  brand, type,class) 
SELECT CONCAT('T', p.prod_id), p.prod_name, p.brand, p.type, p.class
FROM prod_info AS p 
WHERE p.prod_id = '10003';

INSERT INTO prod_info2(prod_id, prod_name,  brand, type,class) 
SELECT CONCAT('T', p.prod_id), p.prod_name, p.brand, p.type, p.class
FROM prod_info AS p 
WHERE p.prod_id IN ('10004', '10005');


INSERT INTO prod_info2(prod_id, prod_name,  brand, type, class) 
SELECT CONCAT('T', p.prod_id), p.prod_name, p.brand, p.type, p.class
FROM prod_info AS p 
WHERE p.prod_id LIKE '2%';

SELECT * FROM prod_info2 AS p2 ORDER BY p2.prod_id DESC;

SELECT * FROM prod_info2 AS p2 WHERE prod_id LIKE 'T2%';

UPDATE prod_info2
SET class = '日用品'

UPDATE prod_info2
SET class = '零食'
WHERE prod_id LIKE 'T2%';

UPDATE prod_info2
SET class = '饮料'
WHERE prod_id LIKE '3%';

UPDATE prod_info2
SET sale_price = sale_price / 0.9;

SELECT * FROM prod_info2 WHERE prod_name = '抽纸' OR class = '饮料';

UPDATE prod_info2
SET sale_price = sale_price * 0.9
WHERE prod_name = '抽纸' OR class = '饮料';

UPDATE prod_info2
SET sale_price = sale_price / 0.9, cost = cost / 0.9;

SELECT p2.*, p.*
FROM prod_info p, prod_info2 p2
WHERE p2.prod_name = p.prod_name
	AND p2.brand = p.brand
	AND p2.type = p2.type;


UPDATE prod_info2 p2
INNER JOIN prod_info p
SET p2.cost = p.sale_price
WHERE p2.prod_name = p.prod_name
	AND p2.brand = p.brand
	AND p2.type = p2.type;
	
SELECT * FROM prod_info2 WHERE prod_name = '测试商品';

DELETE FROM prod_info2 WHERE prod_name = '测试商品';

DELETE FROM prod_info2 WHERE class = '饮料';

DELETE FROM prod_info2;  -- 慢，一行一行操作

INSERT INTO prod_info2(prod_id, prod_name, type, brand, class, cost, supplier_id) 
SELECT CONCAT('T', p.prod_id), p.prod_name, p.type, p.brand, p.class, p.cost, p.supplier_id 
FROM prod_info AS p 
WHERE p.prod_id = '10002';

TRUNCATE TABLE prod_info2;  -- 快

-- 表操作
 
CREATE TABLE pet2
(name VARCHAR(255) NOT NULL,
owner VARCHAR(255) NOT NULL,
species VARCHAR(255),
sex CHAR(1),
birth DATE,
death DATE
);

SELECT * FROM pet2;

INSERT INTO pet2 VALUES('Bower', 'Diane', 'dog', 'm', '1979-08-31', '1995-07-29');

INSERT INTO pet2(owner, name, species, sex) VALUES('Diane', 'Bower2', 'dog', 'm');

CREATE TABLE pet2
(name VARCHAR(255) NOT NULL,
owner VARCHAR(255) DEFAULT 'police',
species VARCHAR(255),
sex CHAR(1),
birth DATE,
death DATE
);

INSERT INTO pet2(name, species, sex) VALUES('Bower3', 'dog', 'm');

INSERT INTO pet2(owner, name, species, sex) VALUES(NULL, 'Bower4', 'dog', 'm');

UPDATE pet2
SET owner = NULL
WHERE name = 'Bower2'

CREATE TABLE pet3
AS 
SELECT * FROM pet2;

DROP TABLE pet3;

CREATE TABLE pet3
AS 
SELECT p2.name, p2.owner FROM pet2 AS p2;

SELECT * FROM pet3;

CREATE TABLE pet3
AS 
SELECT p2.name, p2.owner FROM pet2 AS p2 WHERE 1 = 2;

ALTER TABLE pet3 ADD sex CHAR(1);

ALTER TABLE pet3 ADD birth DATE NOT NULL;

ALTER TABLE pet3 DROP birth;

ALTER TABLE pet3 DROP birth, DROP sex;

ALTER TABLE pet3 DROP COLUMN birth, DROP COLUMN sex;

ALTER TABLE pet3 MODIFY COLUMN sex VARCHAR(255);

ALTER TABLE pet3 MODIFY COLUMN sex CHAR(1) NOT NULL;

RENAME TABLE pet3 TO pet4;

DROP TABLE pet4;


-- 虚拟表：

CREATE VIEW pet_show
AS
SELECT * FROM pet2;

SELECT ps.name FROM pet_show AS ps WHERE ps.sex =  'f';

DROP VIEW pet_show;

CREATE VIEW pet_show
AS
SELECT name, species FROM pet2;

SELECT * FROM pet_show;

CREATE VIEW pet_show
AS
SELECT name, species FROM pet2
WHERE 1 = 2;

INSERT INTO pet2 VALUES('Buffy', 'Har_old', 'dog', 'f', '1999-05-13', NULL);
INSERT INTO pet2 VALUES('Fluffy', 'Har_old', 'cat', 'm', '1994-03-17', NULL);

CREATE VIEW pet_show
AS
SELECT * FROM pet2
ORDER BY birth;  -- 不推荐，因为很多dbms是禁止的，无效的


/*
new procedure:
CREATE DEFINER=`skip-grants user`@`skip-grants host` PROCEDURE `NewProc`(IN t_num integer)
BEGIN
			CREATE TABLE pet4 AS SELECT * FROM pet2;
			ALTER TABLE pet4 ADD age INT;
			UPDATE pet4 SET age = t_num;
			SELECT * FROM pet4;
			DROP TABLE pet4;
END*/
-- 数据库管理 dcl


