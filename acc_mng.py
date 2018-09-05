#!/bin/python3

import win32com.client as win32
import boto3
from botocore import exceptions
from optparse import OptionParser
import csv
import random
import time


GROUP_NAME = "E"
S = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
PASSLEN = 10


def read_file(file):
    emails = {}
    with open(file, 'r') as csvf:
        read = csv.reader(csvf, delimiter=',')
        for row in read:
            name = row[0].split(' ')[0]
            emails[name] = {}
            emails[name]['username'] = row[1].split('.')[0][0] + row[1].split('.')[1] + '.' + row[1].split('.')[2]
            emails[name]['email'] = row[1]
    return emails


def pass_gen():
    password = "".join(random.sample(S, PASSLEN))
    return password


def create_user(user):
    try:
        created_user_responce = iam.create_user(UserName=user)
        list[user] = {}
        list[user]['Id'] = created_user_responce['User']['UserId']
        temp_password = pass_gen()
        time.sleep(0.5)
        iam.create_login_profile(
            UserName=user,
            Password=temp_password,
            PasswordResetRequired=False
        )
        time.sleep(0.5)
        list[user]['Password'] = temp_password
        create_keys_responce = iam.create_access_key(UserName=user)
        time.sleep(0.5)
        list[user]['AccessKey'] = create_keys_responce['AccessKey']['AccessKeyId']
        list[user]['SecretKey'] = create_keys_responce['AccessKey']['SecretAccessKey']
        iam.add_user_to_group(
            GroupName=GROUP_NAME,
            UserName=user
        )
        print("User {0} created.".format(user))
    except exceptions.ClientError:
        print("Can't create user {0} something is wrong".format(user))


def send_email(email,user, name):
    try:
        outlook = win32.Dispatch('Outlook.Application')
        mail = outlook.CreateItem(0)
        mail.To = email
        mail.Subject = 'reaxys-statistics s3 bucket access' #reaxys-statistics s3 bucket access
        mail.Body = 'Hello {0},\n\n' \
                    'I have created user for you with access to reaxys-statistics s3 bucket.'\
                    'You credentials for https://aws-cm-reaxys.signin.aws.amazon.com/console are next:\n' \
                    'Username: {1}\n' \
                    'Password: {2}\n' \
                    'AccessKey: {3}\n' \
                    'SecretKey: {4}\n\n' \
                    'Do not hesitate to contact me if further assistance is needed.\n\n Regards,\n Artem Buria\n Systems Engineer'.format(name, user, list[user]['Password'], list[user]['AccessKey'], list[user]['SecretKey'])
        mail.Send()
        print("Mail sent to {0}".format(user))
    except Exception:
        print("Cant send email")


def save_result():
    with open('result.csv', 'w') as csvf:
        writer = csv.writer(csvf, delimiter=',')
        for user in list.keys():
            writer.writerow([user, list[user]['Id'], list[user]['Password'], list[user]['AccessKey'], list[user]['SecretKey']])
    print("Result was saved to result.csv")

def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="FILE", help="File containing list of user")
    parser.add_option("-c", "--credentials", dest="PROFILE", help="AWS Credentials to use", type="str")
    (options, args) = parser.parse_args()
    list_of_users = read_file(options.FILE)
    global iam, list
    list = {}
    iam = boto3.client('iam')
    print(list_of_users)
    for user in list_of_users.keys():
        #print(list_of_users[user]['email'],list_of_users[user]['username'],user)
        create_user(list_of_users[user]['username'])
        time.sleep(1)
        send_email(list_of_users[user]['email'],list_of_users[user]['username'],user)
    save_result()


if __name__ == "__main__":
    main()
