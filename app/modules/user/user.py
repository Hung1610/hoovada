from datetime import datetime

from flask import url_for
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

from app.modules.common.model import Model
from app import db
from app.utils.hoovada_utils import remove_markdown, convert_markdown


class SignUpUser(Model):
    '''
    Define the SignUpUser Model.
    '''
    __tablename__ = 'sign_user'

    signup_user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password_hash = db.Column(db.String)
    registered_date = db.Column(db.Date)
    registered_time = db.Column(db.Time)
    activation_code = db.Column(db.String)
    code_created_date = db.Column(db.Date)
    code_created_time = db.Column(db.Time)
    code_duration_time = db.Column(db.Float)
    code_sent_date = db.Column(db.Date)
    code_sent_time = db.Column(db.Time)
    trial_number = db.Column(db.Integer)
    confirm = db.Column(db.Boolean)


class RecoveryUser(Model):
    '''
    Define the RecoveryUser model.
    '''
    __tablename__ = 'recovery_user'

    recovery_user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    new_password_hash = db.Column(db.String)
    required_date = db.Column(db.Date)
    required_time = db.Column(db.Time)
    recovery_code = db.Column(db.String)
    code_created_date = db.Column(db.Date)
    code_created_time = db.Column(db.Time)
    code_duration_time = db.Column(db.Float)
    code_sent_date = db.Column(db.Date)
    code_sent_time = db.Column(db.Time)
    trial_number = db.Column(db.Integer)
    continued = db.Column(db.Boolean)
    session_start_date = db.Column(db.Date)
    session_start_time = db.Column(db.Time)
    session_duration = db.Column(db.Float)
    recovered = db.Column(db.Boolean)


