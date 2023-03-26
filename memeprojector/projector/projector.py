import rasterio
import numpy as np
from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt 
from tempfile import TemporaryDirectory
from rasterio.transform import from_gcps
from rasterio.control import GroundControlPoint
from rasterio.warp import calculate_default_transform, reproject

def project(img: np.array, epsg: int) -> np.array:
    # Input
    in_crs = '+proj=latlong'
    gcps = get_GCPs(img.shape)
    in_transform = from_gcps( gcps )

    # Output CRS, transform and array
    out_crs = rasterio.crs.CRS.from_epsg(epsg)
    out_transform, out_width, out_height = calculate_default_transform(
        in_crs, out_crs, img.shape[0], img.shape[1], gcps=gcps)

    out_imgs = []
    # Reproject image for each band
    for band in range(img.shape[-1]):
        out_img = np.zeros((out_width, out_height))
        out_img, out_transform = reproject(
            img[:,:,band],
            out_img,
            src_transform=in_transform,
            src_crs=in_crs,
            dst_transform=out_transform,
            dst_crs=out_crs,
        )
        out_imgs.append(out_img)
    return np.stack(out_imgs, axis=2)/255

def get_GCPs(img_shape: tuple) -> list:
    row_max, col_max = img_shape[0], img_shape[1]
    xmin, xmax = -179.99, 179.99
    ymin, ymax = -89.99, 89.99
    return [
        GroundControlPoint(
            row=0,
            col=0,
            x=xmin,
            y=ymax,           
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

# if __name__ == '__main__':
#     root = Path(__file__).parents[2]
#     with Image.open(root/"test/spiderman-meme.png") as im:
#         out_im = project(
#             np.asarray(im),
#             2154
#         )
#         print('in_size:', np.asarray(im).shape)
#     print('out_size:', out_im.shape)
#     plt.imsave(root/'test'/'projected.png', out_im)