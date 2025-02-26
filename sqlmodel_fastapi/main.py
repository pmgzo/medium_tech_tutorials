from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel, Session, create_engine, func, or_, select

from models import Car, User
import datetime

app = FastAPI()

## !!! something to extremely avoid in production, use ENV variables instead
engine = create_engine("postgresql://postgres:mysecretpassword@localhost/postgres")

SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

class UserPublic(SQLModel):
  id: int
  name: str

class UserPost(SQLModel):
  name: str
  password: str

@app.post("/user/")
def create_user(session: SessionDep, user: UserPost) -> UserPublic:
    createdUser = User(name=user.name, password=user.password)
    session.add(createdUser)
    session.commit()
    createdUser = session.exec(select(User).where(User.name == user.name)).one()
    return createdUser

@app.get("/users/", response_model=list[UserPublic])
def read_users(session: SessionDep):
    users = session.exec(select(User)).all()
    return users

class CarPublic(SQLModel):
    id: int
    model: str
    brand: str
    purchased_time: datetime.datetime

@app.get("/users/{id}/cars/")
def read_user_cars(session: SessionDep, id: int) -> list[CarPublic]:
    # Warning: here again always important to check the response
    # before calling "one", Otherwise your application may crash.
    cars = session.exec(select(Car).where(Car.user_id == id)).all()
    json_compatible_data = jsonable_encoder(cars)
    return JSONResponse(content=json_compatible_data)


def create_users():
    session = Session(engine)
    cnt = func.count(User.name).label("cnt")
    result = session.exec(select(cnt).where(or_(User.name == "Jacky", User.name == "Juice"))).one()

    if result == 0:
      # DO NOT Copy paste blindly this code, password should be hashed and stored in DB !!
      user_1 = User(name="Jacky", password="Jack's password")
      user_2 = User(name="Juice", password="Juice's password")
      # Added to DB
      session.add_all([user_1, user_2])

      dbuser = session.exec(select(User).where(or_(User.name == "Jacky"))).one()

      car_1 = Car(user_id=dbuser.id, model="Fiat Panda", brand="Fiat", purchased_time=datetime.datetime.now())

      session.add(car_1)
      session.commit()

    session.close()

def main():
    create_users()

if __name__ == "__main__":
    main()