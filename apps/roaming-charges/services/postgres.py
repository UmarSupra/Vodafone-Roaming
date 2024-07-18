import psycopg2
import os, logging
from fastapi import HTTPException
import os, logging
from exceptions.exceptions import PayLoadError


class QueryPostgres:
    def __init__(self):
        self.table_name = os.environ.get("DB_TABLE")

    def postgres(self, query):

        with psycopg2.connect(
            database=os.environ.get("DB_NAME"),
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            port=os.environ.get("DB_PORT"),
        ) as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                    query
                )

                result = cursor.fetchall()
                try:
                    if not result:                        
                        raise PayLoadError()

                except PayLoadError:
                    raise HTTPException(
                        status_code=500, detail="Your query did not return any responses."
                    )

                except PayLoadError:
                    raise HTTPException(
                        status_code=500, detail="Your query did not return any responses."
                    )

                except Exception:
                    raise HTTPException(
                        status_code=500, detail="Failed to access database services."
                    )

                cursor.close()

                return result