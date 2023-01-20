from schemas.general import GeneralCreateSchema
from schemas.subscriber import SubscriberCreateSchema
from schemas.financial import FinancialCreateSchema
from schemas.shareholder import ShareholderCreateSchema
from schemas.prediction import PredictionCreateSchema

import a_tags
import settings
import company_code
from tabs import tab1, tab2, tab3, tab4, tab5
from db.dbmanager import DBManager


def start_scrape(categories):
    shareholders = []
    subscribers = []
    financials = []
    predictions = []
    for category in categories:
        if category == 1:
            result = tab1.scrape_ipostock(code)
            if result:
                general_result.update(result)
        elif category == 2:
            result, shareholders = tab2.scrape_ipostock(code)
            if result:
                general_result.update(result)
        elif category == 3:
            financials = tab3.scrape_ipostock(code)
        elif category == 4:
            result, subscribers = tab4.scrape_ipostock(code)
            if result:
                general_result.update(result)
        elif category == 5:
            predictions, general_result5 = tab5.scrape_ipostock(code)
            if general_result5:
                general_result.update(general_result5)

    return dict(
        general=GeneralCreateSchema(**general_result),
        shareholders=[ShareholderCreateSchema(**shareholder) for shareholder in shareholders],
        subscribers=[SubscriberCreateSchema(**subscriber) for subscriber in subscribers],
        financials=[FinancialCreateSchema(**financial) for financial in financials],
        predictions=[PredictionCreateSchema(**prediction) for prediction in predictions],
    )


if __name__ == "__main__":

    count = 0
    url = f"{settings.IPO_URL}/view_pg"
    company_codes, delisted_codes = company_code.scrape_company_codes()
    print(f"company_codes, delisted_codes: {len(company_codes)}, {len(delisted_codes)}")
    for code in company_codes:
        general_result = {}
        categories = a_tags.scrape_categories(url, code)
        result = start_scrape(categories)

        print(count, code)
        count += 1

        db_instance = DBManager()
        success = db_instance.create(
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
