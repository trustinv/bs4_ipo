import asyncio
from typing import List, Optional
from sqlalchemy import select
from config.settings import settings

from utilities.time_measure import timeit
from sqlalchemy.orm import Session
from db.models import (
    CompanyInfoShareholder as Shareholder,
    CompanyInfoFinancial as Financial,
    CompanyInfoSubscriber as Subscriber,
    CompanyInfoPrediction as Prediction,
    CompanyInfoGeneral as General,
    AppCalendar as Calendar,
)
from schemas.calendar import CalendarCreateSchema
from schemas.general import GeneralCreateSchema
from schemas.financial import FinancialCreateSchema
from schemas.prediction import PredictionCreateSchema
from schemas.shareholder import ShareholderCreateSchema
from schemas.subscriber import SubscriberCreateSchema

from db.config import async_session, engine
from config.config_log import logging

logger = logging.getLogger("info-logger")

DELISTING = settings.DELISTING


class Company:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    async def create(
        self,
        general: General,
        shareholders: List[Shareholder],
        financials: List[Financial],
        subscribers: List[Subscriber],
        predictions: List[Prediction],
        calendars: List[Calendar],
    ) -> bool:

        new_company = general
        new_company.shareholders = shareholders
        new_company.financials = financials
        new_company.subscribers = subscribers
        new_company.predictions = predictions
        new_company.app_calendars = calendars

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

    async def read(self, ci_code: str) -> Optional[General]:
        q = await self._db_session.execute(select(General).where(General.ci_code == ci_code))
        result = q.scalars().first()
        if result:
            return result.ci_code
        return

    async def update(
        self,
        general: General,
        shareholders: List[Shareholder],
        financials: List[Financial],
        subscribers: List[Subscriber],
        predictions: List[Prediction],
        calendars: List[Calendar],
    ) -> int:

        general.shareholders = []
        general.shareholders = shareholders
        general.financials = []
        general.financials = financials
        general.subscribers = []
        general.subscribers = subscribers
        general.predictions = []
        general.predictions = predictions
        general.app_calendars = []
        general.app_calendars = calendars

        # query = (
        #     update(General)
        #     .where(General.ci_code == ci_code)
        #     .values(
        #         **new_company.__dict__,
        #         shareholders=shareholders,
        #         financials=financials,
        #         subscribers=subscribers,
        #         predictions=predictions,
        #         app_calendars=calendars,
        #     )
        # )
        # result = await self._db_session.execute(query)
        # affected_rows = result.rowcount
        await self._db_session.commit()
        return True

    async def upsert(
        self,
        general: GeneralCreateSchema,
        shareholders: List[ShareholderCreateSchema],
        financials: List[FinancialCreateSchema],
        subscribers: List[SubscriberCreateSchema],
        predictions: List[PredictionCreateSchema],
        calendars: List[CalendarCreateSchema],
    ):

        ci_code = general.ci_code
        general = General(**general.dict())
        shareholders = [Shareholder(**shareholder) for shareholder in shareholders]
        financials = [Financial(**financial) for financial in financials]
        subscribers = [Subscriber(**subscriber) for subscriber in subscribers]
        predictions = [Prediction(**prediction) for prediction in predictions]
        calendars = [Calendar(**calendar.dict()) for calendar in calendars]

        existed_ci_code = await self.read(ci_code)
        logger.info(f"existed_ci_code: {existed_ci_code}")
        if existed_ci_code is not None:
            result = await self.update(
                general,
                shareholders,
                financials,
                subscribers,
                predictions,
                calendars,
            )
            if result:
                logger.info("기업 데이터를 수정하였습니다")
                return True
            logger.info("기업 데이터에 실패하였습니다.")
            return False

        else:
            result = await self.create(
                general=general,
                shareholders=shareholders,
                financials=financials,
                subscribers=subscribers,
                predictions=predictions,
                calendars=calendars,
            )
            if result:
                logger.info("기업 데이터를 등록 하였습니다")
                return True
            logger.info("기업 데이터 수정에 실패하였습니다.")
            return False


if __name__ == "__main__":
    from temp import raw_data

    @timeit
    async def main():
        async with async_session() as session:
            # async with session.begin():
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
            async with session.begin():
                r: General = await company_dal.read("1919800")
                print(
                    r,
                )
            # r = await company_dal.get_all_delisted_companies_name()
            # print(r, len(r))
        await engine.dispose()

    asyncio.run(main(), debug=True)
