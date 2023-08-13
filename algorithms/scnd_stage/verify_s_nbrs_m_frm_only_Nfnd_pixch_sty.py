
from PIL import Image
import pickle
import math
import copy
import os, sys
from libraries.cv_globals import top_temp_dir, top_shapes_dir, top_images_dir, internal, pixch_sty_dir, scnd_stage_alg_dir, snd_stg_alg_shp_nbrs_dir
from libraries.cv_globals import sec_smallest_pixc, Lshape_size, third_smallest_pixc
from libraries import read_files_functions, pixel_shapes_functions, image_functions, pixel_functions, same_shapes_functions
import winsound


directory = "videos/street3/resized/min"
im1file = "14"
im2file = "15"
# if target directory is shape_nbrs_matches, make target_dir emtpy, 
# if it's for only_nfnd_pixch_sty. write "/only_nfnd_pixch_sty/" in target_dir
target_dir = "/only_nfnd_pixch_sty2/"
shapes_type = "intnl_spixcShp"

if len(sys.argv) > 1:
   im1file = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   im2file = sys.argv[1][0: len( sys.argv[1] ) - 4 ]
   directory = sys.argv[3]

   print("execute script algorithms/scnd_stage/verify_s_nbrs_m_frm_only_Nfnd_pixch_sty.py file1 " + im1file + " file2 " + im2file + " directory " + directory )



# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'


scnd_stg_alg_shp_nbrs_dir = top_shapes_dir + directory + snd_stg_alg_shp_nbrs_dir + target_dir

scnd_stg_alg_shp_nbrs_dfile1 = scnd_stg_alg_shp_nbrs_dir + im1file + "." + im2file + "." + im1file + ".data"
with open (scnd_stg_alg_shp_nbrs_dfile1, 'rb') as fp:
   # [[['3295', '2086'], ['2875', '2872', '2885']], [['3519', '12318'], ['4713', '4710', '8314', '10715', '14319']], ... ]
   # [ [ [ image1 shapes ], [ image2 shapes ] ], ... ]
   shape_nbrs_matches1 = pickle.load(fp)
fp.close()


scnd_stg_alg_shp_nbrs_dfile2 = scnd_stg_alg_shp_nbrs_dir + im1file + "." + im2file + "." + im2file + ".data"
with open (scnd_stg_alg_shp_nbrs_dfile2, 'rb') as fp:
   # [[['3295', '2086'], ['2875', '2872', '2885']], [['3519', '12318'], ['4713', '4710', '8314', '10715', '14319']], ... ]
   # [ [ [ image1 shapes ], [ image2 shapes ] ], ... ]
   shape_nbrs_matches2 = pickle.load(fp)
fp.close()

original_image = Image.open(top_images_dir + directory + im1file + ".png")
im_width, im_height = original_image.size


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
      cur_shape_xy = []
      for pindex in im1shapes[shapeid]:
         xy = pixel_functions.convert_pindex_to_xy( pindex, im_width )
         
         cur_shape_xy.append( xy )
      
      im1shapes[shapeid] = cur_shape_xy
      
      im1shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels( cur_shape_xy )
      

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
      
      im2shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels( cur_shape_xy )



   shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + im1file + "_shape_nbrs.txt"
   im2shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + im2file + "_shape_nbrs.txt"



# {'79999': ['71555', '73953', ...], ...}
im1shapes_neighbors = read_files_functions.rd_dict_k_v_l(im1file, directory, shape_neighbors_file)
im2shapes_neighbors = read_files_functions.rd_dict_k_v_l(im2file, directory, im2shape_neighbors_file)

im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im1file, directory, shapes_type=shapes_type, min_colors=True)
im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im2file, directory, shapes_type=shapes_type, min_colors=True)


all_shapes_matches = []

for shape_nbrs_match in shape_nbrs_matches1:
   if not shape_nbrs_match in all_shapes_matches:
      all_shapes_matches.append( shape_nbrs_match )

for shape_nbrs_match in shape_nbrs_matches2:
   if not shape_nbrs_match in all_shapes_matches:
      all_shapes_matches.append( shape_nbrs_match )

print( len( all_shapes_matches ) )


def check_shape_size( param_im1shapeid, param_im2shapeid ):
   # check if size is too different
   im1shapes_total = len( im1shapes[param_im1shapeid] )
   im2shapes_total = len( im2shapes[param_im2shapeid] )
      
   im1_2pixels_diff = abs( im1shapes_total - im2shapes_total )
   if im1_2pixels_diff != 0:
      if im1shapes_total > im2shapes_total:
         if im1_2pixels_diff / im2shapes_total > 1:
            return True
      else:
         if im1_2pixels_diff / im1shapes_total > 1:
            return True

   return False            


