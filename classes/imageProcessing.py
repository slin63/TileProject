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

# Begin with a set of unlinked nodes and link them together to form an image
class NodeSet(object):
    def __init__(self, node_set=[]):
        self._nodes = node_set
        print(self._get_W_node())
        print(self._find_long_spacing())

    def add_image(self, img):
        self.node_set.append(img)

    def link_nodes(self):
        # O(N) -> Copy original node list
        search_nodes = self._nodes[:] # Copy the original node set

        # O(N) -> Current node
        current_node = self._get_W_node()

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
            current_node.find_left(search_nodes, spacing_long, spacing_lat)
            current_node.find_right(search_nodes, spacing_long, spacing_lat)

            # Move onto the node below this one
            current_node = current_node._below


    ## TODO: Not working
    def _find_node_below(self, current_node, spacing_lat, spacing_long, search_nodes, TOLERANCE_LONG=0.0001):
        # Node directly below will have ~same long, ~spacing lat
        # below_node = None

        for node in search_nodes:
            diff_long = fabs(node.get_long() - current_node.get_long())
            diff_lat = fabs(node.get_lat() - current_node.get_lat())

            if (diff_long < spacing_long.floor and spacing_lat.inside_range(diff_lat) ):

                return node

    # O(N) --> Returns NorthWest most NODE
    #          Starting node for search
    # Search conditions: # Maximize latitude, then longitude
    def _get_W_node(self):
        max_long = self._nodes[0].get_long()

        for img_data in self._nodes:
            if (img_data.get_long() > max_long):
                max_long = img_data.get_long()

        return self._find_node_by_long(max_long)
        # return LatLong(max_lat, min_long)

    def _find_long_spacing(self, DIFF_TOLERANCE=0.10):
        # Find maximum distance between long rows.
        # Maximum lat spacing to describe different "rows" described by:
        #   MAX(Y_DIST) +- [MAX(Y_DIST) * (SOME_PERCENTAGE_CONSTANT)]
        long_diff_max = 0

        for index, node in enumerate(self._nodes):
            if index == len(self._nodes) - 1: break

            long_this = node.get_long()
            long_next = self._nodes[index + 1].get_long()

            long_diff = fabs(long_next - long_this)

            print(long_diff)

            if long_diff > long_diff_max:
                long_diff_max = long_diff

        diff_ceiling = long_diff_max + (long_diff_max * DIFF_TOLERANCE)
        diff_floor = long_diff_max - (long_diff_max * DIFF_TOLERANCE)

        return FloorCeiling(diff_ceiling, diff_floor)

    def _find_lat_spacing(self, DIFF_TOLERANCE=0.10):
        # Find maximum distance between lat rows.
        # Maximum lat spacing to describe different "rows" described by:
        #   MAX(Y_DIST) +- [MAX(Y_DIST) * (SOME_PERCENTAGE_CONSTANT)]
        lat_diff_max = 0

        for index, node in enumerate(self._nodes):
            if index == len(self._nodes) - 1: break

            lat_this = node.get_lat()
            lat_next = self._nodes[index + 1].get_lat()

            lat_diff = fabs(lat_next - lat_this)

            # print(lat_diff)

            if lat_diff > lat_diff_max:
                lat_diff_max = lat_diff

        diff_ceiling = lat_diff_max + (lat_diff_max * DIFF_TOLERANCE)
        diff_floor = lat_diff_max - (lat_diff_max * DIFF_TOLERANCE)

        return FloorCeiling(diff_ceiling, diff_floor)

    def _find_node_by_long(self, longi):
        for node in self._nodes:
            if (longi == node.get_long()):
                return node

    def _is_corner(self, current, next):
        raise(NotImplementedError)

    def __repr__(self):
        return(self._nodes[0].__repr__())


# LinkedList node that contains image data
class TileNode(object):
    def __init__(self, file_name, lat, longi, height, left_node=None, right_node=None, below_node=None):
        self._file_name = file_name
        self._coord = LatLong(lat=lat, longi=longi)
        self._height = height

        self._left = left_node
        self._right = right_node
        self._below = below_node

    # Conditions for left node:
    # other.lat - this.lat < 0
    # other.lat - this.lat inside spacing_lat
    # other.long within TOLERANCE_LONG
    def find_left(self, search_nodes, spacing_long, spacing_lat, TOLERANCE_LONG=0.0001):
        for node in search_nodes:
            diff_lat = node.get_lat() - self.get_lat()
            diff_long = node.get_long() - self.get_long()

            passes = diff_lat < 0 and spacing_lat.inside_range(diff_lat) and fabs(diff_long) < TOLERANCE_LONG

            if (passes):
                search_nodes.remove(node)

                # Assign as our left node
                self._left = node

                # Send this thing on its quest
                node.find_left(search nodes, spacing_long, spacing_lat, TOLERANCE_LONG)

    def find_right(self, search_nodes, spacing_long, spacing_lat, TOLERANCE_LONG=0.0001):
        pass


    def get_coord(self):
        return self._coord

    def get_lat(self):
        return self._coord._lat

    def get_long(self):
        return self._coord._long

    def smaller_lat(self, other):
        return this._lat < other._lat

    def smaller_long(self, other):
        return this._long < other._long

    def __repr__(self):
        return "{0}: [{1}], Z: {2}".format(self._file_name, self._coord, self._height)


class FloorCeiling(object):
    def __init__(self, floor, ceiling):
        self.floor = floor
        self.ceiling = ceiling

    def inside_range(self, other):
        return (self.floor <= float(other) <= self.ceiling)


# Coordinate logic
class LatLong(object):
    def __init__(self, lat, longi):
        self._lat = float(lat)
        self._long = float(longi)

    def __eq__(self, other):
        return (self._lat, self._long) == (other._lat, other._long)

    def __repr__(self):
        return "LAT: {0}, LONG: {1}".format(self._lat, self._long)

