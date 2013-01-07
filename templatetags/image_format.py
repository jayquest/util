#coding=utf-8
import os.path

from django import template

FMT = 'PNG'
EXT = 'png'
QUAL = 100

register = template.Library()


def resized_path(path, size, method):
    "Returns the path for the resized image."

    directory, name = os.path.split(path)
    image_name, ext = name.rsplit('.', 1)
    if directory != '':
        directory += '/'
    return os.path.join(directory, '_%s_%s_%s.%s' % (image_name, method, size, EXT))


def scale(imagefield, size, method='scale'):
    """ 
    Template filter used to scale an image
    that will fit inside the defined area.

    Returns the url of the resized image.

    {% load image_format %}
    {{ profile.picture|scale:"48x48" }}
    """

    # imagefield can be a dict with "path" and "url" keys
    if imagefield.__class__.__name__ == 'dict':
        imagefield = type('imageobj', (object,), imagefield)

    image_path = resized_path(imagefield.path, size, method)

    need_resize = True

    if not os.path.exists(image_path):
        try:
            import Image
        except ImportError:
            try:
                from PIL import Image
            except ImportError:
                raise ImportError('Cannot import the Python Image Library.')

        image = Image.open(imagefield.path)

        # normalize image mode
        if image.mode != 'RGBA' or image.mode != 'RGB':
            image = image.convert('RGBA')

        # parse size string 'WIDTHxHEIGHT'
        width, height = [int(i) for i in size.split('x')]

        need_resize = width != image.size[0] or height != image.size[1]

        # use PIL methods to edit images
        if method == 'scale' and need_resize:
            premultiply(image)
            image.thumbnail((width, height), Image.ANTIALIAS)
            unmultiply(image)
            image.save(image_path, FMT, quality=QUAL)

        elif method == 'crop' and need_resize:
            try:
                import ImageOps
            except ImportError:
                from PIL import ImageOps

            premultiply(image)
            image = ImageOps.fit(image, (width, height), Image.ANTIALIAS)
            unmultiply(image)
            image.save(image_path, FMT, quality=QUAL)

    if need_resize:
        return resized_path(imagefield.url, size, method)
    return imagefield.url



def crop(imagefield, size):
    """
    Template filter used to crop an image
    to make it fill the defined area.

    {% load image_format %}
    {{ profile.picture|crop:"48x48" }}

    """
    return scale(imagefield, size, 'crop')


register.filter('scale', scale)
register.filter('crop', crop)

def premultiply(im):
    pixels = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = pixels[x, y]
            if a != 255:
                r = r * a // 255
                g = g * a // 255
                b = b * a // 255
                pixels[x, y] = (r, g, b, a)

def unmultiply(im):
    pixels = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = pixels[x, y]
            if a != 255 and a != 0:
                r = 255 if r >= a else 255 * r // a
                g = 255 if g >= a else 255 * g // a
                b = 255 if b >= a else 255 * b // a
                pixels[x, y] = (r, g, b, a)