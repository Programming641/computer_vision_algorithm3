
import os, sys
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions
from libraries import read_files_functions
from libraries.cv_globals import top_shapes_dir


# directory should be as follows.
# video directory/pixch example "videos/cat/resized/min/pixch"
def do_create( im_file, im2file, directory ):

   # check if directory's last directory is "pixch". if not add pixch directory to it
   if directory[-1] != "/":
      add_slash = True
      pixch_word_len = 5
      pixch_word_end = len( directory )
   else:
      add_slash = False
      pixch_word_len = 6
      pixch_word_end = len( directory ) - 1    # excluding "/"
   
   pixch_word_start = len( directory ) - pixch_word_len
   
   pixch_word = directory[ pixch_word_start: pixch_word_end ]
  
   if pixch_word == "pixch":
      if add_slash is True:
         directory += "/"
   else:
      if add_slash is True:
         directory += "/pixch/"
      else:
         directory += "pixch/"
   
   location_fname = im_file + "." + im2file + "_loc.txt"




   if os.path.exists(top_shapes_dir + directory + "locations/" ) == False:
      os.makedirs(top_shapes_dir + directory + "locations/")

   pixch_fname = im_file + "." + im2file

   # returned value has below form
   # shapes[shapes_id][pixel_index] = {}
   # shapes[shapes_id][pixel_index]['x'] = x
   # shapes[shapes_id][pixel_index]['y'] = y
   shapes = read_files_functions.rd_shapes_file(pixch_fname, directory)
   shape_locations = []
   for shapeid in shapes:


      shape_location = pixel_shapes_functions.get_shape_im_locations(pixch_fname, directory, shapes[shapeid], shapeid  )
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



if __name__ == '__main__':
   im1file = ""
   im2file = ""
   directory = ""
   
   do_create( im1file, im2file, directory )

































