
import random
import email
import smtplib
from email.message import EmailMessage
import boto3
import json




s3 = boto3.resource('s3')

content_object = s3.Object('xmass-pairing-s3', 'participantList.json')
file_content = content_object.get()['Body'].read().decode('utf-8')
json_dict = json.loads(file_content)

for key in json_content:
    print(key)


