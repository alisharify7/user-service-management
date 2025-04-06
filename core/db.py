from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from core.config import get_config

Setting = get_config()


engine = create_engine(
    url=Setting.SQLALCHEMY_DATABASE_URI,
    pool_size=30,
    max_overflow=10,
    echo=Setting.DEBUG_QUERY,
)


Session = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

BaseModelClass = declarative_base()

def get_session() -> sessionmaker:
    """get a fresh session for connection to database
    """
    session = Session()
    try:
        yield session
    finally:
        session.close()


