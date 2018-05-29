#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import argparse
from redis import Redis

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from utils import vcap


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--redis-tag',
        dest='redis_tag',
        default=None
    )
    return parser.parse_args()


def main():
    args = parse_args()
    redis_creds = vcap.strip_redis_creds(
        vcap.creds('hsdp-redis-sentinel', tag=args.redis_tag))
    r = Redis(**redis_creds)
    r.flushall()
    print("Redis data flushed!")


if __name__ == '__main__':
    main()
