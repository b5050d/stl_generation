# stl_generation
A repo to house my stl generation methods and experiments

Can start with just converting png to edges

Alright so this project has a few components
- Image preparation (images move from png to black and white, to binary matrix (1's and 0's))
- Edge collection (matrixes of 1's and 0's are converted to edges) / Edge processing into list of data points
- tessellation of data points into triangles
- building the geometry of the stl file
- writing the stl file



# The Rules of the Triangles (for STL)
- Triangles have 3x points each with 3 coords. Triangles also have a 3x vector that points outward from the shape
- Triangles are listed in ascending vertical order as much as is possible
- Triangles points are listed counter clockwise

