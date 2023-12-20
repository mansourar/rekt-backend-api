from sqlalchemy import Column, String, func, DateTime, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.testing.entities import ComparableEntity

Base = declarative_base()


class Asset(Base, ComparableEntity):
    __tablename__ = "assets"
    asset_id = Column(String(50), primary_key=True)
    asset_name = Column(String(50))
    asset_type = Column(String(50))
    s3_location = Column(String(100))
    changelist = Column(Integer)
    checksum = Column(String(50))
    time_stamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
