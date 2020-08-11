#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
import argparse

# own modules
from app import create_app

__version__ = "1.0.0"
__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


def parse_args():
    parser = argparse.ArgumentParser( description='Arguments parsing for hoovada.')
    group = parser.add_argument_group('Arguments')

    group.add_argument('-m', '--mode', default='dev', required=False, type=str, help='dev for development and prod for production')
    group.add_argument('-i', '--ip', default='0.0.0.0', required=False, type=str, help='The IP address')
    group.add_argument('-p', '--port', default='5000', required=False, type=str, help='The port to run app')
    arguments = parser.parse_args()
    return arguments

if __name__ == '__main__':
    args = parse_args()
    debug = True if args.mode == 'dev' else False
    app = create_app(args.mode)    
    app.run(debug=debug, host=args.ip, port=args.port)
