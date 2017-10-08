from classes.NodeSet import NodeSet
from classes.TileNode import TileNode
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

var = parseLocations("locations.txt")
var.link_nodes()
print(var)

import pdb; pdb.set_trace()  # breakpoint 167e6085 //
