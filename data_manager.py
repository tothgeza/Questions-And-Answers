import connection
import util
from typing import List, Dict
import datetime

QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
TITLE_HEADER = ['Id', 'Date', 'View', 'Vote', 'Title', 'Message']


@connection.connection_handler
def get_tags_to_question_id(cursor):
    query = """
                SELECT question_tag.question_id, tag.name, tag.id 
                FROM question_tag, tag
                WHERE question_tag.tag_id = tag.id;
                """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_tag_name_by_question_id(cursor, question_id):
    query = """
                SELECT * FROM tag
                WHERE id in
                (SELECT tag_id FROM question_tag
                WHERE %(question_id)s=question_id);
                """
    value = {'question_id': question_id}
    cursor.execute(query, value)
    return cursor.fetchall()


@connection.connection_handler
def modify_tag(cursor, question_id, tag):
    query = """
            INSERT INTO tag (name)
            SELECT %(tag)s
            WHERE NOT EXISTS (SELECT name FROM tag WHERE name = %(tag)s);
            INSERT INTO question_tag(question_id, tag_id)
            SELECT %(question_id)s, (SELECT id FROM tag WHERE name = %(tag)s)
            WHERE NOT EXISTS (SELECT question_id, tag_id FROM question_tag 
            WHERE question_id = %(question_id)s and tag_id = (SELECT id FROM tag WHERE name = %(tag)s));
                """
    value = {'tag': tag, 'question_id': question_id}
    cursor.execute(query, value)


@connection.connection_handler
def get_tag_that_not_in_question(cursor, question_id):
    query = """
                SELECT name FROM tag
                WHERE id not in
                (SELECT tag_id FROM question_tag
                WHERE question_id = %(question_id)s);
                """
    value = {'question_id': question_id}
    cursor.execute(query, value)
    return cursor.fetchall()


@connection.connection_handler
def get_questions(cursor, order_by, reverse) -> List:
    query = """
                SELECT q.*, u.username
                FROM question q
                JOIN users u 
                ON q.user_id = u.id
                ORDER BY {} {};
                """.format(order_by, reverse)
    value = {'order_by': order_by, 'reverse': reverse}
    cursor.execute(query, value)
    return cursor.fetchall()


@connection.connection_handler
def get_latest_five_questions(cursor, order_by, reverse) -> List:
    query = """
                WITH question_five AS (SELECT * FROM question ORDER BY submission_time DESC LIMIT 5)
                SELECT q.*, u.username
                FROM question_five q
                JOIN users u
                ON q.user_id = u.id
                ORDER BY {} {};
                """.format(order_by, reverse)
    value = {'order_by': order_by, 'reverse': reverse}
    cursor.execute(query, value)
    return cursor.fetchall()


@connection.connection_handler
def get_answers_by_question_id(cursor, question_id):
    query = """
                SELECT a.*, u.username
                FROM answer a
                JOIN users u
                ON a.user_id = u.id
                WHERE a.question_id = %(question_id)s
                ORDER BY vote_number DESC;
                """
    value = {'question_id': question_id}
    cursor.execute(query, value)
    return cursor.fetchall()


@connection.connection_handler
def get_an_answer(cursor, answer_id):
    query = """
                SELECT a.*, u.username 
                FROM answer a
                JOIN users u 
                ON a.user_id = u.id
                WHERE a.id = %(answer_id)s;
                """
    value = {'answer_id': answer_id}
    cursor.execute(query, value)
    return cursor.fetchall()


@connection.connection_handler
def get_question_by_id(cursor, question_id):
    query = """
                SELECT q.*, u.username
                FROM question q
                JOIN users u 
                ON q.user_id = u.id
                WHERE q.id = %(question_id)s;
                """
    value = {'question_id': question_id}
    cursor.execute(query, value)
    return cursor.fetchall()


@connection.connection_handler
def get_question_comments_with_username(cursor, question_id):
    query = """
                SELECT c.*, u.username FROM comment c
                JOIN users u
                ON c.user_id = u.id
                WHERE question_id = %(question_id)s
                ORDER BY submission_time DESC;;
                """
    value = {'question_id': question_id}
    cursor.execute(query, value)
    return cursor.fetchall()


@connection.connection_handler
def get_comments_by_id(cursor, comment_id):
    query = """
                SELECT * FROM comment
                WHERE %(comment_id)s=id
                ORDER BY submission_time DESC;
                """
    value = {'comment_id': comment_id}
    cursor.execute(query, value)
    return cursor.fetchall()


