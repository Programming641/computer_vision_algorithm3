
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

im2 = Image.open(top_images_dir + directory + im2file + ".png" )
im2pxls = im2.getdata()

print("im2pxls len " + str( len(im2pxls) ) )

shapes_dir = top_shapes_dir + directory  + "shapes/"
shapes_dfile = shapes_dir + im1file + "shapes.data"
with open (shapes_dfile, 'rb') as fp:
   # { 79999: [79999, ... ], ... }
   # { shapeid: [ pixel indexes ], ... }
   im1shapes = pickle.load(fp)
fp.close()

im1shapeid_by_pindex = {}
for shapeid in im1shapes:
   for pindex in im1shapes[shapeid]:
      im1shapeid_by_pindex[pindex] = shapeid

shp_by_index_dir = shapes_dir + 'shapeids_by_pindex/'
shp_by_index_dfile = shp_by_index_dir + im1file + ".data"
with open (shp_by_index_dfile, 'rb') as fp:
   # { pindex: { shapeids }, ... }
   im1shapeids_by_pindex = pickle.load(fp)
fp.close()


original_image = Image.open(top_images_dir + directory + im1file + ".png")
im_width, im_height = original_image.size

frth_smallest_pixc = cv_globals.get_frth_smallest_pixc( im1.size )


shapes_dfile2 = shapes_dir + im2file + "shapes.data"
with open (shapes_dfile2, 'rb') as fp:
   # { 79999: [79999, ... ], ... }
   # { shapeid: [ pixel indexes ], ... }
   im2shapes = pickle.load(fp)
fp.close()

im2shapeid_by_pindex = {}
for shapeid in im2shapes:
   for pindex in im2shapes[shapeid]:
      im2shapeid_by_pindex[pindex] = shapeid

shp_by_index_dfile2 = shp_by_index_dir + im2file + ".data"
with open (shp_by_index_dfile2, 'rb') as fp:
   # { pindex: { shapeids }, ... }
   im2shapeids_by_pindex = pickle.load(fp)
fp.close()



template_folder = top_shapes_dir + directory  + "template/"
result_im1dir = template_folder + im1file + "." + im2file + "." + im1file + "/"
# delete and create folder
if os.path.exists(result_im1dir) == True:
   shutil.rmtree(result_im1dir)
os.makedirs(result_im1dir)

result_im2dir = template_folder + im1file + "." + im2file + "." + im2file + "/"
# delete and create folder
if os.path.exists(result_im2dir) == True:
   shutil.rmtree(result_im2dir)
os.makedirs(result_im2dir)


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


def get_opposite_shapes( opposite_im, pixels, enough_pixels_len ):
   opposite_im_shapes = {}
   
   for pindex in pixels:
      for opposite_shapeid in im_shapeids_by_pindex[opposite_im][pindex]:

         if opposite_shapeid not in opposite_im_shapes.keys():
            opposite_im_shapes[ opposite_shapeid ] = set()
            opposite_im_shapes[ opposite_shapeid ].add(pindex)

      else:
         opposite_im_shapes[ opposite_shapeid ].add(pindex)      


   enough_matched_opposite_im_shapeids = { temp_shapeid for temp_shapeid in opposite_im_shapes if len( opposite_im_shapes[temp_shapeid] ) >= enough_pixels_len }
      
   # { shapeid: { matched pixels }, ... }
   matched_opposite_im_shapes = {}
   for opposite_shapeid in opposite_im_shapes:
      if len( opposite_im_shapes[opposite_shapeid] ) / len( im_shapes[opposite_im][opposite_shapeid] ) < opposite_im_match_threshold or \
         opposite_shapeid not in enough_matched_opposite_im_shapeids :
         continue

      matched_opposite_im_shapes[opposite_shapeid] = opposite_im_shapes[opposite_shapeid]


   return matched_opposite_im_shapes




move_amount = 16
matched_color = ( 255, 0, 0 )
match_threshold = 0.6
opposite_im_match_threshold = 0.4

# [ { im1shapeid: { matched pindexes } }, { im2shapeid: { matched pindexes }, ... } ]
most_matched_im_shapeid_with_pindexes = [ {}, {} ]
# [ { im1shapeid: ( matched movement ), ... }, { im2shapeid: ( matched movement ), ... } ]
most_matched_im_shape_movements = [ {}, {} ]

