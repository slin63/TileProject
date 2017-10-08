from classes.NodeSet import NodeSet
from classes.TileNode import TileNode
from classes.Stitcher import Stitcher
import argparse
import csv

# Read in locations.txt and parse data as ImageData class, compile into ImageSet
def parseLocations(locationsFile):
    nodes = []

    with open(locationsFile) as csvFile:
        reader = csv.DictReader(csvFile, delimiter=' ')
        for row in reader:
            node = TileNode(
                file_name  = row["#name"],
                lat        = row["latitude/Y"],
                longi      = row["longitude/X"],
                height     = row["height/Z"]
            )
            nodes.append(node)

    return NodeSet(nodes)


## TODO: Traverse nodes into 2d numpy array.
##     : Generate map with OpenCV

if __name__ == "__main__":
    # All caps -> User provided constants
    IMAGE_DIR = "/Users/sSDSD/Documents/ABE498/TileProject/undistort"
    OUT_DIR = "/Users/sSDSD/Documents/ABE498/TileProject/output"
    LOCATION_DIR = "/Users/sSDSD/Documents/ABE498/TileProject/locations.txt"
    VERBOSE = True

    parser = argparse.ArgumentParser(description="Given an image directory, location file, and output directory, stitch together a collection of aerial photos.")
    parser.add_argument('-IMAGE_DIR', help="Directory containing images to stitch", default=IMAGE_DIR)
    parser.add_argument('-OUT_DIR', help="Directory to output the stitched image", default=OUT_DIR)
    parser.add_argument('-LOCATIONS', help="Location file containing GPS information", default=LOCATION_DIR)
    parser.add_argument('-VERBOSE', help="Verbosity of processing", default=True)

    args = parser.parse_args()

    nodes = parseLocations(args.LOCATIONS)
    nodes.link_nodes()

    stitch = Stitcher(nodes, args.IMAGE_DIR, args.OUT_DIR, args.VERBOSE)

    stitch.stitch_images()
    stitch.export()
