from app import db
from common.models.model import Model


class RequestLog(Model):
    __tablename__ = 'request_log'

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(500))
    country_short = db.Column(db.String(500))
    country_long = db.Column(db.String(500))
    region = db.Column(db.String(500))
    city = db.Column(db.String(500))
    isp = db.Column(db.String(500))
    latitude = db.Column(db.String(500))
    longtitude = db.Column(db.String(500))
    domain = db.Column(db.String(500))
    zipcode = db.Column(db.String(500))
    timezone = db.Column(db.String(500))
    netspeed = db.Column(db.String(500))
    idd_code = db.Column(db.String(500))
    area_code = db.Column(db.String(500))
    weather_code = db.Column(db.String(500))
    weather_name = db.Column(db.String(500))
    mcc = db.Column(db.String(500))
    mnc = db.Column(db.String(500))
    mobile_brand = db.Column(db.String(500))
    elevation = db.Column(db.String(500))
    usage_type = db.Column(db.String(500))
    access_date = db.Column(db.Date)
    access_time = db.Column(db.Time)
    request_url = db.Column(db.String(500))
    referrer = db.Column(db.String(500))
