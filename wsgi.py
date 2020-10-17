#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
from app import create_app

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

app = create_app('dev')

if __name__ == "__main__":
    app.run()