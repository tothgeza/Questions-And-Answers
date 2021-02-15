import calendar
import time
from datetime import datetime
import bcrypt


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def convert_timestamp(timestamp):
    return datetime.fromtimestamp(int(timestamp))


def get_current_time():
    return calendar.timegm(time.gmtime())


def get_file_name_by_id(list_of_dicts, header, id_number, ):
    file_name_list = []
    for dictionary in list_of_dicts:
        if int(dictionary[header]) == int(id_number):
            file_name_list.append(dictionary['image'])
    return file_name_list
