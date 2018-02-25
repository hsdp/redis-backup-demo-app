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

from utils.vcap_creds import get_creds


def redis_restore(redis_creds, tempfile):
    with open(tempfile, 'r') as f:
        redisdl.load(
            f,
            host=redis_creds['host'],
            password=redis_creds['password'],
        )


def copy_from_s3(s3_creds, s3_key, tempfile):
    session = Session(
        aws_access_key_id=s3_creds['api_key'],
        aws_secret_access_key=s3_creds['secret_key']
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket(s3_creds['bucket'])
    bucket.download_file(s3_key, tempfile)


def remove_file(tempfile):
    if os.path.exists(tempfile):
        os.remove(tempfile)


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
        '--tempfile',
        dest='tempfile',
        default='/tmp/redis.bak'
    )
    parser.add_argument(
        '-k',
        '--s3-key',
        dest='s3_key',
        default='redis.bak'
    )
    return parser.parse_args()


def main():
    args = parse_args()
    bucket_creds = get_creds('hsdp-s3', tag=args.s3_tag)
    redis_creds = get_creds('hsdp-redis-sentinel', tag=args.redis_tag)
    copy_from_s3(bucket_creds, args.s3_key, args.tempfile)
    redis_restore(redis_creds, args.tempfile)
    remove_file(args.tempfile)
    print("Redis restore complete.")


if __name__ == '__main__':
    main()
