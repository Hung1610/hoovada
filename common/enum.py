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


class TimelineActivityEnum(enum.Enum):
    FIRST_COMMENT = 1
    FIRST_UPVOTE = 2
    FIRST_SHARE = 3
    HUNDREDTH_COMMENT = 4
    HUNDREDTH_UPVOTE = 5
    HUNDREDTH_SHARE = 6

class FrequencySettingEnum(enum.Enum):
    weekly = 1
    daily = 2


class OrganizationStatusEnum(enum.Enum):
    submitted = 1
    approved = 2
    rejected = 3
    deactivated = 4

class OrganizationUserStatusEnum(enum.Enum):
    submitted = 1
    approved = 2
    rejected = 3
    deactivated = 4

class EntityTypeEnum(enum.Enum):
    user = 1
    organization = 2