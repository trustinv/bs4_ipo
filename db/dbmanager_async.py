import asyncio
from sqlalchemy import and_, func, select, update, insert
from sqlalchemy.orm import selectinload, sessionmaker


from config.settings import DELISTING
from config.settings import settings

from utilities.time_measure import timeit
from sqlalchemy.orm import Session

from db import models
from db.models import CompanyInfoGeneral as cig
from db.config import async_session

ASYNC_DB_URL = settings.ASYNC_DB_URL
DELISTING = settings.DELISTING


class DBManager:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    async def read(self, ci_name: str):
        q = await self._db_session.execute(select(cig).where(cig.ci_name == ci_name))
        return q.scalars().first()

    async def delist(self, ci_name: str):
        async with self._db_session() as session:
            query = (
                update(cig)
                .where(cig.ci_name == ci_name, cig.ci_demand_forecast_date != DELISTING)
                .values({cig.ci_demand_forecast_date: DELISTING})
            )
            result = await session.execute(query)
            affected_rows = result.rowcount
            await session.commit()
            return affected_rows

    async def create(self, *args, **kwargs):
        general = kwargs["general"]
        shareholders = kwargs["shareholders"]
        predictions = kwargs["predictions"]
        subscribers = kwargs["subscribers"]
        financials = kwargs["financials"]

        async with self._session_maker() as session:
            async with session.begin():
                go = models.CompanyInfoGeneral(
                    **general,
                    predictions=[
                        models.CompanyInfoPrediction(**prediction) for prediction in predictions
                    ],
                    financials=[
                        models.CompanyInfoFinancial(**financial) for financial in financials
                    ],
                    shareholders=[
                        models.CompanyInfoShareholder(**shareholder) for shareholder in shareholders
                    ],
                    subscribers=[
                        models.CompanyInfoSubscriber(**subscriber) for subscriber in subscribers
                    ],
                )
                await session.in_transaction.add(go)
                await session.commit()
                return True


if __name__ == "__main__":
    from temp import raw_data

    @timeit
    async def main():
        instance = DBManager()
        async with async_session() as session:
            async with session.begin():
                book_dal = BookDAL(session)
                return await book_dal.create_book(name, author, release_year)
        # data = await instance.read("래몽래인")
        # await engine.dispose()
        # await instance.create(
        #     general=raw_data.general_dict,
        #     shareholders=raw_data.shareholders_dict,
        #     financials=raw_data.financials_dict,
        #     subscribers=raw_data.subscribers_dict,
        #     predictions=raw_data.predictions_dict,
        # )
        # await engine.dispose()

    asyncio.run(main(), debug=True)
