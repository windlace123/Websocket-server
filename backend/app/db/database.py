from sqlalchemy import Engine, URL, create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.core.config import settings
from backend.app.db.models import Base, Player


class Database:
    def __init__(self) -> None:
        self.db_url: URL = URL.create(
            drivername="postgresql+psycopg2",
            username=settings.postgres_user,
            password=settings.postgres_password,
            host=settings.postgres_host,
            port=settings.postgres_port,
            database=settings.postgres_database,
        )

        self.engine: Engine = create_engine(self.db_url, echo=True, pool_pre_ping=True)
        Base.metadata.create_all(self.engine)

        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autoflush=True,
            expire_on_commit=True,
        )

    def add_player(self, player_id: int, host: str, port: int) -> None:
        with self.SessionLocal() as session:
            new_player = Player(id=player_id, host=host, port=port)
            session.add(new_player)
            session.commit()

    def delete_player(self, player_id: int) -> None:
        with self.SessionLocal() as session:
            player = session.query(Player).filter_by(id=player_id).first()

            if player:
                session.delete(player)
                session.commit()
