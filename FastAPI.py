'''Speziell für Rest APIs und einfach zu implementieren deswegen fastAPI gewählt'''
import time
from fastapi import FastAPI
import uvicorn
import threading

App = FastAPI()

'''Zugreifen über http://127.0.0.1:8000/docs#/'''
@App.get("/get-twin-names-api/")
def get_twins():
   return {"Test"}

if __name__ == "__main__":
    uvicorn.run("FastAPI:App", host='127.0.0.1', port=8000, debug=True)



# Test = threading.Thread(target=test())
# Test.start()


