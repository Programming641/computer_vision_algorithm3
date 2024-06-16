
from libraries import  btwn_amng_files_functions, pixel_shapes_functions, pixel_functions, image_functions, same_shapes_functions
from libraries import shapes_results_functions


from PIL import ImageTk, Image
import os, sys
import pickle
import copy
import math
import shutil

from libraries.cv_globals import top_shapes_dir, top_images_dir, scnd_stg_all_files
from libraries.cv_globals import scnd_stg_spixc_dir, scnd_stg_ch_btwn_frames_dir
from libraries import cv_globals

directory = "videos/street3/resized/min1"

if len( sys.argv ) >= 2:
   directory = sys.argv[1]

# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

shapes_dir = top_shapes_dir + directory  + "shapes/"



across_all_files_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/data/"
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


obj_shapes_dir = top_shapes_dir + directory + "trd_stage/obj_shapes/"
obj_shapes_ddir = obj_shapes_dir + "data/"
move_shapes_dfile = obj_shapes_ddir + "move_shapes2.data"
with open (move_shapes_dfile, 'rb') as fp:
   # {'25.26': [ ( {14441, 20843, 12047, 16400, 20058, 10430}, {10432, 38065}, (0, 0) ), ... ], ... }
   # { files: [ ( { image1 shapeids }, { image2 shapeids }, ( movement ) ), ... ], ... }
   shapes_movements = pickle.load(fp)
fp.close()

lowest_fnum, highest_fnum = btwn_amng_files_functions.get_low_highest_filenums( directory )
im1 = Image.open(top_images_dir + directory + str(lowest_fnum) + ".png" )
im_size = im1.size
im1.close()
smallest_pixc = cv_globals.get_smallest_pixc( im_size )
Lshape_size = cv_globals.get_Lshape_size( im_size )
indpnt_shape_size = cv_globals.get_indpnt_shape_size( im_size )



if "min" in directory:
   min_colors = True
else:
   min_colors = False

neighbor_match_threshold = 0.5

pixch_ddir = top_shapes_dir + directory + "pixch/data/"

