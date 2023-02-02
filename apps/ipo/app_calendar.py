import re
import datetime


async def parse_appcalendar_data(**kwargs):
    date_criteria = dict(
        ci_public_subscription_date=(1, "청약일"),
        ci_listing_date=(2, "상장일"),
        ci_refund_date=(3, "환불일"),
        ci_demand_forecast_date=(4, "수요예측일"),
    )

    ci_public_subscription_date = (
        False
        if kwargs.get("ci_public_subscription_date") == "공모철회"
        else kwargs.get("ci_public_subscription_date")
    )
    ac_company_name = kwargs.pop("ci_name")

    result = []
    for key, value in kwargs.items():
        ac_category, ac_category_name = date_criteria.get(key)
        match = re.search(r"\d{4}", value)
        if match:
            start_end = value.split("~")
            if ac_category_name in ("환불일", "상장일"):
                ac_sdate = ac_edate = start_end[0]
            elif ac_category_name in ("수요예측일", "공모일"):
                ac_sdate, ac_edate = start_end
            else:
                if len(value.split("~")) != 2:
                    ac_sdate, ac_edate = value.split("~")
                else:
                    ac_sdate = ac_edate = ""
            if not ci_public_subscription_date:
                result.append(
                    dict(
                        ac_sdate="공모철회",
                        ac_edate="공모철회",
                        ac_category=ac_category,
                        ac_category_name=ac_category_name,
                        ac_company_name=ac_company_name,
                        ac_vitalize=1,
                        ac_datetime=datetime.datetime.now(),
                    )
                )
            else:
                result.append(
                    dict(
                        ac_sdate=ac_sdate,
                        ac_edate=ac_edate,
                        ac_category=ac_category,
                        ac_category_name=ac_category_name,
                        ac_company_name=ac_company_name,
                        ac_vitalize=1,
                        ac_datetime=datetime.datetime.now(),
                    )
                )
    return result
