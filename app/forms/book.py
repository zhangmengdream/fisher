from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, AnyOf


class SearchForm(Form):
    q = StringField()
    page = IntegerField(default=1)



