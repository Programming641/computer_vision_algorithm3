
import os, sys
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions, pixel_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir, internal
import pickle
import math



def do_create( im_fname , directory ):

   location_fname = im_fname + "_loc.data"

   # directory is specified but does not contain /
   if directory != "" and directory[-1] != '/':
      directory +='/'

   original_image = Image.open(top_images_dir + directory + im_fname + ".png")
   im_width, im_height = original_image.size

   shapes_dir = top_shapes_dir + directory + "shapes/"
   location_dir = shapes_dir + "locations/" 
   if os.path.exists(location_dir) == False:
      os.makedirs(location_dir)
      
   shapes_dfile = shapes_dir + im_fname + "shapes.data"  
   with open (shapes_dfile, 'rb') as fp:
      # {  97199: [97199, 96659, 96658, 96657, 96119, 96118, 96117, 95579, 95578, 96116], ... }
      # { shapeid: [ pixel indexes ], ... }
      shapes = pickle.load(fp)
   fp.close()
      
      
   shapes_locations = {}
   for shapeid, pindexes in shapes.items():
      cur_shape_pixels = set()
      for pindex in pindexes:
         xy = pixel_functions.convert_pindex_to_xy( pindex, im_width )

         cur_shape_pixels.add( xy )

      temp_shape_location = pixel_shapes_functions.get_shape_im_locations(im_fname, directory, cur_shape_pixels, shapeid  )
      # for saving data to file, convert all data into string.
      shapes_locations[shapeid] = []
      for src_s_loc in temp_shape_location[ list(temp_shape_location.keys())[0] ]:
         shapes_locations[shapeid].append( int(src_s_loc) )

   with open(location_dir + location_fname , 'wb') as fp:
      pickle.dump(shapes_locations, fp)
   fp.close()


def do_update( im_fname , directory, target_shapeids ):

   location_fname = im_fname + "_loc.data"

   # directory is specified but does not contain /
   if directory != "" and directory[-1] != '/':
      directory +='/'

   original_image = Image.open(top_images_dir + directory + im_fname + ".png")
   im_width, im_height = original_image.size

   shapes_dir = top_shapes_dir + directory + "shapes/"
   location_dir = shapes_dir + "locations/" 
      
   shapes_dfile = shapes_dir + im_fname + "shapes.data"  
   with open (shapes_dfile, 'rb') as fp:
      # {  97199: [97199, 96659, 96658, 96657, 96119, 96118, 96117, 95579, 95578, 96116], ... }
      # { shapeid: [ pixel indexes ], ... }
      shapes = pickle.load(fp)
   fp.close()

   with open (shapes_dfile, 'rb') as fp:
      # {  97199: [97199, 96659, 96658, 96657, 96119, 96118, 96117, 95579, 95578, 96116], ... }
      # { shapeid: [ pixel indexes ], ... }
      shapes = pickle.load(fp)
   fp.close()

   with open (location_dir + location_fname, 'rb') as fp:
      # { shapeid: [ 1,2,5, ... ], .... }
      shapes_locations = pickle.load(fp)
   fp.close()

   for shapeid in target_shapeids:
      cur_shape_pixels = set()
      for pindex in shapes[shapeid]:
         xy = pixel_functions.convert_pindex_to_xy( pindex, im_width )

         cur_shape_pixels.add( xy )

      temp_shape_location = pixel_shapes_functions.get_shape_im_locations(im_fname, directory, cur_shape_pixels, shapeid  )
      # for saving data to file, convert all data into string.
      shapes_locations[shapeid] = []
      for src_s_loc in temp_shape_location[ list(temp_shape_location.keys())[0] ]:
         shapes_locations[shapeid].append( int(src_s_loc) )


   with open(location_dir + location_fname , 'wb') as fp:
      pickle.dump(shapes_locations, fp)
   fp.close()


def do_delete( im_fname , directory, target_shapeids ):

   location_fname = im_fname + "_loc.data"

   # directory is specified but does not contain /
   if directory != "" and directory[-1] != '/':
      directory +='/'

   shapes_dir = top_shapes_dir + directory + "shapes/"
   location_dir = shapes_dir + "locations/" 

   with open (location_dir + location_fname, 'rb') as fp:
      # { shapeid: [ 1,2,5, ... ], .... }
      shapes_locations = pickle.load(fp)
   fp.close()

   for shapeid in target_shapeids:
      shapes_locations.pop( shapeid )


   with open(location_dir + location_fname , 'wb') as fp:
      pickle.dump(shapes_locations, fp)
   fp.close()











if __name__ == '__main__':
   
   if len( sys.argv ) >= 2:
      image_filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
      directory = sys.argv[1]
      
      do_create( image_filename, directory )
   else:
   
      im1file = "11"
      directory = "videos/street6/resized/min3"
   
      do_create( im1file, directory )


























