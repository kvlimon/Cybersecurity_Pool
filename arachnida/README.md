
# Arachnida

Prepare the environment by installing all dependencies via : **`pip install -r requirements.txt`** / **`python3 -m pip install -r requirements.txt`**

The **`spider.py`** program allow you to extract all the images from a website, recursively, by providing a url as a parameter.

**`./spider [-rlpu]`**, example **`python3 spider.py -r -l 5 -p --url https://www.example.com/`**


-  **Option -r** : recursively downloads the images in a URL received as a parameter.

-  **Option -r -l [N]** : indicates the maximum depth level of the recursive download. If not indicated, it will be 5.

-  **Option -p [PATH]** : indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.

-  **Option -u** : URL specifier


The program will download the following extensions by default :

- .jpg/jpeg

- .png

- .gif

- .bmp

The **`scorpion.py`** program allow you to retrieve any metadata of an image with EXIF.
On this github repo you can find images that have metadata : *https://github.com/ianare/exif-samples*.