def check_match_by_neighbors( each_shapes, cur_im_shapes, cur_im_shapes_neighbors, cur_im_shapes_colors, im_shapeids_by_pindex, big_size_ok=False ):

   # { pindex: (r,g,b), ... } for use by match_t_shape_w_nbrs_while_moving_it
   param_im_shapes_pixels = [ {}, {} ]
   
   # first, filling each_shapes pixels into param_im_shapes_pixels
   target_im_pixels = [ {}, {} ]
   
   for im1or2 in range(2):
      for pindex in cur_im_shapes[im1or2][ each_shapes[im1or2] ]:
         param_im_shapes_pixels[im1or2][pindex] = cur_im_shapes_colors[im1or2][ each_shapes[im1or2] ]
         
         target_im_pixels[im1or2][pindex] = cur_im_shapes_colors[im1or2][ each_shapes[im1or2] ]
   
   # for use by match_by_mov_shape_against_im
   param_im_shapes_pixels2 = set()
   
   # neighbors do not accumulate into param_im_shapes_pixels, but each of them get paired with each_shapes. so delete them before the next neighbors
   accumulate_neighbors = [ False, False ]
   
   # match difficulty increases with increasing number of shapes. so the match calculation should be adjusted with the numbers of shapes to be matched
   # variables to be used for determining match difficulty: number of neighbors. pixels of each neighbors.
   # see documentation. match difficulty variable.docx. 
   # [ [ pixels of added neighbor shape, pixels of added neighbor shape, ... ], [ pixels of added neighbor shape, pixels of added neighbor shape, ... ] ]
   # first list for image1, second list for image2.
   added_neighbors = [ [], [] ]
   
   # if shape appears in cur_matched_shapeids often enough, and it is in the top 10%, then it is probably likely to be a match
   matches_from_mov_against_im = []
   
   matched_shapeids = set()
   matched = None
   for im1shape_neighbor in cur_im_shapes_neighbors[0][ each_shapes[0] ]:
      # if im1shape_neighbor is too big, it is hard to judge the match, so if it is too big, skip it
      size_too_big = same_shapes_functions.check_size_by_pixels( cur_im_shapes[0][ each_shapes[0] ], cur_im_shapes[0][im1shape_neighbor], size_threshold=25  )
      if size_too_big is True and big_size_ok is False:
         continue
      # delete previous image1 neighbors pixels only if previous neighbors done checking. if previous neighbors was not big enough 
      # and did not go through checking, then previous pixels should add to current run.
      if accumulate_neighbors[0] is False:
         param_im_shapes_pixels[0] = copy.deepcopy( target_im_pixels[0] )
      
         param_im_shapes_pixels2 = set( cur_im_shapes[0][ each_shapes[0] ] )
         added_neighbors = [ [], [] ]
         
      
      for pindex in cur_im_shapes[0][ im1shape_neighbor ]:
         param_im_shapes_pixels[0][pindex] = cur_im_shapes_colors[0][ im1shape_neighbor ]
      
      param_im_shapes_pixels2 |= set( cur_im_shapes[0][ im1shape_neighbor ] )
      added_neighbors[0].append( len( cur_im_shapes[0][ im1shape_neighbor ] ) )
      
      assert len(param_im_shapes_pixels[0]) == len(param_im_shapes_pixels2)
      
      if len(param_im_shapes_pixels2) < Lshape_size:
         # current neighbors pixels not big enough, add current pixels to the next run
         accumulate_neighbors[0] = True
         continue
      
      # matching will be done for the current image1 run. so delete current pixels will be deleted before the next run.
      accumulate_neighbors[0] = False
      
      #image_functions.cr_im_from_pixels( "27", directory, param_im_shapes_pixels2, pixels_rgb=(255,0,0) ) 
      #image_functions.cr_im_from_pixels( "27", directory, set( cur_im_shapes[0][ each_shapes[0] ] ), pixels_rgb=(255,0,0) ) 
      
      # [ ( best matched image data shapeid, score ), ( second best matched image data shapeid, score ), ... ]
      cur_matched_shapeids = same_shapes_functions.match_by_mov_shape_against_im( cur_im_shapes_colors, im_shapeids_by_pindex, param_im_shapes_pixels2, set( cur_im_shapes[0][ each_shapes[0] ] ), 
                        im1.size, min_colors, cur_im_shapes[1], return_shapeids=True )        

      # take only top 30% as matched shapeid
      top30percent = len(cur_matched_shapeids) * 0.3
      for matched_index, cur_matched_shapeid in enumerate(cur_matched_shapeids):
         # ( shapeid, score )
         if matched_index > top30percent:
            break
         
         if  cur_matched_shapeid[0] in matches_from_mov_against_im:
            matched_shapeids.add(cur_matched_shapeid[0])
         matches_from_mov_against_im.append( cur_matched_shapeid[0] )
      
      if each_shapes[1] in matched_shapeids:  
         return True, matched_shapeids
         

      for im2shape_neighbor in cur_im_shapes_neighbors[1][ each_shapes[1] ]:
         # initialize param_im_shapes_pixels[1] with each_shapes[1] pixels in this form { pindex: (r,g,b), ... }
         if accumulate_neighbors[1] is False:
            param_im_shapes_pixels[1] = copy.deepcopy( target_im_pixels[1] )
            added_neighbors[1] = []
            

         for pindex in cur_im_shapes[1][ im2shape_neighbor ]:
            param_im_shapes_pixels[1][pindex] = cur_im_shapes_colors[1][ im2shape_neighbor ]
         
         added_neighbors[1].append( len( cur_im_shapes_colors[1][ im2shape_neighbor ] ) )
         
         if len(param_im_shapes_pixels[1]) < Lshape_size:
            # current neighbors pixels not big enough, add another neighbor pixels
            accumulate_neighbors[1] = True
            continue

         accumulate_neighbors[1] = False
         # now image1 and 2 pixels are prepared. check match

         #image_functions.cr_im_from_pixels( "25", "videos/street3/resized/min1/", param_im_shapes_pixels[0].keys(), pixels_rgb=(255,0,0) ) 
         #image_functions.cr_im_from_pixels( "26", "videos/street3/resized/min1/", param_im_shapes_pixels[1].keys(), pixels_rgb=(0,0,255) ) 


         
         match = same_shapes_functions.match_t_shape_w_nbrs_while_moving_it( param_im_shapes_pixels[0], param_im_shapes_pixels[1], target_im_pixels[0], target_im_pixels[1], 
                 im1.size, min_colors, added_neighbors )
         if match is True:
            return match, matched_shapeids      
         else:
            matched = False
   
   
   if len(matches_from_mov_against_im) == 1 and cur_matched_shapeids[0][1] >= 0 and cur_matched_shapeids[0][0] == each_shapes[1]:
      # went through only one im1shape_neighbor
      matched_shapeids.add(each_shapes[1])
      return True, matched_shapeids      
      
         
   return matched, matched_shapeids


