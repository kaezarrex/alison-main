import os

from flask import Flask, Markup, redirect, render_template, send_from_directory

from decorators import memorize
import portfolio


app = Flask(__name__, static_folder='deploy', template_folder='layout')


class Resource():

    class Meta():
        category = None

    meta = Meta()

    def __init__(self, category=None):
        self.meta.category = category


@memorize
def portfolio_index_data(category):
    return portfolio.projects(category)


def portfolio_index_handler(category):
    projects = portfolio_index_data(category)

    if len(projects) == 0:
        return ''

    return redirect(projects[0]['src'])


@memorize
def portfolio_data(category, path):
    dropbox_path = os.path.join('/', category, path)

    if not portfolio.is_project(dropbox_path):
        return None

    projects = portfolio.projects(category)

    images = list(portfolio.image_urls(dropbox_path))
    description = portfolio.description_html(dropbox_path)
    description = Markup(description) if description is not None else None

    return dict(category=category, projects=projects, images=images,
                description=description)


def portfolio_handler(category, path, resource=None):

    params = portfolio_data(category, path)

    if params is None:
        return redirect('/' + category)

    if resource is None:
        resource = Resource()

    return render_template('portfolio.j2', resource=resource, **params)


@app.route('/')
def index_handler():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/media/<path:path>')
def media_handler(path):
    return send_from_directory(app.static_folder, os.path.join('media', path))


@app.route('/work')
def work_root_handler():
    return portfolio_index_handler('work')


@app.route('/work/<path:path>')
def work_handler(path):
    return portfolio_handler('work', path)


@app.route('/gettingmarried/stationery')
def stationery_root_handler():
    return portfolio_index_handler('gettingmarried/stationery')


@app.route('/gettingmarried/stationery/<path:path>')
def stationery_handler(path):
    resource = Resource('weddings')
    return portfolio_handler('gettingmarried/stationery', path, resource)


@app.route('/<path:path>')
def path_handler(path):
    return send_from_directory(app.static_folder, os.path.join(path, 'index.html'))
