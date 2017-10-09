from csv import DictReader
from .TileNode import TileNode
from .NodeSet import NodeSet

# Read in locations.txt and parse data as ImageData class, compile into ImageSet
def parse_locations(locationsFile):
    nodes = []

    with open(locationsFile) as csvFile:
        reader = DictReader(csvFile, delimiter=' ')
        for row in reader:
            node = TileNode(
                file_name=row["#name"],
                lat=row["latitude/Y"],
                longi=row["longitude/X"],
                height=row["height/Z"]
            )
            nodes.append(node)

    return NodeSet(nodes)
