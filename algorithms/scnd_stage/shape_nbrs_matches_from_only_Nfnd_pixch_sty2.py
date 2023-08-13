# shape_nbrs_matches_from_only_Nfnd_pixch_sty2.py
# what is different from shape_nbrs_matches_from_only_Nfnd_pixch_sty.py is that this uses the match_shape_while_moving_it for judging 
# the match while shape_nbrs_matches_from_only_Nfnd_pixch_sty.py uses find_match_by_eachShp_loc
from PIL import Image
import pickle
import math
import copy
import os, sys
from libraries.cv_globals import top_temp_dir, top_shapes_dir, top_images_dir, internal, pixch_sty_dir, scnd_stage_alg_dir, snd_stg_alg_shp_nbrs_dir
from libraries.cv_globals import frth_smallest_pixc, Lshape_size, third_smallest_pixc
from libraries import read_files_functions, pixel_shapes_functions, image_functions, pixel_functions, same_shapes_functions



directory = "videos/street3/resized/min"
im1file = "14"
im2file = "15"
switch_filename = True

shapes_type = "intnl_spixcShp"


if len(sys.argv) > 1:
   im1file = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   im2file = sys.argv[1][0: len( sys.argv[1] ) - 4 ]
   switch_filename = sys.argv[2]
   directory = sys.argv[3]
   
   shapes_type = "intnl_spixcShp"
   
   display_or_not = False

   print("execute script algorithms/styLshapes/find_styLshp_wo_pixch_btwn_frames.py file1 " + im1file + " file2 " + im2file + " directory " + directory )


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

# for getting non-found shapes
pixch_dir = top_shapes_dir + directory + pixch_sty_dir + "/"
pixch_sty_dfile = pixch_dir + "data/" + im1file + "." + im2file + "verified.data"
with open (pixch_sty_dfile, 'rb') as fp:
   # [ [('10.11_11.12', ('59525', '59913')),
   #    ('11.12_12.13', ('59913', '60331')), ('12.13_13.14', ('60331', '60716'))] ]
   # 
   # [ [ ('10.11_11.12', ( image11 shapeid, image12 shapeid)),
   #     ('11.12_12.13', ( image12s shapeid, image13 shapeid)), ('12.13_13.14', (image13 shapeid, image14 shapeid)) ] ]
   pixch_stayed_shapes = pickle.load(fp)
fp.close()


if switch_filename is True:
   temp_filename = im1file
   im1file = im2file
   im2file = temp_filename

original_image = Image.open(top_images_dir + directory + im1file + ".png")
orig_im_data = original_image.getdata()
im_width, im_height = original_image.size
image2obj = Image.open(top_images_dir + directory + im2file + ".png")
im2data = image2obj.getdata()


im1shapes_boundaries = {}
im2shapes_boundaries = {}
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
      cur_shape_xy = set()
      for pindex in im1shapes[shapeid]:
         xy = pixel_functions.convert_pindex_to_xy( pindex, im_width )
         
         cur_shape_xy.add( xy )
      
      im1shapes[shapeid] = cur_shape_xy
      
      im1shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels( cur_shape_xy )
      

   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()

   for shapeid in im2shapes:
      cur_shape_xy = set()
      for pindex in im2shapes[shapeid]:
         xy = pixel_functions.convert_pindex_to_xy( pindex, im_width )
         
         cur_shape_xy.add( xy )
      
      im2shapes[shapeid] = cur_shape_xy
      
      im2shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels( cur_shape_xy )


   shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + im1file + "_shape_nbrs.txt"
   im2shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + im2file + "_shape_nbrs.txt"



# {'79999': ['71555', '73953', ...], ...}
im1shapes_neighbors = read_files_functions.rd_dict_k_v_l(im1file, directory, shape_neighbors_file)
im2shapes_neighbors = read_files_functions.rd_dict_k_v_l(im2file, directory, im2shape_neighbors_file)


