# find staying large shapes between frames.py
# if pixel changes ocurr only a little inside the shape and not at the boundaries, then this likely implies that
# shape is still at the same location.
import tkinter
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions, same_shapes_btwn_frames, read_files_functions, image_functions, pixel_functions
from libraries.cv_globals import  top_shapes_dir, top_images_dir, styLshapes, spixc_shapes, internal, Lshape_size
import pickle
import math
import winsound
import sys, os

###########################                    user input begin                ##################################
im1file = "26"
directory = "videos/street3/resized/min1"
im2file = "27"
shapes_type = "intnl_spixcShp"
###########################                    user input end                  ##################################

if len(sys.argv) > 1:
   im1file = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   im2file = sys.argv[1][0: len( sys.argv[1] ) - 4 ]
   directory = sys.argv[3]
   
   shapes_type = "intnl_spixcShp"

   print("execute script algorithms/styLshapes/" + str( os.path.basename(__file__) ) +  " im1file " +  im1file  + " im2file " + im2file + " directory " + directory )



# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

original_image = Image.open(top_images_dir + directory + im1file + ".png")
im_width, im_height = original_image.size

if shapes_type == "normal":
   print("shapes_type normal is not supported")
   sys.exit()
   
   
elif shapes_type == "intnl_spixcShp":

   s_pixcShp_intnl_dir = top_shapes_dir + directory + spixc_shapes  + "/" + internal + "/"
   
   s_pixcShp_intnl_loc_dir = s_pixcShp_intnl_dir + "locations/"
   im1shapes_locations_path = s_pixcShp_intnl_loc_dir + im1file + "_loc.data"   
   im2shapes_locations_path = s_pixcShp_intnl_loc_dir + im2file + "_loc.data"  

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

   im1shape_by_pindex = {}
   for shapeid in im1shapes:
      for pindex in im1shapes[shapeid]:
         im1shape_by_pindex[pindex] = shapeid

   im2shape_by_pindex = {}
   for shapeid in im2shapes:
      for pindex in im2shapes[shapeid]:
         im2shape_by_pindex[pindex] = shapeid

   
else:
   print("ERROR at " + str( os.path.basename(__file__) ) + " shapes_type " + shapes_type + " is not supported")
   sys.exit()



pixch_dir = top_shapes_dir + directory + "pixch/data/"
pixch_file = pixch_dir + im1file + "." + im2file + ".data"
with open (pixch_file, 'rb') as fp:
   #  {'378', '20048', ...}
   pixch = pickle.load(fp)
fp.close()

im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im1file, directory, shapes_type=shapes_type, min_colors=True)
im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im2file, directory, shapes_type=shapes_type, min_colors=True)

result_matches = []

progress_counter = len( im1shapes )
for im1shapeid in im1shapes:
   progress_counter -= 1
   if len( im1shapes[ im1shapeid ] ) < Lshape_size:
      continue

   print( str( progress_counter ) + " remaining" )

   overlapped_im2shapes = {}
   overlapped_pixels = {}
   for im1pixel in im1shapes[im1shapeid]:
      overlapped_im2shapeid = im2shape_by_pindex[im1pixel]
      
      if im1shapes_colors[im1shapeid] != im2shapes_colors[overlapped_im2shapeid]:
         continue
      
      if overlapped_im2shapeid not in overlapped_im2shapes.keys():
         overlapped_im2shapes[ overlapped_im2shapeid ] = 1
         overlapped_pixels[ overlapped_im2shapeid ] = set()
      else:
         overlapped_im2shapes[ overlapped_im2shapeid ] += 1
      
      overlapped_pixels[ overlapped_im2shapeid ].add( im1pixel )
   
   most_overlapped_count = 0
   most_overlapped_shapeid = None
   for shapeid, overlapped_count in overlapped_im2shapes.items():
      
      if overlapped_count > most_overlapped_count:
         most_overlapped_count = overlapped_count
         most_overlapped_shapeid = shapeid
   
   if most_overlapped_count / len( im1shapes[im1shapeid] ) >= 0.6:
      result_matches.append( (im1shapeid, most_overlapped_shapeid) )
   
   if im1shapeid == "4097" and most_overlapped_shapeid == "4906":
      
      save_im1filepath = top_shapes_dir + directory + "temp/im1.png"
      image_functions.cr_im_from_pixels( im2file, directory, im1shapes[ im1shapeid ], pixels_rgb=(255,0,0), save_filepath=save_im1filepath )
      
      im2pixch_overlapped_pixels = set()
      for pixel in im2shapes[ most_overlapped_shapeid ]:
         if pixel in pixch:
            im2pixch_overlapped_pixels.add( pixel )

      image_functions.cr_im_from_pixels( "26", directory, im2pixch_overlapped_pixels, pixels_rgb=(255,255,0), input_im=save_im1filepath )


      save_im2filepath = top_shapes_dir + directory + "temp/im2.png"
      image_functions.cr_im_from_pixels( im1file, directory, im2shapes[ most_overlapped_shapeid ], pixels_rgb=(0,0,255), save_filepath=save_im2filepath )
      
      im1pixch_overlapped_pixels = set()
      for pixel in im1shapes[ im1shapeid ]:
         if pixel in pixch:
            im1pixch_overlapped_pixels.add( pixel )

      image_functions.cr_im_from_pixels( "26", directory, im1pixch_overlapped_pixels, pixels_rgb=(255,255,0), input_im=save_im2filepath )

      
      
      '''
      im1shouldve_matched_pixels = set()
      for pixel in im2shapes["43613"]:
         if pixel in pixch:
            im1shouldve_matched_pixels.add( pixel )
      
      image_functions.cr_im_from_pixels( "27", directory, im1shouldve_matched_pixels, pixels_rgb=(255,255,0) )  
      
      im2shouldve_matched_pixels = set()
      for pixel in im1shapes["44054"]:
         if pixel in pixch:
            im2shouldve_matched_pixels.add( pixel )
      
      image_functions.cr_im_from_pixels( "26", directory, im2shouldve_matched_pixels, pixels_rgb=(255,255,0) )
      '''



staying_Lshapes_Ddir = top_shapes_dir + directory + styLshapes + "/2/data/"
if os.path.exists(staying_Lshapes_Ddir ) == False:
   os.makedirs(staying_Lshapes_Ddir )

staying_Lshapes1to2_dfile = staying_Lshapes_Ddir + im1file + "." + im2file + ".data"
with open(staying_Lshapes1to2_dfile, 'wb') as fp:
   pickle.dump(result_matches, fp)
fp.close()

















