import mysql.connector


tones_dict = {0:"Обычный",1:"Токсичный"}


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Qwerty1234",
        database="comments_ml_db"
    )


def get_comments():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                get_query = ''' SELECT * FROM comments '''
                cursor.execute(get_query)
                result = cursor.fetchall()
                result_dict = {"id":[],'comment': [], "tone_id":[]}
                for i in result:
                    result_dict["id"].append(i[0])
                    result_dict["comment"].append(i[1])
                    result_dict["tone_id"].append(i[2])
                return result
    except Exception as e:
        print(e)


def update_comment_tone(ob:dict):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                update_query = ''' Update comments SET comment_tone =%s where comment_id = %s; '''
                cursor.execute(update_query, (ob.get("comment_tone"),ob.get("comment_id")))

                conn.commit()

    except Exception as e:
        print(e)


def add_new_comment(ob:dict):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                insert_query = ''' INSERT INTO comments (comment_text, comment_tone) VALUES(%s, %s); '''
                cursor.execute(insert_query, (ob.get("comment_text"), ob.get("comment_tone")))

                conn.commit()

    except Exception as e:
        print(e)

