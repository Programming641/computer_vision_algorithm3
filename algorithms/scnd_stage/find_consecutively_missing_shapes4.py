import tkinter
from PIL import ImageTk, Image
from libraries import btwn_amng_files_functions, cv_globals, pixel_shapes_functions, same_shapes_functions, pixel_functions, image_functions
from libraries import shapes_results_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files
import pickle
import sys, pathlib, os

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


shp_by_index_dir = shapes_dir + 'shapeids_by_pindex/'


result_shapes = {}

prev_file_shapes = None
prev_filename = None
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
frth_smallest_pixc = None

for each_file in all_matches_so_far:
   print( each_file )
   
   cur_im1file = each_file.split(".")[0]
   cur_im2file = each_file.split(".")[1]

   if ref_imagefile_op is False:
      im1 = Image.open(top_images_dir + directory + cur_im1file + ".png" )
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

   boundary_dir = shapes_dir + "boundary/"
   boundary_dfile = boundary_dir + cur_im1file + ".data"
   with open (boundary_dfile, 'rb') as fp:
      im1shapes_boundaries = pickle.load(fp)
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
      im1shapes_by_pindex = pickle.load(fp)
   fp.close()

   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()

   boundary_dfile2 = boundary_dir + cur_im2file + ".data"
   with open (boundary_dfile2, 'rb') as fp:
      im2shapes_boundaries = pickle.load(fp)
   fp.close()

   for shapeid in im2shapes:
      cur_pixels = set()
      
      for temp_p in im2shapes[shapeid]:
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im2shapes[shapeid] = cur_pixels


   im1shape_neighbors_file = shapes_dir + "shape_nbrs/" + cur_im1file + "_shape_nbrs.data"
   im2shape_neighbors_file = shapes_dir + "shape_nbrs/" + cur_im2file + "_shape_nbrs.data"

   with open (im1shape_neighbors_file, 'rb') as fp:
      im1shapes_neighbors = pickle.load(fp)
   fp.close()

   with open (im2shape_neighbors_file, 'rb') as fp:
      im2shapes_neighbors = pickle.load(fp)
   fp.close()
   
   if "min" in directory:
      min_colors = True
   else:
      min_colors = False
   
   im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im1file, directory, min_colors=min_colors)
   im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im2file, directory, min_colors=min_colors)

  
   if prev_file_shapes is None:
      prev_file_shapes = all_matches_so_far[each_file]
      prev_filename = each_file
      
      prev_im1shapes = im1shapes
      prev_im2shapes = im2shapes
      prev_im1shapes_nbrs = im1shapes_neighbors
      prev_im2shapes_nbrs = im2shapes_neighbors
      
      prev_im1shapes_clrs = im1shapes_colors
      
      
      prev_im1shapes_by_pindex = im1shapes_by_pindex
   
   else:
      prev_im1file = prev_filename.split(".")[0]
      prev_im2file = prev_filename.split(".")[1]
                           
      result_shapes[each_file] = set()
      result_shapes[prev_im1file + "." + cur_im1file ] = set()

   
      for each_shapes in all_matches_so_far[each_file]:
         if len( im1shapes[ each_shapes[0] ] ) < frth_smallest_pixc:
            continue

         found_shapes = { True for temp_shapes in prev_file_shapes if each_shapes[0] == temp_shapes[1] }
         if len( found_shapes ) == 0:
            # current image1 shape not found in previous image2 shape
            
            # {(231, 63), (244, 82), ... }
            vicinity_pixels = pixel_shapes_functions.get_shape_vicinity_pixels( im1shapes_boundaries[ each_shapes[0] ], 13, im_size, param_shp_type=1 )
            
            vicinity_pindexes = set()
            # convert xy to pixel indexes
            for pixel in vicinity_pixels:
               pixel_index = pixel_functions.convert_xy_to_pindex( pixel, im_width )
               
               vicinity_pindexes.add( pixel_index )


            # get all previous shapes that are inside vicinity_pixels
            prev_im1shapes_in_vicinity = set()
            for vicinity_pixel in vicinity_pindexes:
               # check if this previous image1 shape is big enough and is not already matched
               for prev_im1shapeid in prev_im1shapes_by_pindex[ vicinity_pixel ]:
                  if len( prev_im1shapes[ prev_im1shapeid ] ) < frth_smallest_pixc or prev_im1shapeid in prev_im1shapes_in_vicinity:
                     continue
               
                  already_matched = { True for temp_shapes in prev_file_shapes if prev_im1shapeid == temp_shapes[0] }
                  if len( already_matched ) > 0:
                     continue
               
                  prev_im1shapes_in_vicinity.add( prev_im1shapeid )


            for prev_im1shape in prev_im1shapes_in_vicinity:
               # { ( image1 shapeid, image2 shapeid ), ... }
               result = shapes_results_functions.verify_matches( [ ( prev_im1shape, each_shapes[0] ) ], [ prev_im1shapes, im1shapes ], [ prev_im1shapes_clrs, im1shapes_colors ],
                                        [ prev_im1shapes_nbrs, im1shapes_neighbors], im_size, min_colors )            
               
               if len( result) > 0:
                  # match is found
                  result_shapes[prev_im1file + "." + cur_im1file ].add( ( prev_im1shape, each_shapes[0] ) )







      prev_file_shapes = all_matches_so_far[each_file]
      prev_filename = each_file

      prev_im1shapes = im1shapes
      prev_im2shapes = im2shapes
      prev_im1shapes_nbrs = im1shapes_neighbors
      prev_im2shapes_nbrs = im2shapes_neighbors
      
      prev_im1shapes_clrs = im1shapes_colors

      prev_im1shapes_by_pindex = im1shapes_by_pindex


missed_shapes_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/consecutive_missed/data/"
if os.path.exists(missed_shapes_ddir ) == False:
   os.makedirs(missed_shapes_ddir )

possible_matches_dfile = missed_shapes_ddir + "possible_matches.data"
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
         result_shapes[each_files] = possible_match_shapes[each_files]   



with open(possible_matches_dfile, 'wb') as fp:
   pickle.dump(result_shapes, fp)
fp.close()

with open(all_matches_so_far_dfile, 'wb') as fp:
   pickle.dump(all_matches_so_far, fp)
fp.close()





















