from libraries import pixel_functions, pixel_shapes_functions, image_functions, same_shapes_functions
from libraries import shapes_results_functions, btwn_amng_files_functions, cv_globals

from PIL import Image
import math
import os, sys
import winsound, time
import pickle

from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, styLshapes, styLshapes_wo_pixch


im1file = '32'
im2file = "33"
shapes_type = "intnl_spixcShp"
directory = "videos/street3/resized/min1"

if len(sys.argv) >= 2:
   # excluding .png extension 
   im1file = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   im2file = sys.argv[1][0: len( sys.argv[1] ) - 4 ]
   rest_of_fname = sys.argv[2]
   directory = sys.argv[3]
   
   shapes_type = "intnl_spixcShp"
   
   print("execute pixch/find_pixch_shapes_matches.py"  )
   print("im1file " + im1file + " im2file " + im2file + " directory " + directory )


# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

pixch_ddir = top_shapes_dir + directory + "pixch/data/"
pixch_shapes_file = pixch_ddir + im1file + "." + im2file + "." + im1file + "pixch_shapes.data"
with open (pixch_shapes_file, 'rb') as fp:
   # { '79652': { pixch pindexes }, ... }
   # { shapeid: % of pixch, ... }
   im1pixch_shapes = pickle.load(fp)
fp.close()

pixch_shapes2_file = pixch_ddir + im1file + "." + im2file + "." + im2file + "pixch_shapes.data"
with open (pixch_shapes2_file, 'rb') as fp:
   im2pixch_shapes = pickle.load(fp)
fp.close()


pixch_dfile = pixch_ddir  + im1file + "." + im2file + ".data"
with open (pixch_dfile, 'rb') as fp:
   # {  '34933', '3241', ... }
   pixch = pickle.load(fp)
fp.close()

changed_shapes_dir = top_shapes_dir + directory + "pixch/ch_shapes/pixch_shapes/"
if os.path.exists(changed_shapes_dir ) == False:
   os.makedirs(changed_shapes_dir )
changed_shapes_ddir = changed_shapes_dir + "data/"
if os.path.exists(changed_shapes_ddir ) == False:
   os.makedirs(changed_shapes_ddir )
save_result_fpath = changed_shapes_ddir + im1file + "." + im2file + ".data"

image1 = Image.open(top_images_dir + directory + im1file + ".png")
im_width, im_height = image1.size
image1data = image1.getdata()

image2 = Image.open( top_images_dir + directory + im2file + ".png")
image2data = image2.getdata()

sixth_s_pixc = cv_globals.get_6th_s_pixc( image1.size )

shapes_dir = top_shapes_dir + directory + "shapes/"
shapes_dfile = shapes_dir + im1file + "shapes.data"
   

with open (shapes_dfile, 'rb') as fp:
   # { '79999': ['79999', ... ], ... }
   # { 'shapeid': [ pixel indexes ], ... }
   im1shapes = pickle.load(fp)
fp.close()

boundary_dir = shapes_dir + "boundary/"
boundary_dfile = boundary_dir + im1file + ".data"
with open (boundary_dfile, 'rb') as fp:
   im1shapes_boundaries = pickle.load(fp)
fp.close()

shp_by_index_dir = shapes_dir + 'shapeids_by_pindex/'
shp_by_index_dfile = shp_by_index_dir + im1file + ".data"
with open (shp_by_index_dfile, 'rb') as fp:
   # { pindex: { shapeids }, ... }
   im1shapeids_by_pindex = pickle.load(fp)
fp.close()      


im2shapes_dfile = shapes_dir + im2file + "shapes.data"   
with open (im2shapes_dfile, 'rb') as fp:
   # { '79999': ['79999', ... ], ... }
   # { 'shapeid': [ pixel indexes ], ... }
   im2shapes = pickle.load(fp)
fp.close()

boundary_dfile2 = boundary_dir + im2file + ".data"
with open (boundary_dfile2, 'rb') as fp:
   im2shapes_boundaries = pickle.load(fp)
fp.close()

shp_by_index_dfile2 = shp_by_index_dir + im2file + ".data"
with open (shp_by_index_dfile2, 'rb') as fp:
   # { pindex: { shapeids }, ... }
   im2shapeids_by_pindex = pickle.load(fp)
