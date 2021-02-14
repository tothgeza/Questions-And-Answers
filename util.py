import calendar
import time
from datetime import datetime


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