result_shapes = {}

for each_files in all_matches_so_far:
   print( each_files )

   result_shapes[each_files] = []

   cur_im1file = each_files.split(".")[0]
   cur_im2file = each_files.split(".")[1]

   im1 = Image.open(top_images_dir + directory + cur_im1file + ".png" )
   im1pixels = im1.getdata()
   im1.close()
   
   im2 = Image.open( top_images_dir + directory + cur_im2file + ".png" )
   im2pixels = im2.getdata()
   im2.close()

   shapes_dfile = shapes_dir + cur_im1file + "shapes.data"
   with open (shapes_dfile, 'rb') as fp:
      # { 79999: [79999, ... ], ... }
      # { shapeid: [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()
   
   im1shapes_xy = {}
   for shapeid in im1shapes:
      pixels = set()
      for pindex in im1shapes[shapeid]:
         xy = pixel_functions.convert_pindex_to_xy( pindex, im_size[0] )
         pixels.add(xy)
      
      im1shapes_xy[shapeid] = pixels


   shapes_im2dfile = shapes_dir + cur_im2file + "shapes.data"
   with open (shapes_im2dfile, 'rb') as fp:
      im2shapes = pickle.load(fp)
   fp.close()   

   im2shapes_xy = {}
   for shapeid in im2shapes:
      pixels = set()
      for pindex in im2shapes[shapeid]:
         xy = pixel_functions.convert_pindex_to_xy( pindex, im_size[0] )
         pixels.add(xy)
      
      im2shapes_xy[shapeid] = pixels

   im1shapes_boundaries_dfile = shapes_dir + "boundary/" + cur_im1file + ".data"
   im2shapes_boundaries_dfile = shapes_dir + "boundary/" + cur_im2file + ".data"

   with open (im1shapes_boundaries_dfile, 'rb') as fp:
      im1shapes_shapes_boundaries = pickle.load(fp)
   fp.close()   

   with open (im2shapes_boundaries_dfile, 'rb') as fp:
      im2shapes_shapes_boundaries = pickle.load(fp)
   fp.close()   

   im1shape_neighbors_file = shapes_dir + "shape_nbrs/" + cur_im1file + "_shape_nbrs.data"
   im2shape_neighbors_file = shapes_dir + "shape_nbrs/" + cur_im2file + "_shape_nbrs.data"
   with open (im1shape_neighbors_file, 'rb') as fp:
      im1shapes_neighbors = pickle.load(fp)
   fp.close()   

   with open (im2shape_neighbors_file, 'rb') as fp:
      im2shapes_neighbors = pickle.load(fp)
   fp.close()   

   im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im1file, directory, min_colors=min_colors)
   im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im2file, directory, min_colors=min_colors)

   im1shapeids_by_pindex_dfile = shapes_dir + "shapeids_by_pindex/" + cur_im1file + ".data"
   with open (im1shapeids_by_pindex_dfile, 'rb') as fp:
      im1shapeids_by_pindex = pickle.load(fp)
   fp.close()           
      
   im2shapeids_by_pindex_dfile = shapes_dir + "shapeids_by_pindex/" + cur_im2file + ".data"
   with open (im2shapeids_by_pindex_dfile, 'rb') as fp:
      im2shapeids_by_pindex = pickle.load(fp)
   fp.close()            

   pixch_shapes_file = pixch_ddir + each_files + "." + cur_im1file + "pixch_shapes.data"
   with open (pixch_shapes_file, 'rb') as fp:
      # { '79652': 0.45348837209302323, '79682': 1.0, '79689': 0.44104134762633995, '79942': 0.6, ... }
      # { shapeid: % of pixch, ... }
      im1pixch_shapes = pickle.load(fp)
   fp.close()

   pixch_shapes2_file = pixch_ddir + each_files + "." + cur_im2file + "pixch_shapes.data"
   with open (pixch_shapes2_file, 'rb') as fp:
      im2pixch_shapes = pickle.load(fp)
   fp.close()

   im_shapes = [im1shapes, im2shapes]
   im_pixch_shapes = [im1pixch_shapes, im2pixch_shapes]

   skip = False
   for each_shapes in all_matches_so_far[each_files]:
      # ( 255, 333 )
      
      if skip is True:
         if each_shapes !=  (66495, 67290):
            continue
      skip = False

      if len( im1shapes[ each_shapes[0] ] ) < smallest_pixc or len( im2shapes[ each_shapes[1] ] ) < smallest_pixc:
         # smallest_pixc shapes have high probability to be wrong compared to other shapes. so remove them 
         continue
      
      delete = None
      # small shapes are more prone to be wrong
      if len( im1shapes[ each_shapes[0] ] ) < indpnt_shape_size * 1.5 and len( im2shapes[ each_shapes[1] ] ) < indpnt_shape_size * 1.5:
         
         app_im1shapes_pixels = set(im1shapes[ each_shapes[0] ])
         app_im2shapes_pixels = set(im2shapes[ each_shapes[1] ])
         cur_im_shapeids = ( set(), set() )

         cur_im_shapeids[0].add( each_shapes[0] )
         cur_im_shapeids[1].add( each_shapes[1] )  

         # [ {(33200, 32031), ...}, {(16400, 38065), ...} ]
         neighbor_matches = pixel_shapes_functions.get_nbr_matches( cur_im_shapeids, [ im1shapes_neighbors, im2shapes_neighbors ], all_matches_so_far[each_files] ) 
         common_nbr_matches = neighbor_matches[0].intersection( neighbor_matches[1] )
            
         # one neighbor needs to match only one pair. if neighbor is matching multiple shapes in next image, then this has to match only one pair
         # for example. 
         # image1 shape neighbor matches {(79689, 56505), (79689, 70906), (79689, 79676), (65536, 79999)}
         # 79689 matched 3 shapes. 79689 needs to match only one pair.
         # here is image2 shape neighbor matches {(79689, 70906), (54222, 79999), (55568, 79999), ... }
         distinct_neighbors = [ set(), set() ]
         for im1or2_index, nbr_matches in enumerate(neighbor_matches):
            distinct_neighbors[im1or2_index] = { temp_match[im1or2_index] for temp_match in nbr_matches }
            
            
         distinct_neighbors_len = [ len( distinct_neighbors[0] ), len( distinct_neighbors[1] ) ]
         '''
         # check correct match by numbers of neighbors. at least 2 neighbors matches needed for this
         if distinct_neighbors_len[0] >= 2 or distinct_neighbors_len[1] >= 2:
            distinct_nbrs_len_match = min( distinct_neighbors_len ) / max( distinct_neighbors_len )
            if distinct_nbrs_len_match < 0.4:
               print("wrong match by distinct_nbrs_len_match")
               delete = True
            else:
               common_nbr_matches_percent = len(common_nbr_matches) /  min( distinct_neighbors_len )
               if common_nbr_matches_percent < 0.5:
                  print("wrong match by common_nbr_matches_percent")
                  delete = True
         '''
         app_im1shapes_nbr_pixels = pixel_shapes_functions.get_only_nbr_pixels( im1shapes_shapes_boundaries[ each_shapes[0] ], app_im1shapes_pixels, im_size, input_xy=True )
         app_im2shapes_nbr_pixels = pixel_shapes_functions.get_only_nbr_pixels( im2shapes_shapes_boundaries[ each_shapes[1] ], app_im2shapes_pixels, im_size, input_xy=True )
            
         if delete is None:
            # returns None, True, or False
            same_shapes = same_shapes_functions.check_by_pixels_attachment( common_nbr_matches, [ im1shapes_xy, im2shapes_xy ], [ app_im1shapes_nbr_pixels, app_im2shapes_nbr_pixels ],
                                                                            im_size, [ im1shapes_shapes_boundaries[ each_shapes[0] ], im2shapes_shapes_boundaries[ each_shapes[1] ] ], 
                                                                            [ im1pixels, im2pixels ], shapes_movements[each_files], min_colors  )

            if same_shapes is False:
               delete = True
            elif same_shapes is True:
               delete = False
         if min(distinct_neighbors_len) >= 1 and len(common_nbr_matches) / min( distinct_neighbors_len ) >= 0.5 and len(common_nbr_matches) / max(distinct_neighbors_len) >= 0.5:
            big_size_ok = True
         if delete is None:
            match_by_neighbors = check_match_by_neighbors( each_shapes, im_shapes, [im1shapes_neighbors, im2shapes_neighbors],
                              [ im1shapes_colors, im2shapes_colors ], [ im1shapeids_by_pindex, im2shapeids_by_pindex ], big_size_ok=True )

            if match_by_neighbors[0] is False:
               delete = True
            elif match_by_neighbors[0] is True:
               delete = False




      elif len( im1shapes[ each_shapes[0] ] ) >= indpnt_shape_size or len( im2shapes[ each_shapes[1] ] ) >= indpnt_shape_size:
         # one or both shapes are big enough.
         save_filepath = top_shapes_dir + "videos/street3/resized/min1/temp/test1.png"
         '''
         image_functions.cr_im_from_pixels( "26", "videos/street3/resized/min1/", im1shapes[ each_shapes[0] ], pixels_rgb=(255,0,0), save_filepath=save_filepath ) 
         image_functions.cr_im_from_pixels( "26", "videos/street3/resized/min1/", im1pixch_shapes[ each_shapes[0] ], pixels_rgb=(0,255,255), input_im=save_filepath ) 
         image_functions.cr_im_from_pixels( "27", "videos/street3/resized/min1/", im2shapes[ each_shapes[1] ], pixels_rgb=(0,0,255), save_filepath=save_filepath ) 
         image_functions.cr_im_from_pixels( "26", "videos/street3/resized/min1/", im2pixch_shapes[ each_shapes[1] ], pixels_rgb=(0,255,255), input_im=save_filepath ) 
         '''
         # condition1: 1.1 each_shapes[0] has other match and each_shapes[1] also has other match.
         #             1.2 other matches are big enough for each_shapes
         # condition2: check by changed pixels
         #             2.1 more than half of the each_shapes pixels are stayed pixels.
         #             2.2 other match image1 has more than half overlapped pixels with each_shapes[1]. Likewise, other match image2 has more than half overlapped pixels
         #              with each_shapes[0]. each_shapes[0] has less overlapped pixels with each_shapes[1]. The lesser the overlapped pixels, less likely each_shapes
         #              are correct match.
         
         # [ condition1.1, condition1.2 ( % of image1 other match pixels with each_shapes[0], % of image2 other match pixels with each_shapes[1] ), 
         #   condition2.1 ( im1pixch_shapes[ each_shapes[0] ], im2pixch_shapes[ each_shapes[1] ] ), condition2.2 ( other match image1 and each_shapes[0] overlapped pixels, 
         #   other match image2 and each_shapes[1] overlapped pixels ) ]
         conditions = [ False, None, None, None ]
         
         each_shapes_set = ( set( im1shapes[ each_shapes[0] ] ), set( im2shapes[ each_shapes[1] ] ) )
         each_shapes_len = ( len( each_shapes_set[0] ), len( each_shapes_set[1] ) )
         
         # [ image1 shapes pixels, image2 shapes pixels ]
         other_match_pixels = [ set(), set() ]
         for im1or2 in range(2):
            other_matches = { temp_match for temp_match in all_matches_so_far[each_files] if each_shapes[im1or2] == temp_match[im1or2] and each_shapes != temp_match }
            
            ano_im = abs( im1or2 - 1 )
            for other_match in other_matches:
               other_match_pixels[ano_im] |= set( im_shapes[ano_im][ other_match[ano_im] ] )
               '''
               image_functions.cr_im_from_pixels( str( 26 + ano_im ), "videos/street3/resized/min1/", im_shapes[ano_im][ other_match[ano_im] ], pixels_rgb=(100,150,0), 
                                                  save_filepath=save_filepath ) 
               image_functions.cr_im_from_pixels( "", "", im_pixch_shapes[ano_im][ other_match[ano_im] ] , pixels_rgb=(0,255,255), input_im=save_filepath ) 
               '''
         if len( other_match_pixels[0] ) >= 1 and len( other_match_pixels[1] ) >= 1:
            # condition1.1
            conditions[0] = True
         # condition1.2
         conditions[1] = ( len( other_match_pixels[0] ) / each_shapes_len[0], len( other_match_pixels[1] ) / each_shapes_len[1] )
         # condition2.1
         conditions[2] = ( len( im1pixch_shapes[ each_shapes[0] ] ) / each_shapes_len[0], len( im2pixch_shapes[ each_shapes[1] ] ) / each_shapes_len[1] )
         
         other_match_im1_overlap = each_shapes_set[0].intersection( other_match_pixels[1] )
         other_match_im2_overlap = each_shapes_set[1].intersection( other_match_pixels[0] )
         
         each_shapes_overlap = each_shapes_set[0].intersection( each_shapes_set[1] )
         
         # condition2.2
         conditions[3] = ( len( other_match_im1_overlap ) / each_shapes_len[0], len( other_match_im2_overlap ) / each_shapes_len[1],
                           len(each_shapes_overlap) / each_shapes_len[0], len(each_shapes_overlap) / each_shapes_len[1] )       
         
         # now all conditions are filled in. check if all conditions are met
         if conditions[0] is True and conditions[1][0] >= 0.5 and conditions[1][1] >= 0.5 and conditions[2][0] < 0.5 and conditions[2][1] < 0.5 and \
            conditions[3][0] >= 0.5 and conditions[3][1] >= 0.5 and conditions[3][2] < 0.5 and conditions[3][3] < 0.5:
            delete = True            

         # most of the pixels are stayed pixels but there is little overlap between each_shapes
         if ( conditions[2][0] < 0.3 or conditions[2][1] < 0.3 ) and ( conditions[3][0] >= 0.7 or conditions[3][1] >= 0.7 ) and \
            ( conditions[3][2] < 0.15 and conditions[3][3] < 0.15 ):
            delete = True

      if delete is True:
         #image_functions.cr_im_from_shapeslist2( cur_im1file, directory, [each_shapes[0]], shapes_rgbs=[(255,0,0)] )
         #image_functions.cr_im_from_shapeslist2( cur_im2file, directory, [each_shapes[1]], shapes_rgbs=[(0,0,255)] )

         result_shapes[each_files].append( each_shapes )
         

