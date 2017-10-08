# Collection of associated TileNode objects ultimately meant to be tiled together

# Latitude  : high lat = N (y)
#           : low  lat = S

# Longitude : high long  = E -> (e.g. -1) (e.g. 10) (x)
#           : low long   = W <- (e.g. -3) (e.g. 0)

# Finding "width" and "height"
#   Find maximum / minimum (lat / long) vals

# User manually inputs "tolerance" that defines differences
#   between LAT and LONG columns
# --> What happens if a tolerance is wrong?
# --> We can automate this section.
#     --> Find average maximum difference between long coords.
#     --> If the difference between two lat/longs is less than that
#         Then they share the same row/col

# Recursive approach using linkedLists with leftmost as HEAD:
    # Input: all images.
    # Image A = image in top right corner (MAX Lat, MIN long)
    # Image C = image below image A. Used as base point for next iteration
    # While VALID
        # Image B = "same" long, but with smallest diff latitude
        # Once there is no NEXT smallest diff lattitude with same long
        # Repeat WHILE with image C
# Assumptions:
# - Photos are evenly spaced
# - Photos always form a complete rectangular grid.

from math import fabs
from .TileNode import FloorCeiling, TileNode, LatLong

TOLERANCE_LONG = 0.005
DIFF_TOLERANCE = 0.15

# Begin with a set of unlinked nodes and link them together to form an image
class NodeSet(object):
    def __init__(self, node_set=[]):
        self._nodes = node_set
        # print(self._get_N_node())
        # print(self._find_long_spacing())

    def add_image(self, img):
        self.node_set.append(img)

    def link_nodes(self):
        # O(N) -> Copy original node list
        search_nodes = self._nodes[:] # Copy the original node set

        # O(N) -> Current node
        current_node = self._get_N_node()

        # O(N) -> Define average meaningful spacings
        spacing_long = self._find_long_spacing()
        spacing_lat  = self._find_lat_spacing()

        # While the node set still has unlinked nodes
        while (search_nodes):
            # Remove the current node from the search set
            search_nodes.remove(current_node)

            # Define the node directly below us for the next iteration
            current_node._below = self._find_node_below(current_node, spacing_lat, spacing_long, search_nodes)

            # Recursively search for left and right nodes
            # Remove each found node from search_nodes
            current_node.find_left(search_nodes, spacing_long, spacing_lat, TOLERANCE_LONG)
            current_node.find_right(search_nodes, spacing_long, spacing_lat, TOLERANCE_LONG)
            current_node.print_left()
            current_node.print_right()
            import pdb; pdb.set_trace()  # breakpoint b7e4db16 //

            # Move onto the node below this one
            current_node = current_node._below


    ## TODO: Not working
    def _find_node_below(self, current_node, spacing_lat, spacing_long, search_nodes, TOLERANCE_LONG=TOLERANCE_LONG):
        # Node directly below will have ~same long, ~spacing lat
        # below_node = None

        for node in search_nodes:
            diff_long = fabs(node.get_long() - current_node.get_long())
            diff_lat = fabs(node.get_lat() - current_node.get_lat())

            if (diff_long < spacing_long.floor and spacing_lat.inside_range(diff_lat) ):

                return node

    # O(N) --> Returns NorthWest most NODE
    #          Starting node for search
    # Search conditions: # Maximize lat
    def _get_N_node(self):
        max_lat = self._nodes[0].get_lat()

        for img_data in self._nodes:
            if (img_data.get_lat() > max_lat):
                max_lat = img_data.get_lat()

        import pdb; pdb.set_trace()  # breakpoint f29833d0 //

        return self._find_node_by_lat(max_lat)
        # return LatLong(max_lat, min_long)

    def _find_long_spacing(self, DIFF_TOLERANCE=DIFF_TOLERANCE):
        # Find maximum distance between long rows.
        # Maximum lat spacing to describe different "rows" described by:
        #   MAX(Y_DIST) +- [MAX(Y_DIST) * (SOME_PERCENTAGE_CONSTANT)]
        long_diff_max = 0

        for index, node in enumerate(self._nodes):
            if index == len(self._nodes) - 1: break

            long_this = node.get_long()
            long_next = self._nodes[index + 1].get_long()

            long_diff = fabs(long_next - long_this)


            if long_diff > long_diff_max:
                long_diff_max = long_diff

        diff_ceiling = long_diff_max + (long_diff_max * DIFF_TOLERANCE)
        diff_floor = long_diff_max - (long_diff_max * DIFF_TOLERANCE)

        return FloorCeiling(diff_ceiling, diff_floor)

    def _find_lat_spacing(self, DIFF_TOLERANCE=DIFF_TOLERANCE):
        # Find maximum distance between lat rows.
        # Maximum lat spacing to describe different "rows" described by:
        #   MAX(Y_DIST) +- [MAX(Y_DIST) * (SOME_PERCENTAGE_CONSTANT)]
        lat_diff_max = 0

        for index, node in enumerate(self._nodes):
            if index == len(self._nodes) - 1:
                break

            lat_this = node.get_lat()
            lat_next = self._nodes[index + 1].get_lat()

            lat_diff = fabs(lat_next - lat_this)

            # print(lat_diff)

            if lat_diff > lat_diff_max:
                lat_diff_max = lat_diff

        diff_ceiling = lat_diff_max + (lat_diff_max * DIFF_TOLERANCE)
        diff_floor = lat_diff_max - (lat_diff_max * DIFF_TOLERANCE)

        return FloorCeiling(diff_floor, diff_ceiling)

    def _find_node_by_lat(self, lat):
        for node in self._nodes:
            if (lat == node.get_lat()):
                return node

    def _is_corner(self, current, next):
        raise(NotImplementedError)

    def __repr__(self):
        return(self._nodes[0].__repr__())


