# Find images in folder

import os
import imagehash
from PIL import Image

image_directory = './'
file_types = ['.jpg', '.png']
images_in_directory = []
image_hash_comparison_cutoff = 5


def index_files():
    """
    Indexes files in directory `directory` and pushes them to images_in_directory array
    """

    print("Indexing files")

    for root, _, files in os.walk(image_directory):
        for item in files:
            for file_type in file_types:
                if file_type in item:
                    images_in_directory.append(os.path.join(root, item))

    print(f'Finished indexing {len(images_in_directory)} files')

    pass


def get_average_hash(image_path):
    """
    Returns an `average_hash` using `Imagehash`

    Parameters
    ----------
        image_path : str, required
    """

    return imagehash.average_hash(Image.open(image_path))


def check_images():
    print(f'Looking for duplicate images...')

    for image in images_in_directory:
        duplicate = check_image_for_duplicates(image)

        if (duplicate):
            print(f'Found {duplicate} to be a duplicate image of: {image}')
            remove_image(duplicate)
    pass


def check_image_for_duplicates(original_image):
    original_image_hash = get_average_hash(original_image)

    print(f'Checking for duplicate images for {original_image}')

    for potential_duplicate_image in images_in_directory:
        potential_duplicate_image_hash = get_average_hash(
            potential_duplicate_image)

        if ((original_image != potential_duplicate_image) & compare_image_hashes(original_image_hash, potential_duplicate_image_hash)):
            return potential_duplicate_image

    pass


def compare_image_hashes(image_hash, potential_duplicate_hash):
    """
    Checks two average image hashes against eachother with a threshhold defined in `image_hash_comparison_cutoff`

    Parameters
    ----------
        image_hash : imagehash.average_hash, required
        potential_duplicate_hash : imagehash.average_hash, required
    """

    return image_hash - potential_duplicate_hash < image_hash_comparison_cutoff


def remove_image(image_path):
    os.remove(image_path)
    images_in_directory.remove(image_path)

    print(f'removed {image_path} from directory')

    pass


def main():
    index_files()
    check_images()


main()
