from math import fabs

# LinkedList node that contains image data
class TileNode(object):
    def __init__(self, file_name, lat, longi, height, below_node=None, above_node=None, right_node=None):
        self._file_name = file_name
        self._coord = LatLong(lat=lat, longi=longi)
        self._height = height

        self._below = below_node
        self._above = above_node

        self._right = right_node

    def get_name(self):
        return self._file_name

    def get_above(self):
        return self._above

    def get_below(self):
        return self._below

    def get_right(self):
        return self._right

    # Conditions for below node:
    # other.lat < this.lat
    # other.lat - this.lat inside spacing_lat
    # other.long LESS THAN LONG_SPACE.FLOOR
    def find_below(self, search_nodes, spacing_long, spacing_lat):
        for node in search_nodes:
            diff_lat = node.get_lat() - self.get_lat()
            diff_long = node.get_long() - self.get_long()

            passes = diff_lat < 0 and spacing_lat.inside_range(diff_lat) and fabs(diff_long) < spacing_long.floor

            if (passes):
                search_nodes.remove(node)

                # Assign as our below node
                self._below = node

                # Send this thing on its quest
                node.find_below(search_nodes, spacing_long, spacing_lat)

    # Conditions for above node:
    # other.lat > this.lat
    # other.lat - this.lat inside spacing_lat
    # other.long LESS THan LONG_SPACE.FLOOR
    def find_above(self, search_nodes, spacing_long, spacing_lat):
        for node in search_nodes:
            diff_lat = node.get_lat() - self.get_lat()
            diff_long = node.get_long() - self.get_long()

            passes = diff_lat > 0 and spacing_lat.inside_range(diff_lat) and fabs(diff_long) < spacing_long.floor

            if (passes):
                search_nodes.remove(node)

                # Assign as our above node
                self._above = node

                # Send this thing on its quest
                node.find_above(search_nodes, spacing_long, spacing_lat)

    def get_coord(self):
        return self._coord

    def get_lat(self):
        return self._coord._lat

    def get_long(self):
        return self._coord._long

    def print_above(self):
        try:
            print(self)
            self._above.print_above()
        except AttributeError as e:
            print("No more above branches!")

    def print_below(self):
        try:
            print(self)
            self._below.print_below()
        except AttributeError as e:
            print("No more below branches!")

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