fp.close()      

im1shape_neighbors_filepath = shapes_dir + "shape_nbrs/" + im1file + "_shape_nbrs.data"
im2shape_neighbors_filepath = shapes_dir + "shape_nbrs/" + im2file + "_shape_nbrs.data"

with open (im1shape_neighbors_filepath, 'rb') as fp:
   im1shapes_neighbors = pickle.load(fp)
fp.close()

with open (im2shape_neighbors_filepath, 'rb') as fp:
   im2shapes_neighbors = pickle.load(fp)
fp.close()

if "min" in directory:
   min_colors = True
else:
   min_colors = False

# { shapeid: (r,g,b), ... }
im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im1file, directory, min_colors=min_colors)
im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im2file, directory, min_colors=min_colors)


def check_shape_size( param_im1shapeid, param_im2shapeid, param_shapes, param_ano_shapes, size_threshold=1 ):
   # check if size is too different
   im1shapes_total = len( param_shapes[param_im1shapeid] )
   im2shapes_total = len( param_ano_shapes[param_im2shapeid] )
      
   im1_2pixels_diff = abs( im1shapes_total - im2shapes_total )
   if im1_2pixels_diff != 0:
      if im1shapes_total > im2shapes_total:
         if im1_2pixels_diff / im2shapes_total > size_threshold:
            return True
      else:
         if im1_2pixels_diff / im1shapes_total > size_threshold:
            return True

   return False      
   
   
# search_shapes -> { shapeid: { pixch pindexes }, ... }
# directly_UD is directly up or down. if it is true, it goes directly up or down with left or right value 0.
def move_pixels( target_shape, target_shape_color, move_direction, directly_UD, step, move_total, search_shapes, search_im_shapes, target_image_data ):


   for move_LR in range( 0, move_total, step ):

      if directly_UD is False and move_LR == 0:
         continue

      move_x = None
      if "left" in move_direction.lower():
         # subtract from x
         if move_LR != 0:
            move_x = move_LR * -1
         else:
            move_x = 0
      
      elif "right" in move_direction.lower():
         # add to x
         if move_LR != 0:
            move_x = move_LR
         else:
            move_x = 0
         
      
      for move_UD in range( 0, move_total, step ):
         move_y = None
         
         if "up" in move_direction.lower():
            # subtract from y
            if move_UD != 0:
               move_y = move_UD * -1
            else:
               move_y = 0
         
         elif "down" in move_direction.lower():
            # add to y
            if move_UD != 0:
               move_y = move_UD
            else:
               move_y = 0

         moved_target_shape = set()
         moved_target_shape_pixch = set()
         for pindex in target_shape:
            xy = pixel_functions.convert_pindex_to_xy( pindex, im_width )
            moved_xy = ( xy[0] + move_x, xy[1] + move_y )

            # check if pixel is out of the image
            if moved_xy[0] < 0 or moved_xy[0] >= im_width or moved_xy[1] < 0 or moved_xy[1] >= im_height:
               continue

            moved_pindex = pixel_functions.convert_xy_to_pindex( moved_xy, im_width )
            
            if min_colors is True:
               if target_shape_color != target_image_data[moved_pindex]:
                  moved_target_shape_pixch.add( moved_pindex )
               else:
                  moved_target_shape.add( moved_pindex )
            
            else:
               appear_diff = pixel_functions.compute_appearance_difference( target_shape_color, target_image_data[moved_pindex] )
               if appear_diff is True:
                  # appearance changed
                  moved_target_shape_pixch.add( moved_pindex )
               else:
                  moved_target_shape.add( moved_pindex )


         
         for search_shapeid in search_shapes:
            matched_pixch = search_shapes[search_shapeid].intersection( moved_target_shape_pixch )
            matched_shape_pixels = set( search_im_shapes[search_shapeid] ).intersection( moved_target_shape )
            
            if len( matched_pixch ) <= 0 or len( matched_shape_pixels ) <= 0:
               continue
            
            t_shape_pixch_matched_percent = len( matched_pixch ) / len( moved_target_shape_pixch )
            t_shape_pix_matched_percent = len( matched_shape_pixels ) / len( moved_target_shape )
            
            if t_shape_pixch_matched_percent >= 0.65 and t_shape_pix_matched_percent >= 0.65:
               # pixch and shape pixels matched. then, check if also the location matches

               #debug_pixels = { pindex: (255,255,0) for pindex in moved_target_shape_pixch }
               #debug_pixels.update( { pindex: ( 255,0,0 ) for pindex in moved_target_shape } )
               #image_functions.cr_im_from_pixels( "26", directory, debug_pixels, with_colors=True )
               
               overlapped_pixels = set()
               overlapped_pixels |= set( search_im_shapes[search_shapeid] ).intersection( moved_target_shape_pixch )
               overlapped_pixels |= set( search_im_shapes[search_shapeid] ).intersection( moved_target_shape )
               
               if len( overlapped_pixels ) / ( len( moved_target_shape_pixch ) + len( moved_target_shape ) ) >= 0.7:
                  return search_shapeid
         
   return None       


