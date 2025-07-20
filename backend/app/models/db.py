from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content = Column(Text, nullable=False)  # full raw text of resume
    parsed_data = Column(Text, nullable=True)  # JSON string of parsed analysis
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    file_url = Column(String, nullable=True)


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)  # job title if extracted
    content = Column(Text, nullable=False)  # full raw text of job description
    parsed_data = Column(Text, nullable=True)  # JSON string of parsed analysis
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
