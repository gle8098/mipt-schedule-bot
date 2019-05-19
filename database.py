from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    group = Column(String)

    def __repr__(self):
        return "<User(id={}, chat_id={}, group={})>".format(self.id, self.chat_id, self.group)


class BotDatabase:
    _engine = None

    def init(self):
        self._engine = create_engine('sqlite:///users.db', echo=True)
        Base.metadata.create_all(self._engine)

    def del_group(self, chat_id):
        Session = sessionmaker(bind=self._engine)
        session = Session()

        query = session.query(User).filter(User.chat_id == chat_id)
        if query.count() > 0:
            query.delete()
            session.commit()

    def set_group(self, chat_id, group):
        self.del_group(chat_id)  # Delete record if it exists

        Session = sessionmaker(bind=self._engine)
        session = Session()

        user = User(chat_id=chat_id, group=group)
        session.add(user)
        session.commit()

    def get_group(self, chat_id):
        Session = sessionmaker(bind=self._engine)
        session = Session()

        query = session.query(User).filter_by(chat_id=chat_id)
        if query.count() == 0:
            return None

        return query.one().group
