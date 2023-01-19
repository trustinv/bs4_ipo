import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import DB_URL
from utilities.session import session_scope
from db import models
from sqlalchemy import and_
from settings import DB_URL, DELISTING
from utilities.session import session_scope


class DbManager:
    def __init__(self, *args, **kwargs):
        self.engine = create_engine(DB_URL, pool_recycle=3600)
        self.Session = sessionmaker(bind=self.engine)

    def read(self, ci_name, delisting=0, **kwargs):
        if not delisting:
            result = None
            with session_scope(self.Session) as session:
                result = (
                    session.query(models.CompanyInfoGeneral).filter(
                        and_(
                            models.CompanyInfoGeneral.ci_name == ci_name,
                            models.CompanyInfoGeneral.ci_demand_forecast_date != DELISTING,
                        )
                    )
                ).first()
            return result
            # return result

    def delist(self, ci_name=None):
        with session_scope(self.Session) as session:
            result = (
                session.query(models.CompanyInfoGeneral)
                .filter(
                    and_(
                        models.CompanyInfoGeneral.ci_name == ci_name,
                        models.CompanyInfoGeneral.ci_demand_forecast_date != DELISTING,
                    )
                )
                .update({models.CompanyInfoGeneral.ci_demand_forecast_date: DELISTING})
                .first()
            )
            if result:
                return True
            return False

    def update(self, DELISTING="공모철회", **kwargs):
        general = kwargs["general"]
        shareholders = kwargs["shareholders"]
        predictions = kwargs["predictions"]
        subscribers = kwargs["subscribers"]
        financials = kwargs["financials"]
        # 상장철회가 아니었던 종목이 '상장철회'로 업데이트 하는 경우

        if DELISTING:
            with session_scope(self.Session) as session:
                result = (
                    session.query(models.CompanyInfoGeneral)
                    .filter(
                        and_(
                            models.CompanyInfoGeneral.ci_name == general.ci_name,
                            models.CompanyInfoGeneral.ci_demand_forecast_date != DELISTING,
                        )
                    )
                    .update({models.CompanyInfoGeneral.ci_demand_forecast_date: DELISTING})
                    .first()
                )

                if result:
                    return True
                return False
        # '상장철회 이외 데이터가 업데이트 되는 경우'
        pass

    def create(self, **kwargs):

        general = kwargs["general"]
        shareholders = kwargs["shareholders"]
        predictions = kwargs["predictions"]
        subscribers = kwargs["subscribers"]
        financials = kwargs["financials"]

        with session_scope(self.Session) as session:
            session.begin_nested()
            company = models.CompanyInfoGeneral(**general.dict())
            session.add(company)
            session.flush()
            session.commit()
            session.bulk_insert_mappings(
                models.CompanyInfoShareholder,
                [{**shareholder.dict(), "ci_idx": company.ci_idx} for shareholder in shareholders],
            )
            session.bulk_insert_mappings(
                models.CompanyInfoPrediction,
                [{**prediction.dict(), "ci_idx": company.ci_idx} for prediction in predictions],
            )
            session.bulk_insert_mappings(
                models.CompanyInfoSubscriber,
                [{**subscriber.dict(), "ci_idx": company.ci_idx} for subscriber in subscribers],
            )
            session.bulk_insert_mappings(
                models.CompanyInfoFinancial,
                [{**financial.dict(), "ci_idx": company.ci_idx} for financial in financials],
            )
            session.commit()
            return True


if __name__ == "__main__":

    instance = DbManager()
    instance.read("래몽래인")
