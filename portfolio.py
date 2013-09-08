import os

import dropbox
import markdown

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
client = dropbox.client.DropboxClient(ACCESS_TOKEN)


def _project_src(dropbox_path):
    ''' Given a dropbox path, return an html src
    Example: /work/3-CCH Collection -> cch-collection
    '''
    return dropbox_path.split('-', 1)[-1].lower().replace(' ', '-')


def _project_name(dropbox_path):
    ''' Given a dropbox path, return a human-readable name
    Example: /work/3-CCH Collection -> CCH Collection
    '''
    return dropbox_path.split('/')[-1].split('-', 1)[-1]


def _project_path(src):
    ''' Given an html src, return the dropbox_path or None
    Example: /work/cch-collection -> /work/3-CCH Collection
    '''
    dropbox_path = '/' + '/'.join(src.split('/')[:-1])
    key = src.split('/')[-1]
    contents = client.metadata(dropbox_path)['contents']
    dirs = dict((_project_src(c['path']), c['path']) for c in contents if c['is_dir'])
    return dirs.get(key)


def is_project(dir_path):
    return _project_path(dir_path) is not None


def projects(name):
    contents = client.metadata('/' + name)['contents']
    dirs = (c['path'] for c in contents if c['is_dir'])
    return list({'name': _project_name(d), 'src': _project_src(d)} for d in dirs)


def image_urls(dir_path):

    dropbox_path = _project_path(dir_path)
    contents = client.metadata(dropbox_path)['contents']
    images = [c['path'] for c in contents if 'image/' in c['mime_type']]

    for image_path in images:
        share_link = client.share(image_path, short_url=False)['url']
        embed_link = share_link.replace('www.dropbox.com', 'dl.dropboxusercontent.com', 1)
        yield embed_link


def description_html(dir_path):

    dropbox_path = _project_path(dir_path)
    contents = client.metadata(dropbox_path)['contents']

    try:
        description_path = [c['path'] for c in contents if c['path'][-3:] == '.md'][0]
    except IndexError:
        return None

    f = client.get_file(description_path)
    html = markdown.markdown(f.read())

    return html
