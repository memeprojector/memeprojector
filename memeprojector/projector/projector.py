import rasterio
import numpy as np
from PIL import Image
from pathlib import Path
from tempfile import TemporaryDirectory
from rasterio.transform import from_gcps
from rasterio.control import GroundControlPoint
from rasterio.warp import (
    calculate_default_transform,
    reproject, Resampling
)

def project(img: np.array, epsg: int) -> np.array:
    print(img.shape)
    out_crs = rasterio.crs.CRS.from_epsg(epsg)
    transf = from_gcps( get_GCPs(img.shape) )
    
    with TemporaryDirectory() as tmp_path:
        tmp_path = Path(tmp_path)
        with rasterio.open(
            tmp_path / 'tmp.tif',
            'w',
            driver='GTiff',
            height=img.shape[0],
            width=img.shape[1],
            count=img.shape[2],
            dtype=img.dtype,
            crs='+proj=latlong',
            transform=transf,
        ) as swap:
            for i in range(img.shape[2]):
                swap.write(img[:,:,i], i+1)
            (  out_transform,
               out_width,
               out_height    ) = calculate_default_transform(
                                    swap.crs, out_crs,
                                    swap.width, swap.height,
                                    *swap.bounds)
            
            out_img, out_transf = reproject(
                        img[:,:,0],
                        src_transform=swap.transform,
                        src_crs=swap.crs,
                        #dst_transform=out_transform,
                        dst_crs=out_crs,
                        )
    return out_img

def get_GCPs(img_shape: tuple) -> list:
    row_max, col_max = img_shape[0], img_shape[1]
    xmin, xmax = -179.99, 179.99
    ymin, ymax = -89.99, 89.99
    return [
        GroundControlPoint(
            row=0,
            col=0,
            x=xmin,
            y=ymin,           
        ),
        GroundControlPoint(
            row=row_max,
            col=0,
            x=xmax,
            y=ymax, 
        ),
        GroundControlPoint(
            row=row_max,
            col=col_max,
            x=xmax,
            y=ymin,    
        ),
        GroundControlPoint(
            row=0,
            col=col_max,
            x=xmin,
            y=ymin, 
        ),
        GroundControlPoint(
            row=int(row_max/2),
            col=int(col_max/2),
            x=(xmax-xmin)/2,
            y=(ymax-ymin)/2, 
        ),
    ]

if __name__ == '__main__':
    root = Path(__file__).parents[2]
    with Image.open(root/"test/spiderman-meme.png") as im:
        out_im = project(
            np.asarray(im),
            31467
        )
    im = Image.fromarray(out_im)
    im.save(root/"projected.png")