def find_neighbor_matches( first_call, cur_shapeids, cur_match, already_processed_shapes,  cur_match_count ):
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
         
         if cur_neighbor in cur_match[0]:
            # cur_neighbor has already matched with earlier iteration of cur_im2neighbor
            break
         
         if len( im2shapes[cur_im2neighbor] ) < third_smallest_pixc:
            already_processed_shapes[1].append( cur_im2neighbor )
            continue

         if im1shapes_colors[cur_neighbor] != im2shapes_colors[cur_im2neighbor]:
            continue        

         # [(12, 15), (11, 15), ... ]
         im1shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( im1shapes[cur_neighbor], im_width, param_shp_type=1 )  
         im2shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( im2shapes[cur_im2neighbor], im_width, param_shp_type=1 )
         
         if len( im1shapes[cur_neighbor] ) > len( im2shapes[cur_im2neighbor] ):
            # checking from larger shape effectively means checking from both sides, smaller and larger.
            im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( im1shp_coord_xy, im2shp_coord_xy )
         else:
            im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( im2shp_coord_xy, im1shp_coord_xy )
         
         if im1im2nbr_match is True:
            result =   pixel_shapes_functions.check_shape_attached_near( im1shapes_boundaries[cur_shapeids[0]], im1shapes_boundaries[cur_neighbor], im2shapes_boundaries[cur_shapeids[1]],
                                                                 im2shapes_boundaries[cur_im2neighbor], original_image.size )
            if result is not True:
               continue
               
            if first_call is True:
               cur_match[0].append( cur_shapeids[0] )
               cur_match[1].append( cur_shapeids[1] )
         
               cur_match_count[0] += len( im1shapes[ cur_shapeids[0] ] )           
               
            cur_match[0].append( cur_neighbor )
            cur_match[1].append( cur_im2neighbor )
         
            cur_match_count[0] += len( im1shapes[ cur_neighbor ] )
         
            already_processed_shapes[0].append( cur_neighbor )
            already_processed_shapes[0].append( cur_im2neighbor )

   
            find_neighbor_matches( False, [ cur_neighbor, cur_im2neighbor ], cur_match, already_processed_shapes, cur_match_count )
            
            # cur_neighbor has already matched, so go to next cur_neighbor
            break
            





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


im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im1file, directory, shapes_type=shapes_type, min_colors=True)
im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im2file, directory, shapes_type=shapes_type, min_colors=True)

all_matches_wk = []
progress_counter = len( start_not_f_shapes )
for start_non_found_shape in start_not_f_shapes:
   print( str(progress_counter) + " remaining" )
   progress_counter -= 1

   # {(152, 8), (141, 8), ... }
   vicinity_pixels = pixel_shapes_functions.get_shape_vicinity_pixels( im1shapes[start_non_found_shape], 13, original_image.size, 1 )

   for im2start_not_f_shape in im2start_not_f_shapes:
      same_locations =  vicinity_pixels.intersection( im2shapes[im2start_not_f_shape] )
      if len( same_locations ) == 0:
         continue   

      if im1shapes_colors[start_non_found_shape] != im2shapes_colors[im2start_not_f_shape]:
         continue

      cur_match = [ [], [] ]
      already_processed_shapes = [ [], [] ]
      cur_match_count = [0]
   
      # [(12, 15), (11, 15), ... ]
      im1shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( im1shapes[start_non_found_shape], im_width, param_shp_type=1 )  
      im2shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( im2shapes[im2start_not_f_shape], im_width, param_shp_type=1 )
   
      match = same_shapes_functions.match_shape_while_moving_it( im1shp_coord_xy, im2shp_coord_xy )
      if match is True:
         already_processed_shapes[0].append( start_non_found_shape )
         already_processed_shapes[0].append( im2start_not_f_shape )
   
         find_neighbor_matches( True, [ start_non_found_shape, im2start_not_f_shape ], cur_match, already_processed_shapes, cur_match_count )
         if len( cur_match[0] ) == 0:
            continue
         
         # at last, check if image1 shapes and image2 shapes match as a whole
         image1pixels = []
         image2pixels = []
         
         for im1shapeid in cur_match[0]:
            image1pixels.extend( im1shapes[im1shapeid] )
         for im2shapeid in cur_match[1]:
            image2pixels.extend( im2shapes[im2shapeid] )
            
         # first check if image1 total pixel amount is too different from image2 total pixels

         im1shapes_total = len( image1pixels )
         im2shapes_total = len( image2pixels )
      
         im1_2pixels_diff = abs( im1shapes_total - im2shapes_total )
         if im1_2pixels_diff != 0:
            if im1shapes_total > im2shapes_total:
               if im1_2pixels_diff / im2shapes_total > 1:
                  continue
            else:
               if im1_2pixels_diff / im1shapes_total > 1:
                  continue          


         if switch_filename is True:
            temp_im1match = cur_match[1]
            temp_im2match = cur_match[0]
            cur_match = [ temp_im1match, temp_im2match ]
         else:
            temp_im1match = cur_match[0]
            temp_im2match = cur_match[1]
            cur_match = [ temp_im1match, temp_im2match ]         
         
         all_matches_wk.append( cur_match )
         #image_functions.cr_im_from_shapeslist2( im1file, directory, cur_match[0], save_filepath=None , shapes_rgb=(255, 0, 0 ) )
         #image_functions.cr_im_from_shapeslist2( im2file, directory, cur_match[1], save_filepath=None , shapes_rgb=(0, 0, 255 ) )
         
         # start_non_found_shape has matched, so go to next start_non_found_shape
         break
         

scnd_stage_alg_shpDir = top_shapes_dir + directory + scnd_stage_alg_dir + "/"
if os.path.exists(scnd_stage_alg_shpDir ) == False:
   os.makedirs(scnd_stage_alg_shpDir )

scnd_stg_alg_shp_nbrs_dir = top_shapes_dir + directory + snd_stg_alg_shp_nbrs_dir + "/only_nfnd_pixch_sty2/"

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



















