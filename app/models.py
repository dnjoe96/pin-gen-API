from app import db
from datetime import datetime


class Pin(db.Model):
    __tablename__ = 'generated_pin'

    s_n = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    pin = db.Column(db.String(140), unique=True, nullable=False)
    request_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, s_n, pin):
        self.s_n = s_n
        self.pin = pin

    def __repr__(self):
        return '<pin {}>'.format(self.pin)