class User(Model):
    """
    Define the User model.
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(128), unique=True)
    title = db.Column(db.String(10))

    first_name = db.Column(db.String(128))
    middle_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))

    gender = db.Column(db.String(10))
    age = db.Column(db.String(3))
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(128), default='')

    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    email_confirmed_at = db.Column(db.DateTime(), nullable=True)

    profile_pic_url = db.Column(db.String(255))
    profile_pic_data_url = db.Column(db.String(10000))
    admin = db.Column(db.Boolean(), default=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)

    reputation = db.Column(db.Integer, default=0)
    profile_views = db.Column(db.Integer, default=0)
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    website_url = db.Column(db.String(200))

    # about_me = db.Column(db.String(3000))
    _about_me = db.Column(db.Text)
    _about_me_markdown = db.Column(db.Text)
    _about_me_html = db.Column(db.Text)

    people_reached = db.Column(db.Integer, default=0)
    job_role = db.Column(db.String(255))
    company = db.Column(db.String(255))
    # Settings
    show_email_publicly_setting = db.Column(db.Boolean, nullable=False, default=False)
    hoovada_digests_setting = db.Column(db.Boolean, nullable=False, default=True)
    hoovada_digests_frequency_setting = db.Column(db.String(6), nullable=False, default='weekly')

    questions_you_asked_or_followed_setting = db.Column(db.Boolean, nullable=False, default=True)
    questions_you_asked_or_followed_frequency_setting = db.Column(db.String(6), nullable=False, default='weekly')
    people_you_follow_setting = db.Column(db.Boolean, nullable=False, default=True)

    people_you_follow_frequency_setting = db.Column(db.String(6), nullable=False, default='weekly')
    email_stories_topics_setting = db.Column(db.Boolean, nullable=False, default=True)
    email_stories_topics_frequency_setting = db.Column(db.String(6), nullable=False, default='weekly')

    @hybrid_property
    def about_me(self):
        """Return the value of _about_me but the html version."""
        return self._about_me_html

    @about_me.setter
    def about_me(self, markdown):
        """Constrain markdown with html so html is never set directly"""
        self._about_me = remove_markdown(markdown)
        self._about_me_markdown = markdown
        self._about_me_html = convert_markdown(markdown)

    @hybrid_property
    def about_me_markdown(self):
        """Return the value of _markdown."""
        return self._about_me_markdown

    @hybrid_property
    def about_me_html(self):
        """Return the value of _html."""
        return self._about_me_html

    # _topics = db.relationship(
    #     'Topic',
    #     secondary=user_topics,
    #     lazy='subquery',
    #     backref=db.backref('users_topics', lazy=True)
    # )

    # @hybrid_property
    # def followed_questions(self):
    #     """Return the value of _followed_questions."""
    #     return self._followed_questions
    #
    # @topics.setter
    # def followed_questions(self, question):
    #     """Associate questions with this entry."""
    #     self._followed_questions.append(question)

    @hybrid_property
    def topics(self):
        """Return the value of _topics."""
        return self._topics

    # @topics.setter
    # def topics(self, topiclist):
    #     """Associate topics with this entry. The topiclist is expected to be
    #     already normalized without duplicates."""
    #     for topic_name in topiclist:
    #         self._topics.append(Topic.get_or_create(topic_name))
    #
    # @property
    # def tagged_questions(self):
    #     tagged_questions = Question.query.join(user_topics, (user_topics.c.topic_id == Question.user_id)).filter(
    #         user_topics.c.user_id == self.id).order_by(Question.created_at.desc())
    #     # own = Question.query.filter_by(user_id=self.id)
    #     return tagged_questions

    @property
    def current_user_topics(self):
        return self.topics + self.assigned_topics

    def get_topicstring(self):
        """Return the topics for this instance as a comma separated string"""
        return ', '.join([topic.name for topic in self.topics])

    # messages_sent = db.relationship(
    #     'Message',
    #     foreign_keys='Message.sender_id',
    #     backref='sender',
    #     lazy='dynamic'
    # )
    # messages_received = db.relationship(
    #     'Message',
    #     foreign_keys='Message.recipient_id',
    #     backref='recipient',
    #     lazy='dynamic'
    # )
    # last_message_read_time = db.Column(db.DateTime)

    # def new_messages_count(self):
    #     last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
    #     return Message.query.filter_by(
    #         recipient=self
    #     ).filter(
    #         Message.sent_time > last_read_time
    #     ).count()

    # # last_notification_read_time = db.Column(db.DateTime)
    # notifications = db.relationship(
    #     'Notification',
    #     backref='user',
    #     lazy='dynamic'
    # )
    # email_addresses = db.relationship(
    #     'EmailAddresses',
    #     backref='user',
    #     lazy='dynamic'
    # )

    # def add_notification(self, name, data):
    #     self.notifications.filter_by(name=name).delete()
    #     n = Notification(name=name, payload_json=json.dumps(data), user=self)
    #     db.session.add(n)
    #     return n

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def avatar(self):
        if self.profile_pic_url:
            return self.profile_pic_url
        if self.profile_pic_data_url:
            return self.profile_pic_data_url
        else:
            return url_for('static', filename='img/pro-pic.png', _scheme='https', _external=True)

    @property
    def is_admin(self):
        if self.admin:
            return True
        else:
            return False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    # def is_following(self, user):
    #     return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    # def followed_questions(self):
    #     followed = Question.query.join(
    #         followers, (followers.c.followed_id == Question.user_id)
    #     ).filter(
    #         followers.c.follower_id == self.id
    #     )
    #     own = Question.query.filter_by(user_id=self.id)
    #     return followed.union(own).order_by(Question.created_at.desc())

    @property
    def name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return f'{self.display_name}'

    @property
    def email_confirmed(self):
        if self.confirmed:
            return True
        else:
            return False

    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address
        return address

    class Meta:
        order_by = ('-joined_date')

    def __repr__(self):
        return (
            f'User [ID: {self.id}]\nName: {self.display_name}\nEmail: {self.email}'
        )

    def __eq__(self, other):
        if isinstance(other, User):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal
