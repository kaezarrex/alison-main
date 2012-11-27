import argparse, os, shutil

from markdown import markdown


DESCRIPTION_FILENAME = 'description.md'
CONTENT_PATH = 'content/work/'
MEDIA_PATH = 'content/media/portfolio/'
IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png']
FIRST_IMAGE_TEMPLATE = '<div class="item active"><img src="{{ media_url(\'portfolio/%s\') }}"></div>\n'
IMAGE_TEMPLATE = '<div class="item"><img src="{{ media_url(\'portfolio/%s\') }}"></div>'
PAGE_TEMPLATE = '''---
extends: portfolio.j2
title: ???
description: ???
---

{%% block carousel %%}
%s
{%% endblock %%}

{%% block description %%}
%s
{%% endblock %%}
'''

parser = argparse.ArgumentParser()
parser.add_argument('path', help='path to portfolio')
args = parser.parse_args()


def create_page_name(path):
    base = os.path.basename(root)
    base = base.lower()
    base = base.replace(' ', '-')
    base = base.replace('&', '+')
    return base


def extension(filename):
    return filename.split('.')[-1].lower()


if __name__ == '__main__':

    for root, dirs, files in os.walk(args.path):
        if DESCRIPTION_FILENAME in files:
            page_name = create_page_name(root)
            page_path = os.path.join(CONTENT_PATH, page_name)
            index_path = os.path.join(page_path, 'index.html')
            description_path = os.path.join(root, DESCRIPTION_FILENAME)

            images = [f for f in files if extension(f) in IMAGE_EXTENSIONS]
            image_map = ((img, '%02i.%s' % (i, extension(img))) for i, img in enumerate(images))
            image_map = tuple((os.path.join(root, old), os.path.join(page_name, new)) for old, new in image_map)

            image_string = FIRST_IMAGE_TEMPLATE % image_map[0][1]
            image_string += '\n'.join(IMAGE_TEMPLATE % new for old, new in image_map[1:])

            try:
                print os.path.join(MEDIA_PATH, page_name)
                os.makedirs(os.path.join(MEDIA_PATH, page_name))
            except OSError:
                pass

            for old, new in image_map:
                new = os.path.join(MEDIA_PATH, new)
                shutil.copy(old, new)

            description_file = open(description_path)
            description = markdown(description_file.read())
            description_file.close()

            try:
                os.makedirs(page_path)
            except OSError:
                pass

            f = open(index_path, 'w')
            f.write(PAGE_TEMPLATE % (image_string, description))
            f.close()
