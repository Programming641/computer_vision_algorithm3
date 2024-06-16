
from PIL import Image
import pickle, copy

import os, sys, shutil
from libraries.cv_globals import top_shapes_dir, top_images_dir, internal
from libraries import image_functions, pixel_shapes_functions, pixel_functions, same_shapes_functions
from libraries import cv_globals


directory = "videos/street3/resized/min1"
im1file = "25"
im2file = "26"


if len(sys.argv) > 1:
   im1file = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   im2file = sys.argv[1][0: len( sys.argv[1] ) - 4 ]

   directory = sys.argv[3]

   print("execute script template/match_by_whole_image_pixels_template.py. file1 " + im1file + " file2 " + im2file + " directory " + directory )




# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'


im1 = Image.open(top_images_dir + directory + im1file + ".png" )
im1pxls = im1.getdata()
im1width, im1height = im1.size

frth_smallest_pixc = cv_globals.get_frth_smallest_pixc( im1.size )

shapes_dir = top_shapes_dir + directory  + "shapes/"
shapes_dfile = shapes_dir + im1file + "shapes.data"
with open (shapes_dfile, 'rb') as fp:
   # { 79999: [79999, ... ], ... }
   # { shapeid: [ pixel indexes ], ... }
   im1shapes = pickle.load(fp)
fp.close()

shp_by_index_dir = shapes_dir + 'shapeids_by_pindex/'
shp_by_index_dfile1 = shp_by_index_dir + im1file + ".data"
with open (shp_by_index_dfile1, 'rb') as fp:
   # { pindex: { shapeids }, ... }
   im1shapeids_by_pindex = pickle.load(fp)
fp.close()

shapes_dfile2 = shapes_dir + im2file + "shapes.data"
with open (shapes_dfile2, 'rb') as fp:
   # { 79999: [79999, ... ], ... }
   # { shapeid: [ pixel indexes ], ... }
   im2shapes = pickle.load(fp)
fp.close()

shp_by_index_dfile2 = shp_by_index_dir + im2file + ".data"
with open (shp_by_index_dfile2, 'rb') as fp:
   # { pindex: { shapeids }, ... }
   im2shapeids_by_pindex = pickle.load(fp)
fp.close()


default_clr_threshold = cv_globals.get_default_color_threshold()
   
color_variation_file = top_shapes_dir + directory + "data/color_variations.data"
with open (color_variation_file, 'rb') as fp:
   # [ (r,g,b), ... ]
   color_variations = pickle.load(fp)
fp.close()  
   
rgb_step = image_functions.get_rgb_step( len(color_variations) )

# for the amount of moved pixel, non image pixels need to fill original pixel    
non_image_colors = image_functions.get_non_existing_colors( color_variations, default_clr_threshold, rgb_steps=rgb_step )
non_image_colors = list(non_image_colors)
non_image_color = non_image_colors[0]

move_amount = 16
match_threshold = 0.6
opposite_im_match_threshold = 0.4

if "min" in directory:
   min_colors = True
else:
   min_colors = False

im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im2file, directory, min_colors=min_colors)


# { shapeid: pixels, ... }
most_matched_im2shapes = {}
most_matched_im1movements = {}
for shapeid in im2shapes:
  most_matched_im2shapes[shapeid] = set()

# { im2shapeid: { matched im1shapeids }, ... }
im2shape_matched_im1shapeids = {}

def get_matched_im1shapeid( matched_im2shape_pixels, movement, im2pixels ):
   
   overlapped_im1shapeids = set()
   for pindex in matched_im2shape_pixels:
      original_position = ( movement[0] * -1, movement[1] * -1 )
      # matched image1 pixels
      orig_pindex = pixel_functions.get_pindex_with_xy_input( pindex, original_position, im1width )

      overlapped_im1shapeids |= im1shapeids_by_pindex[orig_pindex]
      
   return overlapped_im1shapeids
      





