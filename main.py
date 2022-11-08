from fastapi import FastAPI

app = FastAPI() #Instancia de FastAPI 

@app.get("/")
def get():
    return {
        "bb":"cito"
    }
