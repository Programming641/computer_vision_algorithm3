
from PIL import Image
import pickle
import math
import copy
import os, sys
from libraries.cv_globals import top_temp_dir, top_shapes_dir, top_images_dir, internal, pixch_sty_dir, scnd_stage_alg_dir, snd_stg_alg_shp_nbrs_dir
from libraries.cv_globals import only_nfnd_pixch_sty_dir
from libraries.cv_globals import frth_smallest_pixc, Lshape_size, third_smallest_pixc
from libraries import read_files_functions, pixel_shapes_functions, image_functions, pixel_functions, same_shapes_functions, same_shapes_btwn_frames
import winsound


directory = "videos/street3/resized/min"
im1file = "12"
im2file = "13"
shapes_type = "intnl_spixcShp"


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'


scnd_stg_alg_shp_nbrs_dir = top_shapes_dir + directory + snd_stg_alg_shp_nbrs_dir + "/" + only_nfnd_pixch_sty_dir + "/"
with open(scnd_stg_alg_shp_nbrs_dir + im1file + "." + im2file + "." + im1file + ".data",  'rb') as fp:
   # [[['2072', '867', '1669', '2080', '53280'], ['1236', '8439', '13231', '44819', '57316']], ... ]
   # [ [ [ image1 shapeids ], [ image2 shapeids ] ], ... ]
   shapes_neighbors_matches = pickle.load(fp)
fp.close()


original_image = Image.open(top_images_dir + directory + im1file + ".png")
im_width, im_height = original_image.size

im1shapes_boundaries = {}
im2shapes_boundaries = {}

if shapes_type == "normal":
   print("ERROR at " + str( os.path.basename(__file__) ) + " shapes_type " + shapes_type + " is not supported")
   sys.exit()   

elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" +  internal + "/"
   
   shapes_dir = s_pixcShp_intnl_dir + "shapes/"
   shapes_dfile = shapes_dir + im1file + "shapes.data"
   im2shapes_dfile = shapes_dir + im2file + "shapes.data"

   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()
   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()    


   # get boundary pixels of all shapes
   for shapeid in im1shapes:
      cur_shape_pixels = set()
      for pindex in im1shapes[shapeid]:
            
         y = math.floor( int(pindex) / im_width)
         x  = int(pindex) % im_width 
      
         cur_shape_pixels.add( (x,y) )

      im1shapes[shapeid] = cur_shape_pixels
      # [(104, 54), (105, 54), (105, 55), (105, 56), (105, 57)]
      im1shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels(cur_shape_pixels )
      

      

   # get boundary pixels of all shapes
   for shapeid in im2shapes:
      cur_shape_pixels = set()
      for pindex in im2shapes[shapeid]:
            
         y = math.floor( int(pindex) / im_width)
         x  = int(pindex) % im_width 
      
         cur_shape_pixels.add( (x,y) )

      im2shapes[shapeid] = cur_shape_pixels

      im2shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels(cur_shape_pixels )


for shapes_neighbors_match in shapes_neighbors_matches:
   # shapes_neighbors_match -> [['2072', '867', '1669', '2080', '53280'], ['1236', '8439', '13231', '44819', '57316']]
   
   
   cur_im1pixels = set()
   cur_im1boundaries = set()
   for im1shapeid in shapes_neighbors_match[0]:
      cur_im1boundaries |= set( im1shapes_boundaries[im1shapeid] )
      
      cur_im1pixels |= im1shapes[im1shapeid]

   cur_im2pixels = set()
   cur_im2boundaries = set()
   for im2shapeid in shapes_neighbors_match[1]:
      cur_im2boundaries |= set( im2shapes_boundaries[im2shapeid] )
      
      cur_im2pixels |= im2shapes[im2shapeid]

   shape_ids = ( shapes_neighbors_match[0][0], shapes_neighbors_match[1][0] )
   
   filenames = [ im1file, im2file ]

   #relpos_result = same_shapes_btwn_frames.boundary_rel_pos(cur_im1boundaries, cur_im2boundaries, filenames, directory, shapeids=None)

   boundary_result = same_shapes_btwn_frames.process_boundaries(cur_im1boundaries, cur_im2boundaries, shape_ids, filenames)
   boundary_result -= len( cur_im1pixels )
   #result = same_shapes_btwn_frames.find_shapes_in_diff_frames(cur_im1pixels, cur_im2pixels,  "consecutive_count", shape_ids)    

   #print( relpos_result )

   if boundary_result < -200:
      continue

   #image_functions.cr_im_from_shapeslist2( im1file, directory, shapes_neighbors_match[0], save_filepath=None , shapes_rgb=(255,0,0) )
   #image_functions.cr_im_from_shapeslist2( im2file, directory, shapes_neighbors_match[1], save_filepath=None , shapes_rgb=(255,0,0) )






frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)





















