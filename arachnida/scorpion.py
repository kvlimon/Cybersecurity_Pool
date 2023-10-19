import sys
import exiftool

def main():
	if len(sys.argv) < 2:
		print("Usage: ./scorpion FILE1 [FILE2 ...]")
		sys.exit(1)

	with exiftool.ExifToolHelper() as et:
		metadata = et.get_metadata(sys.argv[1:])
		for d in metadata:
			print(d)

if __name__ == "__main__":
	main()
