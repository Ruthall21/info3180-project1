from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed

class PropertyForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    bedrooms = IntegerField('Bedrooms', validators=[DataRequired()])
    bathrooms = IntegerField('Bathrooms', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])

    property_type = SelectField(
        'Property Type',
        choices=[('House','House'), ('Apartment','Apartment')]
    )

    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])