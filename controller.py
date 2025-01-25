from fastapi import APIRouter
from handler.numberPlateToText import getNumberPlate
from utils.loggerSetup import logger

logger.info("hi")

number_plate_router = APIRouter(prefix="/traffic-control", tags=["Number plate detection"])

@number_plate_router.get("/getNumberPlate")
async def get_provider_route():
    logger.info("extract number plate value")
    return await getNumberPlate()


