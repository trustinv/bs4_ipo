import asyncio
from typing import List, Optional
from sqlalchemy import and_, func, select, update, insert

from config.settings import settings

from utilities.time_measure import timeit
from sqlalchemy.orm import Session

from db import models
from db.models import CompanyInfoGeneral as General
from db.models import CompanyInfoShareholder as Shareholder
from db.models import CompanyInfoFinancial as Financial
from db.models import CompanyInfoSubscriber as Subscriber
from db.models import CompanyInfoPrediction as Prediction
from db.config import async_session, engine

DELISTING = settings.DELISTING


class Company:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    async def create(self, *args, **kwargs):
        general = kwargs["general"]
        shareholders = kwargs["shareholders"]
        financials = kwargs["financials"]
        subscribers = kwargs["subscribers"]
        predictions = kwargs["predictions"]

        new_company = models.CompanyInfoGeneral(**general)
        new_company.shareholders = [Shareholder(**shareholder) for shareholder in shareholders]
        new_company.financials = [Financial(**financial) for financial in financials]
        new_company.subscribers = [Subscriber(**subscriber) for subscriber in subscribers]
        new_company.predictions = [Prediction(**prediction) for prediction in predictions]

        self._db_session.add(new_company)
        await self._db_session.flush()
        return True

    async def get_all_companies(self) -> List[General]:
        q = await self.db_session.execute(select(General).order_by(General.id))
        return q.scalars().all()

    async def read(self, ci_name: str):
        q = await self._db_session.execute(select(General).where(General.ci_name == ci_name))
        return q.scalars().first()

    # async def delist(self, ci_name: str):
    #     async with self._db_session() as session:
    #         query = (
    #             update(cig)
    #             .where(cig.ci_name == ci_name, cig.ci_demand_forecast_date != DELISTING)
    #             .values({cig.ci_demand_forecast_date: DELISTING})
    #         )
    #         result = await session.execute(query)
    #         affected_rows = result.rowcount
    #         await session.commit()
    #         return affected_rows


if __name__ == "__main__":
    from temp import raw_data

    @timeit
    async def main():
        async with async_session() as session:
            async with session.begin():
                company_dal = Company(session)
                await company_dal.create(
                    raw_data.general_dict,
                    raw_data.shareholders_dict,
                    raw_data.financials_dict,
                    raw_data.subscribers_dict,
                    raw_data.predictions_dict,
                )
        await engine.dispose()

    asyncio.run(main(), debug=True)