def get_neighbors_Hatch_nbr( param_shapes_match, cur_shape_boundaries, cur_s_pixels, param_im_neighbors, param_im_shapes, param_im_shape_bnd, param_image ):
   im_shapes_nbrs = set()
   im_highest_attachd_nbr_len = None
   im_secH_attached_nbr_len = None
   im_highest_attachd_nbr = None
   for im_shape in param_shapes_match:
      for temp_im_s_nbr in param_im_neighbors[im_shape]:
         if len( param_im_shapes[temp_im_s_nbr] ) < third_smallest_pixc or temp_im_s_nbr in param_shapes_match or temp_im_s_nbr in im_shapes_nbrs:
            continue
         
         im_shapes_nbrs.add( temp_im_s_nbr )
         
         attached_pixels = pixel_shapes_functions.get_attached_pixels( cur_shape_boundaries, cur_s_pixels, set( param_im_shapes[temp_im_s_nbr] ), 
                                                                       original_image.size   )
         
         if im_highest_attachd_nbr_len is None:
            im_highest_attachd_nbr_len = len( attached_pixels )
            im_highest_attachd_nbr = temp_im_s_nbr
         elif len( attached_pixels ) > im_highest_attachd_nbr_len:
               
            # previous highest becomes the second highest
            im_secH_attached_nbr_len = im_highest_attachd_nbr_len
            
            # highest is replaced by the current one
            im_highest_attachd_nbr_len = len( attached_pixels )
            im_highest_attachd_nbr = temp_im_s_nbr
         
         elif im_secH_attached_nbr_len is None:
            im_secH_attached_nbr_len = len( attached_pixels )
         
         elif len( attached_pixels ) > im_secH_attached_nbr_len:
            # smaller than im_highest_attachd_nbr but bigger than im_secH_attached_nbr_len
            im_secH_attached_nbr_len = len( attached_pixels )



   return im_shapes_nbrs, im_highest_attachd_nbr_len, im_highest_attachd_nbr, im_secH_attached_nbr_len



