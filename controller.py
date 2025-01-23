from fastapi import APIRouter
from handler.extractQA import extractQuestion
from utils.loggerSetup import logger

logger.info("hi")

provider_router = APIRouter(prefix="/provider", tags=["provider"])

@provider_router.get("/extractQuestion")
async def get_provider_route():
    logger.info("extract questions")
    return await extractQuestion()


