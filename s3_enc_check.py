#!/usr/bin/env python3

import boto3
import csv
from botocore import exceptions
from optparse import OptionParser
import datetime
import time


DAYS = 5


def retrive_list(file):
    buckets = set()
    try:
        with open(file, 'r') as flow:
            for line in flow.readlines():
                buckets.add(line.strip())
        return buckets
    except (NameError, OSError):
        print("Can't open file.\n'{0}' wasn't found or wrong path was specified".format(file))
        exit(1)


def paginate_over_bucket(target_bucket):
    objects_list = []
    paginator = s3.get_paginator('list_objects_v2')
    page_iter = paginator.paginate(Bucket=target_bucket)
    for page in page_iter:
        if 'Contents' in page.keys():
            for object in page['Contents']:
                if object['Key'][-1] != '/':
                    objects_list.append(object['Key'])
    return objects_list


def restore_object(target_bucket, object_key):
    print("Start restoring {0}".format(object_key))
    try:
        s3.restore_object(Bucket=target_bucket,
                          Key=object_key,
                          RestoreRequest={
                              'Days':DAYS,
                              'GlacierJobParameters': {
                                  'Tier': 'Standard'
                              }
                          })
        statistic[target_bucket][object_key]['ActionR'] = 'Restored'
    except exceptions.ClientError:
        print("Can't restore object {0}.".format(object_key))


def head_object(target_bucket,object_key):
    try:
        head = s3.head_object(Bucket=target_bucket, Key=object_key)
        return head
    except exceptions.ClientError:
        print("Can't get objects head {0}".format(object_key))
        for param in statistic[target_bucket][object_key].keys():
            statistic[target_bucket][object_key][param] = "no access"
        return False

def create_report(account_statistic):
    with open(reportfile, 'w') as csvf:
        reporting = csv.writer(csvf, delimiter=',')
        reporting.writerow(['Bucket',
                            'Default_Encryption',
                            'Object',
                            'Encryption',
                            'Action',
                            'IsArchived',
                            'Action_on_restored_object'])
        for bucket in account_statistic.keys():
            reporting.writerow([bucket, account_statistic[bucket]['DefaultEncryption']])
            print("Report for {0}".format(bucket))
            if len(account_statistic[bucket].keys()) != 1:
                for object in account_statistic[bucket].keys():
                    if object != 'DefaultEncryption':
                        reporting.writerow(['', '', object, account_statistic[bucket][object]['Encryption'],
                                            account_statistic[bucket][object]['ActionE'],
                                            account_statistic[bucket][object]['IsArchived'],
                                            account_statistic[bucket][object]['ActionR']])
            else:
                continue
        reporting.writerow(['']*7)
    print("File {0} with report created".format(reportfile))


def encrypt_object(target_bucket, object_key):
    try:
        s3.copy_object(CopySource={
                       'Bucket': target_bucket,
                       'Key': object_key
                       },
                       Bucket=target_bucket,
                       Key=object_key,
                       ServerSideEncryption='AES256')
        statistic[target_bucket][object_key]['ActionE'] = 'Encrypted'
        statistic[target_bucket][object_key]['Encryption'] = True
    except exceptions.ClientError:
        statistic[target_bucket][object_key]['ActionE'] = ''
        statistic[target_bucket][object_key]['Encryption'] = False
        print("Cant copy file {0}.".format(object_key))


def check_objects_enc(target_bucket):
    is_restored = False
    s3common = s3.list_objects(Bucket=target_bucket)
    if'Contents' in s3common:
        objects_list = paginate_over_bucket(target_bucket)
        for object_key in objects_list:
            statistic[target_bucket][object_key] = {}
            object_head = head_object(target_bucket,object_key)
            statistic[target_bucket][object_key]['Encryption'] = ''
            statistic[target_bucket][object_key]['IsArchived'] = False
            statistic[target_bucket][object_key]['ActionE'] = ''
            statistic[target_bucket][object_key]['ActionR'] = ''
            if not object_head:
                continue
            if 'StorageClass' in object_head and object_head['StorageClass'] == 'GLACIER':
                statistic[target_bucket][object_key]['IsArchived'] = True
                print("{0} archieved".format(object_key))
                restore_object(target_bucket, object_key)
                is_restored = True
                continue
        if is_restored:
            print("Wait for restoring objects...")
            time.sleep(10800)
        for object_key in objects_list:
            object_head = head_object(target_bucket, object_key)
            if not object_head:
                continue
            if 'ServerSideEncryption' in object_head:
                statistic[target_bucket][object_key]['Encryption'] = True
            else:
                encrypt_object(target_bucket, object_key)
    else:
        print("Bucket {0} is empty+".format(target_bucket))


def check_enc(target_bucket):
    print("Scanning {0} for non-encrypted objects".format(target_bucket))
    try:
        s3.get_bucket_encryption(Bucket=target_bucket)
        statistic[target_bucket]['DefaultEncryption'] = True
    except exceptions.ClientError:
        print("Bucket {0} has no encryption.".format(target_bucket))
        statistic[target_bucket]['DefaultEncryption'] = False
    check_objects_enc(target_bucket)


def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="FILENAME", help="Required.Path to file containing list of s3 buckets", type="str")
    parser.add_option("-c", "--creds", dest="PROFILE", help="Required.AWS Credentials Profile to use", type="str")
    parser.add_option("-r", "--report", dest="REPORTFILE", help="CSV file that will contain report.", type="str")
    (options, args) = parser.parse_args()
    if not options.FILENAME or not options.PROFILE:
        print("Required parameters FILENAME and PROFILE should be specified to run this script.")
        exit(1)
    list_of_buckets = retrive_list(options.FILENAME)
    global s3, reportfile, statistic
    if not options.REPORTFILE:
        current_date = datetime.datetime.now()
        reportfile = "{0}{1}-report.csv".format(current_date.strftime("%Y-%m-%d"), options.PROFILE)
    try:
        session = boto3.Session(profile_name=options.PROFILE)
        s3 = session.client('s3')
    except Exception:
        print("Something went wrong during session establishment.\n{0}".format(Exception))
        exit(1)
    statistic = {}
    for bucket in list_of_buckets:
        statistic[bucket] = {}
        try:
            s3.head_bucket(Bucket=bucket)
        except exceptions.ClientError:
            print("Wrong name of the bucket or bucket {0} doesn't exist.".format(bucket))
            statistic[bucket]['DefaultEncryption'] = "doesn't exist"
            continue
        check_enc(bucket)
    create_report(statistic)


if __name__ == "__main__":
    main()
