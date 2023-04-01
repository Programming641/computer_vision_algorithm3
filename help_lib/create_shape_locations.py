
import os, sys
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions
from libraries import read_files_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir, internal
import pickle
import math


# shapes_type
# normal is the one created by find_shapes
# intnl_spixcShp are shapes that incorporate internal small pixel count shapes
def do_create( im_fname , directory, shapes_type=None ):

   location_fname = im_fname + "_loc.txt"

   # directory is specified but does not contain /
   if directory != "" and directory[-1] != '/':
      directory +='/'

   original_image = Image.open(top_images_dir + directory + im_fname + ".png")
   im_width, im_height = original_image.size

   shape_locations = []
   if shapes_type == "normal":

      if os.path.exists(top_shapes_dir + directory + "locations/" ) == False:
         os.makedirs(top_shapes_dir + directory + "locations/")

      # returned value has below form
      # shapes[shapes_id][pixel_index] = {}
      # shapes[shapes_id][pixel_index]['x'] = x
      # shapes[shapes_id][pixel_index]['y'] = y
      shapes = read_files_functions.rd_shapes_file(im_fname, directory)
      
      for shapeid in shapes:

         shape_location = pixel_shapes_functions.get_shape_im_locations(im_fname, directory, shapes[shapeid], shapeid  )
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
     
      
   
   elif shapes_type == "intnl_spixcShp":
      s_pixcShp_intnl_loc_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/locations/"
      shapes_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/" + "shapes/"
      shapes_dfile = shapes_dir + im_fname + "shapes.data"

      if os.path.exists(s_pixcShp_intnl_loc_dir ) == False:
         os.makedirs(s_pixcShp_intnl_loc_dir)      

   
      with open (shapes_dfile, 'rb') as fp:
         # { '79999': ['79999', ... ], ... }
         # { 'shapeid': [ pixel indexes ], ... }
         shapes = pickle.load(fp)
      fp.close()
   
      for shapeid, pindexes in shapes.items():
         cur_shape_pixels = { }
         for pindex in pindexes:
            cur_shape_pixels[pindex] = {}
            
            y = math.floor( int(pindex) / im_width)
            x  = int(pindex) % im_width 
      
            cur_shape_pixels[pindex]['x'] = x
            cur_shape_pixels[pindex]['y'] = y


         shape_location = pixel_shapes_functions.get_shape_im_locations(im_fname, directory, cur_shape_pixels, shapeid  )
         # for saving data to file, convert all data into string.
         temp = { shapeid: [] }
         for src_s_loc in shape_location[ list(shape_location.keys())[0] ]:
            temp[shapeid].append( str(src_s_loc) )

        
         shape_locations.append( temp ) 

      print("saving file " + s_pixcShp_intnl_loc_dir + location_fname  )
      print()
      file = open(s_pixcShp_intnl_loc_dir + location_fname, 'w')
      file.write(str(shape_locations))
      file.close()


     
   else:
      print("ERROR at help_lib/create_shape_locations.py unsupported shapes_type " + shapes_type )
      sys.exit()




if __name__ == '__main__':
   im1file = "14"
   directory = "videos/street3/resized/min"
   
   do_create( im1file, directory, "normal" )

























