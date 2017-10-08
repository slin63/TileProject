import numpy as np
from datetime import datetime
from os import listdir
import cv2

# DEBUG = True
DEBUG = False

# Assumptions:
#   Images are all same resolution


class Stitcher(object):
    def __init__(self, node_set, image_dir, out_dir, verbose):
        self._node_set = node_set
        self._verbose = verbose
        self._out_dir = out_dir

        self._stitched_image = None

        self._image_dict = self._load_images(image_dir)

    # https://stackoverflow.com/questions/7589012/combining-two-images-with-opencv
    # Recursively step through nodes and stich images as we go.
    def stitch_images(self):
        image_cols = []

        # O(N) -> Copy original node list
        stitch_nodes = self._node_set.get_nodes()[:]

        # O(N) -> Set the current node
        current_node = self._node_set.get_root()

        # Concatenate above nodes
        # Concatenate below nodes
        # After above/below accounted for, save matrix and
        # change current node to right node.
        while (stitch_nodes):
            stitch_nodes.remove(current_node)

            # Our initial image tile
            tile_current = self._image_dict[current_node.get_name()]

            # Our image tile after tiling above images
            tile_current = self._stitch_above(current_node, tile_current, stitch_nodes)

            # Our image tile after tiling below images
            tile_current = self._stitch_below(current_node, tile_current, stitch_nodes)

            # Save image tile
            image_cols.append(tile_current)

            # Identify our next root node for the next iteration
            current_node = current_node.get_right()

            if self._verbose:
                print("New stitching root: {0}".format(current_node))

        self._stitched_image = self._merge_cols(image_cols)


    def export(self):
        if self._stitched_image is None:
            raise(Exception("Stitcher.export(): No stitched image yet. Call stitch_images() first"))

        out_name = 'stitched-{0}.png'.format(datetime.now())
        out_dir = "{0}/{1}".format(self._out_dir, out_name)

        cv2.imwrite(out_dir, self._stitched_image)

    # Combine each image in image_cols adjacently to form the final tiled image
    def _merge_cols(self, image_cols):
        # Stats data
        num_cols = len(image_cols)
        col_count = 1

        # Identify left-most image column
        stitched = image_cols[0]

        # Remove from image column set
        image_cols.remove(stitched)

        for col in image_cols:
            h1, w1 = stitched.shape[:2]
            h2, w2 = col.shape[:2]

            # Create empty matrix
            stitched_img = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)

            # Combine 2 images -> next tile is attached above current tile
            stitched_img[:h1, :w1, :3] = stitched
            stitched_img[:h2, w1:w1+w2, :3] = col

            # Set the newly stitched image as the new base for the next iteration
            stitched = stitched_img

        return stitched


    # Steps through linked list and adds images above
    def _stitch_above(self, root_node, tile_current, stitch_nodes):
        if DEBUG:
            print("_stitch_above")
        node_above = root_node.get_above()
        tile_above = self._image_dict[root_node.get_above()]

        # While we still have something after this
        while (tile_above is not None):
            # Remove this node from the set of non-stitched nodes
            stitch_nodes.remove(node_above)

            if self._verbose:
                self.__report_stitching(node_above)

            h1, w1 = tile_current.shape[:2]
            h2, w2 = tile_above.shape[:2]

            # Create empty matrix
            stitched_img = np.zeros((h1 + h2, max(w1, w2), 3), np.uint8)

            # Combine 2 images -> next tile is attached above current tile
            stitched_img[:h2, :w2, :3] = tile_below
            stitched_img[h2:h1+h2, :w1, :3] = tile_current

            # Set the current tile to the stitched image so far
            tile_current = stitched_img
            # Set the next tile to the tile above our previous tile
            node_above = node_above.get_above()

            if node_above is not None:
                tile_above = self._image_dict[node_above.get_name()]
            else:
                tile_above = None

        if DEBUG:
            out_name = 'above-{0}.png'.format(datetime.now())
            out_dir = "{0}/{1}".format(self._out_dir, out_name)

            cv2.imwrite(out_dir, tile_current)

        return tile_current

    def _stitch_below(self, root_node, tile_current, stitch_nodes):
        if DEBUG:
            print("_stitch_below")
        node_below = root_node.get_below()
        tile_below = self._image_dict[root_node.get_below().get_name()]

        # While we still have something after this
        while (tile_below is not None):
            # Remove this node from the set of non-stitched nodes
            stitch_nodes.remove(node_below)

            if self._verbose:
                self.__report_stitching(node_below)

            h1, w1 = tile_current.shape[:2]
            h2, w2 = tile_below.shape[:2]

            #create empty matrix
            stitched_img = np.zeros((h1 + h2, max(w1, w2), 3), np.uint8)

            # Combine 2 images -> next tile is attached below current tile
            stitched_img[:h1, :w1, :3] = tile_current
            stitched_img[h1:h1+h2, :w2, :3] = tile_below

            # Set the current tile to the stitched image so far
            tile_current = stitched_img
            # Set the next tile to the tile below our previous tile
            node_below = node_below.get_below()

            if node_below is not None:
                tile_below = self._image_dict[node_below.get_name()]
            else:
                tile_below = None

        if DEBUG:
            out_name = 'below-{0}.png'.format(datetime.now())
            out_dir = "{0}/{1}".format(self._out_dir, out_name)

            cv2.imwrite(out_dir, tile_current)

        return tile_current

    def __report_stitching(self, tile1):
        print("Stitching: {0}".format(tile1))

    # Assumes image directory contains only the images we're tiling
    # Loads images into stitcher
    def _load_images(self, image_dir):
        print(image_dir)
        image_dict = {None: None}
        image_dir_l = listdir(image_dir)
        num_images = len(image_dir_l)
        image_count = 1

        for filename in image_dir_l:
            abs_dir = "{0}/{1}".format(image_dir, filename)
            if self._verbose:
                print("Loading image [{0}/{1}]: \n\t{2}".format(image_count, num_images, abs_dir))

            img = cv2.imread(abs_dir, cv2.IMREAD_COLOR)
            image_dict[filename] = img

            image_count += 1

        return image_dict

    def __repr__(self):
        return self._image_dir, self._node_set
