# SkyTile - slin63@illinois.edu

## Written for ABE498 - Field Robotics at UIUC.

Images are converted into “nodes” containing GPS information as well as links to nodes geographically above, below, and to the right of the current node (figure 3).

The algorithm picks a root node at an extreme location and recursively finds all adjacent nodes from that first root (traversing up, down, then right). The final result is a collection of doubly-linked nodes whose linkages represent the actual geographical shapes of their corresponding image files.
