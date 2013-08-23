import os

import dropbox
import markdown

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
client = dropbox.client.DropboxClient(ACCESS_TOKEN)


def projects(name):
    contents = client.metadata('/' + name)['contents']
    return list(c['path'] for c in contents if c['is_dir'])


def image_urls(dir_path):

    contents = client.metadata(dir_path)['contents']
    images = [c['path'] for c in contents if 'image/' in c['mime_type']]

    for image_path in images:
        share_link = client.share(image_path, short_url=False)['url']
        embed_link = share_link.replace('www.dropbox.com', 'dl.dropboxusercontent.com', 1)
        yield embed_link


def description_html(dir_path):

    contents = client.metadata(dir_path)['contents']

    try:
        description_path = [c['path'] for c in contents if c['path'][-3:] == '.md'][0]
    except IndexError:
        return None

    f = client.get_file(description_path)
    html = markdown.markdown(f.read())

    return html


