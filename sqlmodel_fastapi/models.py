import datetime
from sqlmodel import Field, SQLModel


class Car(SQLModel, table=True): # only informative 
  id: int = Field(primary_key=True)
  user_id: int = Field(index=True, foreign_key="user.id")
  model: str
  brand: str
  purchased_time: datetime.datetime

class User(SQLModel, table=True): # interpreted as SQL table
    __tablename__ = "user"

    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    password: str



