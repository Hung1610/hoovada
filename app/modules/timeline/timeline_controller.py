#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
import dateutil.parser
from flask import current_app, request
from flask_restx import marshal

# own modules 
from common.db import db
from app.modules.timeline.timeline_dto import TimelineDto
from common.enum import TimelineActivityEnum
from common.utils.response import paginated_result
from common.controllers.controller import Controller
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


Timeline = db.get_model('Timeline')


class TimelineController(Controller):
    query_classname = 'Timeline'
    allowed_ordering_fields = ['activity_date']
    
    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary form")
        
        if not 'activity' in data:
            return send_error(message='Must contain at least the activity type.')

        current_user, _ = current_app.get_logged_user(request)
        data['user_id'] = current_user.id

        try:
            timeline = self._parse_timeline(data=data, timeline=None)
            db.session.add(timeline)
            db.session.commit()
            return send_result(message='Timeline was created successfully.', data=marshal(timeline, TimelineDto.timeline_model_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message='Could not create timeline. Contact administrator for solution.')


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error("Timeline ID is null")
        timeline = Timeline.query.filter_by(id=object_id).first()
        if timeline is None:
            return send_error(message='Could not find timeline with the ID {}'.format(object_id))

        return send_result(data=marshal(timeline, TimelineDto.timeline_model_response), message='Success')


    def apply_filtering(self, query, params):
        query = super().apply_filtering(query, params)
        if params.get('from_date'):
            query = query.filter(Timeline.activity_date >= dateutil.parser.isoparse(params.get('from_date')))
        if params.get('to_date'):
            query = query.filter(Timeline.activity_date <= dateutil.parser.isoparse(params.get('to_date')))
        return query


    def get(self, args):
        try:
            query = self.get_query_results(args)
            res, code = paginated_result(query)
            timelines = res.get('data')
            results = []
            for timeline in timelines:
                result = timeline._asdict()
                result['user'] = timeline.user
                results.append(result)
            res['data'] = marshal(results, TimelineDto.timeline_model_response)
            return res, code
        except Exception as e:
            print(e.__str__())
            return send_error("Could not load timelines. Contact your administrator for solution.")


    def update(self):
        pass


    def delete(self, object_id):
        try:
            if object_id is None:
                return send_error("Timeline ID is null")
            timeline = Timeline.query.filter_by(id=object_id).first()
            if timeline is None:
                return send_error(message='Could not find timeline with the ID {}'.format(object_id))
            db.session.delete(timeline)
            db.session.commit()
            return send_result(message='Timeline deletion successful.')
        except Exception as e:
            print(e)
            return send_error(message='Timeline deletion failed.')


    def _parse_timeline(self, data, timeline=None):
        if timeline is None:
            timeline = Timeline()
        if 'user_id' in data:
            try:
                timeline.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'question_id' in data:
             try:
                timeline.question_id = int(data['question_id'])
             except Exception as e:
                print(e.__str__())
                pass
        if 'answer_id' in data:
             try:
                timeline.answer_id = int(data['answer_id'])
             except Exception as e:
                print(e.__str__())
                pass
        if 'article_id' in data:
             try:
                timeline.article_id = int(data['article_id'])
             except Exception as e:
                print(e.__str__())
                pass
        if 'activity' in data:
            try:
                activity = int(data['activity'])
                timeline.activity = TimelineActivityEnum(activity).name
            except Exception as e:
                print(e.__str__())
                pass
        return timeline