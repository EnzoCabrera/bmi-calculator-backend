from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP, func, Text, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Integer, default=1) # 1 = common, 2 = plus, 3 = admin
    created_at = Column(TIMESTAMP, server_default=func.now())

    user_bmi = relationship("UserBMI", back_populates="user")
    trainings = relationship("Training", back_populates="user")
    diets = relationship("Diet", back_populates="user")

class BMIStatus(Base):
    __tablename__ = "bmi_status"

    id = Column(Integer, primary_key=True)

    user_bmi = relationship("UserBMI", back_populates="bmi_status")
    trainings = relationship("Training", back_populates="bmi_status")
    diets = relationship("Diet", back_populates="bmi_status")

class UserBMI(Base):
    __tablename__ = "user_bmi"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bmi_status_id = Column(Integer, ForeignKey("bmi_status.id"), nullable=False)
    bmi_value = Column(Float, nullable=False)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="user_bmi")
    bmi_status = relationship("BMIStatus", back_populates="user_bmi")

class Training(Base):
    __tablename__ = "trainings"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    bmi_status_id = Column(Integer, ForeignKey("bmi_status.id"), nullable=False)
    image_path = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="trainings")
    bmi_status = relationship("BMIStatus", back_populates="trainings")

class Diet(Base):
    __tablename__ = "diets"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    bmi_status_id = Column(Integer, ForeignKey("bmi_status.id"), nullable=False)
    image_path = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    intolerances = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="diets")
    bmi_status = relationship("BMIStatus", back_populates="diets")


