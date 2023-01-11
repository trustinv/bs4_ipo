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


def scrate_categories():
    # request 통신 에러 발생시 시스템 종료
    try:
        req = requests.get(url, headers={"User-Agent": get_user_agents()})
    except Exception:
        sys.exit()

    soup = BeautifulSoup(req.content, "html.parser", from_encoding="utf-8")


if __name__ == "__main__":
    import a_tags

    code = "B202206162"
    url = "http://www.ipostock.co.kr/view_pg"
    categories = a_tags.scrape_categories(url, code)

    general_result1 = tab1.scrape_ipostock(categories[0])
    general_result2, shareholder_results = tab2.scrape_ipostock(categories[1])
    financial_results = tab3.scrape_ipostock(categories[2])
    general_result4, subscriber_results = tab4.scrape_ipostock(categories[3])
    prediction_results, general_result5 = tab5.scrape_ipostock(categories[4])

    general_result = {**general_result1, **general_result2, **general_result4, **general_result5}

    general_results = GeneralCreateSchema(**general_result)
    share_results = [ShareholderCreateSchema(**shareholder) for shareholder in shareholder_results]
    sub_results = [SubscriberCreateSchema(**subscriber) for subscriber in subscriber_results]
    f_results = [FinancialCreateSchema(**shareholder) for shareholder in financial_results]
    p_results = [PredictionCreateSchema(**prediction) for prediction in prediction_results]

    print(
        general_results,
        share_results,
        sub_results,
        f_results,
        p_results,
    )
