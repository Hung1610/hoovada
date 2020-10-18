#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


# # Create Messages
msg_create_success = 'Entry created successful.'
msg_create_success_without_topics = 'Entry created partially successful(no topics for article).'
msg_article_already_exists = 'Bạn đã tạo bài viết với chủ đề {} từ trước.'
msg_create_failed = 'Failed to create entry'

# # Get Messages
msg_get_all_failed = 'Không thể lấy bài viết. Vui lòng liên hệ admin để khắc phục.'
msg_lacking_id = 'Vui lòng cung cấp ID bài viết!'

# # Get Single/Update Messages
msg_update_failed_insensitive_title = 'Không thể sửa bài viết vì nhan đề mới của bạn không hợp lệ.'
msg_update_failed_insensitive_body = 'Không thể sửa câu hỏi vì nội dung mới của bạn không hợp lệ.'
msg_update_success = 'Cập nhật bài viết thành công.'
msg_update_failed = 'Cập nhật bài viết thất bại.'

# # Delete Messages
msg_delete_success_with_id = 'Bài viết với ID {} đã được xóa thành công.'
msg_delete_failed_with_id = 'Không thể xóa bài viết với ID {}'

# # General Errors
msg_wrong_data_format = 'Dữ liệu không đúng định dạng, vui lòng kiểm tra lại!'
msg_lacking_query_params = 'Query parameters not provided.'
msg_not_found = 'Entry not found'
msg_not_found_with_id = 'Entry not found with ID: {}'
msg_search_failed = 'Tìm kiếm thất bại. Vui lòng xem lại dữ liệu.'
msg_must_contain_title = 'Bài viết phải chứa nhan đề.'
msg_must_contain_fixed_topic_id = 'Bài viết phải chứa lĩnh vực.'
msg_must_contain_topics_id = 'Bài viết phải chứa chủ đề.'
msg_insensitive_title = 'Nhan đề bài viết của bạn không hợp lệ.'
msg_insensitive_body = 'Nội dung câu hỏi của bạn không hợp lệ.'