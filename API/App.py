from fastapi import FastAPI
App = FastAPI()

'''Zugreifen über http://127.0.0.1:8000/docs#/'''
@App.get("/get-twin-names-api/")
async def Anzahl_Twins():
   return (Anzahl_Twins)

