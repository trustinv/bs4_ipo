import asyncio
from typing import List, Optional
from sqlalchemy import and_, func, select, update, insert
from config.settings import settings

from utilities.time_measure import timeit
from sqlalchemy.orm import Session
from db.models import (
    CompanyInfoShareholder as Shareholder,
    CompanyInfoFinancial as Financial,
    CompanyInfoSubscriber as Subscriber,
    CompanyInfoPrediction as Prediction,
    CompanyInfoGeneral as General,
    AppCalendar as Calendar
)

from db.config import async_session, engine

DELISTING = settings.DELISTING


class Company:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    async def create(self, general: dict,
    shareholders: List[dict],
    financials: List[dict],
    subscribers: List[dict],
    predictions: List[dict],
    calendars: List[dict],
    ) -> bool:

        new_company =General(**general)
        new_company.shareholders = [Shareholder(**shareholder) for shareholder in shareholders]
        new_company.financials = [Financial(**financial) for financial in financials]
        new_company.subscribers = [Subscriber(**subscriber) for subscriber in subscribers]
        new_company.predictions = [Prediction(**prediction) for prediction in predictions]
        new_company.app_calendars = [Calendar(**calendar) for calendar in calendars]

        self._db_session.add(new_company)
        await self._db_session.flush()
        return True

    async def get_all_companies(self) -> List[General]:
        q = await self._db_session.execute(select(General).order_by(General.id))
        return q.scalars().all()

    async def get_all_delisted_companies_name(self) -> List[str]:
        q = await self._db_session.execute(
            select([General.ci_name])
            .where(General.ci_demand_forecast_date != DELISTING)
            .order_by(General.ci_datetime)
        )
        return [row[0][:10] for row in q]

    async def read(self, ci_name: str) -> Optional[General]:
        q = await self._db_session.execute(select(General).where(General.ci_name == ci_name))
        return q.scalars().first()

    async def delist(self, ci_name: str) -> int:
        query = (
            update(General)
            .where(General.ci_name == ci_name, General.ci_demand_forecast_date != DELISTING)
            .values({General.ci_demand_forecast_date: DELISTING})
        )
        result = await self._db_session.execute(query)
        affected_rows = result.rowcount
        await self._db_session.commit()
        return affected_rows


if __name__ == "__main__":
    from temp import raw_data

    @timeit
    async def main():
        async with async_session() as session:
            async with session.begin():
                company_dal: General = Company(session)
                # await company_dal.create(
                #     raw_data.general_dict,
                #     raw_data.shareholders_dict,
                #     raw_data.financials_dict,
                #     raw_data.subscribers_dict,
                #     raw_data.predictions_dict,
                # )
                #     r: General = await company_dal.read("툴젠")
                #     print(r.ci_name, r.ci_demand_forecast_date)
                # async with session.begin():
                #     r = await company_dal.delist(r.ci_name)
                #     print(r)
                # async with session.begin():
                #     r: General = await company_dal.read("툴젠")
                #     print(r.ci_name, r.ci_demand_forecast_date)
                r = await company_dal.get_all_delisted_companies_name()
                print(r, len(r))
        await engine.dispose()

    asyncio.run(main(), debug=True)
