from classes.NodeSet import NodeSet
from classes.TileNode import TileNode
from classes.Stitcher import Stitcher
from classes.parsers import parse_locations
import argparse


if __name__ == "__main__":
    # All caps -> User provided constants
    IMAGE_DIR = "/Users/sSDSD/Documents/ABE498/TileProject/undistort"
    OUT_DIR = "/Users/sSDSD/Documents/ABE498/TileProject/output"
    LOCATION_DIR = "/Users/sSDSD/Documents/ABE498/TileProject/locations.txt"
    VERBOSE = True

    parser = argparse.ArgumentParser(
        description="Given an image directory, location file, and output directory, stitch together a collection of aerial photos.")
    parser.add_argument('-IMAGE_DIR', help="Directory containing images to stitch", default=IMAGE_DIR)
    parser.add_argument('-OUT_DIR', help="Directory to output the stitched image", default=OUT_DIR)
    parser.add_argument('-LOCATIONS', help="Location file containing GPS information", default=LOCATION_DIR)
    parser.add_argument('-VERBOSE', help="Verbosity of processing", default=True)

    args = parser.parse_args()

    nodes = parse_locations(args.LOCATIONS)
    nodes.link_nodes()

    stitch = Stitcher(nodes, args.IMAGE_DIR, args.OUT_DIR, args.VERBOSE)

    stitch.stitch_images()
    stitch.export()
