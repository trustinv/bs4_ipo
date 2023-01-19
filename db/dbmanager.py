import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import DB_URL
from utilities.session import session_scope
from db import models
from sqlalchemy import and_
from settings import DB_URL, DELISTING
from utilities.session import session_scope


class DBManager:
    def __init__(self, *args, **kwargs):
        self.engine = create_engine(DB_URL, pool_recycle=3600)
        self.Session = sessionmaker(bind=self.engine)

    def read(self, ci_name, **kwargs):
        with session_scope(self.Session) as session:
            result = (
                session.query(models.CompanyInfoGeneral).filter(
                    and_(
                        models.CompanyInfoGeneral.ci_name == ci_name,
                    )
                )
            ).first()
            if result is None:
                return False, None
            return True, result.ci_demand_forecast_date

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

    def upsert(self, DELISTING=0, **kwargs):
        general = kwargs["general"]
        shareholders = kwargs["shareholders"]
        predictions = kwargs["predictions"]
        subscribers = kwargs["subscribers"]
        financials = kwargs["financials"]
        # 상장철회가 아니었던 종목이 '상장철회'로 업데이트 하는 경우

        DELISTING = '공모철회' if DELISTING else ''
        with session_scope(self.Session) as session:
            if DELISTING:
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
            else:
                session.begin_nested()
                company = models.CompanyInfoGeneral(**general.dict())
                session.merge(company)
                session.commit()

                for shareholder in shareholders:
                    session.merge(models.CompanyInfoShareholder(**{**shareholder.dict(), "ci_idx": company.ci_idx}))
                    session.commit()

                for prediction in predictions:
                    session.merge(models.CompanyInfoPrediction(**{**prediction.dict(), "ci_idx": company.ci_idx}))
                    session.commit()

                for subscriber in subscribers:
                    session.merge(models.CompanyInfoSubscriber(**{**subscriber.dict(), "ci_idx": company.ci_idx}))
                    session.commit()

                for financial in financials:
                    session.merge(models.CompanyInfoFinancial(**{**financial.dict(), "ci_idx": company.ci_idx}))
                    session.commit()
                return True

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

    instance = DBManager()
    instance.read("래몽래인")
