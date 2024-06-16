
from libraries import pixel_shapes_functions, pixel_functions, image_functions, same_shapes_functions, btwn_amng_files_functions
from libraries.cv_globals import top_shapes_dir, scnd_stg_all_files, scnd_stg_spixc_dir, scnd_stg_ch_btwn_frames_dir
from libraries.cv_globals import internal, top_images_dir
from libraries import cv_globals

from PIL import Image
import math
import os, sys
import copy, pickle


# param_shapes
# list of tuple image1 shape and image2 shape
# [ ( image1 shapeid, image2 shapeid ), ... ]
# tuple can be list also.
# outer list can also be set.
# list of tuple or set of tuple or list of list.
#
# returns verified_shapes
# { ( image1 shapeid, image2 shapeid ), ... }
def verify_matches( param_shapes, im_shapes, im_colors, im_neighbors, im_size, min_colors, match_nbr_count=0.43 ):

   verified_shapes = set()
   
   frth_smallest_pixc = cv_globals.get_frth_smallest_pixc( im_size )

   for each_shapes in param_shapes:

         
      # neighbor match counting needs to be done from smaller shape.
      total_neighbors = 0
      
      cur_nbr_match_counter = 0
      matched = False
      matched_im2neighbors = []
      for im1nbr in im_neighbors[0][each_shapes[0]]:
         if len( im_shapes[0][im1nbr] ) < frth_smallest_pixc:
            continue
         
         cur_count_done = False
         for im2nbr in im_neighbors[1][each_shapes[1]]:
         
            if len( im_shapes[1][im2nbr] ) < frth_smallest_pixc or im2nbr in matched_im2neighbors:
               continue
            
            # check if size is too different
            im1shapes_total = len( im_shapes[0][im1nbr] )
            im2shapes_total = len( im_shapes[1][im2nbr] )
      
            im1_2pixels_diff = abs( im1shapes_total - im2shapes_total )
            if im1_2pixels_diff != 0:
               if im1shapes_total > im2shapes_total:
                  if im1_2pixels_diff / im2shapes_total > 1:
                     continue
               else:
                  if im1_2pixels_diff / im1shapes_total > 1:
                     continue                
            
            if cur_count_done is False:
               total_neighbors += 1
               cur_count_done = True

            if min_colors is True:
               if im_colors[0][im1nbr] != im_colors[1][im2nbr]:
                  continue
            else:
               appear_diff = pixel_functions.compute_appearance_difference(im_colors[0][im1nbr], im_colors[1][im2nbr] )
               if appear_diff is True:
                  # different appearance
                  continue               

            # get first element to check if it is (x,y) or pixel index
            if type( list( im_shapes[0][im1nbr] )[0] ) is tuple :
               param_shp_type = 1
            else:
               param_shp_type = 0
            
            # [(12, 15), (11, 15), ... ]
            im1shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( im_shapes[0][im1nbr], im_size[0], param_shp_type=param_shp_type )  
            im2shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( im_shapes[1][im2nbr], im_size[0], param_shp_type=param_shp_type )
            
            #image_functions.cr_im_from_shapeslist2( "10", "videos/street3/resized/min/", [ im1nbr ] )
            #image_functions.cr_im_from_shapeslist2( "11", "videos/street3/resized/min/", [ im2nbr ] )
            
            
            # match from smaller shape
            if im1shapes_total > im2shapes_total:
               im1_im2_nbr_match = same_shapes_functions.match_shape_while_moving_it( im2shp_coord_xy, im1shp_coord_xy, match_threshold=0.6 )
            else:
               im1_im2_nbr_match = same_shapes_functions.match_shape_while_moving_it( im1shp_coord_xy, im2shp_coord_xy, match_threshold=0.6 )
            if im1_im2_nbr_match is True:     
               
               cur_nbr_match_counter += 1
               matched_im2neighbors.append( im2nbr )


      if total_neighbors < 3:
         continue
      if cur_nbr_match_counter >= 1 and cur_nbr_match_counter / total_neighbors >= match_nbr_count:
         verified_shapes.add( (each_shapes[0], each_shapes[1]) )

   

   return verified_shapes



