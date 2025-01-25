from fastapi import FastAPI
from controller import number_plate_router
import uvicorn

app = FastAPI(title="MatchNP project", version="1.0")

app.include_router(number_plate_router)

if __name__ == "__main__":
    # Run the application with Uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)