from shared import DataStorage, log_message 
# from GUI import update_tables
import re
import datetime

def get_timestamp():
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H-%M-%S.%f")
    timestamp = timestamp[:-3]  
    return timestamp

def intialize_token(token, isGroup):
    return [-1, "", "", -1, get_timestamp(), -1, -1]

def creat_token_if_doesnt_exist(token):
    if not DataStorage.check_token_exist(token):
        DataStorage.store_token(token, intialize_token(token, False))

def add_token_to_group(token, rssi = -1):
    group_num = 0
    if DataStorage.group_number_already_assigned(token):
        DataStorage.store_group_token(token, DataStorage.get_value_of_key(token))
        group_num = DataStorage.get_value_of_key(token)[3]

    else:
        value = DataStorage.get_value_of_key(token)
        value[3] = DataStorage.get_group_number() 
        DataStorage.store_group_token(token, value)
        group_num = value[3]

    if rssi != -1:
        DataStorage.update_stored_token_in_group(token, 6, rssi)
    
    return group_num
        


def get_company_and_roll(message, token, maxSize):
    
    # [Db <===] Data incomplete with message size 5. Make roll and company name = message[2]
    # [Db <===] Data incomplete with message size 4. Make roll and company name = unknown 
    # size 4. Make Roll = message[2] and cn = message[3]

    if len(message) == maxSize:
        DataStorage.update_stored_token(token, 1, message[len(message) - 3])
        DataStorage.update_stored_token(token, 2, message[len(message) - 3])
        DataStorage.falg_token(token)

    elif len(message) == maxSize - 1 and message[len(message) - 2] == "Db":
        DataStorage.update_stored_token(token, 1, "Unknown")
        DataStorage.update_stored_token(token, 2, "Unknown")
        DataStorage.falg_token(token)

    elif len(message) == maxSize - 1:
        DataStorage.update_stored_token(token, 1, message[len(message) - 1])
        DataStorage.update_stored_token(token, 2, message[len(message) - 2])
        if message[len(message) - 1] == "Unknown" or message[len(message) - 2] == "Unknown":
            DataStorage.falg_token(token)

def compose_message(message, id):
    return message[0] + ": " + "Token ID-" + id

def format_hex_number(number):
    return number.zfill(4)

def is_hex(s):
    hex_pattern = r'^[0-9a-fA-F]+$'
    return bool(re.match(hex_pattern, s))

def DISC_info(message):           
    tokenId = format_hex_number(message[1])
    creat_token_if_doesnt_exist(tokenId)
    DataStorage.update_stored_token(tokenId, 0, message[3])
    get_company_and_roll(message, tokenId, 9)
    return add_token_to_group(tokenId, message[5])

def ANRY_info(message):
    tokenId = format_hex_number(message[1])
    creat_token_if_doesnt_exist(tokenId)
    get_company_and_roll(message, tokenId, 5)
    return add_token_to_group(tokenId)

def button_info(message):   #[key: token id][Bat, Company, Roll, rssi, tmp, BLE, nfc, hmv, fwv, mdl, coldrst, bod]
    tokenId = format_hex_number(message[3])
    creat_token_if_doesnt_exist(tokenId)
    DataStorage.output_buffer.put(compose_message(message, tokenId))
    return add_token_to_group(tokenId)

def get_info(message):
    tokenId = format_hex_number(message[0])
    creat_token_if_doesnt_exist(tokenId)   
    DataStorage.update_stored_token(tokenId, 0, message[1])
    get_company_and_roll(message, tokenId, 5) 
    return add_token_to_group(tokenId)

def handel_alarm(message):
    tokenId = format_hex_number(message[2])
    creat_token_if_doesnt_exist(tokenId)
    if message[4] == "3":
        DataStorage.add_alarm(tokenId, compose_message(message, tokenId))
    else:
        DataStorage.remove_alarm(tokenId)
    return add_token_to_group(tokenId)

def decode_message(message):
    words = re.split(r'[ ,:]+|0x', message)
    if words[0] == "ANRY":
        log_message(message + " Group: " + str(ANRY_info(words)))

    elif words[0] == "DISC":
        log_message(message + " Group: " + str(DISC_info(words)))

    elif words[0] == "INFO":
        log_message(message + " Group: " + str(button_info(words)))

    elif is_hex(words[0]): 
        log_message(message + " Group: " + str(get_info(words)))

    elif words[0] == "ALARM":
        log_message(message + " Group: " + str(handel_alarm(words)))

    # update_tables()

    

 