from astropy.io import fits
import numpy as np
from pathlib import Path
from typing import List

class image:

    def __init__(self, filepath, fits_imagetyp='', fits_exptime=0, fits_filter='', fits_time_obs=0,
                 fits_naxis1=0, fits_naxis2=0, fits_binning=1):
        self.filepath = filepath # Absolute
        self.filename = filepath.name
        self.imagetyp = fits_imagetyp.lower()
        self.exptime = fits_exptime
        self.filter = fits_filter
        self.time_obs = fits_time_obs
        self.naxis1 = fits_naxis1
        self.naxis2 = fits_naxis2
        self.binning = fits_binning
        self.good = True
        self.aligned = False
        self.corrected = False

    def __str__(self):
        return f'Image {self.filename} in {self.filter} type {self.type}'
    
    def sort_key(self):
        """Returns the key to use when sorting multiple objects"""
        return self.time_obs

    def data(self):
        hdu = fits.open(self.filepath)
        return hdu[0].data 
        hdu.close()

    def header(self):
        hdu = fits.open(self.filepath)
        return hdu[0].header 
        hdu.close()

def gen_table(image_list: list, idx0 = 0) -> str:
    """Returns a nice table with the images and their properties"""
    table = ''
    s = "{:<3s} {:<36s} {:<15s} {:<8s} {:<10s} {:<12s} {:4s} {:<4s}\n"
    s = s.format('idx', 'filename', 'image typ', 'exp time', 'filter', 'time_obs', 'lenX', 'lenY', 'binnig')
    table += s

    table += ("="*len(s))
    table += '\n'
    i = idx0
    for im in image_list:
        s = f'{i:<3d} {im.filename:<36} {im.imagetyp:<15} {im.exptime:<8} {im.filter:<10}' +\
            f'{im.time_obs:<12} {im.naxis1:<4d} {im.naxis2:<4d}'
        table += s
        table += '\n'
        i += 1

    return table

def get_images(path: str) -> List[image]:
    path = Path(path)
    files = path.iterdir()
    imgs = []
    for f in files:
        if f.suffix.lower() in ['.fits', '.fit', '.fts']:
            hdulist = fits.open(f)
            hdr = hdulist[0].header

            imtype = 'LIGHT'
            if 'IMAGETYP' in hdr:
                imtype = hdr['IMAGETYP']
            
            exptime = '1'
            if 'EXPTIME' in hdr:
                exptime = hdr['EXPTIME']

            filt = 'V'
            if 'FILTER' in hdr:
                filt = hdr['FILTER']

            time = 0
            if 'TIME-OBS' in hdr:
                time = hdr['TIME-OBS']
            
            nx1 = 0
            if 'NAXIS1' in hdr:
                nx1 = hdr['NAXIS1']
            
            nx2 = 0
            if 'NAXIS2' in hdr:
                nx2 = hdr['NAXIS2']

            binning = 1
            if 'XBINNING' in hdr:
                binning = hdr['XBINNING']

            newimage = image(f, fits_imagetyp=imtype, fits_exptime=exptime, fits_filter=filt, fits_time_obs=time,
                            fits_naxis1=nx1, fits_naxis2=nx2, fits_binning=binning)
            imgs.append(newimage)
            hdulist.close()
    return imgs