# remove very small isolated shapes
# param_shapes -> [ [ shapes ], [ shapes ] ]
def rm_vsmall_isolated_shapes( param_shapes, im_shapes, im_boundaries, im_shape_by_pindex, im_size ):
   
   result_shapes = []
   
   def _rm_vsmall_isolated_shapes( _param_shapes, _im_shapes, _im_boundaries, _im_shape_by_pindex ):
      
      _result_shapes = []
      
      biggest_shape_len = max( [ len( _im_shapes[ temp_shape ] ) for temp_shape in _param_shapes ] )
      
      biggest_shapes = [ temp_shape for temp_shape in _param_shapes if len( _im_shapes[ temp_shape ] ) == biggest_shape_len ]
      _result_shapes.extend( biggest_shapes )
      
      for each_shape in _param_shapes:
         # {(231, 63), (244, 82), ... }
         vicinity_pixels = pixel_shapes_functions.get_shape_vicinity_pixels( _im_boundaries[ each_shape ], 3, im_size, param_shp_type=1 )         
      
         vicinity_shapes = set()
         # convert xy to pixel indexes
         for pixel in vicinity_pixels:
            pixel_index = pixel_functions.convert_xy_to_pindex( pixel, im_size[0] )
            
            for temp_shapeid in _im_shape_by_pindex[ pixel_index ]:
               vicinity_shapes.add(temp_shapeid )      
      
         
         for temp_shape in _param_shapes:
            if temp_shape != each_shape and temp_shape in vicinity_shapes:
               
               if biggest_shape_len / 25 < len( _im_shapes[ temp_shape ] ):
                  _result_shapes.append( each_shape )

                  break
      
      
      return _result_shapes




   if len( param_shapes[0] ) > 1:
      _results = _rm_vsmall_isolated_shapes( param_shapes[0], im_shapes[0], im_boundaries[0], im_shape_by_pindex[0] )

      result_shapes.append( _results )
         
      
   else:
      result_shapes.append( param_shapes[0] )
   
   if len( param_shapes[1] ) > 1:
      _results = _rm_vsmall_isolated_shapes( param_shapes[1], im_shapes[1], im_boundaries[1], im_shape_by_pindex[1] )

      result_shapes.append( _results )
   
   else:
      result_shapes.append( param_shapes[1] )


   return result_shapes


