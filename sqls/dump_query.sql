mysqldump -uroot -pdara100400! trustinv --tables \
company_info_general \
company_info_financial \
company_info_prediction \
company_info_subscriber \
company_info_shareholder \
app_calendar > crawloing_ipo_backup_230202.sql


---

mysql -h -uroot -pdara100400! [database_name] < [dump_file].sql

---
drop database test_trustinv;

create database
    test_trustinv character set utf8mb4 collate utf8mb4_general_ci;

select count(*) from test_trustinv.app_calendar ;

select count(*) from test_trustinv.company_info_general ;

select count(*) from test_trustinv.company_info_financial ;

select count(*) from test_trustinv.company_info_prediction ;

select count(*) from test_trustinv.company_info_shareholder ;

select count(*) from test_trustinv.company_info_subscriber ;

select * from test_trustinv.app_calendar ;

select * from test_trustinv.company_info_general ;

select * from test_trustinv.company_info_financial ;

select * from test_trustinv.company_info_prediction ;

select * from test_trustinv.company_info_shareholder ;

select * from test_trustinv.company_info_subscriber ;