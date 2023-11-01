import sys
from PIL import Image
from PIL.ExifTags import TAGS

allowed_extensions = [
	'.jpg',
	'jpeg',
	'.png',
	'.gif',
	'.bmp'
]

def has_allowed_extension(filename):
	return any(filename.lower().endswith(ext) for ext in allowed_extensions)

def analyze_exif_metadata(image_path):
	try:
		img = Image.open(image_path)
		exifdata = img.getexif()

		print(f"\nEXIF metadata: {image_path}")
		for tag_id in exifdata:
			tag = TAGS.get(tag_id, tag_id)
			data = exifdata.get(tag_id)
			if isinstance(data, bytes):
				data = data.decode()
			print(f"{tag:25}: {data}")
	except Exception as e:
		print(f"An error occurred while analyzing the image {image_path}: {str(e)}")

def main():
	if len(sys.argv) < 2:
		print("Usage: ./scorpion FILE1 [FILE2 ...]")
		sys.exit(1)

	image_paths = sys.argv[1:]

	for image_path in image_paths:
		if (has_allowed_extension(image_path)):
			analyze_exif_metadata(image_path)
		else:
			print(f"{image_path} has no valid extension")

if __name__ == "__main__":
    main()
