#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import argparse
import boto3
import redisdl
from boto3.session import Session

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from utils import vcap


def backup_redis(redis_creds, outfile):
    with open(outfile, 'w') as f:
        redisdl.dump(
            f,
            host=redis_creds['host'],
            password=redis_creds['password'],
        )


def copy_to_s3(s3_creds, outfile, s3_key):
    session = Session(
        aws_access_key_id=s3_creds['api_key'],
        aws_secret_access_key=s3_creds['secret_key']
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket(s3_creds['bucket'])
    data = open(outfile, 'rb')
    bucket.put_object(Key=s3_key, Body=data)


def remove_file(outfile):
    if os.path.exists(outfile):
        os.remove(outfile)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--s3-tag',
        dest='s3_tag',
        default=None
    )
    parser.add_argument(
        '--redis-tag',
        dest='redis_tag',
        default=None
    )
    parser.add_argument(
        '-f',
        '--outfile',
        dest='outfile',
        default='/tmp/redis.bak'
    )
    parser.add_argument(
        '-s',
        '--s3-key',
        dest='s3_key',
        default='redis.bak'
    )

    return parser.parse_args()


def main():
    args = parse_args()
    bucket_creds = vcap.creds('hsdp-s3', tag=args.s3_tag)
    redis_creds = vcap.strip_redis_creds(
        vcap.creds('hsdp-redis-sentinel', tag=args.redis_tag))
    backup_redis(redis_creds, args.outfile)
    copy_to_s3(bucket_creds, args.outfile, args.s3_key)
    remove_file(args.outfile)
    print("Redis backup complete.")


if __name__ == '__main__':
    main()
