from math import fabs

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
    def find_left(self, search_nodes, spacing_long, spacing_lat, TOLERANCE_LONG=0.0005):
        for node in search_nodes:

            diff_lat = node.get_lat() - self.get_lat()
            diff_long = node.get_long() - self.get_long()

            print("CHECKING: {} vs. {}".format(node, self))
            passes = diff_lat < 0 and spacing_lat.inside_range(diff_lat) and fabs(diff_long) < TOLERANCE_LONG

            if (passes):
                search_nodes.remove(node)

                # Assign as our left node
                self._left = node

                # Send this thing on its quest
                node.find_left(search_nodes, spacing_long, spacing_lat, TOLERANCE_LONG)

    # Conditions for left node:
    # other.lat - this.lat > 0
    # other.lat - this.lat inside spacing_lat
    # other.long within TOLERANCE_LONG
    def find_right(self, search_nodes, spacing_long, spacing_lat, TOLERANCE_LONG=0.0005):
        for node in search_nodes:
            diff_lat = node.get_lat() - self.get_lat()
            diff_long = node.get_long() - self.get_long()

            passes = diff_lat > 0 and spacing_lat.inside_range(diff_lat) and fabs(diff_long) < TOLERANCE_LONG

            if (passes):
                search_nodes.remove(node)

                # Assign as our left node
                self._right = node

                # Send this thing on its quest
                node.find_right(search_nodes, spacing_long, spacing_lat, TOLERANCE_LONG)

    def get_coord(self):
        return self._coord

    def get_lat(self):
        return self._coord._lat

    def get_long(self):
        return self._coord._long

    def print_right(self):
        try:
            print(self)
            self._right.print_right()
        except AttributeError as e:
            print("No more right branches!")

    def print_left(self):
        try:
            print(self)
            self._left.print_left()
        except AttributeError as e:
            print("No more left branches!")

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
        return (self.floor <= fabs(float(other)) <= self.ceiling)


# Coordinate logic
class LatLong(object):
    def __init__(self, lat, longi):
        self._lat = float(lat)
        self._long = float(longi)

    def __eq__(self, other):
        return (self._lat, self._long) == (other._lat, other._long)

    def __repr__(self):
        return "LAT: {0}, LONG: {1}".format(self._lat, self._long)

