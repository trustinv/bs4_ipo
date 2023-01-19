from schemas.general import GeneralCreateSchema
from schemas.subscriber import SubscriberCreateSchema
from schemas.financial import FinancialCreateSchema
from schemas.shareholder import ShareholderCreateSchema
from schemas.prediction import PredictionCreateSchema

import a_tags
import settings
import company_code
from tabs import tab1, tab2, tab3, tab4, tab5
from db.dbmanager import DbManager

if __name__ == "__main__":

    count = 0
    url = f"{settings.IPO_URL}/view_pg"
    company_codes = company_code.scrape_company_codes()

    for code in company_codes:
        # for code in ["B201509242"]:
        general_result = {}

        categories = a_tags.scrape_categories(url, code)
        shareholder_results = []
        subscriber_results = []
        financial_results = []
        prediction_results = []
        for category in categories:
            if category == 1:
                result = tab1.scrape_ipostock(code)
                if result:
                    general_result.update(result)
            elif category == 2:
                result, shareholder_results = tab2.scrape_ipostock(code)
                if result:
                    general_result.update(result)
            elif category == 3:
                financial_results = tab3.scrape_ipostock(code)
            elif category == 4:
                result, subscriber_results = tab4.scrape_ipostock(code)
                if result:
                    general_result.update(result)
            elif category == 5:
                prediction_results, general_result5 = tab5.scrape_ipostock(code)
                if general_result5:
                    general_result.update(general_result5)

        general = GeneralCreateSchema(**general_result)
        shareholders = [
            ShareholderCreateSchema(**shareholder) for shareholder in shareholder_results
        ]
        subscribers = [SubscriberCreateSchema(**subscriber) for subscriber in subscriber_results]
        financials = [FinancialCreateSchema(**financial) for financial in financial_results]
        predictions = [PredictionCreateSchema(**prediction) for prediction in prediction_results]

        for i in predictions:
            ci_turnover = general.dict()["ci_turnover"]
            ci_before_corporate_tax = general.dict()["ci_before_corporate_tax"]
            ci_net_profit = general.dict()["ci_net_profit"]
            ci_capital = general.dict()["ci_capital"]
            print(ci_turnover, ci_before_corporate_tax, ci_net_profit, ci_capital)
        print()
        print(count, code)
        count += 1
        dbmanager = DbManager()
        success = dbmanager.create(
            general=general,
            shareholders=shareholders,
            predictions=predictions,
            subscribers=subscribers,
            financials=financials,
        )

        if success:
            print("종목 데이터가 성공적으로 생성 되었습니다")
        else:
            print("실패")
