
import os, sys
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions
from libraries import read_files_functions
from libraries.cv_globals import top_shapes_dir


im_file = "11"

directory = "videos/street3/resized/min"

location_fname = im_file + "_loc.txt"

if len(sys.argv) > 1:
   im_file = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   
   location_fname = im_file + "_loc.txt"

   directory = sys.argv[1]

   print("execute script create_shape_locations.py. filename " + im_file + " directory " + directory )




# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

if os.path.exists(top_shapes_dir + directory + "locations/" ) == False:
   os.makedirs(top_shapes_dir + directory + "locations/")


# returned value has below form
# shapes[shapes_id][pixel_index] = {}
# shapes[shapes_id][pixel_index]['x'] = x
# shapes[shapes_id][pixel_index]['y'] = y
shapes = read_files_functions.rd_shapes_file(im_file, directory)
shape_locations = []
for shapeid in shapes:


   shape_location = pixel_shapes_functions.get_shape_im_locations(im_file, directory, shapes[shapeid], shapeid  )
   # for saving data to file, convert all data into string.
   temp = { shapeid: [] }
   for src_s_loc in shape_location[ list(shape_location.keys())[0] ]:
      temp[shapeid].append( str(src_s_loc) )
   
   
   shape_locations.append( temp ) 
   

print("saving file " + top_shapes_dir + directory + "locations/" + location_fname  )
print()
file = open(top_shapes_dir + directory + "locations/" + location_fname, 'w')
file.write(str(shape_locations))
file.close()
























