import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, Diet, UserBMI, User, Training
from app.main import app
from app.db.session import get_db
from app.api.auth import get_current_user, hash_password
from datetime import datetime
from app.services.endpoint_limit_service import post_rate_limiter, get_rate_limiter, auth_rate_limiter

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class DummyTexts:
    test_diet = "Segunda: Café da Manhã: Prato: Pão com ovo; Ingredientes: Pão, ovo, manteiga Almoço: Prato: Arroz e feijão; Ingredientes: Arroz, feijão, carne Café da Tarde: Prato: Bolo; Ingredientes: Farinha, açúcar, ovo Jantar: Prato: Sopa; Ingredientes: Legumes, sal Terça: Café da Manhã: Prato: Tapioca; Ingredientes: Goma, queijo Almoço: Prato: Macarrão; Ingredientes: Massa, molho, carne Café da Tarde: Prato: Iogurte; Ingredientes: Iogurte natural Jantar: Prato: Omelete; Ingredientes: Ovo, tomate, cebola"
    test_training = "Segunda: Exercicio 1: 4x10; Exercicio 2: 3x12; Terça: Exercicio 3: 3x10; Exercicio 4: 3x10; Quarta: Exercicio 5: 4x10; Exercicio 6: 3x10; Quinta: Exercicio 7: 3x12; Exercicio 8: 4x10; Sexta: Exercicio 9: 4x15; Exercicio 10: 3x10;"

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def populate_test_database(db_session):
    password = hash_password("123")
    user = User(
        id=1,
        full_name="Test User",
        email="test@email.com",
        password_hash=password,
        role=3
    )
    db_session.add(user)

    user_bmi = UserBMI(
        bmi_status_id=2,
        user_id=1,
        bmi_value=22.5,
        height=1.75,
        weight=69.0,
        created_at=datetime.utcnow(),
    )
    db_session.add(user_bmi)

    diet = Diet(
        description=DummyTexts.test_diet,
        bmi_status_id=2,
        user_id=1,
        created_at=datetime.utcnow(),
    )
    db_session.add(diet)

    training = Training(
        description=DummyTexts.test_training,
        bmi_status_id=2,
        user_id=1,
        created_at=datetime.utcnow(),
    )
    db_session.add(training)
    db_session.commit()

@pytest.fixture
def client(db_session, populate_test_database):
    def override_get_db():
        yield db_session

    def override_get_current_user():
        return db_session.query(User).filter(User.id == 1).first()

    def override_rate_limiter():
        pass

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[post_rate_limiter] = override_rate_limiter
    app.dependency_overrides[get_rate_limiter] = override_rate_limiter
    app.dependency_overrides[auth_rate_limiter] = override_rate_limiter

    yield TestClient(app)
    app.dependency_overrides.clear()