# im_dir example: videos/street3/resized/min1.
# shapeid_or_pixels: if shapeid 2553. if pixels { (x,y), ... }
# im1or2 if search in image1 then, 0. if search in image2 then 1.
# search_file: 25.26. 25 image and 26 image file.
# pindex_or_xy: xy or pindex
def search_in_all_matches( im_dir, shapeid_or_pixels, im1or2, search_file, pindex_or_xy='' ):
   all_results = []

   across_all_files_ddir = top_shapes_dir + im_dir + scnd_stg_all_files + "/data/"
   across_all_files_dfile = across_all_files_ddir + "all_files.data"
   with open (across_all_files_dfile, 'rb') as fp:
      acrs_all_files_shapes = pickle.load(fp)
   fp.close()

   all_matches_so_far_dfile = across_all_files_ddir + "all_matches.data"
   if os.path.exists( all_matches_so_far_dfile ):
      with open (all_matches_so_far_dfile, 'rb') as fp:
         all_matches_so_far = pickle.load(fp)
      fp.close()
   else:
      all_matches_so_far = acrs_all_files_shapes
   
   all_results.append( all_matches_so_far )
   
   verified2shapes_dfile = across_all_files_ddir + "verified2.data"
   if os.path.exists( verified2shapes_dfile ):
      with open (verified2shapes_dfile, 'rb') as fp:
         # {'10.11': [('37042', '43422'), ('40641', '43422'), ... ], ... }
         # { prev filename_cur filename: [ ( image1 shapeid, image2 shapeid), ... ], ... }
         verified2_shapes = pickle.load(fp)
      fp.close()

   all_results.append( verified2_shapes )

   relpos_nbr_dfile = top_shapes_dir + im_dir + scnd_stg_all_files + "/relpos_nbr/data/1" + ".data"
   if os.path.exists( relpos_nbr_dfile ):
      with open (relpos_nbr_dfile, 'rb') as fp:
         relpos_nbr_shapes = pickle.load(fp)
      fp.close()

   all_results.append( relpos_nbr_shapes )

   relpos_nbr2_dfile = top_shapes_dir + im_dir + scnd_stg_all_files + "/relpos_nbr/data/2.data"
   if os.path.exists( relpos_nbr2_dfile ):
      with open (relpos_nbr2_dfile, 'rb') as fp:
         relpos_nbr2_shapes = pickle.load(fp)
      fp.close()

   all_results.append( relpos_nbr2_shapes )

   relpos_nbr3_dfile = top_shapes_dir + im_dir + scnd_stg_all_files + "/relpos_nbr/data/verified3.data"
   if os.path.exists( relpos_nbr3_dfile ):
      with open (relpos_nbr3_dfile, 'rb') as fp:
         relpos_nbr3_shapes = pickle.load(fp)
      fp.close()

   all_results.append( relpos_nbr3_shapes )

   missed_shapes2_ddir = top_shapes_dir + im_dir + scnd_stg_all_files + "/consecutive_missed/data/2" + ".data"
   if os.path.exists( missed_shapes2_ddir ):
      with open (missed_shapes2_ddir, 'rb') as fp:
         # {'10.11': [('37042', '43422'), ('40641', '43422'), ... ], ... }
         # { prev filename_cur filename: [ ( image1 shapeid, image2 shapeid), ... ], ... }
         missed_shapes2 = pickle.load(fp)
      fp.close()

   all_results.append( missed_shapes2 )

   missed_shapes3_ddir = top_shapes_dir + im_dir + scnd_stg_all_files + "/consecutive_missed/data/3" + ".data"
   if os.path.exists( missed_shapes3_ddir ):
      with open (missed_shapes3_ddir, 'rb') as fp:
         # {'10.11': [('37042', '43422'), ('40641', '43422'), ... ], ... }
         # { prev filename_cur filename: [ ( image1 shapeid, image2 shapeid), ... ], ... }
         missed_shapes3 = pickle.load(fp)
      fp.close()

   all_results.append( missed_shapes3 )

   missed_shapes5_ddir = top_shapes_dir + im_dir + scnd_stg_all_files + "/consecutive_missed/data/5" + ".data"
   if os.path.exists( missed_shapes5_ddir ):
      with open (missed_shapes5_ddir, 'rb') as fp:
         # {'10.11': {('37042', '43422'), ('40641', '43422'), ... }, ... }
         # { prev filename_cur filename: { ( image1 shapeid, image2 shapeid), ... }, ... }
         missed_shapes5 = pickle.load(fp)
      fp.close()

   all_results.append( missed_shapes5 )

   move_together_ddir = top_shapes_dir + im_dir + scnd_stg_all_files + "/move_together/data/"
   move_together_dfile = move_together_ddir + "move_together.data"
   if os.path.exists( move_together_dfile ):
      with open (move_together_dfile, 'rb') as fp:
         # { filename: { matched shapes : [ ( moving togher shape image1 shape, moving together shape image2 shape ), ... ], ... }, ... }
         # {'10.11': {'39441.39842': [('28205', '26606'), ('40243', '40248')], ... }, ... }
         move_together_shapes = pickle.load(fp)
      fp.close()

   all_results.append( move_together_shapes )

   spixc_dir = top_shapes_dir + im_dir + scnd_stg_spixc_dir
   spixc_shapes_dfile = spixc_dir + "/data/" + "1.data"
   if os.path.exists( spixc_shapes_dfile ):
      with open (spixc_shapes_dfile, 'rb') as fp:
         # { '10.11': [ [ [ im1shapes ], [ im2shapes ] ], ...  ], ... }
         spixc_shapes = pickle.load(fp)
      fp.close()

   all_results.append( spixc_shapes )

   ch_btwn_frames_ddir = top_shapes_dir + im_dir + scnd_stg_ch_btwn_frames_dir + "/data/"
   ch_btwn_frames4_dfile = ch_btwn_frames_ddir + "4.data"
   if os.path.exists( ch_btwn_frames4_dfile ):
      with open (ch_btwn_frames4_dfile, 'rb') as fp:
         # { '10.11': [ [ [ im1shapes ], [ im2shapes ] ], ...  ], ... }
         pixch_on_notfnd_shapes = pickle.load(fp)
      fp.close()

   all_results.append( pixch_on_notfnd_shapes )

   image_template_ddir = top_shapes_dir + im_dir + scnd_stg_all_files + "/image_template/data/"
   multi_shapes_by_img_tmpl_dfile = image_template_ddir + "verified_multi1.data"  
   if os.path.exists( multi_shapes_by_img_tmpl_dfile ):
      with open (multi_shapes_by_img_tmpl_dfile, 'rb') as fp:
         # {'1.2': [[{'68452', '52800'}, ['56042', '68454']]], '2.3': [[['37593', '33271'], {'33811', '32189', ... }], ... ], ... }
         multi_shapes_by_img_tmpl = pickle.load(fp)
      fp.close()

   all_results.append( multi_shapes_by_img_tmpl )

   third_stage_notfnd_shapes_dir = top_shapes_dir + im_dir + "trd_stage/notfnd_shapes/"
   third_st_notfnd_shapes_ddir = third_stage_notfnd_shapes_dir + "data/"

   third_st_staying_dfile = third_st_notfnd_shapes_ddir + "staying.data"
   if os.path.exists( third_st_staying_dfile ):
      with open (third_st_staying_dfile, 'rb') as fp:
         third_st_sty_shapes = pickle.load(fp)
      fp.close()

   all_results.append( third_st_sty_shapes )
   
   matches_wk = []

   cur_im1file = search_file.split(".")[0]
   cur_im2file = search_file.split(".")[1]
   
   target_file = search_file.split(".")[im1or2]
   
   im1 = Image.open(top_images_dir + im_dir  + cur_im1file + ".png" )
   im_size = im1.size   

   if type( shapeid_or_pixels ) is int:
      # shapeid

      for each_result in all_results:
         if search_file in each_result.keys():
      
            for each_shapes in each_result[ search_file ]:
               if type( each_shapes[0] ) is list or type( each_shapes[0] ) is set:
                  if shapeid_or_pixels in each_shapes[ im1or2 ]:
                     matches_wk.append( each_shapes )
               else:
                  if shapeid_or_pixels == each_shapes[im1or2]:
                     matches_wk.append( each_shapes )

   else:
      # pixels
      
      shapes_dir = top_shapes_dir + im_dir + "shapes/"
      
      if pindex_or_xy == "xy":
         target_im_shapes, lowest_file_num = btwn_amng_files_functions.get_all_image_shapes( shapes_dir, convert_to_xy=True, target_files=[target_file] )
      elif pindex_or_xy == "pindex":
         target_im_shapes, lowest_file_num = btwn_amng_files_functions.get_all_image_shapes( shapes_dir, target_files=[target_file] )
      
      
      target_file_index = int(target_file) - lowest_file_num
      for each_result in all_results:
         if search_file in each_result.keys():
            
            for each_shapes in each_result[ search_file ]:  
               # ( 111, 222 ) or [ [ im1shapes ], [ im2shapes ] ]    
               pixels = set()
               if type( each_shapes[im1or2] ) is int:
                  # image shapes get updated so shapeid may already be deleted
                  if each_shapes[im1or2] not in target_im_shapes[target_file_index]:
                     continue
                  
                  pixels = set( target_im_shapes[target_file_index][ each_shapes[im1or2] ] )
               else:
                  for shapeid in each_shapes[im1or2]:
                     if shapeid not in target_im_shapes[target_file_index]:
                        continue
                     pixels |= set( target_im_shapes[target_file_index][ shapeid ] )
                              
               common_pixels = shapeid_or_pixels.intersection( pixels )
               if len( common_pixels ) >= 1:
                  matches_wk.append( each_shapes )
               
   
   # delete duplicates
   matches = []
   [matches.append(x) for x in matches_wk if x not in matches]

   return matches


