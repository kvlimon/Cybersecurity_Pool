import os
import argparse

def extract_images(url, depth, save_path):
	return

# Modify default path with env PWD
# Check help msg, issue with uppercase flags

def main():
	parser = argparse.ArgumentParser(description="Extract all the images from a website, recursively, by providing a URL as a parameter")
	parser.add_argument('URL', help="URL from which to download images")
	parser.add_argument('-r', action="store_true", help="Recursive image download")
	parser.add_argument('-l', type=int, default=5, help="Maximum depth for recursive download")
	parser.add_argument('-p', default="./data/", help="Path to save downloaded files")

	args = parser.parse_args()

	if args.r:
		url = args.URL
		depth = args.l
		save_path = args.p

		if not os.path.exists(save_path):
			os.makedirs(save_path)
		extract_images(url, depth, save_path)
	else:
		print("-r flag is required for recursive download.")

if __name__ == '__main__':
	main()