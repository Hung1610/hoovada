#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import enum

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class VotingStatusEnum(enum.Enum):
    NEUTRAL = 1
    UPVOTED = 2
    DOWNVOTED = 3


class ReportTypeEnum(enum.Enum):
    GENERAL = 1
    INAPPROPRIATE = 2
    DUPLICATE = 3


class BanTypeEnum(enum.Enum):
    EMAIL = 1
    PHONE_NUMBER = 2


class FileTypeEnum(enum.Enum):
    AUDIO = 1
    VIDEO = 2