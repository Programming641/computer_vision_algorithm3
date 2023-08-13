
from libraries import  read_files_functions, pixel_shapes_functions, pixel_functions, image_functions, same_shapes_functions


from PIL import ImageTk, Image
import os, sys
import pickle
import copy
import math
import shutil

from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files, frth_smallest_pixc, third_smallest_pixc

directory = sys.argv[1]
shapes_type = "intnl_spixcShp"


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
   print("ERROR. shapes_type normal is not supported")
   sys.exit()

elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"
   
   shapes_dir = s_pixcShp_intnl_dir + "shapes/"


else:
   print("ERROR at " + str( os.path.basename(__file__) ) + " shapes_type " + shapes_type + " is not supported")
   sys.exit()



shapes_m_types_dir = top_shapes_dir + directory + scnd_stg_all_files + "/shp_match_types/"
one_to_one_matched_dfile = shapes_m_types_dir + "data/matched_pixels.data"
with open (one_to_one_matched_dfile, 'rb') as fp:
      # image file num: [ ('57125', '57529'), ... ]
      # or 
      # image file num: [ [ [ [image1 shapes], [image2 shapes] ] ], ... ]
   one_to_one_m_shapes = pickle.load(fp)
fp.close()


def check_shape_size( param_im1shapeid, param_im2shapeid, param_shapes, param_ano_shapes ):
   # check if size is too different
   im1shapes_total = len( param_shapes[param_im1shapeid] )
   im2shapes_total = len( param_ano_shapes[param_im2shapeid] )
      
   im1_2pixels_diff = abs( im1shapes_total - im2shapes_total )
   if im1_2pixels_diff != 0:
      if im1shapes_total > im2shapes_total:
         if im1_2pixels_diff / im2shapes_total > 1:
            return True
      else:
         if im1_2pixels_diff / im1shapes_total > 1:
            return True

   return False     


move_together_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/move_together/data/"
if os.path.exists(move_together_ddir ) == False:
   os.makedirs(move_together_ddir )

