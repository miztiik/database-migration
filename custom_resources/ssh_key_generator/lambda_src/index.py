# -*- coding: utf-8 -*-
import json
import logging
import os


import boto3
import cfnresponse


class GlobalArgs:
    """ Global statics """
    OWNER = "Mystique"
    ENVIRONMENT = "production"
    MODULE_NAME = "ssh_key_generator_lambda"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def set_logging(lv=GlobalArgs.LOG_LEVEL):
    """ Helper to enable logging """
    logging.basicConfig(level=lv)
    logger = logging.getLogger()
    logger.setLevel(lv)
    return logger


logger = set_logging()
SSH_KEY_NAME = os.getenv("SSH_KEY_NAME", "mystique-automation-ssh-key")


def create_key(event, context):
    """ Create EC2 key pair and persist it in the SSM Parameter Store"""
    try:
        ec2 = boto3.client("ec2")
        result = ec2.create_key_pair(KeyName=SSH_KEY_NAME)
        key = result['KeyMaterial']
        # store key as SSM parameter
        ssm = boto3.client("ssm")
        ssm.put_parameter(Name=SSH_KEY_NAME, Type="String",
                          Value=key, Overwrite=True)
    except Exception as e:
        print(e)


def delete_key(event, context):
    """ Delete EC2 key pair from the SSM Parameter Store"""
    try:
        ec2 = boto3.client("ec2")
        ec2.delete_key_pair(KeyName=SSH_KEY_NAME)
        ssm = boto3.client("ssm")
        ssm.delete_parameter(Name=SSH_KEY_NAME)
    except Exception as e:
        print(e)


def lambda_handler(event, context):
    logger.info(f"rcvd_evnt:\n{event}")
    physical_id = "MystiqueAutomationCustomRes"
    attributes = {"ssh_key_gen_status": "SUCCESS"}

    try:
        if event["RequestType"] == "Update":
            return cfnresponse.send(event, context, cfnresponse.SUCCESS, attributes, physical_id)
        elif event["RequestType"] == "Create":
            create_key(event, context)
        elif event["RequestType"] == "Delete":
            delete_key(event, context)
        else:
            logger.error("FAILED!")
            attributes = {"ssh_key_gen_status": "FAILED"}
            return cfnresponse.send(event, context, cfnresponse.FAILED, attributes, physical_id)

        cfnresponse.send(event, context, cfnresponse.SUCCESS,
                         attributes, physical_id)
    except Exception as e:
        logger.exception(e)
        attributes = {"ssh_key_gen_status": "FAILED"}
        cfnresponse.send(event, context, cfnresponse.FAILED,
                         attributes, physical_id)
