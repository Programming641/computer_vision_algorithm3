
from PIL import Image
import pickle
import math
import copy
import os, sys
from libraries.cv_globals import top_temp_dir, top_shapes_dir, top_images_dir, internal, pixch_sty_dir, scnd_stage_alg_dir, snd_stg_alg_shp_nbrs_dir
from libraries.cv_globals import frth_smallest_pixc, Lshape_size, third_smallest_pixc
from libraries import read_files_functions, pixel_shapes_functions, image_functions, pixel_functions, same_shapes_functions
import winsound


directory = "videos/street3/resized/min"
im1file = "14"
im2file = "15"
switch_filename = True

shapes_type = "intnl_spixcShp"


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'



# for getting non-found shapes
pixch_dir = top_shapes_dir + directory + pixch_sty_dir + "/"
pixch_sty_dfile = pixch_dir + "data/" + im1file + "." + im2file + "verified.data"
with open (pixch_sty_dfile, 'rb') as fp:
   # [('1270', '2072'), ('2062', '2062'), ... ]
   # [ ( image1 shapeid, image2 shapeid ), ... ]
   pixch_stayed_shapes = pickle.load(fp)
fp.close()


if switch_filename is True:
   temp_filename = im1file
   im1file = im2file
   im2file = temp_filename

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
   
   for shapeid in im1shapes:
      cur_shape_xy = []
      for pindex in im1shapes[shapeid]:
         xy = pixel_functions.convert_pindex_to_xy( pindex, im_width )
         
         cur_shape_xy.append( xy )
      
      im1shapes[shapeid] = cur_shape_xy
      

   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()

   for shapeid in im2shapes:
      cur_shape_xy = []
      for pindex in im2shapes[shapeid]:
         xy = pixel_functions.convert_pindex_to_xy( pindex, im_width )
         
         cur_shape_xy.append( xy )
      
      im2shapes[shapeid] = cur_shape_xy


   im1shapes_locations_file = s_pixcShp_intnl_dir + "locations/" + im1file + "_loc.data"
   im2shapes_locations_file = s_pixcShp_intnl_dir + "locations/" + im2file + "_loc.data"
   with open (im1shapes_locations_file, 'rb') as fp:
      #  { '79949': ['25', '20'], '79999': ['25'], ...}
      im1shapes_locations = pickle.load(fp)
   fp.close()
   with open (im2shapes_locations_file, 'rb') as fp:
      im2shapes_locations = pickle.load(fp)
   fp.close()


   shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + im1file + "_shape_nbrs.txt"
   im2shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + im2file + "_shape_nbrs.txt"



# {'79999': ['71555', '73953', ...], ...}
im1shapes_neighbors = read_files_functions.rd_dict_k_v_l(im1file, directory, shape_neighbors_file)
im2shapes_neighbors = read_files_functions.rd_dict_k_v_l(im2file, directory, im2shape_neighbors_file)


def find_neighbor_matches( cur_shapeids, cur_im_shapes, already_processed_shapes,  cur_highest_match_count, cur_highest_match ):
   # image1 shape neighbors
   for cur_neighbor in im1shapes_neighbors[ cur_shapeids[0] ]:
      if cur_neighbor in already_processed_shapes[0] or cur_neighbor not in non_found_shapes:
         continue
      
      if len( im1shapes[cur_neighbor] ) < third_smallest_pixc:
         already_processed_shapes[0].append( cur_neighbor )
         continue
      
      for cur_im2neighbor in im2shapes_neighbors[ cur_shapeids[1] ]:
         if cur_im2neighbor in already_processed_shapes[1] or cur_im2neighbor not in im2non_found_shapes:
            continue
         
         
         if len( im2shapes[cur_im2neighbor] ) < third_smallest_pixc:
            already_processed_shapes[1].append( cur_im2neighbor )
            continue
         
         if cur_neighbor in already_processed_shapes[0]:
            # cur_neighbor already matched with earlier iteration of cur_im2neighbor
            break
         
         
         cur_im_shapes[0][ cur_neighbor ] = im1shapes[cur_neighbor]
         
         cur_im_shapes[1][ cur_im2neighbor ] = im2shapes[cur_im2neighbor]
         
         # [['2876', '1270', ... ], ['78052', '50081', ...]]
         # [ [ image1 shapeids ], [ image2 shapeids ] ]
         match, total_match_count = same_shapes_functions.find_match_by_eachShp_loc( cur_im_shapes[0], cur_im_shapes[1], [im1shapes_colors, im2shapes_colors], 
                    im_width, check_both_sides=True )


         if match is not None and len( match[0] ) > 0:
            already_processed_shapes[0].append( cur_neighbor )
            already_processed_shapes[1].append( cur_im2neighbor )
            
            if total_match_count > cur_highest_match_count[0]:
               cur_highest_match_count[0] = total_match_count
               cur_highest_match = match
            find_neighbor_matches( [ cur_neighbor, cur_im2neighbor ], cur_im_shapes, already_processed_shapes, cur_highest_match_count, cur_highest_match  )         


if switch_filename is True:
   im1pixch_sty_shapes = [shape[1] for shape in pixch_stayed_shapes]
   im2pixch_sty_shapes = [shape[0] for shape in pixch_stayed_shapes]   

else:
   im1pixch_sty_shapes = [shape[0] for shape in pixch_stayed_shapes]
   im2pixch_sty_shapes = [shape[1] for shape in pixch_stayed_shapes]

non_found_shapes = []
start_not_f_shapes = []
for shapeid in im1shapes:
   if shapeid not in im1pixch_sty_shapes:
      non_found_shapes.append( shapeid )
      
      if len( im1shapes[shapeid] ) >= frth_smallest_pixc:
         start_not_f_shapes.append( shapeid )


