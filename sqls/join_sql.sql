select *
from company_info_general cig
    left join company_info_financial as cif on cig.ci_idx = cif.ci_idx
    left join company_info_prediction as cip on cig.ci_idx = cip.ci_idx
    left join company_info_shareholder as cish on cig.ci_idx = cish.ci_idx
    left join company_info_subscriber as cisb on cig.ci_idx = cisb.ci_idx
where cig.ci_name = '펨트론';

select *
from company_info_general cig
    join company_info_financial as cif on cig.ci_idx = cif.ci_idx
    join company_info_prediction as cip on cig.ci_idx = cip.ci_idx
    join company_info_shareholder as cish on cig.ci_idx = cish.ci_idx
    join company_info_subscriber as cisb on cig.ci_idx = cisb.ci_idx
where cig.ci_name = '펨트론';

select * from company_info_general where ci_idx = 359;

select * from company_info_prediction where ci_idx = 359;

select * from company_info_shareholder where ci_idx = 359;

select * from company_info_subscriber where ci_idx = 359;