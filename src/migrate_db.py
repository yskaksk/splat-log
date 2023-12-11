from sqlalchemy import create_engine


from src.models.battlelog import Base


DB_URL = "mysql+pymysql://root@db:3306/splat?charset=utf8"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    reset_database()
