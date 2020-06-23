from app import db
from app.modules.common.model import Model


class RequestLog(Model):
    __tablename__ = 'request_log'

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String)
    country_short = db.Column(db.String)
    country_long = db.Column(db.String)
    region = db.Column(db.String)
    city = db.Column(db.String)
    isp = db.Column(db.String)
    latitude = db.Column(db.String)
    longtitude = db.Column(db.String)
    domain = db.Column(db.String)
    zipcode = db.Column(db.String)
    timezone = db.Column(db.String)
    netspeed = db.Column(db.String)
    idd_code = db.Column(db.String)
    area_code = db.Column(db.String)
    weather_code = db.Column(db.String)
    weather_name = db.Column(db.String)
    mcc = db.Column(db.String)
    mnc = db.Column(db.String)
    mobile_brand = db.Column(db.String)
    elevation = db.Column(db.String)
    usage_type = db.Column(db.String)
    access_date = db.Column(db.Date)
    access_time = db.Column(db.Time)
    request_url = db.Column(db.String)
    referrer = db.Column(db.String)
