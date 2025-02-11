from pathlib import Path
import matplotlib.pyplot as plt
import cv2
import numpy as np
import rasterio
from rasterio.merge import merge


def geotif_mosaic_merge(images_folder: Path, save_path='mosaic.tif', labels=False):
	path_images = [path for path in images_folder.iterdir() if path.suffix == ".tif"]
	print(path_images)
	geo_images = [rasterio.open(f) for f in path_images]
	mosaic, out_trans = merge(geo_images)

	out_meta = geo_images[0].meta.copy()
	out_meta.update({
		"height": mosaic.shape[1],
		"width": mosaic.shape[2],
		"transform": out_trans
	})
	with rasterio.open(save_path, 'w+', **out_meta) as geo_mosaic:
		geo_mosaic.write(mosaic)
		if labels:
			put_labels(geo_mosaic, geo_images, path_images)