verified_shapes = []
progress_counter = len( all_shapes_matches )
for shapes_match in all_shapes_matches:
   # shapes_match -> [['3295', '2086'], ['2875', '2872', '2885']]
   
   print( str( progress_counter ) + " remaining" )
   progress_counter -= 1
      
   cur_im1s_bnd = set()
   cur_im1s_pixels = set()
   for im1shape in shapes_match[0]:
      cur_im1s_bnd |= set( im1shapes_boundaries[im1shape] )
      cur_im1s_pixels |= set( im1shapes[im1shape] )
      
   
   # getting all image1 shape neighbors, image1 highest attached neighbor length, im1highest_attached_nbr, and im1secHattach_nbr_len
   im1shapes_nbrs, im1Hattch_nbr_len, im1Hattach_nbr, im1secHattach_nbr_len = get_neighbors_Hatch_nbr( shapes_match[0], 
                                   cur_im1s_bnd, cur_im1s_pixels, im1shapes_neighbors, im1shapes, im1shapes_boundaries, "im1"   )


   
   cur_im2s_bnd = set()
   cur_im2s_pixels = set()
   for im2shape in shapes_match[1]:
      cur_im2s_bnd |= set( im2shapes_boundaries[im2shape] )
      cur_im2s_pixels |= set( im2shapes[im2shape] )

   im2shapes_nbrs, im2Hattach_nbr_len, im2Hattach_nbr, im2secHattach_nbr_len = get_neighbors_Hatch_nbr( shapes_match[1],
                                   cur_im2s_bnd, cur_im2s_pixels, im2shapes_neighbors, im2shapes, im2shapes_boundaries, "im2" )


   if len( im1shapes_nbrs ) < 3 or len( im2shapes_nbrs ) < 3:
      continue
   
   
   # highest attached neighbor check check is only done if the highest attached neighbor has twice more attached pixels than the 
   # second highest attached pixels
   check_highest_attached_nbrs = [ True, True ]
   if im1Hattch_nbr_len > im1secHattach_nbr_len * 2 and len( im1shapes[im1Hattach_nbr] ) > Lshape_size:
      # highest attached neighbor check is needed
      check_highest_attached_nbrs[0] = False
   if im2Hattach_nbr_len > im2secHattach_nbr_len * 2 and len( im2shapes[im2Hattach_nbr] ) > Lshape_size:
      # highest attached neighbor check is needed
      check_highest_attached_nbrs[1] = False

   
   matched_nbrs = 0
   matched_im1nbrs = []
   matched_im2nbrs = []
   
   # before checking all neighbors, check image1 and image2 highest attached neighbors.
   if check_highest_attached_nbrs[0] is False:
      for im2nbr in im2shapes_nbrs:
         if im1shapes_colors[im1Hattach_nbr] != im2shapes_colors[im2nbr]:
            continue      

         size_too_diff = check_shape_size( im1Hattach_nbr, im2nbr )
         if size_too_diff is True:
            continue

         # [(12, 15), (11, 15), ... ]
         im1shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( im1shapes[im1Hattach_nbr], im_width, param_shp_type=1 )  
         im2shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( im2shapes[im2nbr], im_width, param_shp_type=1 )
         
         if len( im1shapes[im1Hattach_nbr] ) > len( im2shapes[im2nbr] ):
            im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( im2shp_coord_xy, im1shp_coord_xy )
         else:
            im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( im1shp_coord_xy, im2shp_coord_xy )

         if im1im2nbr_match is True:
            check_highest_attached_nbrs[0] = True
            matched_nbrs += 1
            matched_im1nbrs.append( im1Hattach_nbr )
            matched_im2nbrs.append( im2nbr )
            break
   
   if check_highest_attached_nbrs[1] is False:
      for im1nbr in im1shapes_nbrs:
         if im2shapes_colors[im2Hattach_nbr] != im1shapes_colors[im1nbr]:
            continue      

         
         size_too_diff = check_shape_size( im1nbr , im2Hattach_nbr )
         if size_too_diff is True:
            continue

         # [(12, 15), (11, 15), ... ]
         im2shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( im2shapes[im2Hattach_nbr], im_width, param_shp_type=1 )  
         im1shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( im1shapes[im1nbr], im_width, param_shp_type=1 )

         if len( im1shapes[im1nbr] ) > len( im2shapes[im2Hattach_nbr] ):
            im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( im2shp_coord_xy, im1shp_coord_xy )
         else:
            im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( im1shp_coord_xy, im2shp_coord_xy )

         if im1im2nbr_match is True:
            check_highest_attached_nbrs[1] = True
            matched_nbrs += 1
            matched_im1nbrs.append( im1nbr )
            matched_im2nbrs.append( im2Hattach_nbr )
            break

   
   
   if all(check_highest_attached_nbrs) is False:
      continue
      
   smaller_neighbor_len = 0
   if len( im1shapes_nbrs ) > len( im2shapes_nbrs ):
      smaller_neighbor_len = len( im2shapes_nbrs )
   else:
      smaller_neighbor_len = len( im1shapes_nbrs )
   

   for im1nbr in im1shapes_nbrs:
      if im1nbr in matched_im1nbrs:
         continue
      
      for im2nbr in im2shapes_nbrs:
         
         if im1shapes_colors[im1nbr] != im2shapes_colors[im2nbr] or im2nbr in matched_im2nbrs:
            continue

         # check if size is too different
         size_too_diff = check_shape_size( im1nbr, im2nbr )
         if size_too_diff is True:
            continue

         # [(12, 15), (11, 15), ... ]
         im1shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( im1shapes[im1nbr], im_width, param_shp_type=1 )  
         im2shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( im2shapes[im2nbr], im_width, param_shp_type=1 )
         
         if len( im1shapes[im1nbr] ) > len( im2shapes[im2nbr] ):
            im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( im2shp_coord_xy, im1shp_coord_xy )
         else:
            im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( im1shp_coord_xy, im2shp_coord_xy )
         if im1im2nbr_match is True:
            
            matched_nbrs += 1
            matched_im2nbrs.append( im2nbr )
            break
   


   if matched_nbrs < 2:
      continue
   
   if matched_nbrs / smaller_neighbor_len >= 0.33:
      # 33% or more of neighbors matched
      verified_shapes.append( shapes_match )


dulicate_ones = set()
# removing duplicates
for lindex, each_verif_shapes in enumerate(verified_shapes):
   # each_verif_shapes -> [['20949', '21343', '22138'], ['20951', '21745', '22140']]
   
   if lindex in dulicate_ones:
      continue
   
   for ano_lindex, ano_each_verif_shapes in enumerate(verified_shapes):
      if lindex == ano_lindex or ano_lindex in dulicate_ones:
         # itself
         continue
         
      temp_im1shapes = set( each_verif_shapes[0] ).difference( ano_each_verif_shapes[0] )
      temp_im1shapes2 = set( ano_each_verif_shapes[0] ).difference( each_verif_shapes[0] )
      
      temp_im2shapes = set( each_verif_shapes[1] ).difference( ano_each_verif_shapes[1] )
      temp_im2shapes2 = set( ano_each_verif_shapes[1] ).difference( each_verif_shapes[1] )
      
      if len( temp_im1shapes ) == 0 and len( temp_im2shapes ) == 0 and len( temp_im1shapes2 ) == 0 and len( temp_im2shapes2 ) == 0:
         dulicate_ones.add( ano_lindex )
   
deleted = 0   
for dulicate_one in dulicate_ones:
   verified_shapes.pop( dulicate_one - deleted )
   deleted += 1



print( len( verified_shapes ) )


with open(scnd_stg_alg_shp_nbrs_dir + im1file + "." + im2file + ".data", 'wb') as fp:
   pickle.dump(verified_shapes, fp)
fp.close()
   


















