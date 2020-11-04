#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
import dateutil.parser
from flask import current_app, request
from flask_restx import marshal
from sqlalchemy import desc

# own modules 
from app.app import db
from app.modules.q_a.timeline.timeline import Timeline, TimelineActivity
from app.modules.q_a.timeline.timeline_dto import TimelineDto
from common.controllers.controller import Controller
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class TimelineController(Controller):
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
            return send_result(message='Timeline was created successfully.',
                                       data=marshal(timeline, TimelineDto.timeline_model_response))
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

    def get(self, args):
        """ Search timeline.
        """
        query = Timeline.query
        current_user, _ = current_app.get_logged_user(request)

        if not isinstance(args, dict):
            return send_error(message='Could not parse the params.')
        user_id, question_id, answer_id, comment_id, article_id, article_comment_id, from_date, to_date = None, None, None, None, None, None, None, None
        if args.get('user_id'):
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if args.get('question_id'):
            try:
                question_id = int(args['question_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if args.get('answer_id'):
            try:
                answer_id = int(args['answer_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if args.get('comment_id'):
            try:
                comment_id = int(args['comment_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if args.get('article_id'):
            try:
                article_id = int(args['article_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if args.get('article_comment_id'):
            try:
                article_comment_id = int(args['article_comment_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if args.get('from_date'):
            try:
                from_date = dateutil.parser.isoparse(args['from_date'])
            except Exception as e:
                print(e.__str__())
                pass
        if args.get('to_date'):
            try:
                to_date = dateutil.parser.isoparse(args['to_date'])
            except Exception as e:
                print(e.__str__())
                pass

        query = query.filter(Timeline.answer_id == answer_id)
        query = query.filter(Timeline.question_id == question_id)
        query = query.filter(Timeline.article_id == article_id)
        if comment_id is not None:
            query = query.filter(Timeline.comment_id == comment_id)
        if article_comment_id is not None:
            query = query.filter(Timeline.article_comment_id == article_comment_id)
        if user_id is not None:
            query = query.filter(Timeline.user_id == user_id)
        if from_date is not None:
            query = query.filter(Timeline.activity_date >= from_date)
        if to_date is not None:
            query = query.filter(Timeline.activity_date <= to_date)

        timelines = query.order_by(desc(Timeline.activity_date)).all()
        if timelines is not None and len(timelines) > 0:
            results = list()
            for timeline in timelines:
                result = timeline._asdict()
                result['user'] = timeline.user
                results.append(result)
            return send_result(marshal(results, TimelineDto.timeline_model_response), message='Success')
        else:
            return send_error(message='Could not find timelines. Please check your parameters again.')

    def update(self, object_id, data, is_put=False):
        try:
            if object_id is None:
                return send_error("Timeline ID is null")
            timeline = Timeline.query.filter_by(id=object_id).first()
            if timeline is None:
                return send_error(message='Could not find timeline with the ID {}'.format(object_id))
            if is_put:
                db.session.delete(timeline)
                return self.create(data)
            timeline = self._parse_timeline(data=data, timeline=timeline)
            db.session.commit()
            return send_result(message='Timeline was created successfully.',
                                       data=marshal(timeline, TimelineDto.timeline_model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could update timeline. Please check your parameters again.')

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
        if 'timeline_id' in data:
             try:
                timeline.timeline_id = int(data['timeline_id'])
             except Exception as e:
                print(e.__str__())
                pass
        if 'answer_id' in data:
             try:
                timeline.answer_id = int(data['answer_id'])
             except Exception as e:
                print(e.__str__())
                pass
        if 'comment_id' in data:
             try:
                timeline.comment_id = int(data['comment_id'])
             except Exception as e:
                print(e.__str__())
                pass
        if 'article_id' in data:
             try:
                timeline.article_id = int(data['article_id'])
             except Exception as e:
                print(e.__str__())
                pass
        if 'article_comment_id' in data:
             try:
                timeline.article_comment_id = int(data['article_comment_id'])
             except Exception as e:
                print(e.__str__())
                pass
        if 'activity' in data:
            try:
                activity = int(data['activity'])
                timeline.activity = TimelineActivity(activity).name
            except Exception as e:
                print(e.__str__())
                pass
        return timeline