for pos_neg_RL in [ 1, -1 ]:
   if pos_neg_RL == 1:
      start_position_RL = 0
   else:
      start_position_RL = 1
   
   for move_RL in range( start_position_RL, move_amount ):
      move_RL *= pos_neg_RL
      
      for pos_neg_UD in [ 1, - 1 ]:
         if pos_neg_UD == 1:
            start_position_UD = 0
         else:
            start_position_UD = 1
         
         for move_UD in range( start_position_UD, move_amount ):
            move_UD *= pos_neg_UD
      
            print("move_RL " + str(move_RL) + " move_UD " + str(move_UD) )
            
            matched_pixels = set()
            
            # { pindex: ( r,g,b ), ... }
            moved_image_data = image_functions.move_image( im1pxls, move_RL, move_UD, im1.size, non_image_color )
            '''
            image_pixels_len = im1width * im1height
            debug_image_data = []
            for pindex in range(image_pixels_len):
               debug_image_data.append( moved_image_data[pindex] )
            
            
            im2.putdata( debug_image_data )
            im2.show()
            '''
            
            
            for pindex in moved_image_data:
               pixel_matched = False
               
               mv_im_color = moved_image_data[pindex]
               
               for occupied_shapeid in im2shapeids_by_pindex[pindex]:
                  im2color = im2shapes_colors[occupied_shapeid]
   
                  if "min" in directory:
                     if mv_im_color == im2color:
                        pixel_matched = True
                        break
         
                  else:
                     appearance_diff = pixel_functions.compute_appearance_difference(mv_im_color, im2color )
                     if appearance_diff is False:
                        # same color
                        pixel_matched = True
                        break                        

               if pixel_matched is True:
                  matched_pixels.add(pindex)
            
            #image_functions.cr_im_from_pixels( im2file, directory, matched_pixels, pixels_rgb=non_image_color )

            for im2shapeid in im2shapes:
               if len(im2shapes[im2shapeid]) < frth_smallest_pixc:
                  continue

               im2shape_pixels = set( im2shapes[im2shapeid] )
               matched_im2shape_pixels = im2shape_pixels.intersection( matched_pixels )
               '''
               image_functions.cr_im_from_pixels( im2file, directory, matched_im2shape_pixels, pixels_rgb=non_image_color )
               debug_matched_im1pixels = set()
               for pixel in matched_im2shape_pixels:
                  original_position = ( move_RL * -1, move_UD * -1 )
                  # matched image1 pixels
                  orig_pindex = pixel_functions.get_pindex_with_xy_input( pixel, original_position, im1width )
                  if orig_pindex in im1shapes[8890]:
                     debug_matched_im1pixels.add(orig_pindex)
               
               image_functions.cr_im_from_pixels( im1file, directory, debug_matched_im1pixels, pixels_rgb=non_image_color )
               '''
               if len(matched_im2shape_pixels) / len(im2shape_pixels) >= match_threshold and len(matched_im2shape_pixels) > len( most_matched_im2shapes[im2shapeid] ):
               
                  matched_im1shapeids = get_matched_im1shapeid( matched_im2shape_pixels, ( move_RL, move_UD ), im2shapes[im2shapeid]  )
                  
                  most_matched_im2shapes[im2shapeid] = matched_im2shape_pixels
                  most_matched_im1movements[im2shapeid] = ( move_RL, move_UD )
                  
                  im2shape_matched_im1shapeids[im2shapeid] = matched_im1shapeids
               
               matched_pixels = matched_pixels.difference( im2shape_pixels )

            
            
            #image_functions.cr_im_from_pixels( im2file, directory, matched_pixels, pixels_rgb=non_image_color )






template_ddir = top_shapes_dir + directory  + "template/data/"
if os.path.exists(template_ddir ) == False:
   os.makedirs(template_ddir )

result_fpath = template_ddir + "3.data"
with open(result_fpath, 'wb') as fp:
   pickle.dump(most_matched_im2shapes, fp)
fp.close()

movement_fpath = template_ddir + "3movement.data"
with open(movement_fpath, 'wb') as fp:
   pickle.dump(most_matched_im1movements, fp)
fp.close()

matched_im1shapeids_fpath = template_ddir + "3matched_im1shapeids.data"
with open(matched_im1shapeids_fpath, 'wb') as fp:
   pickle.dump(im2shape_matched_im1shapeids, fp)
fp.close()


















