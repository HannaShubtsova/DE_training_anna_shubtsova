--1. вывести количество фильмов в каждой категории, отсортировать по убыванию.
select 
	t1."name" ,
	COUNT(t2.film_id ) as film_count, 
from 
	public.category t1 
	join
	public.film_category t2
	on t1.category_id =t2.category_id
group by 1 
order by 2 desc


--2. вывести 10 актеров, чьи фильмы большего всего арендовали, отсортировать по убыванию.

-- по количеству  rentals
select 
 concat(first_name, ' ', last_name) ,
 COUNT (T5.rental_id)
from 
	public.actor T1
	join public.film_actor T2
	on T1.actor_id  = t2.actor_id
	join public.film T3
	on T2.film_id  = T3.film_id 
	join public.inventory  T4 
	on T3.film_id  = T4.inventory_id 
	join public.rental T5
	on T4.inventory_id  = T5.inventory_id 
group by 1
order by 2 desc 
limit 10;

--  по общей продолжительности rental duration
select distinct
 concat(first_name, ' ', last_name)  as name,
 sum(t3.rental_duration)
from 
	public.actor T1
	join public.film_actor T2
	on T1.actor_id  = t2.actor_id
	join public.film T3
	on T2.film_id  = T3.film_id 
group by 1
order by  sum(t3.rental_duration) desc 
limit 10

--3. вывести категорию фильмов, на которую потратили больше всего денег.

select 
	t1."name" ,
	sum(t6.amount)
from 
	public.category t1 
	join
	public.film_category t2
	on t1.category_id =t2.category_id
	--join public.film T3 
	--on t2.film_id  = t3.film_id
	 join public.inventory  T4 
	on T2.film_id  = T4.film_id 
	join public.rental T5
	on T4.inventory_id  = T5.inventory_id 
	join public.payment t6
	on t5.rental_id = t6.rental_id
group by 1 
order by 2 desc
limit 1
--4. вывести названия фильмов, которых нет в inventory. Написать запрос без использования оператора IN.

select t1.title
from
	public.film T1
	left join public.inventory T2
	on t1.film_id = t2.film_id
where t2.inventory_id is null
order by 1

;


--5. вывести топ 3 актеров, которые больше всего появлялись в фильмах в категории “Children”. 
--Если у нескольких актеров одинаковое кол-во фильмов, вывести всех.

with ds as (select 
 t5."name"  as category,
 concat(first_name, ' ', last_name) as name,
 DENSE_RANK () over (order by count(t3.film_id) desc) as r
from 
	public.actor T1
	join public.film_actor T2
	on T1.actor_id  = t2.actor_id
	join public.film T3
	on T2.film_id  = T3.film_id 
	join public.film_category T4 
	on T3.film_id  = T4.film_id 
	join public.category T5
	on t4.category_id  = t5.category_id and t5.name  = 'Children'
group by 1,2
order by 2 desc )
select  name from ds where r<=3
;

--6. вывести города с количеством активных и неактивных клиентов (активный — customer.active = 1).
-- Отсортировать по количеству неактивных клиентов по убыванию.

select 
t1.city ,
count(distinct case when  active = 1 then t3.CUSTOMER_ID else null end) as active_customers,
count (distinct case when active = 0  then t3.customer_id else null end) as not_active_customers,
from 
public.city t1
join public.address t2
on t1.city_id = t2.city_id 
join public.customer t3
on t2.address_id  = t3.address_id 
group by 1
order by 3 desc


--7. вывести категорию фильмов, у которой самое большое кол-во часов суммарной аренды в городах
-- (customer.address_id в этом city), и которые начинаются на букву “a”.
-- То же самое сделать для городов в которых есть символ “-”. Написать все в одном запросе.
-- не поннятна суть что надо вычислять 
select distinct categoty from
(
SELECT 
	t9.city, t1."name"  as categoty,
	
	--SUM(t3.rental_duration),
	rank () over (partition by t9.city order by  sum (t3.rental_duration) desc) r
	--rank () over (partition by t9.city  order by sum (t3.rental_duration)	 par)
	, sum (t3.rental_duration) 
from 
	public.category t1 
	join
	public.film_category t2
	on t1.category_id =t2.category_id
	join public.film T3 
	on t2.film_id  = t3.film_id
	join public.inventory  T4 
	on T2.film_id  = T4.film_id 
	join public.rental T5
	on T4.inventory_id  = T5.inventory_id 
	join public.payment t6
	on t5.rental_id = t6.rental_id
	join public.customer t7
	on t6.customer_id  = t7.customer_id 
	join public.address t8
	on t7.address_id  = t8.address_id 
	join public.city t9
	on t8.city_id  = t9.city_id 
where  UPPER(t3.title)  like 'A%'  or t9.city like '%-%'
group by 1 ,2
order by 1,3
) ds
where R=1