@connection.connection_handler
def get_answers_comments_with_username(cursor, question_id):
    query = """
                SELECT c.*, u.username 
                FROM comment c
                JOIN users u
                ON c.user_id = u.id
                WHERE answer_id in 
                (SELECT answer.id FROM answer
                WHERE answer.question_id = %(question_id)s)
                ORDER BY submission_time DESC;
                """
    value = {'question_id': question_id}
    cursor.execute(query, value)
    return cursor.fetchall()


@connection.connection_handler
def get_question_by_a_id(cursor, answer_id):
    query = """
                SELECT q.*, u.username
                FROM question q
                JOIN users u 
                ON q.user_id = u.id
                WHERE q.id in 
                (SELECT answer.question_id FROM answer
                WHERE answer.id = %(answer_id)s);
                """
    value = {'answer_id': answer_id}
    cursor.execute(query, value)
    return cursor.fetchall()


@connection.connection_handler
def get_password(cursor, username):
    query = """
            SELECT password
            FROM users
            WHERE username = %(username)s;
            """
    value = {'username': username}
    cursor.execute(query, value)
    return cursor.fetchall()


@connection.connection_handler
def get_all_users(cursor):
    query = """
            SELECT u.id, username, email_address, registration_date, reputation,
            (SELECT COUNT(*) FROM answer WHERE answer.user_id = u.id) AS asks,
            (SELECT COUNT(*) FROM comment WHERE comment.user_id = u.id) AS comments,
            (SELECT COUNT(*) FROM question WHERE question.user_id = u.id) AS questions
            FROM users u
            GROUP BY u.id;
            """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_a_user(cursor, user_id):
    query = """
            SELECT u.id, username, email_address, registration_date, reputation,
            (SELECT COUNT(*) FROM answer WHERE answer.user_id = u.id) AS asks,
            (SELECT COUNT(*) FROM comment WHERE comment.user_id = u.id) AS comments,
            (SELECT COUNT(*) FROM question WHERE question.user_id = u.id) AS questions
            FROM users u
            WHERE u.id  = %(user_id)s 
            GROUP BY u.id;
            """
    value = {'user_id': user_id}
    cursor.execute(query, value)
    return cursor.fetchall()


@connection.connection_handler
def get_data_from_user(cursor, table, user_id):
    query = """
            SELECT *
            FROM {}
            WHERE user_id  = %(user_id)s; 
            """.format(table)
    values = {'user_id': user_id, 'table': table}
    cursor.execute(query, values)
    return cursor.fetchall()


@connection.connection_handler
def get_answers_to_user(cursor, user_id):
    query = """
            SELECT question_id, message
            FROM answer
            WHERE user_id  = %(user_id)s 
            """
    value = {'user_id': user_id}
    cursor.execute(query, value)
    return cursor.fetchall()


@connection.connection_handler
def get_comment_to_user(cursor, user_id):
    query = """
            SELECT question_id, message
            FROM comment
            WHERE user_id  = %(user_id)s AND question_id IS NOT NULL
            """
    value = {'user_id': user_id}
    cursor.execute(query, value)
    return cursor.fetchall()


@connection.connection_handler
def search_in_questions(cursor, search_phrase):
    query = """
                SELECT * FROM question
                WHERE lower(message) Like '%{}%' OR lower(title) Like '%{}%'
                OR id in
                (SELECT question_id FROM answer
                WHERE lower(message) Like '%{}%');
                """.format(search_phrase.lower(), search_phrase.lower(), search_phrase.lower())
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_question_owners(cursor):
    query = """
            SELECT question.id, users.username
            FROM question
            JOIN users
            ON question.user_id = users.id
            """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def search_in_answers(cursor, search_phrase):
    query = """
                SELECT * FROM answer
                WHERE lower(message) Like '%{}%';
                """.format(search_phrase.lower())
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def add_question(cursor, title, message, file_name, user_id):
    new_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    query = """
                INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id) 
                VALUES (%(new_time)s, %(view)s, %(vote)s, %(title)s, %(message)s, %(file_name)s, %(user_id)s);
                """
    value = {'new_time': new_time, 'view': 0, 'vote': 0, 'title': title,
             'message': message, 'file_name': file_name, 'user_id': user_id}
    cursor.execute(query, value)


@connection.connection_handler
def update_question(cursor, title, message, file_name, question_id):
    new_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    query = """
                UPDATE question SET submission_time = %(time)s,
                                    title = %(title)s,
                                    message = %(message)s,
                                    image = %(file_name)s 
                WHERE %(question_id)s=id;
                """
    value = {'time': new_time, 'title': title, 'message': message, 'file_name': file_name, 'question_id': question_id, }
    cursor.execute(query, value)


