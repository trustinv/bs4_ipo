import math
import pandas as pd


def scrape_ipostock(code):
    url = f"http://www.ipostock.co.kr/view_pg/view_03.asp?code={code}"
    keys = [
        "ci_category1",
        "ci_category2",
        "ci_current_asset",
        "ci_non_current_asset",
        "ci_current_liability",
        "ci_non_current_liability",
        "ci_capital",
        "ci_capital_surplus",
        "ci_earned_surplus",
        "ci_other_capital_items",
        "ci_turnover",
        "ci_business_profits",
        "ci_net_income",
    ]
    df = pd.read_html(url)
    df1 = df[21]
    df1 = df1[~df1[0].isin(["자산총계", "부채총계", "자본총계"])]
    df1 = df1.iloc[:, 1:4]
    df_str = df1.iloc[:2, :]
    df2 = df1.loc[2:, :].astype("float")
    result = pd.concat([df_str, df2])
    df3 = result.T.values
    temp_data = []
    for data_row in df3:
        data_instance = {}
        for key, value in zip(keys, data_row):
            if isinstance(value, float):
                if math.isnan(value):
                    processed_value = format(value, ".2f")
                else:
                    processed_value = format(value / (10e7), ".2f")
            else:
                processed_value = value
            data_instance[key] = processed_value
        temp_data.append(data_instance)
    return temp_data


if __name__ == "__main__":
    code = "B202010131"
    financial_result = scrape_ipostock(code)
    from pprint import pprint as pp

    pp(financial_result[1])
    # pp(financial_result[0])
    # pp(financial_result[1])
    # pp(financial_result[2])
    # from schemas.financial import FinancialCreateSchema

    # s = [FinancialCreateSchema(**shareholder) for shareholder in financial_result]
    # print(s)
