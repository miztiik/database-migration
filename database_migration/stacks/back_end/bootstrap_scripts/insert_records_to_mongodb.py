# -*- coding: utf-8 -*-
import json
import logging
import random
import pymongo
import datetime
import time
import os
import socket


class GlobalArgs:
    """ Global statics """
    OWNER = "Mystique"
    ENVIRONMENT = "production"
    MODULE_NAME = "insert_records_to_mongodb"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FILE_NAME = "/var/log/miztiik-automation-mongodb-ingestor.log"
    DB_ADDRESS = "mongodb://localhost:27017/"
    DB_ADMIN_NAME = "mongodbadmin"
    DB_ADMIN_PASS = "Som3thingSh0uldBe1nVault"
    DB_NAME = "miztiik_db"
    DB_COLLECTIONS_1 = "customers"
    DB_COLLECTIONS_2 = "loyalty"
    NO_OF_RECORDS_TO_INSERT = 10
    INSERT_DURATION = 57


def getReferrer():
    x = random.randint(1, 2)
    x = x*10
    y = x+50
    data = {}
    product = random.randint(1, 250)
    data['custid'] = random.randint(x, y)
    data['referrer'] = random.choice(['amazon.com', 'facebook.com', 'twitter.com', 'github.com',
                                      'miztiik', 'myanimelist.net', 'valaxy', 'Akane', 'mystiqueAutomation', 'kon', 'wikileaks'])
    data['url'] = random.choice(['ela_neer_vitrine_nav', 'ela_neer_product_detail',
                                 'ela_neer_vitrine_nav', 'ela_neer_checkout', 'ela_neer_product_detail', 'ela_neer_cart'])
    data['device'] = random.choice(['app_mobile', 'app_tablet', 'browser'])
    data['kiosk_id'] = 0
    time.sleep(.5)
    data['ts'] = str(datetime.datetime.now())
    if data['url'] != 'ela_neer_vitrine_nav':
        data['kiosk_id'] = product
    return data


def insert_records():

    # GET LOCAL IP
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"Connecting to Mongo at IP Address: {ip_address}")
    # client = pymongo.MongoClient("mongodb://mongoDbAdmin:Som3thingSh0uldBe1nVault@10.10.0.52/miztiik_db")
    # mongo -u mongoDbAdmin -p Som3thingSh0uldBe1nVault 10.10.0.123
    # mongodb://mongoDbAdmin:Som3thingSh0uldBe1nVault@18.236.250.136/miztiik_db
    # client = pymongo.MongoClient(GlobalArgs.DB_ADDRESS)
    connection = f"mongodb://{GlobalArgs.DB_ADMIN_NAME}:{GlobalArgs.DB_ADMIN_PASS}@{ip_address}/admin"
    client = pymongo.MongoClient(connection)
    db = client[GlobalArgs.DB_NAME]
    print(connection)
    print(db)
    customers_coll = db[GlobalArgs.DB_COLLECTIONS_1]
    loyalty_coll = db[GlobalArgs.DB_COLLECTIONS_2]
    begin_time = datetime.datetime.now()
    new_time = begin_time
    i = 0
    while (new_time - begin_time).total_seconds() < GlobalArgs.INSERT_DURATION:
        cust_data = getReferrer()
        result = db[GlobalArgs.DB_COLLECTIONS_1].insert_one(cust_data)
        print(f"customer_record_id:{result.inserted_id}")
        insert_loyalty_points(cust_data["custid"])
        new_time = datetime.datetime.now()
        i += 1
    print(f'{{"no_of_records_inserted":{i}}}')
    client.close()
    # print the number of documents in a collection
    print(f'{{"total_coll_count":{customers_coll.estimated_document_count()}}}')
    logging.info(
        f'{{"total_coll_count":{customers_coll.estimated_document_count()}}}')
    print(f'{{"total_loyalty_coll_count":{loyalty_coll.estimated_document_count()}}}')
    logging.info(
        f'{{"total_loyalty_coll_count":{loyalty_coll.estimated_document_count()}}}')


def insert_loyalty_points(cust_id):
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    connection = f"mongodb://{GlobalArgs.DB_ADMIN_NAME}:{GlobalArgs.DB_ADMIN_PASS}@{ip_address}/admin"
    client = pymongo.MongoClient(connection)
    db = client[GlobalArgs.DB_NAME]
    loyalty_coll = db[GlobalArgs.DB_COLLECTIONS_2]
    data={}
    data["custid"] = cust_id
    data["pts"] = random.randint(1, 2500)
    result = db[GlobalArgs.DB_COLLECTIONS_2].insert_one(data)
    print(f"customer_loyalty_record_id:{result.inserted_id}")
    client.close()



logger = logging.getLogger()
logger = logging.getLogger()
logging.basicConfig(
    filename=f"{GlobalArgs.LOG_FILE_NAME}",
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=GlobalArgs.LOG_LEVEL
)
insert_records()
