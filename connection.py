import os
import psycopg2
import psycopg2.extras
# import os.path
from os import path

# QUESTION_FILE_PATH = os.getenv('QUESTION_FILE_PATH') if 'QUESTION_FILE_PATH' in os.environ else 'question.csv'
# ANSWER_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'question.csv'
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
UPLOADER_FOLDER = os.path.join(PROJECT_ROOT, 'static', 'images')


def get_connection_string():
    # setup connection string
    # to do this, please define these environment variables first
    user_name = os.environ.get('PSQL_USER_NAME')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    database_name = os.environ.get('PSQL_DB_NAME')

    env_variables_defined = user_name and password and host and database_name

    if env_variables_defined:
        # this string describes all info for psycopg2 to connect to the database
        return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
            user_name=user_name,
            password=password,
            host=host,
            database_name=database_name
        )
    else:
        raise KeyError('Some necessary environment variable(s) are not defined')


def open_database():
    try:
        # connection_string = get_connection_string()
        connection_string = os.environ.get('DATABASE_URL')
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a RealDictCursor cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value

    return wrapper


def if_file_exist(value):
    if path.exists(UPLOADER_FOLDER + '/' + value):
        return True
    return False


def image_path(file_name):
    return os.path.join(UPLOADER_FOLDER, file_name)


def delete_image(file_name):
    if file_name != "default.png":
        try:
            os.remove(image_path(file_name))
        except FileNotFoundError:
            pass
        except IsADirectoryError:
            pass


def delete_images(file_name_list):
    for file_name in file_name_list:
        delete_image(file_name)
