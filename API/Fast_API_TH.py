import time
import uvicorn
from Class_Server import Server

'''https://stackoverflow.com/questions/61577643/python-how-to-use-fastapi-and-uvicorn-run-without-blocking-the-thread'''

config = uvicorn.Config("Fast_API_MP:App", host="127.0.0.1", port=8000, log_level="info")
server = Server(config=config)

with server.run_in_thread():
    # Server is started.
    ...
    while True:
        print("Helolo")
        time.sleep(2)
    # Server will be stopped once code put here is completed
    ...

# Server stopped.