# all_im_shapes is the one returned by btwn_amng_files_functions.get_all_image_shapes( shapes_dir )
# btwn_files_nums is the one returned by btwn_amng_files_functions.get_btwn_files_nums( lowest_filenum, highest_filenum )
# low_highest_nums is the one returned by btwn_amng_files_functions.get_low_highest_filenums( directory )
def get_all_matches_sfar_search_by_shapeid( all_matches_so_far, all_im_shapes, btwn_files_nums, low_highest_nums ):

   # { each_files: ( image1 all_matches_so_far search by shapeid, image2 all_matches_so_far search by shapeid ), ... }
   # search by image1 shapeid: { image1 shapeid: { ( 555, 222 ), ... }, ... }
   all_m_sfar_by_im_shapeid = {}

   for each_files in btwn_files_nums: 

      cur_im1file = each_files.split(".")[0]
      cur_im2file = each_files.split(".")[1]

      all_m_sfar_by_im_shapeid[ each_files ] = ( {}, {} )
      
      for im1or2 in [ 0, 1 ]:
         cur_file_index = int( cur_im1file ) - low_highest_nums[0] + im1or2
         for shapeid in all_im_shapes[ cur_file_index ]:

            all_m_sfar_by_im_shapeid[each_files][im1or2][shapeid] = { temp_shapes for temp_shapes in all_matches_so_far[each_files] if temp_shapes[im1or2] == shapeid }


   return all_m_sfar_by_im_shapeid























