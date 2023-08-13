import tkinter
from PIL import ImageTk, Image
from libraries import btwn_amng_files_functions, read_files_functions, pixel_shapes_functions, same_shapes_functions, pixel_functions, image_functions
from libraries import shapes_results_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files
from libraries.cv_globals import frth_smallest_pixc, third_smallest_pixc
import pickle
import sys, pathlib, os



shapes_type = "intnl_spixcShp"
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




if shapes_type == "normal":
   print("shapes_type normal is not supported in " + os.path.basename(__file__) )
   sys.exit()
   

elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"

   shapes_dir = s_pixcShp_intnl_dir + "shapes/"



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


# shape_pixels 
# [ shapeid, ( rgb ), { ( xy ), ( xy ), ... } ]
# 
# directly_UD is directly up or down. if it is true, it goes directly up or down with left or right value 0.
def move_pixels( shape_pixels, move_direction, directly_UD, step, move_total, image_data, im_shapeid_by_pindex ):

   matched = False

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

         
         debug = False
         debug_pixels = set()
         matched_pixels = set()
         for xy in shape_pixels[2]:
            _xy = ( xy[0] + move_x, xy[1] + move_y )

            # check if pixel is out of the image
            if _xy[0] < 0 or _xy[0] >= im_width or _xy[1] < 0 or _xy[1] >= im_height:
               continue
               
            debug_pixels.add( _xy )
              
            pindex = pixel_functions.convert_xy_to_pindex( _xy, im_width )
               
            # check if current shape's color is the same as image's pixel
            if shape_pixels[1] != image_data[ pindex ]:
               continue
               
            matched_pixels.add( str(pindex) )


         if len( debug_pixels ) >= 1 and debug is True:
            image_functions.cr_im_from_pixels( "11", directory, debug_pixels, save_filepath=None , pixels_rgb=None )
         
         if len( matched_pixels ) / len( shape_pixels[2] ) >= 0.5:

            matched_shapes = set()
            for matched_pixel in matched_pixels:
               matched_shapes.add( im_shapeid_by_pindex[ matched_pixel ] )
            

            for matched_shape in matched_shapes:

               found_shapes = { True for temp_shapes in all_matches_so_far[ each_file ] if matched_shape == temp_shapes[1] }    

               if len( found_shapes ) >= 1:
                  for matched_shp_pixel in im2shapes[ matched_shape ]:
                     pindex = pixel_functions.convert_xy_to_pindex( matched_shp_pixel, im_width )
                     if str(pindex) in matched_pixels:
                        matched_pixels.remove( str(pindex) )

            if len( matched_pixels ) / len( shape_pixels[2] ) >= 0.5:
               matched = True
            

   return matched



result_shapes = {}

prev_file_shapes = None
prev_filename = None
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
for each_file in all_matches_so_far:
   print( each_file )
   
   cur_im1file = each_file.split(".")[0]
   cur_im2file = each_file.split(".")[1]
   
   result_shapes[each_file] = []

   if ref_imagefile_op is False:
      im1 = Image.open(top_images_dir + directory + cur_im1file + ".png" )
      im2 = Image.open(top_images_dir + directory + cur_im2file + ".png" )
      image2data = im2.getdata()
      im_size = im1.size
      im_width, im_height = im_size
      
      ref_imagefile_op = True

   shapes_dfile = shapes_dir + cur_im1file + "shapes.data"
   im2shapes_dfile = shapes_dir + cur_im2file + "shapes.data"

   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()

   im1shapes_by_pindex = {}
   for shapeid in im1shapes:
      cur_pixels = set()
      for temp_p in im1shapes[shapeid]:
         im1shapes_by_pindex[ temp_p ] = shapeid
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im1shapes[shapeid] = cur_pixels

   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()

   im2shapeid_by_pindex = {}
   for shapeid in im2shapes:
      cur_pixels = set()
      
      for temp_p in im2shapes[shapeid]:
         im2shapeid_by_pindex[temp_p] = shapeid
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im2shapes[shapeid] = cur_pixels


   im1shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + cur_im1file + "_shape_nbrs.txt"
   im2shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + cur_im2file + "_shape_nbrs.txt"

   # {'79999': ['71555', '73953', ...], ...}
   im1shapes_neighbors = read_files_functions.rd_dict_k_v_l(cur_im1file, directory, im1shape_neighbors_file)
   im2shapes_neighbors = read_files_functions.rd_dict_k_v_l(cur_im2file, directory, im2shape_neighbors_file)

   im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im1file, directory, shapes_type=shapes_type, min_colors=True)
   im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im2file, directory, shapes_type=shapes_type, min_colors=True)

   
   for im1shapeid in im1shapes:
      if len( im1shapes[ im1shapeid ] ) < frth_smallest_pixc:
         continue
      

      found_shapes = { True for temp_shapes in all_matches_so_far[ each_file ] if im1shapeid == temp_shapes[0] }      
      if len( found_shapes ) == 0:
         # im1shapeid is not found
            
         not_found_shape = [ im1shapeid, im1shapes_colors[ im1shapeid ], im1shapes[ im1shapeid ] ]

         leftUp_results = move_pixels( not_found_shape, "left_up", True, 2, 16, image2data, im2shapeid_by_pindex  )
         leftDown_results = move_pixels( not_found_shape, "left_down", True, 2, 16, image2data, im2shapeid_by_pindex )
         rightUp_results = move_pixels( not_found_shape, "right_up", False, 2, 16, image2data, im2shapeid_by_pindex )
         rightDown_results = move_pixels( not_found_shape, "right_down", False, 2, 16, image2data, im2shapeid_by_pindex )

         if leftUp_results is False and leftDown_results is False and rightUp_results is False and rightDown_results is False:
            result_shapes[ each_file ].append( im1shapeid )



dis_n_appeard_shapes_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/dis_n_appeared_shapes/data/"
if os.path.exists(dis_n_appeard_shapes_ddir ) == False:
   os.makedirs(dis_n_appeard_shapes_ddir )

dis_n_appeard_shapes_dfile = dis_n_appeard_shapes_ddir + "disappeared.data"  
with open(dis_n_appeard_shapes_dfile, 'wb') as fp:
   pickle.dump(result_shapes, fp)
fp.close()


















