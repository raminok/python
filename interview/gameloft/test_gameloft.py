import pytest
from fastapi.testclient import TestClient
from gameloft import app, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from gameloft import Base, Player
import json

#  Create Database for Test in memory
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#  Test Database Initialize
@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

#  Create Test Client
@pytest.fixture(scope="module")
def client():
    return TestClient(app)

#  Test Data
@pytest.fixture(scope="function")
def sample_player(db):
    player_data = {
        "player_id": "97983be2-98b7-11e7-90cf-082e5f28d836",
        "profile": json.dumps({
            "player_id": "97983be2-98b7-11e7-90cf-082e5f28d836",
            "credential": "apple_credential",
            "level": 3,
            "country": "CA",
            "inventory": {"cash": 123, "coins": 123, "item_1": 1, "item_34": 3, "item_55": 2},
            "active_campaigns": []
        })
    }
    player = Player(**player_data)
    db.add(player)
    db.commit()

#  API Test
def test_get_client_config(client, db, sample_player):
    response = client.get("/get_client_config/97983be2-98b7-11e7-90cf-082e5f28d836")
    print("Response JSON:", response.json())

    assert response.status_code == 200
    data = response.json()
    
    assert "active_campaigns" in data
    assert isinstance(data["active_campaigns"], list)
    
    assert "mycampaign" in data["active_campaigns"]

#  Test for Invalid Data
def test_invalid_player(client):
    response = client.get("/get_client_config/invalid-player-id")
    assert response.status_code == 400

#  For Player is not in Database
def test_player_not_found(client):
    response = client.get("/get_client_config/97983be2-98b7-11e7-90cf-000000000000")
    assert response.status_code == 404


#  use pytest test_gameloft.py in terminal for testing API
