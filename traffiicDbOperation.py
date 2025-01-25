import pymysql
import os
import re


def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE"),
        port=int(os.getenv("DB_PORT", 3306)),
        cursorclass=pymysql.cursors.DictCursor
    )

def check_number_plate_exist(plate_number):
    plate_number_clean = re.sub(r'[^A-Za-z0-9]', '', plate_number)
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Execute the query
            query = "SELECT 1 FROM vehiclenumberplate WHERE PlateNumber = %s"
            cursor.execute(query, (plate_number_clean,))
            result = cursor.fetchone()
            # Return True if the plate exists, else False
            return True if result else False
    except Exception as e:
        # Log or handle the exception if necessary
        return False
    finally:
        if connection:
            connection.close()

def insert_vehicle_plate(plate_number):
    plate_number_clean = re.sub(r'[^A-Za-z0-9]', '', plate_number)
    
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Prepare the INSERT query
            query = "INSERT INTO vehiclenumberplate (PlateNumber) VALUES (%s)"
            cursor.execute(query, (plate_number_clean,))
            connection.commit()
            print(f"Vehicle plate {plate_number_clean} inserted successfully.")
            return {"message": f"Vehicle plate {plate_number_clean} inserted successfully."}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    finally:
        if connection:
            connection.close()

def get_all_vehicle_plates():
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = "SELECT * FROM vehiclenumberplate"
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except Exception as e:
        return {"error": str(e)}
    finally:
        if connection:
            connection.close()


def update_vehicle_plate(old_plate, new_plate):
    old_plate_clean = re.sub(r'[^A-Za-z0-9]', '', old_plate)
    new_plate_clean = re.sub(r'[^A-Za-z0-9]', '', new_plate)
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = "UPDATE vehiclenumberplate SET PlateNumber = %s WHERE PlateNumber = %s"
            cursor.execute(query, (new_plate_clean, old_plate_clean))
            connection.commit()
            if cursor.rowcount > 0:
                return {"message": f"Vehicle plate {old_plate_clean} updated to {new_plate_clean} successfully."}
            else:
                return {"error": f"Vehicle plate {old_plate_clean} not found."}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if connection:
            connection.close()


def delete_vehicle_plate(plate_number):
    plate_number_clean = re.sub(r'[^A-Za-z0-9]', '', plate_number)
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = "DELETE FROM vehiclenumberplate WHERE PlateNumber = %s"
            cursor.execute(query, (plate_number_clean,))
            connection.commit()
            if cursor.rowcount > 0:
                return {"message": f"Vehicle plate {plate_number_clean} deleted successfully."}
            else:
                return {"error": f"Vehicle plate {plate_number_clean} not found."}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if connection:
            connection.close()
