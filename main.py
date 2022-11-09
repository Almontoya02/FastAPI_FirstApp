#Python
from typing import Optional
from enum import Enum #Para poder definir la validaciones

#Pydantic
from pydantic import BaseModel, Field

#FastAPI
from fastapi import FastAPI ,Body, Query, Path

app = FastAPI() #Instancia de FastAPI 

#Models


class HairColor(str,Enum): #Hereda de enum, el str permite que se visualice mejor en swagger
    white = "white"
    brown = "brown"
    black = "black"

class Person(BaseModel):
    first_name:str = Field(
        ...,
        min_length=1,
        max_length=100,
        example="Alejo"
        ) #Para validar el parametro del modelo
    last_name:str = Field(
        ...,
        min_length=1,
        max_length=100,
        example="Montoya"
        ) 
    age:int = Field(
        ...,
        gt=0,
        le=80,
        example=23
        ) 
    hair_color:Optional[HairColor] = Field(default=None)
    is_married:Optional[bool] = Field(default=None)
    

    # class Config:
    #     schema_extra={ #Para enviar una repsuesta por defecto
    #         "example": {
    #             "first_name": "Rodrigo",
    #             "last_name": "Lopez",
    #             "age": 30,
    #             "hair_color": "black",
    #             "is_married": False
    #         }
    #     }

class Location(BaseModel):
    city:str
    state:str
    country:str

#Methods
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
    name:Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Alejito"
        ),
    age: int = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example=23
        ) #Lo hacemos obligatorio, sin embargo con query no es lo ideal manejarlo así
):
    return {name:age}

#Validaciones path parameters
@app.get("/person/detail/{person_id}")
def show_person(
    person_id:int = Path(
        ..., 
        gt=0,
        title="Person ID",
        description="This is the person id. It's greater than 0"
        ),
):
    return {person_id:"Existe"}

#Validaciones path parameters
@app.put("/person/{person_id}")
def update_person(
    person_id:int = Path(
        ..., 
        gt=0,
        title="Person ID",
        description="This is the person id. It's greater than 0",
        example=70
    ),
    person:Person = Body(...),
    location:Location = Body(...)
):
    return {
        "person":person.dict(),
        "location":location.dict()
    }