@connection.connection_handler
def update_answer(cursor, message, file_name, answer_id):
    new_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    query = """
                UPDATE answer SET submission_time = %(time)s,
                                  message = %(message)s,
                                  image = %(file_name)s 
                WHERE %(answer_id)s=id;
                """
    value = {'time': new_time, 'message': message, 'file_name': file_name, 'answer_id': answer_id, }
    cursor.execute(query, value)


@connection.connection_handler
def update_answer_accepted(cursor, answer_id, value):
    query = """
            UPDATE answer SET accepted = %(value)s
            WHERE id = %(answer_id)s;
            """
    value = {'value': value, 'answer_id': answer_id}
    cursor.execute(query, value)


@connection.connection_handler
def update_comment(cursor, message, comment_id):
    new_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    query = """
                UPDATE comment SET  message = %(message)s,
                                    submission_time = %(time)s,
                                    edited_count = COALESCE(edited_count, 0) + 1 
                WHERE %(comment_id)s=id;
                """
    value = {'message': message, 'time': new_time, 'comment_id': comment_id}
    cursor.execute(query, value)


@connection.connection_handler
def check_user_data(cursor, column, data):
    query = """
                SELECT {}  
                FROM users
                WHERE {} = %(data)s;
                """.format(column, column)
    value = {'column': column, 'data': data}
    cursor.execute(query, value)
    # return cursor.fetchall()
    if cursor.fetchall():
        return True
    return False


@connection.connection_handler
def add_user(cursor, username, email_address, password):
    new_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    query = """
                INSERT INTO users (username, email_address, registration_date, reputation, password) 
                VALUES (%(username)s, %(email_address)s, %(registration_date)s, %(reputation)s, %(password)s);
                """
    value = {'username': username, 'email_address': email_address, 'registration_date': new_time,
             'reputation': 0, 'password': password}
    cursor.execute(query, value)


@connection.connection_handler
def get_user_id(cursor, username):
    query = """
                SELECT id
                FROM users
                WHERE username = %(username)s;
                """
    value = {'username': username}
    cursor.execute(query, value)
    return cursor.fetchall()


@connection.connection_handler
def add_answer(cursor, message, question_id, file_name, user_id):
    new_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    query = """
                INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id) 
                VALUES (%(new_time)s, %(vote)s, %(question_id)s, %(message)s, %(file_name)s, %(user_id)s);
                """
    value = {'new_time': new_time, 'vote': 0, 'question_id': question_id,
             'message': message, 'file_name': file_name, 'user_id': user_id}
    cursor.execute(query, value)


@connection.connection_handler
def delete_question_by_id(cursor, question_id):
    question_list = get_question_by_id(question_id)
    file_name_list = util.get_file_name_by_id(question_list, QUESTION_HEADER[0], question_id)
    connection.delete_images(file_name_list)
    query = """
                DELETE FROM question 
                WHERE %(question_id)s = id;
                """
    value = {'question_id': question_id}
    cursor.execute(query, value)


@connection.connection_handler
def delete_answer_by_question_id(cursor, question_id):
    answer_list = get_answers_by_question_id(question_id)
    file_name_list = util.get_file_name_by_id(answer_list, ANSWER_HEADER[3], question_id)
    connection.delete_images(file_name_list)
    query = """
                DELETE FROM answer 
                WHERE %(question_id)s = question_id;
                """
    value = {'question_id': question_id}
    cursor.execute(query, value)


@connection.connection_handler
def delete_answer_by_answer_id(cursor, answer_id):
    answer_list = get_an_answer(answer_id)
    file_name_list = util.get_file_name_by_id(answer_list, ANSWER_HEADER[0], answer_id)
    connection.delete_images(file_name_list)
    query = """
                DELETE FROM answer
                WHERE %(answer_id)s = id;
                """
    value = {'answer_id': answer_id}
    cursor.execute(query, value)


@connection.connection_handler
def delete_all_comments_by_que_id(cursor, question_id):
    query = """
                DELETE FROM comment
                WHERE answer_id in
                (SELECT id FROM answer
                WHERE question_id = %(question_id)s)
                OR question_id =%(question_id)s;
                """
    value = {'question_id': question_id}
    cursor.execute(query, value)


@connection.connection_handler
def delete_all_comments_by_ans_id(cursor, answer_id):
    query = """
                DELETE FROM comment
                WHERE %(answer_id)s = answer_id;
                """
    value = {'answer_id': answer_id}
    cursor.execute(query, value)


@connection.connection_handler
def delete_comment_by_c_id(cursor, comment_id):
    query = """
            DELETE FROM comment
            WHERE %(comment_id)s = id;
            """
    value = {'comment_id': comment_id}
    cursor.execute(query, value)


