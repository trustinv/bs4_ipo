import sys
import requests
from bs4 import BeautifulSoup
from tabs import tab1, tab2, tab3, tab4, tab5
from agents import get_user_agents

from schemas.general import GeneralCreateSchema
from schemas.subscriber import SubscriberCreateSchema
from schemas.financial import FinancialCreateSchema
from schemas.shareholder import ShareholderCreateSchema
from schemas.prediction import PredictionCreateSchema


def scrape_categories():
    # request 통신 에러 발생시 시스템 종료
    try:
        req = requests.get(url, headers={"User-Agent": get_user_agents()})
    except Exception:
        sys.exit()

    soup = BeautifulSoup(req.content, "lxml", from_encoding="utf-8")


if __name__ == "__main__":
    import a_tags
    import settings
    import company_code

    company_codes = company_code.scrape_company_codes()

    url = f"{settings.IPO_URL}/view_pg"
    for code in company_codes:

        categories: list[int] = a_tags.scrape_categories(url, code)
        for category in categories:
            if category == 1:
                general_result1 = tab1.scrape_ipostock(code)
            if category == 2:
                general_result2, shareholder_results = tab2.scrape_ipostock(code)
            if category == 3:
                financial_results = tab3.scrape_ipostock(code)
            if category == 4:
                general_result4, subscriber_results = tab4.scrape_ipostock(code[3])
            if category == 5:
                prediction_results, general_result5 = tab5.scrape_ipostock(code[4])

        general_result = {
            **general_result1,
            **general_result2,
            **general_result4,
            **general_result5,
        }

        general = GeneralCreateSchema(**general_result)
        shareholders = [
            ShareholderCreateSchema(**shareholder) for shareholder in shareholder_results
        ]
        subscribers = [SubscriberCreateSchema(**subscriber) for subscriber in subscriber_results]
        financials = [FinancialCreateSchema(**shareholder) for shareholder in financial_results]
        predictions = [PredictionCreateSchema(**prediction) for prediction in prediction_results]

        print(
            general,
            shareholders,
            subscribers,
            financials,
            predictions,
        )
