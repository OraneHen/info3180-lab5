"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import os
import json
from app import app, db
from flask import render_template, request, jsonify, send_file, make_response, send_from_directory
from werkzeug.utils import secure_filename
from app.models import Movies
from app.forms import MovieForm
from flask_wtf.csrf import generate_csrf


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/movies', methods=['POST', 'GET'])
def movies():
    if request.method == 'POST':
        form = MovieForm()
        
        if form.validate_on_submit():
            title = form.title.data
            response = {}
            description = form.description.data
            poster = form.poster.data.filename

            movie_new = Movies(title=title, description=description, poster=poster)
            db.session.add(movie_new)
            db.session.commit()

            path=os.getcwd() + '\\app\\static\\uploads\\' + str(movie_new.id)

            filename  = secure_filename(form.poster.data.filename)
            form.poster.data.save('uploads/'+ filename)
            movie_new.poster = '/api/v1/posters/' + filename
            db.session.commit()

            response['message'] = "File Uploaded Successfully"
            response['title'] = title
            response['poster'] = poster
            response['description'] = description

            return make_response(
                jsonify(response),
                200,
            )
        else:
            response = {} 
            response['errors'] = form_errors(form)

            return make_response(
                jsonify(response),
                400,
            )
    else:
        movies = Movies.query.all()
        response = {'movies':[],}
        for movie in movies:
            response['movies'].append({
                'id': movie.id,
                'title': movie.title,
                'description': movie.description, 
                'poster': movie.poster,
            })
        return make_response(
            jsonify(response),
            200,
        )

@app.route('/api/v1/posters/<filename>', methods=['GET'])
def get_poster(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)
    

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404