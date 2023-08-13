import tkinter
from PIL import ImageTk, Image
from libraries import btwn_amng_files_functions, read_files_functions, pixel_shapes_functions, same_shapes_functions, pixel_functions, image_functions
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


# find_consecutively_missing_shapes4.py
missed_shapes_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/consecutive_missed/data/"
possible_matches_dfile = missed_shapes_ddir + "possible_matches.data"
with open (possible_matches_dfile, 'rb') as fp:
   possible_match_shapes = pickle.load(fp)
fp.close()

# find_nbr_matches_from_Nfnd_shapes.py
across_all_files_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/data/"
nbr_matches_dfile = across_all_files_ddir + "nbr_matches.data"
with open (nbr_matches_dfile, 'rb') as fp:
   nbr_matched_shapes = pickle.load(fp)
fp.close()

pixch_ch_shapes_dir = top_shapes_dir + directory + "pixch/ch_shapes/ch_from/"


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




result_shapes = {}

ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
for each_file in all_matches_so_far:
   print( each_file )
   
   cur_im1file = each_file.split(".")[0]
   cur_im2file = each_file.split(".")[1]

   # algorithms/pixch/most_ch_shapes_frm_whichShp_in_prev_frm.py
   pixch_ch_shapes_file = pixch_ch_shapes_dir + "data/" + cur_im1file + "." + cur_im2file + "." + cur_im2file + ".data"
   with open (pixch_ch_shapes_file, 'rb') as fp:
      # [[['23933', '27137'], ['13530', '27539']], ... ]
      # [ [ [ image1 shapeids ] [ image2 shapeids ] ], ... ]
      pixch_ch_shapes = pickle.load(fp)
   fp.close()


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
   im1shapes_by_pindex = {}
   for shapeid in im1shapes:
      cur_pixels = set()
      for temp_p in im1shapes[shapeid]:
         im1shapes_by_pindex[ temp_p ] = shapeid
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
   im2shapes_by_pindex = {}
   for shapeid in im2shapes:
      cur_pixels = set()
      
      for temp_p in im2shapes[shapeid]:
         im2shapes_by_pindex[ temp_p ] = shapeid
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im2shapes[shapeid] = cur_pixels
      
      im2shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels( cur_pixels )


   im1shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + cur_im1file + "_shape_nbrs.txt"
   im2shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + cur_im2file + "_shape_nbrs.txt"

   # {'79999': ['71555', '73953', ...], ...}
   im1shapes_neighbors = read_files_functions.rd_dict_k_v_l(cur_im1file, directory, im1shape_neighbors_file)
   im2shapes_neighbors = read_files_functions.rd_dict_k_v_l(cur_im2file, directory, im2shape_neighbors_file)

   im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im1file, directory, shapes_type=shapes_type, min_colors=True)
   im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im2file, directory, shapes_type=shapes_type, min_colors=True)

   
   all_possible_shapes = []
   for each_pixch_shapes in pixch_ch_shapes:
      # each_pixch_shapes -> [['23904', '23502'], ['23100', '23503']]
      # [ [ image1 shapes ], [ image2 shapes ] ]
      all_possible_shapes.append( ( each_pixch_shapes[0][0], each_pixch_shapes[1][0] ), )
      all_possible_shapes.append( ( each_pixch_shapes[0][1], each_pixch_shapes[1][1] ), )
      
   for each_shapes in possible_match_shapes[ each_file ]:
      all_possible_shapes.append( each_shapes )
   
   for each_shapes in nbr_matched_shapes[ each_file ]:
      all_possible_shapes.append( each_shapes )
   
   
   result_shapes[ each_file ] = set()
   
   for each_shapes in all_possible_shapes:
      if each_shapes not in all_matches_so_far[ each_file ] and all_possible_shapes.count( each_shapes ) > 1:
         result_shapes[ each_file ].add( each_shapes )
   

      

for each_files in result_shapes:
      
   if each_files not in all_matches_so_far.keys():
      all_matches_so_far[ each_files ] = result_shapes[ each_files ]
      
   else:
      for each_shapes in result_shapes[ each_files ]:
         if each_shapes not in all_matches_so_far[ each_files ]:
            all_matches_so_far[ each_files ].add( each_shapes )  


if os.path.exists(missed_shapes_ddir ) == False:
   os.makedirs(missed_shapes_ddir )

possible_matches_dfile = missed_shapes_ddir + "5.data"

if os.path.exists(possible_matches_dfile):
   with open (possible_matches_dfile, 'rb') as fp:
      possible_match_shapes = pickle.load(fp)
   fp.close()
   
   for each_files in possible_match_shapes:
      if each_files in result_shapes.keys():
         for each_shapes in possible_match_shapes[each_files]:
            if each_shapes not in result_shapes[each_files]:
               result_shapes[each_files].add( each_shapes )
         
      else:
         result_shapes[each_files] = result_shapes[each_files]   



with open(possible_matches_dfile, 'wb') as fp:
   pickle.dump(result_shapes, fp)
fp.close()

with open(all_matches_so_far_dfile, 'wb') as fp:
   pickle.dump(all_matches_so_far, fp)
fp.close()





















