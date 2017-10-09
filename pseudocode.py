# Member node of linked list of image tiles
class TileNode(object):
    def __init__(self, file_name, lat, longi, height, below_node, above_node, right_node):
        self._file_name = file_name
        self._coord = LatLong(lat=lat, longi=longi)
        self._height = height

        self._below = below_node
        self._above = above_node

        self._right = right_node


# Convert list of GPS coordinates into list of TileNode objects
tile_nodes = parse_locations("locations.txt")

# Select the "West-most" (minimum longitude) node as our root node
root_node = tile_nodes.get_west_most_node()

# Define our search space by making a copy of all existing nodes
search_nodes = tile_nodes.copy()

# Begin our search for adjacent nodes with the current node
current_node = root_node

# Initialize list for linked nodes
paired_nodes = []

# Search for adjacent nodes till every node is paired
while (search_nodes is not empty):
    # Remove the current node from the search set
    search_nodes.remove(current_node)

    # "find_nodes_*()" creates linked lists of nodes above and below the "current_node"
    # Newly paired nodes are also removed from search set
    current_node.find_nodes_above(IN SET: search_nodes)
    current_node.find_nodes_below(IN SET: search_nodes)

    # "current_node" is now linked to all nodes above and below it
    # Add it to the list of linked nodes
    paired_nodes.append(current_node)

    # Look up the node to the east of the current node.
    # We will be using this node as the current node for the next iteration
    current_node = find_east_node(current_node)

    # If we managed to find an adjacent node, we continue to the next iteration
    if current_node is not None:
        continue

# openCV image matrix we'll be writing to
imageData = ImageData()

for linked_node in paired_nodes:
    # Convert each linked node to png and add to the image
    imageData.insert(linked_node.to_png())

# Present the final stitched image
imageData.show()



