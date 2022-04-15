'''Speziell für Rest APIs und einfach zu implementieren deswegen fastAPI gewählt'''
import time
from fastapi import FastAPI
import uvicorn
import multiprocessing

App = FastAPI()
'''Zugreifen über http://127.0.0.1:8000/docs#/'''
@App.get("/get-twin-names-api/")
def Anzahl_Twins():
   return {"Test"}

def uvi_run():
   uvicorn.run("FastAPI:App", host='127.0.0.1', port=8000, debug=True)


if __name__ == "__main__":
   #API = multiprocessing.Process(target=uvi_run)
   API = multiprocessing.Process(target=(uvicorn.run("FastAPI:App", host='127.0.0.1', port=8000, debug=True)))
   API.start()
   while True:
      print("Test")
      time.sleep(2)


