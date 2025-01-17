import cx_Oracle

from backend.oracleconnection import create_matched_jobs_table


def save_matched_jobs(user_id, matched_jobs):
    """
    Save matched jobs to the matched_jobs table for the specific user.
    :param user_id: ID of the user for whom the matched jobs are saved.
    :param matched_jobs: List of matched jobs.
    :return: Success message.
    """
    try:
        dsn = cx_Oracle.makedsn('localhost', 1521, service_name='XE')
        connection = cx_Oracle.connect(user='FYP_01', password='system', dsn=dsn)
        print("Connected to Oracle database for saving matched jobs.")

        with connection.cursor() as cursor:
            table_name = f"matched_jobs_user_{user_id}"
            
            # Ensure the table exists
            create_matched_jobs_table(user_id)

            # Insert matched jobs into the table
            for job in matched_jobs:
                cursor.execute(f"""
                    INSERT INTO {table_name} 
                    (job_id, title, description, time_submitted, currency, budget, status, posted_date, similarity_score)
                    VALUES (:job_id, :title, :description, :time_submitted, :currency, :budget, :status, :posted_date, :similarity_score)
                """, {
                    'job_id': job['id'],
                    'title': job['title'],
                    'description': job['description'],
                    'time_submitted': job['time_submitted'],
                    'currency': job['currency'],
                    'budget': job['budget'],
                    'status': job['status'],
                    'posted_date': job['posted_date'],
                    'similarity_score': job['similarity_score']
                })

        connection.commit()
        print(f"Matched jobs saved successfully for user {user_id}.")
        return f"Matched jobs saved successfully for user {user_id}."
    except Exception as e:
        raise Exception(f"Error saving matched jobs: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

