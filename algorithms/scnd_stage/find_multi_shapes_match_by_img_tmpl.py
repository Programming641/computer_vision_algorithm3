import tkinter
from PIL import ImageTk, Image
from libraries import btwn_amng_files_functions, cv_globals, pixel_shapes_functions, same_shapes_functions, pixel_functions, image_functions
from libraries import shapes_results_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files
import pickle
import sys, pathlib, os

directory = "videos/street6/resized/min"

if len( sys.argv ) >= 2:
   directory = sys.argv[1]


# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

   
across_all_files_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/data/"
across_all_files_dfile = across_all_files_ddir + "all_files.data"
with open (across_all_files_dfile, 'rb') as fp:
   # {'10.11': {('79935', '58671'), ('39441', '39842'), ('45331', '36516')}, '11.12': {('39842', '40243'), ('26336', '27137'), ... }, ... }
   acrs_all_files_shapes = pickle.load(fp)
fp.close()


all_matches_so_far_dfile = across_all_files_ddir + "all_matches.data"
if os.path.exists( all_matches_so_far_dfile ):
   with open (all_matches_so_far_dfile, 'rb') as fp:
      all_matches_so_far = pickle.load(fp)
   fp.close()

else:
   all_matches_so_far = acrs_all_files_shapes


shapes_dir = top_shapes_dir + directory + "shapes/"



def check_shape_size( im1shapes_total, im2shapes_total, size_threshold=1 ):
      
   im1_2pixels_diff = abs( im1shapes_total - im2shapes_total )
   if im1_2pixels_diff != 0:
      if im1shapes_total > im2shapes_total:
         if im1_2pixels_diff / im2shapes_total > size_threshold:
            return True
      else:
         if im1_2pixels_diff / im1shapes_total > size_threshold:
            return True

   return False      


# shape_pixels 
# [ [shapeids ], { pixel index: (r,g,b), ... }, { ( xy ), ( xy ), ... } ]
# 
# directly_UD is directly up or down. if it is true, it goes directly up or down with left or right value 0.
def move_pixels( shape_pixels, move_direction, directly_UD, step, move_total, image_data, im_shapeids_by_pindex, param_shapes, im1or2, param_file ):


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

         
         debug_pixels = set()
         matched_pixels = set()
         for xy in shape_pixels[2]:
            _xy = ( xy[0] + move_x, xy[1] + move_y )

            # check if pixel is out of the image
            if _xy[0] < 0 or _xy[0] >= im_width or _xy[1] < 0 or _xy[1] >= im_height:
               continue
               
            debug_pixels.add( _xy )
              
            shape_pindex = pixel_functions.convert_xy_to_pindex( xy, im_width )
            moved_pindex = pixel_functions.convert_xy_to_pindex( _xy, im_width )
               
            # check if current shape's color is the same as image's pixel
            if min_colors is True:
               if shape_pixels[1][shape_pindex] != image_data[ moved_pindex ]:
                  continue

            else:
               appear_diff = pixel_functions.compute_appearance_difference( shape_pixels[1][shape_pindex],  image_data[ moved_pindex ] )
               if appear_diff is True:
                  # different appearance
                  continue

         
            matched_pixels.add( moved_pindex )


         #if shape_pixels[0] == ['22148', '24541']:
            #image_functions.cr_im_from_pixels( "15", directory, debug_pixels, save_filepath=None , pixels_rgb=None )

         if len( matched_pixels ) / len( shape_pixels[2] ) >= 0.65:

            # { matched shapeid: how many pixels have been matched, ... }
            matched_shapes_w_counts = {}
            for matched_pixel in matched_pixels:
               
               for temp_shapeid in im_shapeids_by_pindex[ matched_pixel ]:
                  if temp_shapeid not in matched_shapes_w_counts.keys():
                     matched_shapes_w_counts[ temp_shapeid ] = 1
                  else:
                     matched_shapes_w_counts[ temp_shapeid ] += 1
            

            matched_shapes_len = 0
            matched_shapes = set()
            for matched_shape in matched_shapes_w_counts:
               if matched_shapes_w_counts[ matched_shape ] / len( param_shapes[ matched_shape ] ) >= 0.3:
                  matched_shapes_len += len( param_shapes[ matched_shape ] ) 
                  matched_shapes.add( matched_shape )
            
            
            if matched_shapes_len / len( shape_pixels[2] ) >= 0.65:
            
               size_diff_result = check_shape_size( len( shape_pixels[2] ), matched_shapes_len, size_threshold=4 )
               if size_diff_result is True:
                  # size is too different
                  continue

            
               if im1or2 == "im2":
                  result_shapes[ param_file ].append( [ shape_pixels[0], matched_shapes ] )
 
               elif im1or2 == "im1":
                  result_shapes[ param_file ].append( [ matched_shapes, shape_pixels[0] ] )
               
               return True
               
   return False