# second stage all files directory
# for some reasons, below file was not included in all_matches_so_far. maybe there were some shapes that were wrong, but I checked all results of it after running
# this algorithm and all algorithms up to trd_stage algorithms. all results were correct. so add them to all_matches_so_far
scnd_st_allf_dir = top_shapes_dir + directory + scnd_stg_all_files
relpos_nbr_dfile = scnd_st_allf_dir + "/relpos_nbr/data/" + "1.data"
with open (relpos_nbr_dfile, 'rb') as fp:
   relpos_nbr_shapes = pickle.load(fp)
fp.close()

for each_files in result_shapes:    

   for each_shapes in result_shapes[each_files]:
      all_matches_so_far[each_files].remove( each_shapes )
      
      if each_shapes in relpos_nbr_shapes[each_files]:
         relpos_nbr_shapes[each_files].remove( each_shapes )
      
for each_files in relpos_nbr_shapes:
   cur_im1file = each_files.split(".")[0]
   cur_im2file = each_files.split(".")[1]

   shapes_dfile = shapes_dir + cur_im1file + "shapes.data"
   with open (shapes_dfile, 'rb') as fp:
      # { 79999: [79999, ... ], ... }
      # { shapeid: [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()

   shapes_im2dfile = shapes_dir + cur_im2file + "shapes.data"
   with open (shapes_im2dfile, 'rb') as fp:
      im2shapes = pickle.load(fp)
   fp.close()  

   for each_shapes in relpos_nbr_shapes[each_files]:
      if each_shapes[0] not in im1shapes.keys() or each_shapes[1] not in im2shapes.keys():
         continue

      all_matches_so_far[each_files].add( each_shapes )

     

correct_matches_ddir = top_shapes_dir + directory + "correct_matches/data/"
if os.path.exists(correct_matches_ddir ) == False:
   os.makedirs(correct_matches_ddir)

correct_matches_dfile = correct_matches_ddir + "1.data"
with open(correct_matches_dfile, 'wb') as fp:
   pickle.dump(result_shapes, fp)
fp.close()

all_matches_ddir = top_shapes_dir + directory + "all_matches/data/"
if os.path.exists(all_matches_ddir ) == False:
   os.makedirs(all_matches_ddir)

all_matches_dfile = all_matches_ddir + "1.data"
with open(all_matches_dfile, 'wb') as fp:
   pickle.dump(all_matches_so_far, fp)
fp.close()