@connection.connection_handler
def delete_all_tag_by_q_id(cursor, question_id):
    query = """
            DELETE FROM question_tag
            WHERE %(question_id)s = question_id;
            """
    value = {'question_id': question_id}
    cursor.execute(query, value)


@connection.connection_handler
def delete_tag_by_q_id(cursor, question_id, tag_id):
    query = """
            DELETE FROM question_tag
            WHERE %(question_id)s = question_id AND %(tag_id)s = tag_id;
            """
    value = {'question_id': question_id, 'tag_id': tag_id}
    cursor.execute(query, value)


@connection.connection_handler
def add_comment_to_question(cursor, message, question_id, user_id):
    new_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    query = """
                INSERT INTO comment (question_id, message, submission_time, user_id) 
                VALUES (%(question_id)s, %(message)s, %(new_time)s, %(user_id)s);
                """
    value = {'question_id': question_id, 'message': message, 'new_time': new_time, 'user_id': user_id}
    cursor.execute(query, value)


@connection.connection_handler
def add_comment_to_answer(cursor, message, answer_id, user_id):
    new_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    query = """
                INSERT INTO comment (answer_id, message, submission_time, user_id) 
                VALUES (%(answer_id)s, %(message)s, %(new_time)s, %(user_id)s);
                """
    value = {'answer_id': answer_id, 'message': message, 'new_time': new_time, 'user_id': user_id}
    cursor.execute(query, value)


# @connection.connection_handler
# def make_question_vote(cursor, question_id, vote):
#     vote = 1 if vote == 'up' else -1
#     query = """
#                 UPDATE question SET vote_number = vote_number + %(vote_direction)s
#                 WHERE %(question_id)s=id;
#                 """
#     value = {'question_id': question_id, 'vote_direction': vote}
#     cursor.execute(query, value)


@connection.connection_handler
def make_answer_vote(cursor, answer_id, vote):
    vote = 1 if vote == 'up' else -1
    query = """
                UPDATE answer SET vote_number = vote_number + %(vote_direction)s
                WHERE %(answer_id)s=id;
                """
    value = {'answer_id': answer_id, 'vote_direction': vote}
    cursor.execute(query, value)


@connection.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    query = """
                SELECT question_id FROM answer
                WHERE %(answer_id)s=id;
                """
    value = {'answer_id': answer_id}
    cursor.execute(query, value)
    return cursor.fetchall()[0]['question_id']


@connection.connection_handler
def increase_display_count(cursor, question_id):
    query = """
            UPDATE question SET view_number=view_number+1
            WHERE %(question_id)s=id;
            """
    value = {'question_id': question_id}
    cursor.execute(query, value)


@connection.connection_handler
def update_vote_to_question(cursor, question_id, vote_num):
    query = """
            UPDATE question
            SET vote_number = vote_number + %(vote_num)s
            WHERE id = %(question_id)s;
            """
    values = {'vote_num': vote_num, 'question_id': question_id}
    cursor.execute(query, values)


@connection.connection_handler
def update_reputation(cursor, owner_id, rep_num):
    query = """
            UPDATE users
            SET reputation = reputation + %(rep_num)s
            WHERE id = %(owner_id)s;
            """
    values = {'rep_num': rep_num, 'owner_id': owner_id}
    cursor.execute(query, values)


@connection.connection_handler
def delete_vote(cursor, column, id_num, user_id):
    query = """
            DELETE FROM votes
            WHERE {} = %(id_num)s AND user_id = %(user_id)s;
            """.format(column)
    values = {'column': column, 'id_num': id_num, 'user_id': user_id}
    cursor.execute(query, values)


@connection.connection_handler
def create_vote(cursor, column, column_id, user_id, value):
    query = """
            INSERT INTO votes ({}, user_id, updown )
            VALUES (%(column_id)s, %(user_id)s, %(value)s)
            """.format(column)
    values = {'column_id': column_id, 'user_id': user_id, 'value': value}
    cursor.execute(query, values)


def check_file_exists(value):
    return connection.if_file_exist(value)


def path_to_image(file_name):
    return connection.image_path(file_name)


def delete_unused_image(file_name):
    connection.delete_image(file_name)


@connection.connection_handler
def check_vote_question(cursor, quest_id, user_id):
    query = """
            SELECT *
            FROM votes
            WHERE  question_id = %(quest_id)s AND user_id = %(user_id)s;
            """
    values = {'quest_id': quest_id, 'user_id': user_id}
    cursor.execute(query, values)
    return cursor.fetchall()