shp_by_index_dir = shapes_dir + 'shapeids_by_pindex/'


result_shapes = {}

prev_file_shapes = None
prev_filename = None
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
frth_smallest_pixc = None

if "min" in directory:
   min_colors = True
else:
   min_colors = False

for each_file in all_matches_so_far:
   print( each_file )
   
   
   cur_im1file = each_file.split(".")[0]
   cur_im2file = each_file.split(".")[1]
   
   result_shapes[each_file] = []

   if ref_imagefile_op is False:
      im1 = Image.open(top_images_dir + directory + cur_im1file + ".png" )
      im2 = Image.open(top_images_dir + directory + cur_im2file + ".png" )
      image1data = im1.getdata()
      image2data = im2.getdata()
      im_size = im1.size
      im_width, im_height = im_size
      
      frth_smallest_pixc = cv_globals.get_frth_smallest_pixc( im_size )
      
      ref_imagefile_op = True

   shapes_dfile = shapes_dir + cur_im1file + "shapes.data"
   im2shapes_dfile = shapes_dir + cur_im2file + "shapes.data"

   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()

   for shapeid in im1shapes:
      cur_pixels = set()
      for temp_p in im1shapes[shapeid]:
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im1shapes[shapeid] = cur_pixels

   shp_by_index_dfile = shp_by_index_dir + cur_im1file + ".data"
   with open (shp_by_index_dfile, 'rb') as fp:
      # { pindex: { shapeids }, ... }
      im1shapeids_by_pindex = pickle.load(fp)
   fp.close()

   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()

   for shapeid in im2shapes:
      cur_pixels = set()
      
      for temp_p in im2shapes[shapeid]:
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im2shapes[shapeid] = cur_pixels

   shp_by_index_dfile2 = shp_by_index_dir + cur_im2file + ".data"
   with open (shp_by_index_dfile2, 'rb') as fp:
      # { pindex: { shapeids }, ... }
      im2shapeids_by_pindex = pickle.load(fp)
   fp.close()

   im1shape_neighbors_file = shapes_dir + "shape_nbrs/" + cur_im1file + "_shape_nbrs.data"
   im2shape_neighbors_file = shapes_dir + "shape_nbrs/" + cur_im2file + "_shape_nbrs.data"

   with open (im1shape_neighbors_file, 'rb') as fp:
      im1shapes_neighbors = pickle.load(fp)
   fp.close()

   with open (im2shape_neighbors_file, 'rb') as fp:
      im2shapes_neighbors = pickle.load(fp)
   fp.close()

   im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im1file, directory, min_colors=min_colors)
   im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im2file, directory, min_colors=min_colors)

   move_step = 2
   move_amount = 16
   for im1shapeid in im1shapes:
      if len( im1shapes[ im1shapeid ] ) < frth_smallest_pixc:
         continue

      found_shapes = { True for temp_shapes in all_matches_so_far[ each_file ] if im1shapeid == temp_shapes[0] }      
      if len( found_shapes ) == 0:
         # im1shapeid is not found
         

         for im1nbr in im1shapes_neighbors[ im1shapeid ]:
            if len( im1shapes[ im1nbr ] ) < frth_smallest_pixc:
               continue

            
            size_diff_result = check_shape_size( len( im1shapes[ im1shapeid ] ), len( im1shapes[ im1nbr ] ), size_threshold=4 )
            if size_diff_result is True:
               # size is too different
               continue
            
            #nbr_matches = [ temp_shapes[1] for temp_shapes in all_matches_so_far[ each_file ] if im1nbr == temp_shapes[0] ]  

            im1pixels = set()
            im1pixel_colors = {}
            
            im1pixels |= im1shapes[ im1shapeid ]
            im1pixels |= im1shapes[ im1nbr ]

            for pixel in im1shapes[ im1shapeid]:
               pindex = pixel_functions.convert_xy_to_pindex( pixel, im_width )
               im1pixel_colors[ pindex ] = im1shapes_colors[ im1shapeid ]
            for pixel in im1shapes[ im1nbr ]:
               pindex = pixel_functions.convert_xy_to_pindex( pixel, im_width )
               im1pixel_colors[ pindex ] = im1shapes_colors[ im1nbr ]
               
                           
            
            not_found_shape = [ [im1shapeid, im1nbr], im1pixel_colors, im1pixels ]

            leftUp_results = move_pixels( not_found_shape, "left_up", True, move_step, move_amount, image2data, im2shapeids_by_pindex, im2shapes, "im2", each_file  )
            leftDown_results = rightUp_results = rightDown_results = False
            if leftUp_results is False:
               leftDown_results = move_pixels( not_found_shape, "left_down", True, move_step, move_amount, image2data, im2shapeids_by_pindex, im2shapes, "im2", each_file )
               if leftDown_results is False:
                  rightUp_results = move_pixels( not_found_shape, "right_up", False, move_step, move_amount, image2data, im2shapeids_by_pindex, im2shapes, "im2", each_file )
                  if rightUp_results is False:
                     rightDown_results = move_pixels( not_found_shape, "right_down", False, move_step, move_amount, image2data, im2shapeids_by_pindex, im2shapes, "im2", each_file )

            
   
   for im2shapeid in im2shapes:
      if len( im2shapes[ im2shapeid ] ) < frth_smallest_pixc:
         continue

      found_shapes = { True for temp_shapes in all_matches_so_far[ each_file ] if im2shapeid == temp_shapes[1] }      
      if len( found_shapes ) == 0:
         # im2shapeid is not found      

         for im2nbr in im2shapes_neighbors[ im2shapeid ]:
            if len( im2shapes[ im2nbr ] ) < frth_smallest_pixc:
               continue

            size_diff_result = check_shape_size( len( im2shapes[ im2shapeid ] ), len( im2shapes[ im2nbr ] ), size_threshold=4 )
            if size_diff_result is True:
               # size is too different
               continue

            #nbr_matches = [ temp_shapes[1] for temp_shapes in all_matches_so_far[ each_file ] if im2nbr == temp_shapes[0] ]  

            im2pixels = set()
            im2pixel_colors = {}
        
            im2pixels |= im2shapes[ im2shapeid ]
            im2pixels |= im2shapes[ im2nbr ]

            for pixel in im2shapes[ im2shapeid]:
               pindex = pixel_functions.convert_xy_to_pindex( pixel, im_width )
               im2pixel_colors[ pindex ] = im2shapes_colors[ im2shapeid ]
            for pixel in im2shapes[ im2nbr ]:
               pindex = pixel_functions.convert_xy_to_pindex( pixel, im_width )
               im2pixel_colors[ pindex ] = im2shapes_colors[ im2nbr ]
               
                           
            
            not_found_shape = [ [im2shapeid, im2nbr], im2pixel_colors, im2pixels ]

            leftUp_results = move_pixels( not_found_shape, "left_up", True, move_step, move_amount, image1data, im1shapeids_by_pindex, im1shapes, "im1", each_file  )
            leftDown_results = rightUp_results = rightDown_results = False
            if leftUp_results is False:
               leftDown_results = move_pixels( not_found_shape, "left_down", True, move_step, move_amount, image1data, im1shapeids_by_pindex, im1shapes, "im1", each_file   )
               if leftDown_results is False:
                  rightUp_results = move_pixels( not_found_shape, "right_up", False, move_step, move_amount, image1data, im1shapeids_by_pindex, im1shapes, "im1", each_file   )
                  if rightUp_results is False:
                     rightDown_results = move_pixels( not_found_shape, "right_down", False, move_step, move_amount, image1data, im1shapeids_by_pindex, im1shapes, "im1", each_file   )

   


image_template_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/image_template/data/"
if os.path.exists(image_template_ddir ) == False:
   os.makedirs(image_template_ddir )

image_template_shapes_dfile = image_template_ddir + "multi1.data"  
with open(image_template_shapes_dfile, 'wb') as fp:
   pickle.dump(result_shapes, fp)
fp.close()


















