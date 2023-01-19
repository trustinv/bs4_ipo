-- 기존 B디비의 데이터가 들어 있는 테이블을 A디비에 새로 생성함.

-- create table test_trustinv.company_info_general as select * from trustinv.company_info_general;

-- create table test_trustinv.company_info_financial as select * from trustinv.company_info_financial;

-- create table test_trustinv.company_info_prediction as select * from trustinv.company_info_prediction;

-- create table test_trustinv.company_info_shareholder as select * from trustinv.company_info_shareholder;

-- create table test_trustinv.company_info_subscriber as select * from trustinv.company_info_subscriber;

-- 테이블 데이터 개수

-- select count(*) from test_trustinv.company_info_general ;

-- select count(*) from test_trustinv.company_info_financial ;

-- select count(*) from test_trustinv.company_info_prediction ;

-- select count(*) from test_trustinv.company_info_shareholder ;

-- select count(*) from test_trustinv.company_info_subscriber ;

-- - truncate test_trustinv tables

-- truncate table test_trustinv.company_info_general ;

-- truncate table test_trustinv.company_info_financial ;

-- truncate table test_trustinv.company_info_prediction ;

-- truncate table test_trustinv.company_info_shareholder ;

-- truncate table test_trustinv.company_info_subscriber ;

select *
from
    test_trustinv.company_info_general
where ci_name = '오브젠';