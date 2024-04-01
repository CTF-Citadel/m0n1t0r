from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Initiated_Flag(Base):

    __tablename__ = 'initiations'

    id = Column(Integer, primary_key=True)
    team_id = Column(String(length=255))
    flag = Column(String(length=255))
    challenge_id = Column(String(length=255))
    initiation_time = Column(Integer)

    def __repr__(self):
        return f'Initiated_Flag(id={self.id}, team_id={self.team_id}, flag={self.flag}, challenge_id={self.challenge_id}, initiation_time={self.initiation_time})'

class Submission(Base):

    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True)
    flag = Column(String(length=255))
    team_id = Column(String(length=255))
    user_id = Column(String(length=255))
    challenge_id = Column(String(length=255))
    submission_time = Column(Integer)
    static = Column(Boolean)

    def __repr__(self):
        return f'Submission(id={self.id}, flag={self.flag}, team_id={self.team_id}, user_id={self.user_id}, challenge_id={self.challenge_id}, submission_time={self.submission_time}, static={self.static})'

class Poisoned(Base):

    __tablename__ = 'poisoned_flags'

    flag = Column(String(length=255), unique=True, primary_key=True)

    def __repr__(self):
        return f'Poisoned(flag={self.flag})'

class Solved(Base):

    __tablename__ = 'solved'

    id = Column(Integer, primary_key=True)
    team_id = Column(String(length=255))
    challenge_id = Column(String(length=255))
    timestamp = Column(Integer)

    def __repr__(self):
        return f'Solved(id={self.id}, team={self.team}, challenge_id={self.challenge_id}, timestamp={self.timestamp})'

class Flagged(Base):

    __tablename__ = 'flagged'

    id = Column(Integer, primary_key=True)
    team_id = Column(String(length=255))
    user_id = Column(String(length=255))
    flag = Column(String(length=255))
    challenge_id = Column(String(length=255))
    flagging_time = Column(Integer)
    flag_share_team = Column(String(length=255))
    reason = Column(String(length=255))

    def __repr__(self):
        return f'Flagged(id={self.id}, team_id={self.team_id}, user_id={self.user_id}, flag={self.flag}, challenge_id={self.challenge_id}, flagging_time={self.flagging_time}, flag_share_team={self.flag_share_team}, reason={self.reason})'