-- 有两张表，一张是员工信息表包含员工的姓名、薪资和部门
-- 一张是部门表包含部门的信息
-- 现在使用sql查出每个部门薪资收入top3的员工

-- 	1.	员工信息表 employee：
-- 	•	id：员工 ID
-- 	•	name：员工姓名
-- 	•	salary：员工薪资
-- 	•	department_id：部门 ID
-- 	2.	部门信息表 department：
-- 	•	id：部门 ID
-- 	•	department_name：部门名称
select e.name,e.salary,a.department_name from
    (
        select name,salary,department_id,
       row_number() over(partition by department_id order by salary desc) as salary_rank
from employee
        ) e
on department a
join e.department_id = e.department_id
where e.salary <= 3