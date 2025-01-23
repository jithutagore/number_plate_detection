from utils.database import get_db_connection
from typing import List

class StagingEmailThreads:
    id: int
    thread_id: str
    sender_email_id: str
    html_content: str
    text_content: str
    received_time: str
    first_name: str
    last_name: str
    attachments_path_json: str

def fetch_all_threads() -> List[StagingEmailThreads]:
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM staging_email_threads"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    finally:
        connection.close()
