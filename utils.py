import Image
import numpy as np

def imgToBW(img, threshold, image=False):
	width, height = img.size
	imgBW = np.asarray(img.convert("L"))

	result = np.ones((height, width), dtype=np.uint8)

	for row in range(height):
		for col in range(width):
			if imgBW[row][col] > threshold:
				result[row][col] = 0xFF
			else:
				result[row][col] = 0x00
	if image:
		return Image.fromarray(result)
	return result