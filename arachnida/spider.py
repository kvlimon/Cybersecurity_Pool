import os
import requests
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

allowed_extensions = [
	'.jpg',
	'jpeg',
	'.png',
	'.gif',
	'.bmp'
]

base_url = ""
visited_links = set()

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

	print(url)
	print(f"depth level {depth}")

	if depth == 0:
		return
	
	if url in visited_links:
		print(f"URL already visited: {url}")
		return

	try:
		response = requests.get(url)

		if response.status_code == 200:
			html_page = BeautifulSoup(response.text, 'html.parser')
			images = html_page.find_all("img")
			visited_links.add(url)

			print(images)

			for i, image in enumerate(images):
				img_src = image.get("src")
				if img_src:
					img_url = urljoin(url, img_src)

					if img_url.lower().endswith(tuple(allowed_extensions)) and is_internal_link(url, img_url):
						img_name = os.path.basename(urlparse(img_url).path)
						img_save_path = os.path.join(save_path, img_name)
						download_image(img_url, img_save_path)

			a_tags = html_page.find_all('a')

			for a_tag in a_tags:
				link = a_tag.get('href')

				if link is None:
					continue
				elif link.startswith('#'):
					continue
				elif not is_valid_URL(link):
					link = urljoin(base_url, link)
				if is_internal_link(base_url, link):
					extract_images(link, depth - 1, save_path)

	except Exception as e:
		print(f"Error retrieving {url} : {str(e)}")

	return

def main():
	parser = argparse.ArgumentParser(description="Extract all the images from a website, recursively, by providing a URL as a parameter")
	
	parser.add_argument('-r', action="store_true", help="Recursive image download")
	parser.add_argument('-l', type=int, default=5, help="Maximum depth for recursive download")
	parser.add_argument('-p', default="./data/", help="Path to save downloaded files")
	parser.add_argument('-u', '--url', type=str, help="URL from which to download images")

	args = parser.parse_args()

	if args.r:
		url = args.url
		depth = args.l
		save_path = args.p

		if not is_valid_URL(url):
			print("Please provide a valid URL..")
			return

		global base_url
		base_url = urlparse(url).scheme + "://" + urlparse(url).netloc

		os.makedirs(save_path, exist_ok=True)
		extract_images(url, depth, save_path)
	else:
		print("-r flag is required for recursive download.")

if __name__ == '__main__':
	main()