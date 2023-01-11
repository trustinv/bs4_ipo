import pandas as pd


def scrape_ipostock(url):
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
    df1 = df[21].iloc[:, 1:4]
    df2 = df1.drop(labels=[4, 7, 12], axis=0)
    df_str = df1.iloc[:2, :]
    df2 = df2.loc[2:, :].astype("float")
    result = pd.concat([df_str, df2])
    df3 = result.T.values
    temp = []
    for data in df3:
        instance = {
            key: float(int(value / (10e7))) if isinstance(value, float) else value
            for key, value in zip(keys, data)
        }
        temp.append(instance)
    return temp


if __name__ == "__main__":
    url = "http://www.ipostock.co.kr/view_pg/view_03.asp?code=B202206162&gmenu="
    financial_result = scrape_ipostock(url)
    from schemas.financial import FinancialCreateSchema

    s = [FinancialCreateSchema(**shareholder) for shareholder in financial_result]
