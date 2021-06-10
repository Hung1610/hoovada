#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-part modules
import dateutil.parser
from flask import g
from flask_restx import marshal
from sqlalchemy import desc

# own modules
from app.constants import messages
from common.db import db
from app.modules.article.share.share_dto import ShareDto
from common.controllers.controller import Controller
from common.models import Article, ArticleShare, User
from common.utils.permission import has_permission
from common.utils.response import send_error, send_result
from common.utils.types import PermissionType

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class ShareController(Controller):

    def create(self, article_id, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        current_user = g.current_user
        if not has_permission(current_user.id, PermissionType.SHARE):
            return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

        data['user_id'] = current_user.id
        data['article_id'] = article_id
        data = self.add_org_data(data)
        try:
            share = self._parse_share(data=data)
            share.created_date = datetime.utcnow()
            db.session.add(share)
            db.session.commit()
            # update other values
            try:
                article = Article.query.filter_by(id=share.article_id).first()
                if not article:
                    return send_error(message=messages.ERR_NOT_FOUND)

                user_voted = User.query.filter_by(id=article.user_id).first()
                if not user_voted:
                    return send_error(message=messages.ERR_NOT_FOUND)

                user_voted.article_shared_count += 1
                if current_user:
                    share.user_id = current_user.id
                    current_user.article_share_count += 1
                db.session.commit()
            except Exception as e:
                pass

            return send_result()
            
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get(self, article_id, args):
        user_id, from_date, to_date, facebook, twitter, zalo = None, None, None, None, None, None

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
        try:
            query = ArticleShare.query
            if user_id is not None:
                data_role = self.get_role_data()
                if data_role['role'] == 'user':
                    query = query.filter(ArticleShare.user_id == user_id, ArticleShare.entity_type == data_role['role'])
                if data_role['role'] == 'organization':
                    query = query.filter(ArticleShare.organization_id == data_role['organization_id'], ArticleShare.entity_type == data_role['role'])
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
            shares = query.all()
            return send_result(data=marshal(shares, ShareDto.model_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))       


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))
        try:
            query = ArticleShare.query
            report = query.filter(ArticleShare.id == object_id).first()
            if report is None:
                return send_error(message=messages.ERR_NOT_FOUND)
            else:
                return send_result(data=marshal(report, ShareDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))   


    def update(self):
        pass


    def delete(self):
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
        if 'entity_type' in data:
            try:
                share.entity_type = data['entity_type']
            except Exception as e:
                print(e.__str__())
                pass

        if 'organization_id' in data:
            try:
                share.organization_id = int(data['organization_id'])
            except Exception as e:
                print(e.__str__())
                pass
        return share


    def get_share_by_user_id(self,args):

        try:
            query = ArticleShare.query
            if not isinstance(args, dict):
                return send_error(message='Could not parse the params.')

            user_id = None 
            if 'user_id' in args:
                try:
                    user_id = int(args['user_id'])
                except Exception as e:
                    print(e.__str__())
                    pass
            if user_id is None :
                return send_error(message='Provide params to search.')

            query = query.filter(ArticleShare.user_id == user_id)

            shares = query.order_by(desc(ArticleShare.created_date)).all()
            results = list()
            for share in shares:
                result = ArticleShare._asdict()

                # get user article
                article = Article.query.filter_by(id=ArticleShare.article_id).first()
                result['article'] = article

                results.append(result)
            return send_result(data=marshal(results, ShareDto.model_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))
