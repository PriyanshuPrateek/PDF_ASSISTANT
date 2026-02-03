from memory.database import get_connection

def save_chat(user_message,assitant_response):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
      
    INSERT INTO chat_history(user_message,assitant_response)
    VALUES(%s , %s)   

    """

    cursor.execute(query,(user_message,assitant_response))
    conn.commit()

    cursor.close()
    conn.close()

def get_chat_history(limit=5):
    conn = get_connection()
    cursor = conn.cursor()

    query = """

    SELECT user_message , assitant_response
    From chat_history
    ORDER BY created_at DESC
    LIMIT %s

    """

    cursor.execute(query,(limit,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    history = ""
    for row in reversed(rows):
        history += f"User: {row[0]}\nAssistant: {row[1]}\n"

    return history
