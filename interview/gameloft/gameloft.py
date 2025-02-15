from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, String, JSON
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from typing import List, Dict
import requests
import logging
import uvicorn
import json


DATABASE_URL = "sqlite:///players.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#  Define Database Models
class Player(Base):
    __tablename__ = "players"

    player_id = Column(String, primary_key=True, index=True)
    profile = Column(JSON)

class Inventory(BaseModel):
    cash: int
    coins: int
    items: Dict[str, int]

class PlayerProfile(BaseModel):
    player_id: str
    credential: str
    level: int
    country: str
    inventory: Inventory
    active_campaigns: List[str] = []
    
#  Create Tables and Mock database connection
Base.metadata.create_all(bind=engine)

#  Create Session and preventing Connection Leak
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#  Mock database for player profiles
mock_player_profile ={
        "player_id": "97983be2-98b7-11e7-90cf-082e5f28d836",
        "credential": "apple_credential",
        "created": "2021-01-10 13:37:17Z",
        "modified": "2021-01-23 13:37:17Z",
        "last_session": "2021-01-23 13:37:17Z",
        "total_spent": 400,
        "total_refund": 0,
        "total_transactions": 5,
        "last_purchase": "2021-01-22 13:37:17Z",
        "active_campaigns": [],
        "devices": [{
                      "id": 1,
                      "model": "apple iphone 11",
                      "carrier": "vodafone",
                      "firmware": "123"
                    }],
        "level": 3,
        "xp": 1000,
        "total_playtime": 144,
        "country": "CA",
        "language": "fr",
        "birthdate": "2000-01-10 13:37:17Z",
        "gender": "male",
        "inventory": 
        {
          "cash": 123,
          "coins": 123,
          "item_1": 1,
          "item_34": 3,
          "item_55": 2
        },
        "clan": 
        {
          "id": "123456",
          "name": "Hello world clan"
        },
        "_customfield": "mycustom"
    }

def seed_database():
    db = SessionLocal()
    player_count = db.query(Player).count()
    if player_count == 0:
        sample_player = Player(
            player_id=mock_player_profile["player_id"],
            profile=mock_player_profile
        )
        
        db.add(sample_player)
        db.commit()

    db.close()

app = FastAPI()


#  sqllit does't support UTC time 
def parse_datetime(date_str):
    formats = ["%Y-%m-%d %H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]
    for fmt in formats:
        try:
            #  offset aware - it always send zone time
            dt = datetime.strptime(date_str, fmt)
            return dt.replace(tzinfo=timezone.utc)  
        except ValueError:
            continue
    return None
        
#  Fetch player profile from database
def get_player_profile(db: Session, player_id: str):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    
    if not player:
        return None

    return player.profile

#  Update player profile in database
def update_player_profile(db: Session, player_id: str, profile: Dict):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found in database")
    
    player.profile = profile
    db.commit()
    
#  Mock API for fetching Active campaigns
def get_active_campaigns():
    return [
        {
          "game": "mygame",
          "name": "mycampaign",
          "priority": 10.5,
          "matchers": {
              "level": {"min": 1, "max": 3},
              "has": {"country": ["US", "RO", "CA"], "items": ["item_1"]},
              "does_not_have": {"items": ["item_4"]}
          },
          "start_date": "2022-01-25 00:00:00Z",
          "end_date": "2022-02-25 00:00:00Z",
          "enabled": True,
          "last_updated": "2021-07-13 11:46:58Z"
        }
    ]

#  Function to check if player profile matches a campaign
def matches_campaign(player, campaign):
    matchers = campaign["matchers"]
    
    if not campaign["enabled"]:
        return False

    #  Check for the validity and expire date of the Campaign 
    end_date = parse_datetime(campaign["end_date"])

    if end_date and end_date < datetime.now(timezone.utc):
        return False
    
    #  Check level
    player_level = player.get("level")
    
    if player_level is None:
        return False
    
    if not (matchers["level"]["min"] <= player_level <= matchers["level"]["max"]):
        return False
    
    #  Check country
    if player["country"] not in matchers["has"]["country"]:
        return False
    
    #  Check required items
    for item in matchers["has"].get("items", []):
        if item not in player["inventory"]:
            return False
        
    inventory = player.get("inventory", {})
    for item in campaign["matchers"]["has"].get("items", []):
        #  Ensure the item exists AND has a positive count
        if inventory.get(item, 0) <= 0:  
            return False

    #  Check forbidden items
    for item in matchers.get("does_not_have", {}).get("items", []):
        if item in inventory:
            return False
    
    return True

@app.get("/get_client_config/{player_id}")
def get_client_config(player_id: str, db: Session = Depends(get_db)):

    #  for preventing SQL injection
    if not player_id or not isinstance(player_id, str) or len(player_id) != 36:
        raise HTTPException(status_code=400, detail="Invalid player ID")

    player_profile = get_player_profile(db, player_id)

    if not player_profile:
        raise HTTPException(status_code=404, detail="Player not found")

    campaigns = get_active_campaigns()
    
    for campaign in campaigns:
        if campaign["enabled"] and matches_campaign(player_profile, campaign):
            if campaign["name"] not in player_profile["active_campaigns"]:
                player_profile["active_campaigns"].append(campaign["name"])
    
    update_player_profile(db, player_id, player_profile)
    return player_profile

if __name__ == "__main__":
    #  Create Database and Tables
    Base.metadata.create_all(bind=engine)
    
    #  Input Sample Data into Table if table is empty
    seed_database()

    #  Run APP and Listen for API
    uvicorn.run(app, host="127.0.0.1", port=8000)
