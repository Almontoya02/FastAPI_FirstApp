#Python
from typing import Optional


#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI ,Body, Query

app = FastAPI() #Instancia de FastAPI 

#Models
class Person(BaseModel):
    first_name:str
    last_name:str
    age:int
    hair_color:Optional[str] = None
    is_married:Optional[bool] = None

@app.get("/")
def get():
    return {
        "bb":"cito"
    }

#Request and response Body
@app.post("/person/new")
def create_person(person: Person = Body(...)): ## los ... ellipsis indican que el body es obligatorio, en versionas mpás recientes no se necesario ponerlo

    return person

@app.get("/person/detail")
def show_person(
    name:Optional[str] = Query(None, min_length=1, max_length=50),
    age: int = Query(...) #Lo hacemos obligatorio, sin embargo con query no es lo ideal manejarlo así
):
    return {name:age}