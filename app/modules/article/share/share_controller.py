#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-part modules
import dateutil.parser
from flask_restx import marshal
from flask import request

# own modules
from app import db
from app.modules.common.controller import Controller
from app.modules.article import constants
from app.modules.article.article import Article
from app.modules.article.share.share import ArticleShare
from app.modules.article.share.share_dto import ShareDto
from app.modules.user.user import User
from app.utils.response import send_error, send_result
from app.modules.auth.auth_controller import AuthController


__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class ShareController(Controller):
    def get(self, article_id, args):
        user_id, from_date, to_date, facebook, twitter, zalo, anonymous = None, None, None, None, None, None, None

        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                pass
        if 'from_date' in args:
            try:
                from_date = dateutil.parser.isoparse(args['from_date'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'to_date' in args:
            try:
                to_date = dateutil.parser.isoparse(args['to_date'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'facebook' in args:
            try:
                facebook = bool(args['facebook'])
            except Exception as e:
                pass
        if 'twitter' in args:
            try:
                twitter = bool(args['twitter'])
            except Exception as e:
                pass
        if 'zalo' in args:
            try:
                zalo = bool(args['zalo'])
            except Exception as e:
                pass
        if 'anonymous' in args:
            try:
                anonymous = bool(args['anonymous'])
            except Exception as e:
                pass

        query = ArticleShare.query
        if user_id is not None:
            query = query.filter(ArticleShare.user_id == user_id)
        if article_id is not None:
            query = query.filter(ArticleShare.article_id == article_id)
        if from_date is not None:
            query = query.filter(ArticleShare.created_date >= from_date)
        if to_date is not None:
            query = query.filter(ArticleShare.created_date <= to_date)
        if facebook is not None:
            query = query.filter(ArticleShare.facebook == facebook)
        if twitter is not None:
            query = query.filter(ArticleShare.twitter == twitter)
        if zalo is not None:
            query = query.filter(ArticleShare.zalo == zalo)
        if anonymous is not None:
            query = query.filter(ArticleShare.anonymous == anonymous)
        shares = query.all()
        if len(shares) > 0:
            return send_result(data=marshal(shares, ShareDto.model_response), message='Success')
        else:
            return send_result(constants.msg_not_found)

    def create(self, article_id, data):
        if not isinstance(data, dict):
            return send_error(message=constants.msg_wrong_data_format)
        current_user, _ = AuthController.get_logged_user(request)

        data['user_id'] = current_user.id
        data['article_id'] = article_id
        try:
            share = self._parse_share(data=data)
            share.created_date = datetime.utcnow()
            db.session.add(share)
            db.session.commit()
            # update other values
            try:
                article = Article.query.filter_by(id=share.article_id).first()
                if not article:
                    return send_error(message=constants.msg_not_found)
                user_voted = User.query.filter_by(id=article.user_id).first()
                if not user_voted:
                    return send_error(message=constants.msg_not_found)
                user_voted.article_shared_count += 1
                if current_user:
                    share.user_id = current_user.id
                    current_user.article_share_count += 1
                db.session.commit()
            except Exception as e:
                pass
            return send_result(data=marshal(share, ShareDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=constants.msg_create_failed)

    def get_by_id(self, object_id):
        query = ArticleShare.query
        report = query.filter(ArticleShare.id == object_id).first()
        if report is None:
            return send_error(message=constants.msg_not_found)
        else:
            return send_result(data=marshal(report, ShareDto.model_response), message='Success')

    def update(self, object_id, data):
        pass

    def delete(self, object_id):
        pass

    def _parse_share(self, data):
        share = ArticleShare()
        if 'user_id' in data:
            try:
                share.user_id = int(data['user_id'])
            except Exception as e:
                pass
        if 'article_id' in data:
            try:
                share.article_id = int(data['article_id'])
            except Exception as e:
                pass
        if 'facebook' in data:
            try:
                share.facebook = bool(data['facebook'])
            except Exception as e:
                pass
        if 'twitter' in data:
            try:
                share.twitter = bool(data['twitter'])
            except Exception as e:
                pass
        if 'linkedin' in data:
            try:
                share.linkedin = bool(data['linkedin'])
            except Exception as e:
                pass
        if 'zalo' in data:
            try:
                share.zalo = bool(data['zalo'])
            except Exception as e:
                pass
        if 'vkontakte' in data:
            try:
                share.vkontakte = bool(data['vkontakte'])
            except Exception as e:
                pass
        if 'anonymous' in data:
            try:
                share.anonymous = bool(data['anonymous'])
            except Exception as e:
                pass
        if 'mail' in data:
            try:
                share.mail = bool(data['mail'])
            except Exception as e:
                pass
        if 'link_copied' in data:
            try:
                share.link_copied = bool(data['link_copied'])
            except Exception as e:
                pass
        return share
