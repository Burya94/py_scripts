#!/bin/Python3

import boto3
from datetime import datetime
from optparse import OptionParser
from pytz import timezone
import csv
from botocore import exceptions

ACC_ID=''

def describe_snapshots():
    snapshots_ids = {}
    paginator = ec2.get_paginator('describe_snapshots')
    responce = paginator.paginate(
        Filters=[
            {
                'Name': 'status',
                'Values': [
                    'completed',
                ]
            }
        ],
        OwnerIds=[
            ACC_IDs,
        ]
    )
    for page in responce:
        for snapshot in page['Snapshots']:
            if date > snapshot['StartTime']:
                snapshots_ids[snapshot['SnapshotId']] = {}
                snapshots_ids[snapshot['SnapshotId']]['StartedTime'] = snapshot['StartTime']
                snapshots_ids[snapshot['SnapshotId']]['Description'] = snapshot['Description']
                snapshots_ids[snapshot['SnapshotId']]['Size'] = snapshot['VolumeSize']
    print(len(snapshots_ids))
    return snapshots_ids


def create_report(snapshots_dict, profile, region):
    with open('./{0}-{1}.csv'.format(profile, region), 'w') as csvf:
        report = csv.writer(csvf, delimiter=',')
        report.writerow(['SnapshotId',
                            'StartedTime',
                            'Description',
                            'Size'])
        for id in snapshots_dict.keys():
            print()
            report.writerow([id,
                             snapshots_dict[id]['StartedTime'],
                             snapshots_dict[id]['Description'],
                             snapshots_dict[id]['Size']
                         ])
    print("Report created in local directory.")


def delete_snapshot(snapshots_dict):
    list_of_used = []
    for id in snapshots_dict.keys():
        try:
            ec2.delete_snapshot(SnapshotId=id)
            print("{0} deleted".format(id))
        except(exceptions.ClientError):
            print("Can't delete {0}".format(id))
            list_of_used.append(id)
            continue
    print(list_of_used)



def main():
    parser = OptionParser()
    parser.add_option("-c", "--creds", dest="PROFILE", help="AWS credentials to be used", type=str)
    parser.add_option("-r", "--region", dest="REGION", help="AWS region", type=str)
    parser.add_option("-d", "--date", dest="DATE", help="ALL snapshots older that this date will be deleted.Example: 01-01-2016")
    (options, args) = parser.parse_args()
    if not options.PROFILE and not options.REGION:
        print("Not enough parameters to run this script.")
        exit(1)
    global ec2
    global date
    date = datetime.strptime(options.DATE, "%d-%m-%Y")
    date = date.replace(tzinfo=timezone('UTC'))
    session = boto3.Session(region_name=options.REGION, profile_name=options.PROFILE)
    ec2 = session.client('ec2')
    print("Searching for old snapshots...")
    old_snapshots = describe_snapshots()
    print("Deleting all old snapshots...")
    delete_snapshot(old_snapshots)
    ##
    ## update to handle snapshots that can't be deleted in report file
    print("Creating report...")
    create_report(old_snapshots, options.PROFILE, options.REGION)






if __name__ == "__main__":
    main()