from sqlalchemy import create_engine, Engine, URL, String, Integer, Column, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()

class Players(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    host = Column(String)
    port = Column(Integer)

class Database:
    def __init__(self) -> None:
        
        self.db_url: URL = URL.create(
            drivername="postgresql+psycopg2",
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME")
        )

        self.engine: Engine = create_engine(self.db_url, echo=True, pool_pre_ping=True)
        Base.metadata.create_all(self.engine)
     
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autoflush=True,
            expire_on_commit=True
        )

    def addPlayer(self, player_id: int, host: str, port: int) -> int:

        with self.SessionLocal() as session:
            new_player = Players(id=player_id, host=host, port=port)
            session.add(new_player)
            session.commit()

    def delPlayer(self, player_id: int) -> None:

        with self.SessionLocal() as session:
            player = session.query(Players).filter_by(id=player_id).first()

            if player:
                session.delete(player)
                session.commit()
        
    # def addPlayerPos(self, id: int, playerPos: JSON) -> None:

    #     with self.SessionLocal() as session:
    #         player = session.query(Players).filter_by(id=id).first()
    #         if player:
    #             player.playerPos = playerPos
    #             session.commit()