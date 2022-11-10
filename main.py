#Python
from typing import Optional
from enum import Enum #Para poder definir la validaciones

#Pydantic
from pydantic import BaseModel, Field, EmailStr

#FastAPI

from fastapi import FastAPI ,Body, Query, Path, Form, Header, Cookie, UploadFile, File, status
from fastapi import HTTPException

app = FastAPI() #Instancia de FastAPI 

#Models


class HairColor(str,Enum): #Hereda de enum, el str permite que se visualice mejor en swagger
    white = "white"
    brown = "brown"
    black = "black"

class PersonBase(BaseModel):
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
class Person(PersonBase):
    password: str = Field(
        ...,
        min_length=8
    )

class PersonOut(PersonBase):
    pass #keyword de python para indicar que no pasa nada
    
class Location(BaseModel):
    city:str
    state:str
    country:str

class LoginOut(BaseModel):
    username: str = Field(...,max_length=20,example="Alejito1234*")
    message:str = Field(default="Login succesfully")
#Methods
@app.get(
    "/", 
    status_code=status.HTTP_200_OK,
    tags=["home"]
    )
def get():
    """
    Get 
    
    This Path operation gets a person
    
    Returns bb cito
    """
    return {
        "bb":"cito"
    }

#Request and response Body
#@app.post("/person/new", response_model= Person, response_model_exclude={"password"}) #Excluye la contraseña sin necesidad de crear una nueva clase

@app.post(
    "/person/new", 
    response_model= PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
    summary="Create person in the app"
    )

def create_person(person: Person = Body(...)): ## los ... ellipsis indican que el body es obligatorio, en versionas mpás recientes no se necesario ponerlo
    """
    Create Person
    
    This Path operation creates a person in the app and save the information in the database
    
    Parameters:
    - Request body parameter:
        - **person: Person** -> A person model with first names, last name, age....
    
    Returns a person model with first name, last name, age, hair color ....
    """
    return person

@app.get(
    "/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
    )
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
    """
    Get Person
    
    This Path operation gets a person
    
    Parameters:
    - Request body parameter:
        - **No required**
    
    Returns a person age and name
    """
    return {name:age}

#Validaciones path parameters

persons = [1,2,3,4,5,6]

@app.get("/person/detail/{person_id}")
def show_person(
    person_id:int = Path(
        ..., 
        gt=0,
        title="Person ID",
        description="This is the person id. It's greater than 0",
        tags=["Persons"]
        ),
):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This person doesn't exist!"
        )
    
    return {person_id:"Existe"}


#Validaciones path parameters
@app.put("/person/{person_id}",tags=["Persons"])
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

#Forms
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Login","Persons"]
)
def login(username:str = Form(...), password:str = Form(...)):
    return LoginOut(username=username)

#Cookies and headers
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Contacts"]
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email:EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent

#Files

@app.post(
    path="/post-image"
)

def post_image(
    image:UploadFile = File(...)
):
    return{
        "Filename":image.filename,
        "Format":image.content_type,
        "Size(kb)":round(len(image.file.read())/1024,ndigits=2)
    }