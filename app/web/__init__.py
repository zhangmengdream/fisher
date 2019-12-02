from flask import Blueprint

web= Blueprint('web',__name__)

from app.web import book
from app.web import gift
from app.web import auth



