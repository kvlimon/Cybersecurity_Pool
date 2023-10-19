import os
import requests
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Telecharger toutes les images de l'URL passe en param 
# Ne pas execute extract_image en recursif sur un lien external.
# Ne pas telecharger des images appartenant a d'autres sites ?

allowed_extensions = [
	'.jpg/jpeg',
	'.png',
	'.gif',
	'.bmp'
]

# netloc is 
# cat.example
# in
# https://cat.example/list;meow?breed=siberian#pawsize

def is_internal_link(base_url, link):
	base_domain = urlparse(base_url).netloc
	link_domain = urlparse(link).netloc
	return base_domain == link_domain

def is_valid_URL(url):
	parsed = urlparse(url)
	return bool(parsed.netloc) and bool(parsed.scheme)

def has_allowed_extension(filename):
	return any(filename.lower().endswith(ext) for ext in allowed_extensions)

def download_image(url, save_path):
	try:
		response = requests.get(url)
		if response.status_code == 200:
			with open(save_path, 'wb') as file:
				file.write(response.content)
			print(f"Downloaded image: {url}")
	except Exception as e:
		print(f"Error downloading image {url}: {str(e)}")

def extract_images(url, depth, save_path):
	print(f"depth level {depth}")

	if depth == 0:
		return
	elif not is_valid_URL(url):
		print("Please provide a valid URL..")
		return

	try:
		response = requests.get(url)

		if response.status_code == 200:
			html_page = BeautifulSoup(response.text, 'html.parser')
			images = html_page.find_all("img")

			print(images)

			for i, image in enumerate(images):
				img_src = image.get("src")

				if img_src:
					img_url = urljoin(url, img_src)
					if is_internal_link(url, img_url) and img_url.lower().endswith(tuple(allowed_extensions)):
						img_name = os.path.basename(urlparse(img_url).path)
						img_save_path = os.path.join(save_path, img_name)
						download_image(img_url, img_save_path)

			a_tags = html_page.find_all('a')
			for a_tag in a_tags:
				link = a_tag.get('href')
				if is_valid_URL(link):
					if not is_internal_link(url, link):
						continue  # Skip external links
					if link.startswith("/"):  # Handle relative links
						link = urljoin(url, link)
					extract_images(link, depth - 1, save_path)

	except Exception as e:
		print(f"Error retrieving {url} : {str(e)}")

	return

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

		os.makedirs(save_path, exist_ok=True)
		extract_images(url, depth, save_path)
	else:
		print("-r flag is required for recursive download.")

if __name__ == '__main__':
	main()