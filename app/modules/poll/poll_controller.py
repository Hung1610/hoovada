#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import g
from flask_restx import marshal

# own modules
from common.db import db
from common.utils.response import send_error, send_result, paginated_result
from common.controllers.controller import Controller
from app.constants import messages
from slugify import slugify
from app.modules.poll.poll_dto import PollDto
from common.dramatiq_producers import update_seen_poll
from common.es import get_model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


PollBookmark = db.get_model('PollBookmark')
Poll = db.get_model('Poll')
PollTopic = db.get_model('PollTopic')
PollSelect = db.get_model('PollSelect')
PollUserSelect = db.get_model('PollUserSelect')
User = db.get_model('User')
Topic = db.get_model('Topic')
ESPoll = get_model('Poll')


class PollController(Controller):
    query_classname = 'Poll'

    def create(self, data):
        print(data)
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'title' in data or data['title'] == '':
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll title'))
        
        if not 'allow_multiple_user_select' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll allow_multiple_user_select'))

        if not 'expire_after_seconds' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll expire_after_seconds'))
        
        if not 'fixed_topic_id' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll fixed_topic_id'))
        fixed_topic = Topic.query.filter_by(id=data['fixed_topic_id']).first()
        
        if (not fixed_topic) or (fixed_topic and fixed_topic.is_fixed != 1):
            return send_error(message=messages.ERR_ISSUE.format('Fixed topic is not found or not fixed'))
        
        if not 'poll_selects' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll poll_selects'))
        
        if not isinstance(data['poll_selects'], list):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not isinstance(data['poll_topics'], list):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        poll_topics = data['poll_topics']

        if len(data['poll_selects']) < 2:
            return send_error(message=messages.ERR_ISSUE.format('Poll must have minimum 2 selections'))

        current_user = g.current_user
        data['user_id'] = current_user.id
        
        data['title'] = data['title'].strip().capitalize()
        poll = Poll.query.filter(Poll.title == data['title']).first()
        if poll is not None:
            return send_error(message=messages.ERR_ALREADY_EXISTS)    

        poll = self._parse_poll(data=data, poll=None)     
        try:
            poll.created_date = datetime.utcnow()
            poll.updated_date = datetime.utcnow()
            poll.is_expire = False
            poll.slug = slugify(poll.title)
            db.session.add(poll)
            db.session.flush()

            for poll_select_content in data['poll_selects']:
                poll_select = PollSelect()
                poll_select.content = poll_select_content
                poll_select.poll_id = poll.id
                poll_select.user_id = current_user.id
                db.session.add(poll_select)
    
            for topic_id in data['poll_topics']:
                poll_topic = PollTopic()
                poll_topic.topic_id = int(topic_id)
                poll_topic.poll_id = poll.id
                db.session.add(poll_topic)
            # index to ES server
            poll_dsl = ESPoll(_id=poll.id, title=poll.title, user_id=poll.user_id, created_date=poll.created_date, updated_date=poll.updated_date)
            poll_dsl.save()

            # Author automatically bookmark the poll
            poll_bookmark = PollBookmark()
            print(poll_bookmark)
            poll_bookmark.user_id = current_user.id
            poll_bookmark.poll_id = poll.id
            db.session.add(poll_bookmark)

            db.session.commit()
            result = poll._asdict()

            result['is_upvoted_by_me'] =  False
            result['is_downvoted_by_me'] =  False
            result['is_bookmarked_by_me'] = True

            update_seen_poll.send(current_user.id, poll.id)
            return send_result(message=messages.MSG_CREATE_SUCCESS, data=marshal(result, PollDto.model_response))

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get(self, args):
        try:
            current_user = g.current_user
            query = self.get_query_results(args)
            res, code = paginated_result(query)
            results = []
            if res['data'] is not None:
                for poll in res['data']:
                    if poll:
                        results.append(poll_dict)

            res['data'] = marshal(results, PollDto.model_response)
            return res, code
        
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(messages.ERR_PLEASE_PROVIDE.format("id"))
        
        try:
            if object_id.isdigit():
                poll = Poll.query.filter_by(id=object_id).first()
            else:
                poll = Poll.query.filter_by(slug=object_id).first()

            current_user = g.current_user
            if poll is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            result = poll._asdict()
            result['user'] = poll.user
            result['topics'] = poll.topics
            result['fixed_topic'] = poll.fixed_topic
            result['poll_selects'] = poll.poll_selects
            update_seen_poll.send(current_user.id, poll.id)
            return send_result(data=marshal(result, PollDto.model_response), message=messages.MSG_GET_SUCCESS)

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def update(self, object_id, data):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format("id"))

        if data is None or not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        poll = Poll.query.filter_by(id=object_id).first()
        if poll is None:
            return send_error(message=messages.ERR_NOT_FOUND)

        current_user = g.current_user
        if poll.user_id != current_user.id:
            return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

        if 'title' in data:
            data['title'] = data['title'].strip().capitalize()
            
        poll = self._parse_poll(data=data, poll=poll)
        try:
            poll.updated_date = datetime.utcnow()
            db.session.commit()
            result = poll._asdict()
            return send_result(message=messages.MSG_UPDATE_SUCCESS, data=marshal(result, PollDto.model_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))


    def delete(self, object_id):
        
        if object_id.isdigit():
            poll = Poll.query.filter_by(id=object_id).first()
        else:
            poll = Poll.query.filter_by(slug=object_id).first()

        if poll is None:
            return send_error(message=messages.ERR_NOT_FOUND)

        current_user = g.current_user
        if poll.user_id != current_user.id:
            return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

        try:
            db.session.delete(poll)
            db.session.commit()
            return send_result(message=messages.MSG_DELETE_SUCCESS)
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


    def _parse_poll(self, data, poll=None):
        if poll is None:
            poll = Poll()

        if 'title' in data:
            try:
                poll.title = data['title'].capitalize()
            except Exception as e:
                print(e.__str__())
                pass

        if 'allow_multiple_user_select' in data:
            try:
                poll.allow_multiple_user_select = bool(data['allow_multiple_user_select'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'user_id' in data:
            try:
                poll.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'fixed_topic_id' in data:
            try:
                poll.fixed_topic_id = int(data['fixed_topic_id'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'expire_after_seconds' in data:
            try:
                poll.expire_after_seconds = data['expire_after_seconds']
            except Exception as e:
                print(e.__str__())
                pass

        if 'is_anonymous' in data:
            try:
                poll.is_anonymous = bool(data['is_anonymous'])
            except Exception as e:
                print(e.__str__())
                pass

        if g.current_user_is_admin:
            if 'allow_voting' in data:
                try:
                    poll.allow_voting = bool(data['allow_voting'])
                except Exception as e:
                    print(e.__str__())
                    pass

        if g.current_user_is_admin:
            if 'allow_comments' in data:
                try:
                    poll.allow_comments = bool(data['allow_comments'])
                except Exception as e:
                    print(e.__str__())
                    pass
        return poll