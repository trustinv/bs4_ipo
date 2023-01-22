import asyncio
import company_code

import a_tags
from config.settings import settings
from apps.tabs import tab1, tab2, tab3, tab4, tab5

from db.config import engine, async_session
from db.dals.company_dal import Company
from schemas.general import GeneralCreateSchema
from schemas.subscriber import SubscriberCreateSchema
from schemas.financial import FinancialCreateSchema
from schemas.shareholder import ShareholderCreateSchema
from schemas.prediction import PredictionCreateSchema
from utilities.time_measure import timeit

IPO_URL = settings.IPO_URL


async def start_scrape(categories, code):
    shareholders = []
    subscribers = []
    financials = []
    predictions = []
    general_result = {}

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

    return dict(
        general=GeneralCreateSchema(**general_result).dict(),
        shareholders=[
            ShareholderCreateSchema(**shareholder).dict() for shareholder in shareholders
        ],
        subscribers=[SubscriberCreateSchema(**subscriber).dict() for subscriber in subscribers],
        financials=[FinancialCreateSchema(**financial).dict() for financial in financials],
        predictions=[PredictionCreateSchema(**prediction).dict() for prediction in predictions],
    )


async def get_companies(company_codes):
    for k in company_codes:
        yield k


@timeit
async def main():
    # for i in range(100):
    count = 0
    url = f"{settings.IPO_URL}/view_pg"
    company_codes = await company_code.scrape_company_codes()
    print(f"company_codes: {len(company_codes)}")

    async for code in get_companies(company_codes):
        categories = await a_tags.scrape_categories(url, code)
        result = await start_scrape(categories, code)

        count += 1
        print(count)
        print(
            result["general"]["ci_name"],
            result["general"]["ci_code"],
        )
        async with async_session() as session:
            async with session.begin():
                company = Company(session)
                success = await company.create(
                    general=result["general"],
                    shareholders=result["shareholders"],
                    predictions=result["predictions"],
                    subscribers=result["subscribers"],
                    financials=result["financials"],
                )

        if success:
            print("종목 데이터가 성공적으로 생성 되었습니다")
        else:
            print("실패")

    await engine.dispose()


asyncio.run(main())