im_shapes = [ im1shapes, im2shapes ]
im_shapeids_by_pindex = [ im1shapeids_by_pindex, im2shapeids_by_pindex ]

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
            
            # { pindex: ( r,g,b ), ... }
            moved_image_data = image_functions.move_image( im1pxls, move_RL, move_UD, im1.size, non_image_color )
            
            # [ { im1shapeid: { matched pindexes } }, { im2shapeid: { matched pindexes }, ... } ]
            cur_matched_im_shapeid_with_pindexes = [ {}, {} ]
            
            for pindex in moved_image_data:
               matched_pixel = False
               
               mv_im_color = moved_image_data[pindex]
               im2color = im2pxls[pindex]
   
               if "min" in directory:
                  if mv_im_color == im2color:
                     matched_pixel = True
         
               else:
                  appearance_diff = pixel_functions.compute_appearance_difference(mv_im_color, im2color )
                  if appearance_diff is False:
                     # same color
                     matched_pixel = True        

               if matched_pixel is True:
                  for im1or2 in range(2):
                     
                     for cur_im_shapeid in im_shapeids_by_pindex[im1or2][pindex]:
                        if cur_im_shapeid not in cur_matched_im_shapeid_with_pindexes[im1or2].keys():
                           cur_matched_im_shapeid_with_pindexes[im1or2][ cur_im_shapeid ] = set()
                           cur_matched_im_shapeid_with_pindexes[im1or2][ cur_im_shapeid ].add( pindex )
                        else:
                           cur_matched_im_shapeid_with_pindexes[im1or2][ cur_im_shapeid ].add( pindex )


            for im1or2 in range(2):
               opposite_im = abs( im1or2 - 1 )
               
               for im_shapeid in cur_matched_im_shapeid_with_pindexes[im1or2]:

                  cur_im_matched_pixels = cur_matched_im_shapeid_with_pindexes[im1or2][im_shapeid]
                  
                  if len( im_shapes[im1or2][im_shapeid] ) < frth_smallest_pixc:
                     continue
                  
                  if len(cur_im_matched_pixels) / len( im_shapes[im1or2][im_shapeid] ) < match_threshold:
                     continue

                  needed_pixels_for_opposite_match = len( im_shapes[im1or2][im_shapeid] ) * 0.4
                  # { shapeid: { matched pixels }, ... }
                  opposite_im_shapes = get_opposite_shapes( opposite_im, cur_im_matched_pixels, needed_pixels_for_opposite_match )
                  if len(opposite_im_shapes) == 0:
                     continue
                  
                  cur_matched_count = sum( [ len( opposite_im_shapes[temp_shapeid] ) for temp_shapeid in opposite_im_shapes ] )

                  if im_shapeid not in most_matched_im_shapeid_with_pindexes[im1or2].keys():
                     most_matched_im_shapeid_with_pindexes[im1or2][im_shapeid] = opposite_im_shapes
                     
                     most_matched_im_shape_movements[im1or2][im_shapeid] = ( move_RL, move_UD )
                  
                  else:
                     most_matched_opposite_im_shapes = most_matched_im_shapeid_with_pindexes[im1or2][im_shapeid] 
                     most_matched_count = sum( [ len( most_matched_opposite_im_shapes[temp_shapeid] ) for temp_shapeid in most_matched_opposite_im_shapes ] )
                     
                     if cur_matched_count > most_matched_count:
                        most_matched_im_shapeid_with_pindexes[im1or2][im_shapeid] = opposite_im_shapes
               
                        most_matched_im_shape_movements[im1or2][im_shapeid] = ( move_RL, move_UD )
                     



      
for im1or2 in range(2):
   opposite_im = abs( im1or2 - 1 )
   
   if im1or2 == 0:
      save_im_dir = result_im1dir
   else:
      save_im_dir = result_im2dir
   
   image_functions.cr_im_from_shapeslist2( str( int(im1file) + im1or2 ), directory, most_matched_im_shapeid_with_pindexes[im1or2].keys(), shapes_rgbs=non_image_colors )
   
   opposite_im_shapeids = set()
   for shapeid in most_matched_im_shapeid_with_pindexes[im1or2]:
      most_matched_opposite_im_shapes = most_matched_im_shapeid_with_pindexes[im1or2][shapeid]    
      
      opposite_im_shapeids |= set( most_matched_opposite_im_shapes.keys() )
   
   image_functions.cr_im_from_shapeslist2( str( int(im1file) + opposite_im ), directory, opposite_im_shapeids, shapes_rgbs=non_image_colors )
   '''
   for shapeid in most_matched_im_shapeid_with_pindexes[im1or2]:
      most_matched_opposite_im_shapes = most_matched_im_shapeid_with_pindexes[im1or2][shapeid] 
      
      save_im_fname = save_im_dir + str(shapeid) + ".png"
      
      save_opposite_im_fname = save_im_dir + str(shapeid) + ".opposite_im.png"
      
      image_functions.cr_im_from_shapeslist2( str( int(im1file) + im1or2 ), directory, [shapeid], save_filepath=save_im_fname , shapes_rgbs=non_image_colors )
      image_functions.cr_im_from_shapeslist2( str( int(im1file) + opposite_im ), directory, most_matched_opposite_im_shapes.keys(), save_filepath=save_opposite_im_fname, shapes_rgbs=non_image_colors )
   '''   

template_dir = top_shapes_dir + directory + "template/"
image_template_dir = template_dir + "image_pixels/"

image_template_ddir = image_template_dir + "data/"

if os.path.exists(template_dir ) == False:
   os.makedirs(template_dir )
if os.path.exists(image_template_dir ) == False:
   os.makedirs(image_template_dir )
if os.path.exists(image_template_ddir ) == False:
   os.makedirs(image_template_ddir )


image_template_dfile = image_template_ddir + im1file + "." + im2file + ".data"
with open(image_template_dfile, 'wb') as fp:
   pickle.dump(final_matched_shapes, fp)
fp.close()



























