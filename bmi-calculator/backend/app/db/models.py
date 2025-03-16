from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

class BMIStatus(Base):
    __tablename__ = "bmi_status"

    id = Column(Integer, primary_key=True)

class UserBMI(Base):
    __tablename__ = "user_bmi"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    bmi_status_id = Column(Integer, ForeignKey("bmi_status.id"))
    bmi_value = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User")
    bmi_status = relationship("BMIStatus")

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    bmi_status_id = Column(Integer, ForeignKey("bmi_status.id"))
    image_path = Column(String, nullable=False)

    bmi_status = relationship("BMIStatus")

class Diet(Base):
    __tablename__ = "diets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    bmi_status_id = Column(Integer, ForeignKey("bmi_status.id"))
    image_path = Column(String, nullable=False)

    bmi_status = relationship("BMIStatus")
