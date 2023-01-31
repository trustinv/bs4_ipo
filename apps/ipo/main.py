import re
import asyncio
import company_code
import datetime

import a_tags
from apps.ipo.tabs import tab1, tab2, tab3, tab4, tab5

from config.settings import IPO_URL
from db.config import engine, async_session
from db.dals.company_dal import Company
from schemas.general import GeneralCreateSchema
from schemas.subscriber import SubscriberCreateSchema
from schemas.financial import FinancialCreateSchema
from schemas.shareholder import ShareholderCreateSchema
from schemas.prediction import PredictionCreateSchema
from schemas.calendar import CalendarCreateSchema
from utilities.time_measure import timeit
from config.config_log import logging

logger = logging.getLogger("info-logger")


async def parse_appcalendar_data(**kwargs):
    date_criteria = dict(
        ci_demand_forecast_date=(1, "수요예측일"),
        ci_public_subscription_date=(2, "공모일"),
        ci_refund_date=(3, "환불일"),
        ci_payment_date=(4, "납입일"),
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
            if ac_category_name in ("환불일", "납입일"):
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


async def start_scrape(categories, code):
    shareholders = []
    subscribers = []
    financials = []
    predictions = []
    general_result = {}
    logger.debug(f"기업코드: {code} / 수집 가능한 탭: {categories}")
    for category in categories:
        if category == 1:
            result = await tab1.scrape_ipostock(code)
            if result:
                general_result.update(result)
        elif category == 2:
            result, shareholders = await tab2.scrape_ipostock(code)
            if result:
                general_result.update(result)
        elif category == 3:
            financials = await tab3.scrape_ipostock(code)
        elif category == 4:
            result, subscribers = await tab4.scrape_ipostock(code)
            if result:
                general_result.update(result)
        elif category == 5:
            predictions, general_result5 = await tab5.scrape_ipostock(code)
            if general_result5:
                general_result.update(general_result5)

    general = GeneralCreateSchema(**general_result)
    logger.info(f"기업명: {general.ci_name}")
    parsed_appcalendar_result = await parse_appcalendar_data(
        ci_demand_forecast_date=general.ci_demand_forecast_date,
        ci_public_subscription_date=general.ci_public_subscription_date,
        ci_refund_date=general.ci_refund_date,
        ci_payment_date=general.ci_payment_date,
        ci_name=general.ci_name,
    )

    result = dict(
        general=general,
        shareholders=[ShareholderCreateSchema(**shareholder) for shareholder in shareholders],
        subscribers=[SubscriberCreateSchema(**subscriber) for subscriber in subscribers],
        financials=[FinancialCreateSchema(**financial) for financial in financials],
        predictions=[PredictionCreateSchema(**prediction) for prediction in predictions],
        calendars=[CalendarCreateSchema(**calendar) for calendar in parsed_appcalendar_result],
    )
    return result


async def get_companies(company_codes):
    for k in company_codes:
        yield k


@timeit
async def main():
    try:
        count = 0
        url = f"{IPO_URL}/view_pg"
        company_codes = await company_code.scrape_company_codes()
        logger.info(f"수집을 시도 할 기업 수: {len(company_codes)}")

        async for code in get_companies(company_codes):
            categories = await a_tags.scrape_categories(url, code)
            result = await start_scrape(categories, code)

            count += 1
            # ci_name = result["general"].ci_name
            # ci_code = result["general"].ci_code
            logger.info(f"총 처리 수: {count}")
            async with async_session() as session:
                async with session.begin():
                    company = Company(session)
                    await company.upsert(
                        general=result["general"],
                        shareholders=result["shareholders"],
                        predictions=result["predictions"],
                        subscribers=result["subscribers"],
                        financials=result["financials"],
                        calendars=result["calendars"],
                    )
    finally:
        logger.info("DB와의 연결을 종료합니다")
        await engine.dispose()
        logger.info("메인 프로세스를 종료합니다.")


asyncio.run(main())
