from console import console
from image import *
import logging
log = logging.getLogger(__name__)


logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO,
    filename='AstroImageProc.log',
    filemode='w'
)

console = console()
images = []

def test(*args):
    log.info(f'TEST! with args = {args}')

def load(*args):
    path = console.getPath()
    log.info(f'Load = {path}')
    global images
    images = get_images(path)
    images.sort(key = lambda x: x.sort_key())

def table(*args):
    global images
    if args:
        im_type = str(args[0])
        im_type = im_type.lower()
        range_im = [x for x in images if x.imagetyp == im_type]
    else:
        range_im = images

    table = gen_table(images, idx0=1)
    console._addToBuffer(table)


console.addFunction('test', test)
console.addFunction('load', load)
console.addFunction('list', table)
if __name__ == '__main__':
    while True:
        console.update()