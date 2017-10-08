from classes.NodeSet import NodeSet
from classes.TileNode import TileNode
from classes.Stitcher import Stitcher
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
    VERBOSE = True

    nodes = parseLocations("locations.txt")
    nodes.link_nodes()

    stitch = Stitcher(nodes, IMAGE_DIR, OUT_DIR, VERBOSE)

    stitch.stitch_images()
    stitch.export()
