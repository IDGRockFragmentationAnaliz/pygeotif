from pathlib import Path
import matplotlib.pyplot as plt
import cv2
import numpy as np
import rasterio
from rasterio.merge import merge

from merge import geotif_mosaic_merge


def main():
	pth = Path("D:/1.ToSaver/profileimages/ShapeBaikal/Target")
	geotif_mosaic_merge(pth)


def geotif2geotif_standart(input_path: Path, output_path: Path):
	with rasterio.open(input_path) as tif:
		meta = tif.meta.copy()
		image = tif.read([1, 2, 3]).astype(np.uint8)

		meta.update({
			"dtype": rasterio.uint8,
			'count': 3
		})

		if output_path.is_dir():
			output_folder = output_path
			name = input_path.stem
		else:
			output_folder = output_path.parent
			name = output_path.name
		with rasterio.open(
			output_folder / f"{name}",
			'w',
			**meta
		) as dst:
			dst.write(image)


def put_labels(geo_mosaic, geo_parts, geo_paths):
	np_mosaic = geo_mosaic.read()
	print(geo_mosaic.meta)
	np_mosaic = np.transpose(np_mosaic, (1, 2, 0))
	np_mosaic = np.ascontiguousarray(np_mosaic)

	bounds = geo_mosaic.bounds
	for part, path in zip(geo_parts, geo_paths):
		bb = part.bounds
		center_x = (bb.left + bb.right) / 2 - bounds.left
		center_y = bounds.top - (bb.top + bb.bottom) / 2
		col = int(center_x / 0.0005)
		row = int(center_y / 0.0005)
		cv2.putText(
			np_mosaic,
			path.stem,
			(col-100, row),
			cv2.FONT_HERSHEY_SIMPLEX,
			1,
			(0, 0, 255),
			2,
			cv2.LINE_AA
		)
	np_mosaic = np.transpose(np_mosaic, (2, 0, 1))
	geo_mosaic.write(np_mosaic)


if __name__ == '__main__':
	main()
