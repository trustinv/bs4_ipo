from contextlib import contextmanager


@contextmanager
def session_scope(Session):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from db import models
    from utilities.session import session_scope
    from settings import DB_URL

    ci_name = "래몽래인"
    DELISTING = "공모철회"

    engine = create_engine(DB_URL, pool_recycle=3600)
    Session = sessionmaker(bind=engine)
    result = None
    with session_scope(Session) as session:
        result = session.query(models.CompanyInfoGeneral).all()
        # for row in result:
        #     print(row)
        result = result
    print(result)