def find_matches( target_shapes, target_im_shapes, target_im_shapes_boundaries, search_im_shape_by_pindex, search_im_shapes, target_shapes_colors, 
                  search_shapes_colors, target_image_data, target_shapes_neighbors, search_shapes_neighbors, im1or2 ):

   for target_shapeid in target_shapes:
      if len( target_im_shapes[ target_shapeid ] ) < sixth_s_pixc:
         continue
      
      if len( target_shapes[ target_shapeid ] ) / len( target_im_shapes[ target_shapeid ] )  < 0.4:
         # take shapes that have 40% or more pixch 
         continue
     
      if im1or2 == "im1":
         already_done_shapes = [ temp_shapes for temp_shapes in all_shapes_matches if temp_shapes[0] == target_shapeid ]
         if len( already_done_shapes ) >= 1:
            continue
     
      else:
         already_done_shapes = [ temp_shapes for temp_shapes in all_shapes_matches if temp_shapes[1] == target_shapeid ]
         if len( already_done_shapes ) >= 1:
            continue
   
      #image_functions.cr_im_from_shapeslist2( "25", directory, [target_shapeid], shapes_rgb=(255,0,0) )

      # get image2 shapes that are in the target_shapeid's vicinity
      # { (319, 9), (308, 18), ... }
      t_shape_vicinity_pixels = pixel_shapes_functions.get_shape_vicinity_pixels( target_im_shapes_boundaries[target_shapeid], 15, image1.size, param_shp_type=1 )
   
      # { shapeid: { pixch pindexes }, ... }
      vicinity_search_im_shapes = {}
      for im1shape_vicinity_pixel in t_shape_vicinity_pixels:
         pindex = pixel_functions.convert_xy_to_pindex( im1shape_vicinity_pixel, im_width )
      
         for search_im_vicinity_shapeid in search_im_shape_by_pindex[ pindex ]:
      
            size_diff = check_shape_size( target_shapeid, search_im_vicinity_shapeid, target_im_shapes, search_im_shapes, size_threshold=1 )
            if size_diff is True:
               continue
      
            if min_colors is True:
               if target_shapes_colors[ target_shapeid ] != search_shapes_colors[ search_im_vicinity_shapeid ]:
                  continue
            else:
               appear_diff = pixel_functions.compute_appearance_difference(target_shapes_colors[ target_shapeid ], search_shapes_colors[ search_im_vicinity_shapeid ] )
               if appear_diff is True:
                  # appearance changed
                  continue
      
            search_im_vcnty_shape_pixch = set( search_im_shapes[search_im_vicinity_shapeid] ).intersection( pixch )
       
            vicinity_search_im_shapes[search_im_vicinity_shapeid] = search_im_vcnty_shape_pixch
      '''
      for search_im_vicinity_shapeid in vicinity_search_im_shapes:   
         debug_pixels = { pindex: ( 255,0,0 ) for pindex in search_im_shapes[search_im_vicinity_shapeid] }
         debug_pixels.update( { pindex: (255,255,0) for pindex in vicinity_search_im_shapes[search_im_vicinity_shapeid] } )
      
         image_functions.cr_im_from_pixels( "26", directory, debug_pixels, with_colors=True )
      '''
   
      matched_shapeid = move_pixels( target_im_shapes[ target_shapeid ], target_shapes_colors[target_shapeid], "left_up", True, 2, 15, vicinity_search_im_shapes,
                                  search_im_shapes, target_image_data  )
      if matched_shapeid is None:
         matched_shapeid = move_pixels( target_im_shapes[ target_shapeid ], target_shapes_colors[target_shapeid], "left_down", False, 2, 15, vicinity_search_im_shapes,
                           search_im_shapes, target_image_data  )
         if matched_shapeid is None:
            matched_shapeid = move_pixels( target_im_shapes[ target_shapeid ], target_shapes_colors[target_shapeid], "right_up", True, 2, 15, vicinity_search_im_shapes,
                              search_im_shapes, target_image_data  )
            if matched_shapeid is None:
               matched_shapeid = move_pixels( target_im_shapes[ target_shapeid ], target_shapes_colors[target_shapeid], "right_down", False, 2, 15, vicinity_search_im_shapes,
                                 search_im_shapes, target_image_data  )
   
      if matched_shapeid is not None:
      
         bigger_nbr_count = smaller_nbr_count = None
         if len( target_shapes_neighbors[ target_shapeid ] ) > len( search_shapes_neighbors[ matched_shapeid ] ):
            bigger_nbr_count = len( target_shapes_neighbors[ target_shapeid ] )
            smaller_nbr_count = len( search_shapes_neighbors[ matched_shapeid ] )
            
         else:
            bigger_nbr_count = len( search_shapes_neighbors[ matched_shapeid ] )
            smaller_nbr_count = len( target_shapes_neighbors[ target_shapeid ] )
            
         if smaller_nbr_count / bigger_nbr_count < 0.55:
            # neighbor count is not matched
            continue
      
         nbr_matched_count = 0
         # neighbor matches
         for target_im_nbr in target_shapes_neighbors[ target_shapeid ]:
            for search_im_nbr in search_shapes_neighbors[ matched_shapeid ]:

               size_diff = check_shape_size( target_im_nbr, search_im_nbr, target_im_shapes, search_im_shapes, size_threshold=1 )
               if size_diff is True:
                  continue            
               
               if min_colors is True:
                  if target_shapes_colors[ target_im_nbr ] != search_shapes_colors[ search_im_nbr ]:
                     continue
               else:
                  appear_diff = pixel_functions.compute_appearance_difference( target_shapes_colors[ target_im_nbr ], search_shapes_colors[ search_im_nbr ] )
                  if appear_diff is True:
                     # appearance changed
                     continue
            
               im1nbr_shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( target_im_shapes[target_im_nbr], im_width, param_shp_type=0 )  
               im2nbr_shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( search_im_shapes[search_im_nbr], im_width, param_shp_type=0 )  
                     
               # matching from smaller shape.
               if len( target_im_shapes[ target_im_nbr ] ) > len( search_im_shapes[ search_im_nbr ] ):
                  im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( im2nbr_shp_coord_xy, im1nbr_shp_coord_xy, match_threshold=0.45 )
               else:
                  im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( im1nbr_shp_coord_xy, im2nbr_shp_coord_xy, match_threshold=0.45 )

               if im1im2nbr_match is True:                  
                  nbr_matched_count += 1
                  break               

         if nbr_matched_count > 0 and nbr_matched_count / smaller_nbr_count >= 0.35:
            if im1or2 == "im1":
               all_shapes_matches.append( ( target_shapeid, matched_shapeid ) )
            else:
               all_shapes_matches.append( ( matched_shapeid, target_shapeid ) )







all_shapes_matches = []
find_matches( im1pixch_shapes, im1shapes, im1shapes_boundaries, im2shapeids_by_pindex, im2shapes, im1shapes_colors, im2shapes_colors, image1data, 
              im1shapes_neighbors, im2shapes_neighbors, "im1" )

find_matches( im2pixch_shapes, im2shapes, im2shapes_boundaries, im1shapeids_by_pindex, im1shapes, im2shapes_colors, im1shapes_colors, image2data,
              im2shapes_neighbors, im1shapes_neighbors, "im2" )
              






with open(save_result_fpath, 'wb') as fp:
   pickle.dump(all_shapes_matches, fp)
fp.close()



































