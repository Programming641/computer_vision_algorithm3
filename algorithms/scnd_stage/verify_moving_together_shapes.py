
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
all_matches_so_far_dfile = across_all_files_ddir + "all_matches.data"
if os.path.exists( all_matches_so_far_dfile ):
   with open (all_matches_so_far_dfile, 'rb') as fp:
      all_matches_so_far = pickle.load(fp)
   fp.close()



move_together_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/move_together/data/"
move_together_dfile = move_together_ddir + "move_together.data"
with open (move_together_dfile, 'rb') as fp:
   move_together_shapes = pickle.load(fp)
fp.close()


if shapes_type == "normal":
   print("ERROR. shapes_type normal is not supported")
   sys.exit()

elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"
   
   shapes_dir = s_pixcShp_intnl_dir + "shapes/"


else:
   print("ERROR at " + str( os.path.basename(__file__) ) + " shapes_type " + shapes_type + " is not supported")
   sys.exit()





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


result_shapes = {}

prev_file_shapes = None
prev_filename = None
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
for each_file in all_matches_so_far:
   print( each_file )

   result_shapes[ each_file ] = []
   
   cur_im1file = each_file.split(".")[0]
   cur_im2file = each_file.split(".")[1]

   if ref_imagefile_op is False:
      im1 = Image.open(top_images_dir + directory + cur_im1file + ".png" )
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

   im1shapes_boundaries = {}
   for shapeid in im1shapes:
      cur_pixels = set()
      for temp_p in im1shapes[shapeid]:
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im1shapes[shapeid] = cur_pixels
      
      im1shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels(cur_pixels)

   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()

   im2shapes_boundaries = {}
   for shapeid in im2shapes:
      cur_pixels = set()
      
      for temp_p in im2shapes[shapeid]:
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im2shapes[shapeid] = cur_pixels

      im2shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels(cur_pixels)


   im1shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + cur_im1file + "_shape_nbrs.txt"
   im2shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + cur_im2file + "_shape_nbrs.txt"

   # {'79999': ['71555', '73953', ...], ...}
   im1shapes_neighbors = read_files_functions.rd_dict_k_v_l(cur_im1file, directory, im1shape_neighbors_file)
   im2shapes_neighbors = read_files_functions.rd_dict_k_v_l(cur_im2file, directory, im2shape_neighbors_file)

   im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im1file, directory, shapes_type=shapes_type, min_colors=True)
   im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im2file, directory, shapes_type=shapes_type, min_colors=True)


   for each_shapes in move_together_shapes[ each_file ]:

      neighbor_match_len = 0
      neighbor_match_count = 0
      
      for im1nbr in im1shapes_neighbors[ each_shapes[0] ]:
         cur_match = False
         neighbor_matches = [ temp_shapes for temp_shapes in all_matches_so_far[ each_file ] if im1nbr == temp_shapes[0] ]
         if len( neighbor_matches ) >= 1:
            neighbor_match_len += 1
            
            for neighbor_match in neighbor_matches:
               
               for im2nbr in im2shapes_neighbors[ neighbor_match[1] ]:
                  if im2nbr == each_shapes[1]:
                     neighbor_match_count += 1
                     cur_match = True
                     break
               
               if cur_match is True:
                  break
      
      if neighbor_match_count != 0 and neighbor_match_count != 0 and neighbor_match_count / neighbor_match_len >= 0.33:
         result_shapes[ each_file ].append( each_shapes )
      
      else:
         image_functions.cr_im_from_shapeslist2( cur_im1file, directory, [each_shapes[0]], save_filepath=None , shapes_rgb=(255,0,0), input_im=None )
         image_functions.cr_im_from_shapeslist2( cur_im2file, directory, [each_shapes[1]], save_filepath=None , shapes_rgb=(0,0,255), input_im=None )
         
  
   if prev_file_shapes is None:
      prev_file_shapes = all_matches_so_far[each_file]
      prev_filename = each_file
      
      prev_im1shapes = im1shapes
      prev_im2shapes = im2shapes
      prev_im1shapes_nbrs = im1shapes_neighbors
      prev_im2shapes_nbrs = im2shapes_neighbors
      
      prev_im1shapes_clrs = im1shapes_colors
      prev_im2shapes_clrs = im2shapes_colors
      
      prev_im1shapes_bnd = im1shapes_boundaries
      prev_im2shapes_bnd = im2shapes_boundaries

   
   else:
      prev_im1file = prev_filename.split(".")[0]
      prev_im2file = prev_filename.split(".")[1]

      

         






      prev_file_shapes = all_matches_so_far[each_file]
      prev_filename = each_file

      prev_im1shapes = im1shapes
      prev_im2shapes = im2shapes
      prev_im1shapes_nbrs = im1shapes_neighbors
      prev_im2shapes_nbrs = im2shapes_neighbors
      
      prev_im1shapes_clrs = im1shapes_colors
      prev_im2shapes_clrs = im2shapes_colors

      prev_im1shapes_bnd = im1shapes_boundaries
      prev_im2shapes_bnd = im2shapes_boundaries
 
   



move_together_dfile = move_together_ddir + "verified.data"
with open(move_together_dfile, 'wb') as fp:
   pickle.dump(result_shapes, fp)
fp.close()















