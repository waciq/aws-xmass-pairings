#Cloud version of the script, containing SSM read for password


import random
import email
import smtplib
from email.message import EmailMessage
import boto3
import json

#Download json file containing the list of participants and turn it into a dictionary
s3 = boto3.resource('s3')

content_object = s3.Object('xmass-pairing-s3', 'participantList.json')
file_content = content_object.get()['Body'].read().decode('utf-8')
json_dict = json.loads(file_content)

emailaddresses = json_dict

#export names into two exact same lists

list1 = []
list2 = []
for name in json_dict:
    list1.append(name)
    list2.append(name)

print(list1)
print(list2)

pairs = {}
ssm = boto3.client('ssm', region_name="eu-west-1")
parameterPass = ssm.get_parameter(Name='/xmass/mailpass', WithDecryption=True)
parameterAddress = ssm.get_parameter(Name='/xmass/mailaddress', WithDecryption=True)

#login
gmail_user = parameterAddress['Parameter']['Value'] #Address
gmail_password = parameterPass['Parameter']['Value']  # PASSWORD




def pairings():
    global pairs 
    random.shuffle(list1)
    random.shuffle(list2)

    for i in range (0,len(list1)):
        pairs[list1[i]] = list2[i]
    
    for key, val in pairs.items():
        if key == val:
            pairs = {}
            pairings()
    return pairs

def mailer():
    ssm = boto3.client('ssm', region_name="eu-west-1")
    parameterUrl = ssm.get_parameter(Name='/xmass/folderurl', WithDecryption=True)
    folderUrl = parameterUrl['Parameter']['Value']
    for name, address in emailaddresses.items():
        msg = EmailMessage()
        S = 'Witaj %s!' % (name)
        msg['From'] = 'pjpietraszuk@gmail.com'
        msg['To'] = address
        msg['Subject'] = S
        msg.set_content("Witaj " + name + "!" + "\n Wylosowana dla ciebie osoba to: " + str(pairs[name]) + "\n \n Oto link do folderu gdzie znajdziesz to, co " + str(pairs[name]) + " chce otrzymać: \n \n" + folderUrl)  #content of hte message
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        server.close()

        print('email sent to ' + name)
    

def main():
    pairings()
    print(pairs)
    mailer()


if __name__ == "__main__":
    main()