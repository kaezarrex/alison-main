import os

from flask import Flask, Markup, redirect, render_template, send_from_directory

from decorators import memorize
import portfolio


app = Flask(__name__, static_folder='deploy', template_folder='layout')


@memorize
def portfolio_handler(category, path):

    dropbox_path = os.path.join('/', category, path)

    if not portfolio.is_project(dropbox_path):
        return redirect('/' + category)

    projects = portfolio.projects(category)

    images = portfolio.image_urls(dropbox_path)
    description = portfolio.description_html(dropbox_path)
    description = Markup(description) if description is not None else None

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


@app.route('/gettingmarried/stationery/<path:path>')
def stationery_handler(path):
    return portfolio_handler('gettingmarried/stationery', path)


@app.route('/<path:path>')
def path_handler(path):
    return send_from_directory(app.static_folder, os.path.join(path, 'index.html'))
