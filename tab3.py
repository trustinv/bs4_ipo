import pandas as pd
from pprint import pprint as pp
import pandas as pd

from bs4 import BeautifulSoup
from agents import get_user_agents


def scrape_ipostock(url):
    df = pd.read_html(url)
    df1 = df[21].iloc[:,1:4]    
    # 총합계 제거 
    df2 = df1.drop(labels=[4,7,12], axis=0)
    # 축변경 후 이중 array
    df_str = df1.iloc[:2,:]
    df1 = df1.loc[2:, :].astype('int')
    return pd.concat([df_str,df1])
    
    


if __name__ == "__main__":
    url = "http://www.ipostock.co.kr/view_pg/view_03.asp?code=B202206162&gmenu="
    result = scrape_ipostock(url)
    print(result.T.values)
