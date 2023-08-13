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


image_template_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/image_template/data/"
image_template_shapes_dfile = image_template_ddir + "1.data"  
with open (image_template_shapes_dfile, 'rb') as fp:
   image_template_shapes = pickle.load(fp)
fp.close()


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



def fill_with_shape_vicinity_pixels( im_shapes_vici_pix_list, param_cur_shapes, im_boundaries  ):
      for cur_shape in param_cur_shapes:
         vicinity_pixels = pixel_shapes_functions.get_shape_vicinity_pixels( im_boundaries[cur_shape], 3, im_size, param_shp_type=1 )
         im_shapes_vici_pix_list.append( vicinity_pixels )   



def is_every_shape_close( shapes_vicinity_pixels ):
   
   if len( shapes_vicinity_pixels ) > 1:
      skip = False
      close_together_shapes = []
      for shape_num, vicinity_pixels in enumerate(shapes_vicinity_pixels):
         pixel_found = False
         
         for ano_shape_num, ano_vicinity_pixels in enumerate(shapes_vicinity_pixels):
            if vicinity_pixels == ano_vicinity_pixels:
               continue
            
            if [ ano_shape_num, shape_num ] in close_together_shapes:
               pixel_found = True
               break
            
            for pixel in vicinity_pixels:
               if pixel in ano_vicinity_pixels:
                  pixel_found = True
                  close_together_shapes.append( [ shape_num, ano_shape_num ] )
                  break
            
            if pixel_found is True:
               break
         
         if pixel_found is False:
            skip = True
      
      if skip is True:
         return False
      elif skip is False:
         return True
      
      
   elif len( shapes_vicinity_pixels ) == 1:
      return True



result_shapes = {}

prev_file_shapes = None
prev_filename = None
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
for each_file in image_template_shapes:
   print( each_file )
   
   cur_im1file = each_file.split(".")[0]
   cur_im2file = each_file.split(".")[1]
   
   result_shapes[each_file] = set()

   if ref_imagefile_op is False:
      im1 = Image.open(top_images_dir + directory + cur_im1file + ".png" )
      im2 = Image.open(top_images_dir + directory + cur_im2file + ".png" )
      image1data = im1.getdata()
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

   im1shapes_boundaries = {}
   im1shapeid_by_pindex = {}
   for shapeid in im1shapes:
      cur_pixels = set()
      for temp_p in im1shapes[shapeid]:
         im1shapeid_by_pindex[ temp_p ] = shapeid
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im1shapes[shapeid] = cur_pixels
      im1shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels( cur_pixels )
      

   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()

   im2shapes_boundaries = {}
   im2shapeid_by_pindex = {}
   for shapeid in im2shapes:
      cur_pixels = set()
      
      for temp_p in im2shapes[shapeid]:
         im2shapeid_by_pindex[temp_p] = shapeid
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


   for each_shapes in image_template_shapes[ each_file ]:
      
      cur_im1shapes = [ temp_shapes[0] for temp_shapes in image_template_shapes[ each_file ] if each_shapes[1] == temp_shapes[1] ]
      cur_im2shapes = [ temp_shapes[1] for temp_shapes in image_template_shapes[ each_file ] if each_shapes[0] == temp_shapes[0] ]
      
      # start of condition1
      # if cur_im1shapes and cur_im2shapes are the match, then all shapes of cur_im1shapes and all shapes of cur_im2shapes should be very 
      # close to one another
      cur_im1shapes_vicinity_pixels = []
      cur_im2shapes_vicinity_pixels = []
      
      fill_with_shape_vicinity_pixels( cur_im1shapes_vicinity_pixels, cur_im1shapes, im1shapes_boundaries )
      fill_with_shape_vicinity_pixels( cur_im2shapes_vicinity_pixels, cur_im2shapes, im2shapes_boundaries )
      
      every_shape_is_close = is_every_shape_close( cur_im1shapes_vicinity_pixels )
      if every_shape_is_close is False:
         continue
      every_shape_is_close = is_every_shape_close( cur_im2shapes_vicinity_pixels )
      if every_shape_is_close is False:
         continue      
      
      # end of condition1
         
      
      
      matched = False
      # below covers one to one type of match and when match has multiple image2 shapes
      if len( cur_im1shapes ) == 1:
         for matched_im1nbr in im1shapes_neighbors[ each_shapes[0] ]:
         
            im2neighbor_matches = [ temp_shapes[1] for temp_shapes in all_matches_so_far[ each_file ] if matched_im1nbr == temp_shapes[0] ]

            for im2neighbor_match in im2neighbor_matches:
            
               for im2neighbor in im2shapes_neighbors[ im2neighbor_match ]:
                  if im2neighbor in cur_im2shapes:
                     matched = True
                  
                     for cur_im2shape in cur_im2shapes:
                        result_shapes[ each_file ].add( ( each_shapes[0], cur_im2shape ) )

                     break
               
               if matched is True:
                  break
            if matched is True:
               break
      
      elif len(cur_im1shapes) > 1:
         # this covers when match has multiple image1 shapes
         for matched_im2nbr in im2shapes_neighbors[ each_shapes[1] ]:
            
            im1neighbor_matches = [ temp_shapes[0] for temp_shapes in all_matches_so_far[ each_file ] if matched_im2nbr == temp_shapes[1] ]
            
            for im1neighbor_match in im1neighbor_matches:
               
               for im1neighbor in im1shapes_neighbors[ im1neighbor_match ]:
                  if im1neighbor in cur_im1shapes:
                     
                     for cur_im1shape in cur_im1shapes:
                        result_shapes[ each_file ].add( ( cur_im1shape, each_shapes[1] ) )

                     break

               if matched is True:
                  break
            if matched is True:
               break


verified_shapes_dfile = image_template_ddir + "verified1.data"  
with open(verified_shapes_dfile, 'wb') as fp:
   pickle.dump(result_shapes, fp)
fp.close()


















