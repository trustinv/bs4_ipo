import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import func
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

# from sqlalchemy.ext.asyncio import async_sessionmaker

from sqlalchemy.orm import selectinload

from db import models
from sqlalchemy import and_
from config.settings import ASYNC_DB_URL, DELISTING
from utilities.session import session_scope

from utilities.time_measure import timeit
from db.models import (
    CompanyInfoGeneral as cig,
    CompanyInfoFinancial as cif,
    CompanyInfoPrediction as cip,
    CompanyInfoSubscriber as cisub,
    CompanyInfoShareholder as cish,
)


class DBManager:
    def __init__(self, *args, **kwargs):
        self.engine = create_async_engine(ASYNC_DB_URL, pool_recycle=3600, pool_timeout=1000)
        self.async_session = sessionmaker(self.engine, expire_on_commit=True, class_=AsyncSession)

    async def read(self, ci_name, async_session=None):
        # try:
        async with self.async_session() as session:
            query = select(cig).where(cig.ci_name == ci_name)
            instance = await session.execute(query)
            data = instance.scalars().first()

            if data is None:
                return None
            return data

    async def delist(self, ci_name=None, async_session=None):
        try:
            async with self.async_session() as session:
                # async with async_session() as session:
                query = (
                    update(cig)
                    .where(cig.ci_name == ci_name, cig.ci_demand_forecast_date != DELISTING)
                    .values({cig.ci_demand_forecast_date: DELISTING})
                )
                result = await session.execute(query)
                affected_rows = result.rowcount
                await session.commit()
                return affected_rows
        finally:
            await self.engine.dispose()


if __name__ == "__main__":

    # @timeit
    async def main():

        # engine = create_async_engine(ASYNC_DB_URL, pool_recycle=3600, pool_timeout=1000)
        # async_session = sessionmaker(engine, expire_on_commit=True, class_=AsyncSession)
        instance = DBManager()

        data = await instance.read("래몽래인")
        # data = await instance.delist("래몽래인")
        print(data)
        # await engine.dispose()

    asyncio.run(main(), debug=True)