movement_threshold = 10
result_matches = {}
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
for each_files in all_matches_so_far:
   print(each_files)

   result_matches[each_files] = {}

   cur_im1file = each_files.split(".")[0]
   cur_im2file = each_files.split(".")[1]

   if ref_imagefile_op is False:
      im1 = Image.open(top_images_dir + directory + cur_im1file + ".png" )
      im_size = im1.size
      im_width, im_height = im_size
      
      ref_imagefile_op = True


   shapes_dfile = shapes_dir + cur_im1file + "shapes.data"
   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()     

   im1shapes_in_shape_coord = {}
   im1shapes_by_pindex = {}
   for shapeid in im1shapes:
      cur_pixels = set()
      
      for temp_p in im1shapes[shapeid]:
         im1shapes_by_pindex[ temp_p ] = shapeid
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im1shapes[shapeid] = cur_pixels   
      im1shapes_in_shape_coord[shapeid] = pixel_shapes_functions.get_shape_pos_in_shp_coord( im1shapes[ shapeid ], im_width, param_shp_type=1 )  


   im2shapes_dfile = shapes_dir + cur_im2file + "shapes.data"
   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()   

   im2shapes_in_shape_coord = {}
   im2shapes_by_pindex = {}
   for shapeid in im2shapes:
      cur_pixels = set()
      
      for temp_p in im2shapes[shapeid]:
         im2shapes_by_pindex[temp_p] = shapeid
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im2shapes[shapeid] = cur_pixels  
      im2shapes_in_shape_coord[shapeid] = pixel_shapes_functions.get_shape_pos_in_shp_coord( im2shapes[ shapeid ], im_width, param_shp_type=1 )  



   im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im1file, directory, shapes_type=shapes_type, min_colors=True)
   im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im2file, directory, shapes_type=shapes_type, min_colors=True)

   result_matches[each_files] = []

   for each_shape in one_to_one_m_shapes[each_files]:
      # each_shape -> ('57125', '57529')
      # or 
      # each_shape -> [ [ [image1 shapes], [image2 shapes] ] ]

      _im1shapes = set()
      _im2shapes = set()
      
      if type( each_shape ) is tuple:
         _im1shapes |= im1shapes[ each_shape[0] ]
         _im2shapes |= im2shapes[ each_shape[1] ]
      
      elif type( each_shape ) is list:
         
         for temp_im1shape in each_shape[0]:
            _im1shapes |= im1shapes[ temp_im1shape ]
         
         for temp_im2shape in each_shape[1]:
            _im2shapes |= im2shapes[ temp_im2shape ]

      
      im1shape_average_pix = pixel_shapes_functions.get_shape_average_pixel( _im1shapes , im_width, pixel_xy=True )
      # rounding to whole number
      im1shape_average_pix = ( round( im1shape_average_pix[0] ), round( im1shape_average_pix[1] ) )
      im2shape_average_pix = pixel_shapes_functions.get_shape_average_pixel( _im2shapes , im_width, pixel_xy=True )
      im2shape_average_pix = ( round( im2shape_average_pix[0] ), round( im2shape_average_pix[1] ) )  
      
      moved_shape_x = im1shape_average_pix[0] - im2shape_average_pix[0]
      moved_shape_y = im1shape_average_pix[1] - im2shape_average_pix[1]
      
      # {(152, 8), (141, 8), ... }
      im1vicinity_pixels = pixel_shapes_functions.get_shape_vicinity_pixels( _im1shapes, 13, im_size, 1 )
      
      im1vicicity_shapes = set()
      for vicinity_pixel in im1vicinity_pixels:
         pindex = pixel_functions.convert_xy_to_pindex( vicinity_pixel, im_width )
         
         im1vicicity_shapes.add( im1shapes_by_pindex[ str(pindex) ] )

      # {(152, 8), (141, 8), ... }
      im2vicinity_pixels = pixel_shapes_functions.get_shape_vicinity_pixels( _im2shapes, 13, im_size, 1 )

      im2vicicity_shapes = set()
      for vicinity_pixel in im2vicinity_pixels:
         pindex = pixel_functions.convert_xy_to_pindex( vicinity_pixel, im_width )
         
         im2vicicity_shapes.add( im2shapes_by_pindex[ str(pindex) ] )      
      
      
      for im1vicicity_shape in im1vicicity_shapes:
         if len( im1shapes[im1vicicity_shape] ) < third_smallest_pixc:
            continue
         
         # check if im1vicicity_shape is already found in all_matches_so_far[each_files]
         im1already_fnd = [ temp_shapes for temp_shapes in all_matches_so_far[each_files] if im1vicicity_shape == temp_shapes[0] ]
         
         if len( im1already_fnd ) >= 1:
            continue
         

         im1vcnty_shape_av_pix = pixel_shapes_functions.get_shape_average_pixel( im1shapes[im1vicicity_shape], im_width, pixel_xy=True )
         im1vcnty_shape_av_pix = ( round( im1vcnty_shape_av_pix[0] ), round( im1vcnty_shape_av_pix[1] ) )
         
         for im2vicicity_shape in im2vicicity_shapes:
            if len( im2shapes[im2vicicity_shape] ) < third_smallest_pixc:
               continue
            
            if ( im1vicicity_shape, im2vicicity_shape ) in result_matches[ each_files ]:
               continue
            
            # check if im2vicicity_shape is already found in all_matches_so_far[each_files]
            im2already_fnd = [ temp_shapes for temp_shapes in all_matches_so_far[each_files] if im2vicicity_shape == temp_shapes[1] ]
         
            if len( im2already_fnd ) >= 1:
               continue
            
            
            if im1shapes_colors[ im1vicicity_shape ] != im2shapes_colors[ im2vicicity_shape ]:
               continue
            
            # check if im1vicicity_shape and im2vicicity_shape size are too different
            size_diff = check_shape_size( im1vicicity_shape, im2vicicity_shape, im1shapes, im2shapes )
            
            if size_diff is True:
               continue
            
            
            # check if im1vicicity_shape and im2vicicity_shape movement is the same as matched image1 and image2 shapes
            im2vcnty_shape_av_pix = pixel_shapes_functions.get_shape_average_pixel( im2shapes[im2vicicity_shape], im_width, pixel_xy=True )
            im2vcnty_shape_av_pix = ( round( im2vcnty_shape_av_pix[0] ), round( im2vcnty_shape_av_pix[1] ) )             
            
            moved_nbr_x = im1vcnty_shape_av_pix[0] - im2vcnty_shape_av_pix[0]
            moved_nbr_y = im1vcnty_shape_av_pix[1] - im2vcnty_shape_av_pix[1]
            
            if abs( moved_shape_x - moved_nbr_x ) > movement_threshold or abs( moved_shape_y - moved_nbr_y ) > movement_threshold:
               continue

            im1shp_coord_xy  = im1shapes_in_shape_coord[ im1vicicity_shape ]
            im2shp_coord_xy = im2shapes_in_shape_coord[ im2vicicity_shape ]                 
                     
            # matching from bigger shape.
            if len( im1shapes[ im1vicicity_shape ] ) > len( im2shapes[im2vicicity_shape] ):
               im1im2_match = same_shapes_functions.match_shape_while_moving_it( im1shp_coord_xy, im2shp_coord_xy )
            else:
               im1im2_match = same_shapes_functions.match_shape_while_moving_it( im2shp_coord_xy, im1shp_coord_xy )

            if im1im2_match is True:      
               
               result_matches[each_files].append( ( im1vicicity_shape, im2vicicity_shape ) )               






move_together_dfile = move_together_ddir + "move_together.data"
with open(move_together_dfile, 'wb') as fp:
   pickle.dump(result_matches, fp)
fp.close()















