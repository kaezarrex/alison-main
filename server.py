import os

from flask import Flask, Markup, render_template, send_from_directory
import redis

import portfolio


ROOT_PATH = 'index.html'

app = Flask(__name__, static_folder='deploy', template_folder='layout')
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis = redis.from_url(redis_url)


# @app.route('/')
# def root_handler():
#     return send_from_directory(app.static_folder, ROOT_PATH)


def portfolio_handler(category, path):
    full_path = os.path.join('/', category, path)
    projects = portfolio.projects(category)
    images = portfolio.image_urls(full_path)
    description = Markup(portfolio.description_html(full_path))
    return render_template('portfolio.j2', category=category,
                           projects=projects, images=images,
                           description=description)


@app.route('/')
def index_handler():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/media/<path:path>')
def media_handler(path):
    return send_from_directory(app.static_folder, os.path.join('media', path))


@app.route('/work/<path:path>')
def work_handler(path):
    return portfolio_handler('work', path)


@app.route('/<path:path>')
def path_handler(path):
    return send_from_directory(app.static_folder, os.path.join(path, 'index.html'))