im2non_found_shapes = []
im2start_not_f_shapes = []
for shapeid in im2shapes:
   if shapeid not in im2pixch_sty_shapes:
      im2non_found_shapes.append( shapeid )
      
      if len( im2shapes[shapeid] ) >= frth_smallest_pixc:
         im2start_not_f_shapes.append( shapeid )
      
      

im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im1file, directory, shapes_type=shapes_type)
im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im2file, directory, shapes_type=shapes_type)

all_matches_wk = []
progress_counter = len( start_not_f_shapes )
for start_non_found_shape in start_not_f_shapes:
   print( str(progress_counter) + " remaining" )
   progress_counter -= 1
   
   cur_shapes_pixels = []
   
   cur_shapes_pixels.extend( im1shapes[start_non_found_shape] )
   
   for im1shape_neighbor in im1shapes_neighbors[start_non_found_shape]:
      # [ [ image1 already processed shapes ], [ image2 already processed shapes ] ]
      if im1shape_neighbor not in non_found_shapes:
         continue
      
      if len( im1shapes[im1shape_neighbor] ) < third_smallest_pixc:
         continue
   
      cur_shapes_pixels.extend( im1shapes[im1shape_neighbor] )
      
      # {(216, 11), (208, 7), ... }
      vicinity_pixels = pixel_shapes_functions.get_shape_vicinity_pixels( cur_shapes_pixels, 13, original_image.size, 1 )
      
      
      # get nearby image2 not found shapes
      nearby_im2start_nfnd_shapes = []
      for temp_im2shapeid in im2start_not_f_shapes:
         found_pixels = set( im2shapes[temp_im2shapeid] ).intersection( vicinity_pixels )
         
         if len( found_pixels ) >= 1:
            nearby_im2start_nfnd_shapes.append( temp_im2shapeid )
      
      cur_highest_match_count = None
      cur_highest_match = None      

      for im2start_not_f_shape in nearby_im2start_nfnd_shapes:

         for im2shape_neighbor in im2shapes_neighbors[im2start_not_f_shape]:
            if im2shape_neighbor not in im2non_found_shapes:
               continue         
            
            if len( im2shapes[im2shape_neighbor] ) < third_smallest_pixc:
               continue

            already_processed_shapes = [ [] ]
            already_processed_shapes[0].append( start_non_found_shape )
            already_processed_shapes[0].append( im1shape_neighbor )

            cur_im1shapes = { start_non_found_shape: im1shapes[start_non_found_shape] }      
            cur_im1shapes[ im1shape_neighbor ] = im1shapes[im1shape_neighbor]

            already_processed_shapes.append( [] )
            already_processed_shapes[1].append( im2start_not_f_shape )    
            already_processed_shapes[1].append( im2shape_neighbor )   
            
            cur_im2shapes = { im2start_not_f_shape: im2shapes[im2start_not_f_shape] }
            cur_im2shapes[ im2shape_neighbor ] = im2shapes[im2shape_neighbor]
            
            
            # [['2876', '1270', ... ], ['78052', '50081', ...]]
            # [ [ image1 shapeids ], [ image2 shapeids ] ]
            match, total_match_count = same_shapes_functions.find_match_by_eachShp_loc( cur_im1shapes, cur_im2shapes, [im1shapes_colors, im2shapes_colors], 
                                       im_width, check_both_sides=True )
            
            if match is not None and len( match[0] ) > 0:

               if cur_highest_match_count is None:
                  cur_highest_match_count = [total_match_count]
                  cur_highest_match = match

               find_neighbor_matches( [ im1shape_neighbor, im2shape_neighbor ], [ cur_im1shapes, cur_im2shapes ], already_processed_shapes, 
                                      cur_highest_match_count, cur_highest_match )
            


      if cur_highest_match_count is not None:

         if switch_filename is True:
            temp_im1match = cur_highest_match[1]
            temp_im2match = cur_highest_match[0]
            cur_highest_match = [ temp_im1match, temp_im2match ]
         else:
            temp_im1match = cur_highest_match[0]
            temp_im2match = cur_highest_match[1]
            cur_highest_match = [ temp_im1match, temp_im2match ]    

         all_matches_wk.append( cur_highest_match )
         #image_functions.cr_im_from_shapeslist2( im1file, directory, cur_highest_match[0], save_filepath=None , shapes_rgb=(255, 0, 0 ) )
         #image_functions.cr_im_from_shapeslist2( im2file, directory, cur_highest_match[1], save_filepath=None , shapes_rgb=(0, 0, 255 ) )


scnd_stage_alg_shpDir = top_shapes_dir + directory + scnd_stage_alg_dir + "/"
if os.path.exists(scnd_stage_alg_shpDir ) == False:
   os.makedirs(scnd_stage_alg_shpDir )

scnd_stg_alg_shp_nbrs_dir = top_shapes_dir + directory + snd_stg_alg_shp_nbrs_dir + "/only_nfnd_pixch_sty/"

if os.path.exists(scnd_stg_alg_shp_nbrs_dir ) == False:
   os.makedirs(scnd_stg_alg_shp_nbrs_dir )

if switch_filename is True:
   with open(scnd_stg_alg_shp_nbrs_dir + im2file + "." + im1file + "." + im1file + ".data", 'wb') as fp:
      pickle.dump(all_matches_wk, fp)
   fp.close()
else:
   with open(scnd_stg_alg_shp_nbrs_dir + im1file + "." + im2file + "." + im1file + ".data", 'wb') as fp:
      pickle.dump(all_matches_wk, fp)
   fp.close()







frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)





















