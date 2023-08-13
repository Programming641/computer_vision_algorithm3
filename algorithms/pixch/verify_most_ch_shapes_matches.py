from libraries import pixel_functions, read_files_functions, pixel_shapes_functions, image_functions, same_shapes_functions

from PIL import Image
import math
import os, sys
import winsound, time
import pickle

from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, third_smallest_pixc



im1file = '14'
im2file = "15"
shapes_type = "intnl_spixcShp"
directory = "videos/street3/resized/min"

if len(sys.argv) > 1:
   im1file = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   im2file = sys.argv[1][0: len( sys.argv[1] ) - 4 ]
   directory = sys.argv[3]
   
   shapes_type = "intnl_spixcShp"

   print("execute script algorithms/pixch/verify_most_ch_shapes_matches.py. file1 " + im1file + " file2 " + im2file + " directory " + directory )

# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'


changed_shapes_ddir = top_shapes_dir + directory + "pixch/ch_shapes/ch_from/data/"
ch_shapes_dfile = changed_shapes_ddir + im1file + "." + im2file + "." + im2file + ".data"
with open (ch_shapes_dfile, 'rb') as fp:
   # [[['23933', '27137'], ['13530', '27539']], 
   # [ [ [image1 shapes ], [image2 shapes ] ], ... ]
   ch_shapes = pickle.load(fp)
fp.close()

original_image = Image.open(top_images_dir + directory + im1file + ".png")
im_width, im_height = original_image.size

if shapes_type == "normal":
   print("shapes_type normal is not supported in " + os.path.basename(__file__) )
   sys.exit()
   

elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"

   shapes_dir = s_pixcShp_intnl_dir + "shapes/"
   shapes_dfile = shapes_dir + im1file + "shapes.data"
   im2shapes_dfile = shapes_dir + im2file + "shapes.data"

   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()    

   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()


   shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + im1file + "_shape_nbrs.txt"
   im2shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + im2file + "_shape_nbrs.txt"



# {'79999': ['71555', '73953', ...], ...}
im1shapes_neighbors = read_files_functions.rd_dict_k_v_l(im1file, directory, shape_neighbors_file)
im2shapes_neighbors = read_files_functions.rd_dict_k_v_l(im2file, directory, im2shape_neighbors_file)

im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im1file, directory, shapes_type=shapes_type)
im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im2file, directory, shapes_type=shapes_type)


verified_shapes = []
progress_counter = len( ch_shapes )
for each_ch_shapes in ch_shapes:
   # each_ch_shapes -> [['23933', '27137'], ['13530', '27539']]
   
   print( str( progress_counter ) + " remaining")
   progress_counter -= 1
   
   im1total_pixels_len = 0
   im1s_neighbors = set()
   im1total_neighbors = 0
   for temp_im1shape in each_ch_shapes[0]:
      im1total_pixels_len += len( im1shapes[temp_im1shape] )
      
      for temp_im1s_nbr in im1shapes_neighbors[ temp_im1shape ]:
         if temp_im1s_nbr not in each_ch_shapes[0] and len( im1shapes[temp_im1s_nbr] ) >= third_smallest_pixc:
            im1s_neighbors.add( temp_im1s_nbr )
            im1total_neighbors += len( im1shapes[temp_im1s_nbr] )
   
   im2total_pixels_len = 0
   im2s_neighbors = set()
   im2total_neighbors = 0
   for temp_im2shape in each_ch_shapes[1]:
      im2total_pixels_len += len( im2shapes[temp_im2shape] )
      
      for temp_im2s_nbr in im2shapes_neighbors[ temp_im2shape ]:
         if temp_im2s_nbr not in each_ch_shapes[1] and len( im2shapes[temp_im2s_nbr] ) >= third_smallest_pixc:
            im2s_neighbors.add( temp_im2s_nbr )
            im2total_neighbors += len( im2shapes[temp_im2s_nbr] )
   
   
   if im1total_neighbors > im2total_neighbors:
      smaller_total_neighbors = im2total_neighbors
   else:
      smaller_total_neighbors = im1total_neighbors
   
   cur_nbr_match_counter = 0
   matched = False
   matched_im2s_neighbors = []
   for im1s_neighbor in im1s_neighbors:
      
      for im2s_neighbor in im2s_neighbors:
         
         if im1shapes_colors[im1s_neighbor] != im2shapes_colors[im2s_neighbor] or im2s_neighbor in matched_im2s_neighbors:
            continue
   
         # [(12, 15), (11, 15), ... ]
         im1shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( im1shapes[im1s_neighbor], im_width, param_shp_type=0 )  
         im2shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( im2shapes[im2s_neighbor], im_width, param_shp_type=0 )
   
         im1_im2_nbr_match = same_shapes_functions.match_shape_while_moving_it( im1shp_coord_xy, im2shp_coord_xy )
         im2_im1_nbr_match = same_shapes_functions.match_shape_while_moving_it( im2shp_coord_xy, im1shp_coord_xy )
         if im1_im2_nbr_match is True and im2_im1_nbr_match is True:         

            cur_nbr_match_counter += 1
            matched_im2s_neighbors.append( im2s_neighbor )


            if cur_nbr_match_counter >= 1 and cur_nbr_match_counter / smaller_total_neighbors >= 0.35:
               verified_shapes.add( each_ch_shapes )
               matched = True
               break
            
      if matched is True:
         break




with open(changed_shapes_ddir + im1file + "." + im2file + "verified.data", 'wb') as fp:
   pickle.dump(verified_shapes, fp)
fp.close()



















