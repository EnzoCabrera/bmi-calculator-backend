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

    user_bmi = relationship("UserBMI", back_populates="user")

class BMIStatus(Base):
    __tablename__ = "bmi_status"

    id = Column(Integer, primary_key=True)

    user_bmi = relationship("UserBMI", back_populates="bmi_status")
    exercises = relationship("Exercise", back_populates="bmi_status")
    diets = relationship("Diet", back_populates="bmi_status")

class UserBMI(Base):
    __tablename__ = "user_bmi"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bmi_status_id = Column(Integer, ForeignKey("bmi_status.id"), nullable=False)
    bmi_value = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User")
    bmi_status = relationship("BMIStatus", back_populates="user_bmi")

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    bmi_status_id = Column(Integer, ForeignKey("bmi_status.id"), nullable=False)
    image_path = Column(String, nullable=False)

    bmi_status = relationship("BMIStatus", back_populates="exercises")

class Diet(Base):
    __tablename__ = "diets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    bmi_status_id = Column(Integer, ForeignKey("bmi_status.id"), nullable=False)
    image_path = Column(String, nullable=False)

    bmi_status = relationship("BMIStatus", back_populates="diets")
