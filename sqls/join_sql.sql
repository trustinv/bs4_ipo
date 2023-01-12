select *
from
    company_info_general cig cmpany_info_financial cif,
    company_info_prediction cip,
    company_info_shareholder cish,
    company_info_subscriber cisb,
    left outer join cmpany_info_financial as cif,
    company_info_prediction as cip,
    company_info_shareholder as cish,
    company_info_subscriber as cisb,
    on cig.ci_idx = cif.ci_idx,
    cif.ci_idx = cip.ci_idx,
    cip.ci_idx = cish.ci_idx,
    cish.ci_idx = cisb.ci_idx,
where cig.ci_name = '바이오노트';