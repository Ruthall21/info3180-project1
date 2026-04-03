
""" Flask Documentation: https://flask.palletsprojects.com/ Jinja2 
    Documentation: https://jinja.palletsprojects.com/ Werkzeug 
    Documentation: https://werkzeug.palletsprojects.com/ 
    This file contains the routes for your application. """

from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.forms import PropertyForm
from app.models import Property
from werkzeug.utils import secure_filename
import os

# Home / About
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html', name="Ruth-Ann Allen")

# -----------------------
# PROPERTY ROUTES
# -----------------------

# CREATE PROPERTY
@app.route('/properties/create', methods=['GET', 'POST'])
def create_property():
    form = PropertyForm()

    if form.validate_on_submit():
        photo = form.photo.data
        filename = secure_filename(photo.filename)

        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(upload_path)

        new_property = Property(
            title=form.title.data,
            description=form.description.data,
            bedrooms=form.bedrooms.data,
            bathrooms=form.bathrooms.data,
            location=form.location.data,
            price=form.price.data,
            property_type=form.property_type.data,
            photo=filename
        )

        db.session.add(new_property)
        db.session.commit()

        flash("Property successfully added!", "success")
        return redirect(url_for('properties'))

    if request.method == 'POST':
        flash_errors(form)

    return render_template('add_property.html', form=form)

# LIST ALL PROPERTIES
@app.route('/properties')
def properties():
    properties = Property.query.all()
    return render_template('properties.html', properties=properties)

# VIEW SINGLE PROPERTY
@app.route('/properties/<int:propertyid>')
def property_detail(propertyid):
    property = Property.query.get_or_404(propertyid)
    return render_template('view_property.html', property=property)

# -----------------------
# HELPERS
# -----------------------

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in the {getattr(form, field).label.text} field - {error}", 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    return app.send_static_file(file_name + '.txt')

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404