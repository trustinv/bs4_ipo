import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import DB_URL
from utilities.session import session_scope
from db import models


class DbManager:
    def __init__(self, *args, **kwargs):
        self.engine = create_engine(DB_URL)
        self.Session = sessionmaker(bind=self.engine)

    def delete(self):
        # "상장철회"일 경우 컬럼 필드 값을 변경함.
        pass

    def create(self):
        pass

    def create_n_update(self):
        """
        1) 데이터 존재여부를 확인.
            - 상장철회 된 데이터는 가져 올 필요가 없음.
        """
        with session_scope(self.Session) as session:
            general_instance = CompanyInfoGeneralSchema(**item)
            # Check if a company with the same name already exists in the database
            existing_company = (
                session.query(models.CompanyInfoGeneral)
                .filter_by(ci_name=general_instance.ci_name)
                .first()
            )
            if existing_company is None:
                # Add the new company to the database
                cig = models.CompanyInfoGeneral(**pydantic_instance.dict())
                session.add(cig)
            else:
                # Check if any of the values have changed
                update_required = False
                for key, value in pydantic_instance.dict().items():
                    if key in ["_sa_instance_state", "id"] or value == getattr(
                        existing_company, key
                    ):
                        continue
                    setattr(existing_company, key, value)
                    update_required = True
                if update_required:
                    session.commit()

    def read(self):
        pass
