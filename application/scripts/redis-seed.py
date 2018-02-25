#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import argparse
from uuid import uuid4
from random_words import LoremIpsum
import redis

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from utils.vcap_creds import get_creds


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
    redis_creds = get_creds('hsdp-redis-sentinel', tag=args.redis_tag)
    r = redis.Redis(**redis_creds)
    li = LoremIpsum()
    sentences = [li.get_sentences(10) for i in xrange(100)]
    for sentence in sentences:
        r.set(str(uuid4()), sentence)
    print("Added 100 records to redis.")


if __name__ == '__main__':
    main()
