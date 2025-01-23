from utils.loggerSetup import logger
from service.getQuestion import processProvider

from databaseOperation.mailDataTable import fetch_all_threads
logger.info("Starting the question extraction process...")

async def extractQuestion():
    try:
        # Fetch threads from the database
        threads = fetch_all_threads()  # This is a synchronous function

        logger.info(f"Fetched {len(threads)} email threads from the database.")
        single_provider=processProvider(threads)
        
        # Process the threads if needed
        # Example: Log some details about the first thread
        

        return single_provider
    
    except Exception as e:
        logger.error(f"An error occurred while extracting questions: {e}")
        raise
