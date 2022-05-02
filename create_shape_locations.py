
import os
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions
from libraries import read_files_functions
from libraries.cv_globals import proj_dir

shapes_dir = proj_dir + "/shapes/"


im_file = "1clrgrp"

directory = "videos/street"

location_fname = im_file + "_loc.txt"

# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

if os.path.exists(shapes_dir + directory + "locations/" ) == False:
   os.makedirs(shapes_dir + directory + "locations/")


# returned value has below form
# shapes[shapes_id][pixel_index] = {}
# shapes[shapes_id][pixel_index]['x'] = x
# shapes[shapes_id][pixel_index]['y'] = y
shapes = read_files_functions.rd_shapes_file(im_file, directory)
shape_locations = []
for shapeid in shapes:


   print("shapeid " + str(shapeid ) )


   shape_location = pixel_shapes_functions.get_shape_im_locations(im_file, directory, shapes[shapeid], shapeid  )
   # for saving data to file, convert all data into string.
   temp = { shapeid: [] }
   for src_s_loc in shape_location[ list(shape_location.keys())[0] ]:
      temp[shapeid].append( str(src_s_loc) )
   
   
   shape_locations.append( temp ) 
   

file = open(shapes_dir + directory + "locations/" + location_fname, 'w')
file.write(str(shape_locations))
file.close()
























