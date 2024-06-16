import tkinter
from PIL import ImageTk, Image
from libraries import btwn_amng_files_functions, pixel_shapes_functions, same_shapes_functions, pixel_functions, image_functions, cv_globals
from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files, scnd_stg_spixc_dir, scnd_stg_ch_btwn_frames_dir
import pickle, copy
import sys, pathlib, os



shapes_type = "intnl_spixcShp"
directory = "videos/street3/resized/min1"


if len( sys.argv ) >= 2:
   directory = sys.argv[1]


# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

shapes_dir = top_shapes_dir + directory + "shapes/"

all_matches_ddir = top_shapes_dir + directory + "all_matches/data/"
all_matches_dfile = all_matches_ddir + "1.data"
with open (all_matches_dfile, 'rb') as fp:
   all_matches = pickle.load(fp)
fp.close()
   
shapes_movements_dfile = all_matches_ddir + "move_shapes2.data"
with open (shapes_movements_dfile, 'rb') as fp:
   # {'25.26': [({66472, 79689, 64081, 69303, 65272}, {79676}, (-11, 2)), ({69703}, {70499}, (-7, 1)), ... ], ... }
   # { each_files: [ ( { image1 shapeids }, { image2 shapeids }, ( movement ) ), ... ], ... }
   shapes_movements = pickle.load(fp)
fp.close()


consecutives_ddir = top_shapes_dir + directory + "all_matches/consecutives2/data/"
consecutives2_dfile = consecutives_ddir + "1to1.2.data"
with open (consecutives2_dfile, 'rb') as fp:
   # [{'25.26': [(55310, 53315), (55310, 55702), (55310, 56108)], '26.27': [(53315, 56105), (55702, 56105), (56108, 56105)], ... }, ... ]
   consecutives = pickle.load(fp)
fp.close()

# both integers.
lowest_filenum, highest_filenum = btwn_amng_files_functions.get_low_highest_filenums( directory )
all_image_nums = { str(temp_im_num) for temp_im_num in range(lowest_filenum, highest_filenum + 1 ) }

# [ lowest number shapes data, second lowest number shapes data, ... ]
all_im_shapes, lowest_filenum = btwn_amng_files_functions.get_all_image_shapes( shapes_dir )

im1 = Image.open(top_images_dir + directory + str(lowest_filenum) + ".png" )
im_size = im1.size
im1.close()

if "min" in directory:
   min_colors = True
else:
   min_colors = False
   
smallest_mv_threshold = cv_globals.get_smallest_mv_threshold( im_size )
sixth_pixc = cv_globals.get_6th_s_pixc( im_size )
   

# ['25.26', '26.27', '27.28', '28.29', '29.30']
all_btwn_files_nums = btwn_amng_files_functions.get_btwn_files_nums( lowest_filenum, highest_filenum )
# [ image1 shapes neighbors, image2 shapes neighbors, image3 shapes neighbors, ... ]
# image shapes neighbors -> { shapeid: [ neighbors ], ... }
all_im_shapes_neighbors = btwn_amng_files_functions.get_all_im_target_data( directory, "neighbors" )

# { each_files: [ [ {33200}, {32031}, (x,y) ], ... ]
all_consec_movements = {}
# { each_files: [ im1shapes_colors, im2shapes_colors ], ... }
all_im_shapes_colors = {}

all_files_shp_mv_shapes = {}
all_files_shp_movements = {}
for each_files in all_btwn_files_nums:
   all_consec_movements[each_files] = []
   all_im_shapes_colors[each_files] = []
   
   cur_im1fnum = each_files.split(".")[0]
   cur_im2fnum = each_files.split(".")[1]
   
   im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im1fnum, directory, min_colors=min_colors)
   im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im2fnum, directory, min_colors=min_colors)
   
   all_im_shapes_colors[each_files].append( im1shapes_colors )
   all_im_shapes_colors[each_files].append( im2shapes_colors )

   cur_files_shp_mv_shapes = []
   cur_files_shp_movements = []
   for each_shapes_movements in shapes_movements[each_files]:
      cur_files_shp_mv_shapes.append( (each_shapes_movements[0], each_shapes_movements[1]) )
      cur_files_shp_movements.append( each_shapes_movements[2] )

   all_files_shp_mv_shapes[each_files] = cur_files_shp_mv_shapes
   all_files_shp_movements[each_files] = cur_files_shp_movements



# { consecutive index number: each_files, ... }
possible_partial_matches = {}
# { consecutive index number: each_files, ... }
consecutives_wrong_matches = {}

def get_each_files_in_order( param_consecutive ):

   all_each_files = []
   for each_files in all_btwn_files_nums:
      if each_files in param_consecutive.keys():
         all_each_files.append(each_files)
   
   return all_each_files


def get_each_files_shapeids( param_consecutive, each_files ):
   
   if len( param_consecutive[each_files] ) == 2 and type( param_consecutive[each_files][0] ) is set and type( param_consecutive[each_files][1] ) is set:
      # current each_files has this data format -> [{4096}, {4096, 4089}]
      cur_im1shapeids = param_consecutive[each_files][0]
      cur_im2shapeids = param_consecutive[each_files][1]
         
   else:
      cur_im1shapeids = { temp_shapes[0] for temp_shapes in param_consecutive[each_files] }
      cur_im2shapeids = { temp_shapes[1] for temp_shapes in param_consecutive[each_files] }

   return [ cur_im1shapeids, cur_im2shapeids ]


def get_shapes_movement( param_im_shapes, each_files ):
   cur_im1fnum = each_files.split(".")[0]
   cur_im2fnum = each_files.split(".")[1]
   
   im1shapes_pixels = {}
   for temp_shapeid in param_im_shapes[0]:
      for temp_pixel in all_im_shapes[ int(cur_im1fnum) - lowest_filenum ][temp_shapeid]:
         im1shapes_pixels[temp_pixel] = all_im_shapes_colors[each_files][0][temp_shapeid]

   im2shapes_pixels = {}
   for temp_shapeid in param_im_shapes[1]:
      for temp_pixel in all_im_shapes[ int(cur_im2fnum) - lowest_filenum ][temp_shapeid]:
         im2shapes_pixels[temp_pixel] = all_im_shapes_colors[each_files][1][temp_shapeid]


   #image_functions.cr_im_from_shapeslist2( cur_im1file, directory, param_im_shapes[0], shapes_rgbs=[(255,0,255)] )
   #image_functions.cr_im_from_shapeslist2( cur_im2file, directory, param_im_shapes[1], shapes_rgbs=[(255,0,255)] )   
   if param_im_shapes in all_files_shp_mv_shapes[each_files]:
      match_mv_index = all_files_shp_mv_shapes.index(param_im_shapes)
      return all_files_shp_movements[match_mv_index]

   # movement could not be found. get it.
   # im1im2_match {8192, 8193, 8198, 8208, ... }. movement (0,0). movement ( right left, up down )
   im1im2_match, movement = same_shapes_functions.match_shape_while_moving_it2( im1shapes_pixels, im2shapes_pixels, im_size, min_colors, best_match=True )  

   return movement


def get_nbr_movements_scores( neighbor_movements ):
    base_movement_score = 1
    valid_target_movements = {}

    # Determine all valid target movements based on thresholds for each neighbor
    for nbr_movement in neighbor_movements:
        x_threshold = nbr_movement[1][0]
        y_threshold = nbr_movement[1][1]

        # put allowed movements as a key into valid_target_movements
        for x in range(int(nbr_movement[0][0] - x_threshold), int(nbr_movement[0][0] + x_threshold) + 1):
            for y in range(int(nbr_movement[0][1] - y_threshold), int(nbr_movement[0][1] + y_threshold) + 1):
                if (x, y) not in valid_target_movements:
                    valid_target_movements[(x, y)] = []

    # Score only valid movements and calculate incremental percentages for additional neighbors
    for target_movement in valid_target_movements:
        base_score = 0
        additional_percentage = 0  # Starting additional percentage

        for index, nbr_movement in enumerate(neighbor_movements):
            x_threshold = nbr_movement[1][0]
            y_threshold = nbr_movement[1][1]
            
            if abs(nbr_movement[0][0] - target_movement[0]) <= x_threshold and abs(nbr_movement[0][1] - target_movement[1]) <= y_threshold:
                distance = ((nbr_movement[0][0] - target_movement[0])**2 + (nbr_movement[0][1] - target_movement[1])**2)**0.5
                distance_weight = 1 / (1 + distance)  # Weight inversely proportional to the distance
                if index == 0:
                    # neighbor movements score make up 40% of the total match score.
                    base_score = (base_movement_score * distance_weight) * 0.4
                else:
                    increment_score = base_score * additional_percentage
                    base_score += increment_score
                    additional_percentage += 0.05  # Increment the additional percentage for the next neighbor
        
        if base_score == 0:
           # the score will be multiplied by the match score. so the movement score needs to have value. 0 will be assigned the lowest value.
           base_score = 0.01
        valid_target_movements[target_movement] = base_score

    return valid_target_movements


def get_all_each_files_matches( each_files_in_order, consecutive ):

   # { each_files: [ shapes matches, neighbor matches ], ... }
   all_each_files_matches = {}

   for each_files in each_files_in_order:

      all_each_files_matches[each_files] = []

      cur_im1file =  each_files.split(".")[0] 
      cur_im2file = each_files.split(".")[1]
   
      # [ { im1shapeids }, { im2shapeids } ]
      cur_im_shapeids = get_each_files_shapeids( consecutive, each_files )
      
      all_each_files_matches[each_files].append( cur_im_shapeids )

      # getting neighbors matches
      cur_neighbors = [ set(), set() ]
      for im1or2 in range(2):
         # index number for all_im_shapes_neighbors
         nbr_im_ref_num = int(cur_im1file) + im1or2 - lowest_filenum
         for cur_im_shapeid in cur_im_shapeids[im1or2]:
            cur_neighbors[im1or2] |= set( all_im_shapes_neighbors[nbr_im_ref_num][cur_im_shapeid] )

      # {(64400, 52002), (32811, 52805), (36864, 44054), (60893, 65208), (52485, 65208), (64400, 65208)}
      pre_nbr_matches = { temp_shapes for temp_shapes in all_matches[each_files] if temp_shapes[0] in cur_neighbors[0] or temp_shapes[1] in cur_neighbors[1] }
      
      done_nbr_matches = set()
      nbr_matches = []
      for pre_nbr_match in pre_nbr_matches:
         if pre_nbr_match in done_nbr_matches:
            continue
         pre_cur_nbr_matches = { temp_shapes for temp_shapes in pre_nbr_matches if temp_shapes[0] == pre_nbr_match[0] or temp_shapes[1] == pre_nbr_match[1] }
         
         _cur_nbr_matches = [ set(), set() ]
         _cur_nbr_matches[0] |= { temp_shapes[0] for temp_shapes in pre_cur_nbr_matches }
         _cur_nbr_matches[1] |= { temp_shapes[1] for temp_shapes in pre_cur_nbr_matches }
         
         found = False
         for nbr_match in nbr_matches:
            im1_common_nbr_matches = nbr_match[0].intersection( _cur_nbr_matches[0] )
            im2_common_nbr_matches = nbr_match[1].intersection( _cur_nbr_matches[1] )
            
            if len(im1_common_nbr_matches) >= 1 or len(im2_common_nbr_matches) >= 1:
               nbr_match[0] |= _cur_nbr_matches[0]
               nbr_match[1] |= _cur_nbr_matches[1]
               
               found = True
               break
         
         if found is False:      
            nbr_matches.append( _cur_nbr_matches )
         
         done_nbr_matches |= pre_cur_nbr_matches

      all_each_files_matches[each_files].append( nbr_matches )


   return all_each_files_matches


def get_all_each_files_movements( all_each_files_matches ):
   # all_each_files_matches
   # {'25.26': [[{33200}, {32031}], [[{39679}, {36864}], [{32847}, {32022}]]], ... }
   # { each_files: [ shapes matches, neighbors_matches ], ... }  shapes_matches -> [ { image1 shapeids }, { image2 shapeids } ]
   # neighbors_matches -> [ [ first neighbor match ], [ second neighbor match ], ... ]
   
   # { each_files: [ cur_shapes movement, neighbor movements ], ... }
   # neighbor movements indexes are same as neighbors indexes in all_each_files_matches. so for example. cur_consec_movements["25.26"][1]
   # can be found from all_each_files_matches["25.26"][1][0]
   
   
   def get_from_existing_movements( target_shapes_match, each_files, cur_consec_movements ):

      before_add_num = len( cur_consec_movements[each_files] )
      
      add_to_all_consec_mv = False
      # check if all_consec_movements contain the target_shapes_match.
      # { each_files: [ [ [ {33200}, {32031} ], (x,y) ], ... ]
      for each_match_movement in all_consec_movements[each_files]:
         if target_shapes_match[0] == each_match_movement[0][0] and target_shapes_match[1] == each_match_movement[0][1]:
            #found from existing_movements
            cur_consec_movements[each_files].append(each_match_movement[1])
            break

      if len( cur_consec_movements[each_files] ) == before_add_num:
         add_to_all_consec_mv = True
         
         movement = get_shapes_movement( target_shapes_match, each_files )
         # even when movement is none, it will be added in cur_consec_movements because every shapes match has its own index in cur_consec_movements
         cur_consec_movements[each_files].append( movement )

      if add_to_all_consec_mv is True and movement is not None:
         all_consec_movements[each_files].append( [ target_shapes_match, movement ] )


   
   cur_consec_movements = {}

   for each_files in all_each_files_matches:
      cur_consec_movements[each_files] = []
      cur_im_shapeids = all_each_files_matches[each_files][0]
      
      get_from_existing_movements( cur_im_shapeids, each_files, cur_consec_movements )

      nbr_matches = all_each_files_matches[each_files][1]

      for nbr_match in nbr_matches:
         get_from_existing_movements( nbr_match, each_files, cur_consec_movements )

   return cur_consec_movements



def find_same_nbr_m_from_adjacent_nbrs( each_files, all_each_files, each_files_in_order ):


   cur_im1file =  each_files.split(".")[0] 
   cur_im2file = each_files.split(".")[1]

   prev_each_files = str( int(cur_im1file) - 1 ) + "." + cur_im1file
   next_each_files = cur_im2file + "." + str( int(cur_im2file) + 1 )
   
   # prev_each_files and next_each_files both need to be present for this check
   if each_files == each_files_in_order[0] or each_files == each_files_in_order[-1]:
      # each_files is the first each_files or each_files is the last each_files
      return None
   
   same_nbr_matches = []
   for cur_nbr_match in all_each_files[each_files][1]:      
      found = False
      prev_neighbor_matches = all_each_files[prev_each_files][1]
      for prev_nbr_match in prev_neighbor_matches:
         # [{44166}, {45382}] index0 -> image1 shapeids. index1 -> image2 shapeids
               
         # check if any image1 shapeids from cur_nbr_match can be found from image2 shapeids from prev_nbr_match
         found_prev_neighbors = cur_nbr_match[0].intersection( prev_nbr_match[1] )
         if len(found_prev_neighbors) >= 1:
            # current image1 has found same match from previous matches
            found = True
            break

      if found is False:
         continue
      next_neighbor_matches = all_each_files[next_each_files][1]
      for next_nbr_match in next_neighbor_matches:
         # [{44166}, {45382}] index0 -> image1 shapeids. index1 -> image2 shapeids
               
         # check if any image2 shapeids from cur_nbr_match can be found from image1 shapeids from next_nbr_match
         found_next_neighbors = cur_nbr_match[1].intersection( next_nbr_match[0] )
         if len(found_next_neighbors) >= 1:
            same_nbr_matches.append( [ found_prev_neighbors, found_next_neighbors ] )


   return same_nbr_matches



def check_by_stationary_pixch( cur_shapes_movement, app_im_pixch, app_im_shapes_pixels, each_files, pixch ):
   if cur_shapes_movement is None:
      return None
   # check if cur_shapes_movement is stationary
   distance_from_0 = abs(cur_shapes_movement[0]) + abs(cur_shapes_movement[1])

   if distance_from_0 >= 5:
      # not stationary
      return None
   
   # check if app_im_pixch is not prepared
   if len(app_im_pixch[0]) == 0:
      for im1or2 in range(2):
         app_im_pixch[im1or2] = app_im_shapes_pixels[im1or2].intersection(pixch)  
         
   # check if most of the pixels remain in the same place
   remain_pixels = [ set(), set() ]
   for im1or2 in range(2):
      remain_pixels[im1or2] = app_im_shapes_pixels[im1or2].difference(app_im_pixch[im1or2])
   
   # stationary match should have enough pixels overlap
   pixels_overlap = app_im_shapes_pixels[0].intersection(app_im_shapes_pixels[1])
   
   if len(app_im_shapes_pixels[0]) > len(app_im_shapes_pixels[1]):
      smaller_shapes_pixels = app_im_shapes_pixels[1]
   else:
      smaller_shapes_pixels = app_im_shapes_pixels[0]
   
   if len(pixels_overlap) / len(smaller_shapes_pixels) < 0.55:
      return False
      
   if len(remain_pixels[0]) / len(smaller_shapes_pixels) >= 0.53 and len(remain_pixels[1]) / len(smaller_shapes_pixels) >= 0.53:
      return True
   else:
      return False
      
   
def check_by_adjacent_movements( all_each_files_movements, cur_each_files, app_im_shapes_pixels, each_files_in_order ):

   cur_im1file = cur_each_files.split(".")[0] 
   cur_im2file = cur_each_files.split(".")[1]
   
   prev_each_files = str( int(cur_im1file) - 1 ) + "." + cur_im1file
   next_each_files = cur_im2file + "." + str( int(cur_im2file) + 1 )

   # prev_each_files and next_each_files both need to be present for this check
   if cur_each_files == each_files_in_order[0] or cur_each_files == each_files_in_order[-1]:
      # each_files is the first each_files or each_files is the last each_files
      return None

   if all_each_files_movements[prev_each_files][0] is None or all_each_files_movements[next_each_files][0] is None:
      return None

   adjacent_diff_x  = abs( all_each_files_movements[prev_each_files][0][0] - all_each_files_movements[next_each_files][0][0] )
   adjacent_diff_y = abs( all_each_files_movements[prev_each_files][0][1] + all_each_files_movements[next_each_files][0][1] )
   if adjacent_diff_x + adjacent_diff_y > 4:
      # adjacent movements don't have the same movement
      return None
   
   average_mv_x = ( all_each_files_movements[prev_each_files][0][0] + all_each_files_movements[next_each_files][0][0] ) / 2
   average_mv_y = ( all_each_files_movements[prev_each_files][0][1] + all_each_files_movements[next_each_files][0][1] ) / 2

   # check if current each_files neighbors have the same movement as the average adjancent movement
   found_mv = None
   skip_cur_match_mv = True
   for nbr_movement in all_each_files_movements[cur_each_files]:
      if skip_cur_match_mv is True:
         # first one is current match movement
         skip_cur_match_mv = False
         continue
      
      if nbr_movement is None:
         continue
      
      mv_diff_x = abs( nbr_movement[0] - average_mv_x )
      mv_diff_y = abs( nbr_movement[1] - average_mv_y )
      
      if mv_diff_x + mv_diff_y < 5:
         # adjacent movements and nbr_movement has the same movement. now check if app_im_shapes_pixels have actually the same movement.
         adjacent_mv = ( round(average_mv_x), round(average_mv_y) )
         
         moved_pixels = pixel_functions.move_pixels( app_im_shapes_pixels[0], adjacent_mv[0], adjacent_mv[1], input_xy=False, im_width=im_size[0] )
         matched_pixels = moved_pixels.intersection( app_im_shapes_pixels[1] )
         
         if len(moved_pixels) > len(app_im_shapes_pixels[1]):
            smaller_pixels = app_im_shapes_pixels[1]
         else:
            smaller_pixels = moved_pixels
         
         if len(matched_pixels) / len(smaller_pixels) >= 0.3:
            # matched
            return adjacent_mv

   
   if found_mv is None:
      if len(all_each_files_movements[cur_each_files]) > 3:
         # even when adjacent movements are the same and enough neighbor movements present, the current movement does not have the same movement 
         # as the adjacent movements. this probably indicates that current match is wrong.
         return False
      
      elif len(all_each_files_movements[cur_each_files]) < 4:
         # not enough neighbor movements to judge if this match is wrong.
         return None 


# check_with_other_each_files_movements. algorithm explanation is available in fix_consecutives folder
# if one each_files movement is different while all other each files movements are the same, then it indicates that inconsistent movement shapes match may be wrong
# so another check is needed
def check_with_other_each_files_mv( all_each_files_movements, cur_consec_results ):
   threshold = 8
   
   # returns True if adjacent is within threshold. False if not.
   def check_adjacent_each_files( inconsistent_each_files, all_movements ):
      prev_each_files = str( int( inconsistent_each_files.split(".")[0] ) - 1 ) + "." + inconsistent_each_files.split(".")[0]
      next_each_files = inconsistent_each_files.split(".")[1] + "." + str( int( inconsistent_each_files.split(".")[1] ) + 1 )
      
      consistent_result = False
      for each_files in [ prev_each_files, next_each_files ]:
         if each_files in all_movements:

            diff_x  = abs( all_movements[each_files][0] - all_movements[inconsistent_each_files][0] )
            diff_y = abs( all_movements[each_files][1] + all_movements[inconsistent_each_files][1] )
            if diff_x + diff_y < threshold:       
               consistent_result = True
      
      return consistent_result
   
   
   def get_consistent_movements( first_each_files, all_movements ):
      # [ each_files, another each_files, ... ]
      consistent_movements = {}

      for ano_each_files in all_movements:
         if first_each_files == ano_each_files:
            continue
         
         diff_x  = abs( all_movements[first_each_files][0] - all_movements[ano_each_files][0] )
         diff_y = abs( all_movements[first_each_files][1] + all_movements[ano_each_files][1] )
         if diff_x + diff_y < threshold:  
            # movement is within threshold.
            consistent_movements[ano_each_files] = True
         else:
            consistent_movements[ano_each_files] = False
      
      return consistent_movements

   
   
   all_movements = {}
   for each_files in all_each_files_movements:
      if cur_consec_results[each_files] is not True:
         # if each_files match is not True, any each_files match after it can not be taken. 
         break
      
      # match made be made from anything other than movement. if so, movement is None.
      if all_each_files_movements[each_files][0] is not None:
         all_movements[each_files] = all_each_files_movements[each_files][0]

   if len(all_movements) < 3:
      # at least 3 movements needed for this judgement
      return None
   
   first_each_files = list(all_movements.keys())[0]
   consistent_movements = get_consistent_movements( first_each_files, all_movements )
   
   # if only 1 inconsistent each_files is found, then it should be either of the two below
   # consistent_movement_pattern1 ->  {'26.27': True, '27.28': True, '28.29': False} 28.29 is inconsistent
   # consistent_movement_pattern2 -> {'26.27': False, '27.28': False, '28.29': False} 25.26 is inconsistent
   # any other combinations of True and False don't have only 1 inconsistent found
   inconsistent_counts = [ temp for temp in consistent_movements.values() ].count(False)
   
   # consistent_movement_pattern2
   if inconsistent_counts == len(consistent_movements):
      # first_each_files is inconsistent with all other each_files. check if another each_files is consistent with other each_files except first one
      # if returned consistent_movements have all consistent results then, only first each_files is inconsistent
      scnd_each_files = list(all_movements.keys())[1]
      consistent_movements = get_consistent_movements( scnd_each_files, all_movements )
      
      consistent_counts = [ temp for temp in consistent_movements.values() ].count(True)
      # -1 for the first_each_files which is inconsistent with scnd_each_files
      if consistent_counts == len(consistent_movements) - 1:
         return first_each_files
      else:
         return None
   
   # consistent_movement_pattern1
   elif inconsistent_counts == 1:
      inconsistent_each_files = [ temp_files for temp_files, consistent_result in consistent_movements.items() if consistent_result is False ][0]
      # check also if inconsistent_each_files is also inconsistent with adjacent each_files
      adjacent_result = check_adjacent_each_files( inconsistent_each_files, all_movements )
      
      if adjacent_result is False:
         return inconsistent_each_files
      else:
         return None
   
   else:
      # only 1 inconsistent requirement is not met
      return None


def check_match_by_connected_pixels( cur_im_shapeids, each_files ):

   def get_furthest_shape_inner_pixels( pixels ):

      inner_pixels = {}

      pixels_xy = [ set(), set() ]
      for pixel in pixels:
         xy = pixel_functions.convert_pindex_to_xy( pixel, im_size[0] )
         
         pixels_xy[0].add(xy[0])
         pixels_xy[1].add(xy[1])
            
      leftmost_pixel = min( pixels_xy[0] )
      rightmost_pixel = max( pixels_xy[0] )
      top_pixel = min( pixels_xy[1] )
      bottom_pixel = max( pixels_xy[1] )
   
      inner_pixels["left"] = rightmost_pixel
      inner_pixels["right"] = leftmost_pixel
      inner_pixels["top"] = bottom_pixel
      inner_pixels["bottom"] = top_pixel
   
      return inner_pixels


   # [ [ { shapeids that are connected }, ... ], [ { shapeids that are connected }, ... ] ]
   connected_shapes = [ [], [] ]
   
   im1fnum = each_files.split(".")[0]
   
   for im1or2 in range(2):
      already_found_shapeids = set()
      temp_im_fnum = int(im1fnum) + im1or2 - lowest_filenum
      
      for temp_shapeid in cur_im_shapeids[im1or2]:
         cur_connected_shapes = set()
         existing_cur_conn_shapes = False
         existing_index = None
         
         if temp_shapeid in already_found_shapeids:
            existing_cur_conn_shapes = True
            
            for index, exist_conn_shapes in enumerate(connected_shapes[im1or2]):
               if temp_shapeid in exist_conn_shapes:
                  cur_connected_shapes = exist_conn_shapes
                  existing_index = index
                  break
         else:
            cur_connected_shapes.add(temp_shapeid)
         
         for ano_shapeid in cur_im_shapeids[im1or2]:
            if temp_shapeid == ano_shapeid:
               continue
               
            if temp_shapeid in all_im_shapes_neighbors[temp_im_fnum][ano_shapeid]:
               cur_connected_shapes.add(ano_shapeid)
               already_found_shapeids.add(ano_shapeid)

          
         if existing_cur_conn_shapes is True:
            connected_shapes[im1or2][existing_index] = cur_connected_shapes
         else:
            connected_shapes[im1or2].append(cur_connected_shapes)

   if len(connected_shapes[0]) == 1 and len(connected_shapes[1]) == 1:
      return None
   
   conn_shapes_pixels = [ set(), set() ]
   im_fnum_with_separate_shapes = None
   for im1or2 in range(2):
      temp_im_fnum = int(im1fnum) + im1or2 - lowest_filenum
      
      if len(connected_shapes[im1or2]) > 1:
         # because image that has all shapes connected need to match all separate shapes on the other image. Size of the all separate shapes will be 
         # calculated by all shapes including space among them. 
         
         im_fnum_with_separate_shapes = im1or2
         
         first = True
         # { farthest left: number, farthest right: number, top: number, bottom: number }
         farthest_pixels = {}
         for each_conn_shapes in connected_shapes[im1or2]:
            
            for temp_shapeid in each_conn_shapes:
               conn_shapes_pixels[im1or2] |= set( all_im_shapes[temp_im_fnum][temp_shapeid] )
               
               if first is True:
                  farthest_pixels = get_furthest_shape_inner_pixels( all_im_shapes[temp_im_fnum][temp_shapeid] )
                  first = False
               else:
                  cur_pixels_in_directions = get_furthest_shape_inner_pixels( all_im_shapes[temp_im_fnum][temp_shapeid] )
                  
                  if farthest_pixels["left"] > cur_pixels_in_directions["left"]:
                     farthest_pixels["left"] = cur_pixels_in_directions["left"]
                  
                  if farthest_pixels["right"] < cur_pixels_in_directions["right"]:
                     farthest_pixels["right"] = cur_pixels_in_directions["right"]
                  
                  if farthest_pixels["top"] > cur_pixels_in_directions["top"]:
                     farthest_pixels["top"] = cur_pixels_in_directions["top"]
                  
                  if farthest_pixels["bottom"] < cur_pixels_in_directions["bottom"]:
                     farthest_pixels["bottom"] = cur_pixels_in_directions["bottom"]
         
   else:
   
      for each_conn_shapes in connected_shapes[im1or2]:
            
         for temp_shapeid in each_conn_shapes:
            conn_shapes_pixels[im1or2] |= set( all_im_shapes[temp_im_fnum][temp_shapeid] )      

   im_fnum_with_conn_shapes = abs( im_fnum_with_separate_shapes - 1 )
   if len( conn_shapes_pixels[im_fnum_with_separate_shapes] ) < len( conn_shapes_pixels[im_fnum_with_conn_shapes] ):
      return True
   else:
      return False


def check_prev_cur_shapes_integrity( prev_files_im_shapes, cur_im_shapeids ):

   if len(prev_files_im_shapes) >= 1 and prev_files_im_shapes != cur_im_shapeids[0]:
         
      prev_cur_common_shapeids = prev_files_im_shapes.intersection(cur_im_shapeids[0])
      prev_cur_shape_nbrs = set()
      separate_pixels = set()
      prev_cur_common_pixels = set()
      for prev_cur_shapeid in prev_cur_common_shapeids:
          prev_cur_shape_nbrs |= set( all_im_shapes_neighbors[ int(cur_im1file) - lowest_filenum ][prev_cur_shapeid] )
          prev_cur_common_pixels |= set(im1shapes[prev_cur_shapeid])

      for temp_shapeid in cur_im_shapeids[0]:

         if temp_shapeid not in prev_cur_shape_nbrs and temp_shapeid not in prev_cur_common_shapeids:
            #current shape is separate from previous current common pixels
            separate_pixels |= set(im1shapes[temp_shapeid])
            
      # check if separate pixels are too big to be considered the same shapes as previous shapes
      if len(prev_cur_common_pixels) == 0 or len(separate_pixels) / len(prev_cur_common_pixels) >= 0.4:
         return False, None

   else:
      prev_cur_common_shapeids = cur_im_shapeids[0]


   prev_files_im_shapes = cur_im_shapeids[1]
   
   return prev_cur_common_shapeids, prev_files_im_shapes







remaining = len(consecutives)
for consec_index, consecutive in enumerate(consecutives):
   # {'25.26': [(2077, 4097)], '26.27': [(4097, 4096)], '27.28': [{4096}, {4096, 4089}], ... }
   
   print("\r" + str(remaining) + " remaining", end="")
   remaining -= 1
   
   each_files_in_order = get_each_files_in_order( consecutive )
   
   # get all each_files shapes matches and their neighbor matches.
   # { each_files: [ shapes matches, neighbor matches ], ... }
   all_each_files_matches = get_all_each_files_matches( each_files_in_order, consecutive )
   
   # { each_files: [ target match movement, target neighbor movement, target neighbor2 movement, ... ], ... }
   all_each_files_movements = get_all_each_files_movements( all_each_files_matches )
   
   # { each_files: true, ... } true means match is true, false otherwise.
   cur_results = {}
   
   # used if inconsistent movement is found.
   matched_by_nbr_movements = {}

   # for use in check_prev_cur_shapes_integrity
   prev_files_im_shapes = set()
   for each_files in each_files_in_order:
      
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

      im1shapeids_by_pindex_dfile = shapes_dir + "shapeids_by_pindex/" + cur_im1file + ".data"
      with open (im1shapeids_by_pindex_dfile, 'rb') as fp:
         im1shapeids_by_pindex = pickle.load(fp)
      fp.close()    


      im2shapeids_by_pindex_dfile = shapes_dir + "shapeids_by_pindex/" + cur_im2file + ".data"
      with open (im2shapeids_by_pindex_dfile, 'rb') as fp:
         im2shapeids_by_pindex = pickle.load(fp)
      fp.close()    

      im_shapes = [im1shapes, im2shapes]
      im_shapeids_by_pindex = [ im1shapeids_by_pindex, im2shapeids_by_pindex ]


      # get pixch for the current each_files
      pixch_dir = top_shapes_dir + directory + "pixch/"
      pixch_dfile = pixch_dir + "data/" + each_files + ".data"
      with open (pixch_dfile, 'rb') as fp:
         #  { 79863, 79864, 79865, 79866, 79921, 79943, 79997, ... }
         pixch = pickle.load(fp)
      fp.close()
      
      cur_im_shapeids = all_each_files_matches[each_files][0]
      
      failed_evaluations = 0
      cur_match_correct = None
      
      # check if previous each_files image2 shapes are the same as current each_files image1 shapes.
      cur_im_shapeids[0], prev_files_im_shapes = check_prev_cur_shapes_integrity( prev_files_im_shapes, cur_im_shapeids )
      if cur_im_shapeids[0] is False:
         #previous each_files image2 shapes were not the same as current image1 shapes
         cur_results[each_files] = cur_match_correct
         break

      app_im_shapes_pixels = [ set(), set() ]
      for im1or2 in range(2):
         for temp_shapeid in cur_im_shapeids[im1or2]:
            app_im_shapes_pixels[im1or2] |= set( im_shapes[im1or2][temp_shapeid] )

      cur_shapes_movement = all_each_files_movements[each_files][0]

      app_im_neighbors_pixels = [ set(), set() ]
      for im1or2 in range(2):
         # index number for all_im_shapes_neighbors
         nbr_im_ref_num = int(cur_im1file) + im1or2 - lowest_filenum
         for cur_im_shapeid in cur_im_shapeids[im1or2]:
            temp_neighbor_shapeids = set( all_im_shapes_neighbors[nbr_im_ref_num][cur_im_shapeid] )
            
            for temp_nbr_shapeid in temp_neighbor_shapeids:
               app_im_neighbors_pixels[im1or2] |= set( im_shapes[im1or2][temp_nbr_shapeid] )

      cur_shapes_mv_by_pixch = None
      app_im_pixch = [ set(), set() ]
      if len(app_im_shapes_pixels[0]) >= sixth_pixc and len(app_im_shapes_pixels[1]) >= sixth_pixc:
         # enough pixels are present to check by pixch

         app_im_nbr_pixch = [ set(), set() ]
         for im1or2 in range(2):
            app_im_pixch[im1or2] = app_im_shapes_pixels[im1or2].intersection(pixch)  
            app_im_nbr_pixch[im1or2] = app_im_neighbors_pixels[im1or2].intersection(pixch)            

         #image_functions.cr_im_from_pixels( cur_im1file, directory, app_im_nbr_pixch[0] , pixels_rgb=(255,0,0) )
         #image_functions.cr_im_from_pixels( cur_im2file, directory, app_im_nbr_pixch[1] , pixels_rgb=(0,0,255) )

         cur_shapes_mv_by_pixch = same_shapes_functions.get_shapes_movement_by_pixch( app_im_shapes_pixels, app_im_pixch, im_size )

      nbr_matches = all_each_files_matches[each_files][1]

      # [ ( neighbor movement, (x_threshold, y_threshold) ), ... ]
      neighbor_movements = []

      # neighbor movement start after index0 of current shapes match movement.
      nbr_movement_index = 1
      for nbr_match in nbr_matches:
         
         nbr_shapes_movement = all_each_files_movements[each_files][nbr_movement_index]
         nbr_movement_index += 1 
         if nbr_shapes_movement is None:
            continue
         
         x_threshold = 0.3 * abs(nbr_shapes_movement[0]) - 0.95 + smallest_mv_threshold
         y_threshold = 0.3 * abs(nbr_shapes_movement[1]) - 0.95 + smallest_mv_threshold
         
         if x_threshold < smallest_mv_threshold:
            x_threshold = smallest_mv_threshold
         if y_threshold < smallest_mv_threshold:
            y_threshold = smallest_mv_threshold
         
         neighbor_movements.append( ( nbr_shapes_movement, ( x_threshold, y_threshold ) ) )

         if cur_shapes_movement is None:
            continue
            
         x_mv_diff = abs( cur_shapes_movement[0] - nbr_shapes_movement[0] )
         y_mv_diff = abs( cur_shapes_movement[1] - nbr_shapes_movement[1] )

         if x_mv_diff <= x_threshold and y_mv_diff <= y_threshold:
            matched_by_nbr_movements[each_files] = nbr_match
            cur_match_correct = True
            break
         
      
      if cur_shapes_mv_by_pixch is not None and cur_shapes_movement is not None:
         # check for partial match
         pixch_mv_diff_threshold = 5
         
         x_diff = abs( cur_shapes_mv_by_pixch[0] - cur_shapes_movement[0] )
         y_diff = abs( cur_shapes_mv_by_pixch[1] - cur_shapes_movement[1] )
         
         if x_diff + y_diff < pixch_mv_diff_threshold:
            if cur_match_correct is True:
               if consec_index in possible_partial_matches.keys():
                  possible_partial_matches[consec_index].append( each_files )
               else:
                  possible_partial_matches[consec_index] = [ each_files ]
            
            else:
               #match by cur_shapes_mv_by_pixch
               cur_match_correct = True
         
         else:
            failed_evaluations += 0.5
         
      
      if cur_match_correct is None:
         
         # if cur_shapes_movement is stationary, then little pixch should be present in both image1 and image2 shapes
         stationary_result = check_by_stationary_pixch( cur_shapes_movement, app_im_pixch, app_im_shapes_pixels, each_files, pixch )
         if stationary_result is True:
            cur_match_correct = True
         elif stationary_result is False:
            failed_evaluations += 1
         

         # check if previous each_files neighbor match or next each_files neighbor match contain the same match as the current each_files neighbor match
         check_from_adjacent_nbrs = find_same_nbr_m_from_adjacent_nbrs( each_files, all_each_files_matches, each_files_in_order )
         if check_from_adjacent_nbrs is not None: 
            
            if len(check_from_adjacent_nbrs) == 0 :
               #check_from_adjacent_nbrs failed
               failed_evaluations += 0.5

                        

      ano_match_found = 0
      if cur_match_correct is None:
         #same movement test failed

         #image_functions.cr_im_from_shapeslist2( cur_im1file, directory, cur_im_shapeids[0], shapes_rgbs=[(255,0,0)] )
         #image_functions.cr_im_from_shapeslist2( cur_im2file, directory, cur_im_shapeids[1], shapes_rgbs=[(0,0,255)] )  


         # check if another match exists.
         overlapped_im_shapeids = [ set(), set() ]
         for im1or2 in range(2):
            for im_shapeid in cur_im_shapeids[im1or2]:
            
               for im_pindex in im_shapes[im1or2][im_shapeid]:
                  overlapped_im_shapeids[im1or2] |= im_shapeids_by_pindex[im1or2][im_pindex] 
   
         ano_matches = set()
         for im1or2 in range(2):
            opposite_im = abs( im1or2 - 1 )
            for temp_im_shapeid in overlapped_im_shapeids[im1or2]:
               ano_matches |= { temp_match for temp_match in all_matches[each_files] if temp_match[im1or2] == temp_im_shapeid and temp_match[opposite_im] not in cur_im_shapeids[opposite_im] } 
         
         ano_match_im_pixels = [set(),set()]
         for ano_match in ano_matches:
            #image_functions.cr_im_from_shapeslist2( cur_im1file, directory, [ano_match[0]], shapes_rgbs=[(255,255,0)] )
            #image_functions.cr_im_from_shapeslist2( cur_im2file, directory, [ano_match[1]], shapes_rgbs=[(0,255,255)] )  
            for im1or2 in range(2):
               ano_match_im_pixels[im1or2] |= set( im_shapes[im1or2][ ano_match[im1or2] ] )        
               
         for im1or2 in range(2):
         
            # check if ano_match contains most pixels of current image2 shapes
            overlapped_im_pixels = set( ano_match_im_pixels[im1or2] ).intersection( app_im_shapes_pixels[im1or2] )
            if len(overlapped_im_pixels) > len( app_im_shapes_pixels[im1or2] ) * 0.8:
               # another match exist.
               ano_match_found += 1

         if ano_match_found < 2:
            # another match was not found. 
            # check if this is a partial match. if so, perform movement solution for partial match. refer to documentation algorithms/all_matches/fix_consecutives.docx
            #size_diff = same_shapes_functions.check_size_by_pixels( app_im_shapes_pixels[0], app_im_shapes_pixels[1], size_threshold=0.5  )
            #if size_diff is True:
            # partial match
            
            # {(-1, 1): 0.10448154998549658, (-1, 2): 0.12360679774997896, ... }
            nbr_movements_scores = get_nbr_movements_scores( neighbor_movements )
               
            matched_movement = same_shapes_functions.match_from_given_movements( nbr_movements_scores, app_im_shapes_pixels, im_size )
            if matched_movement is not None:
               #current shapes is partial match
               cur_match_correct = True
               
      if cur_match_correct is None:
         # check if enough movements data were present to judge by movement.

         # get neighbor movements that exist. sufficient neighor movements number is 3.
         nbrs_movements_cp = copy.copy( all_each_files_movements[each_files] )
         # first, remove cur_shapes_movement
         nbrs_movements_cp.pop(0)
         # removing all None from the nbrs_movements_cp
         nbrs_movements_cp = [ temp_movement for temp_movement in nbrs_movements_cp if temp_movement is not None ]

         if cur_shapes_movement is None:

            if len(nbrs_movements_cp) >= 1:
               # cur_shapes_movement is None and neighbor movements exist. check by adjacent movements. if adjacent match has the same movement, 
               # then the current match probably has the same movement
               adjacent_mv_result = check_by_adjacent_movements( all_each_files_movements, each_files, app_im_shapes_pixels, each_files_in_order )
               if type(adjacent_mv_result) is tuple:
                  cur_match_correct = True
               elif adjacent_mv_result is False:
                  cur_match_correct = False
            
         else:
            failed_evaluations += 0.5
      
      if cur_match_correct is None:
         # check if all shapes in image1 or image2 are all connected. if not, check if they are far too apart to be a match.
         connected_pixels_result = check_match_by_connected_pixels( cur_im_shapeids, each_files )                  
         if connected_pixels_result is False:
            cur_results[each_files] = False
            break
      
      if cur_match_correct is not True and failed_evaluations >= 2:
         cur_match_correct = False
            
      cur_results[each_files] = cur_match_correct
      
      if cur_match_correct is False or cur_match_correct is None:
         break

   # currenct consecutive is done.
    
   # check if only 1 inconsistent movement can be found. if found, returns inconsistent each_files. None otherwise
   inconsistent_each_files = check_with_other_each_files_mv( all_each_files_movements, cur_results )
   if inconsistent_each_files is not None:
      
      # inconsistent_each_files matched by different means other than movement. so skip this check
      if inconsistent_each_files in matched_by_nbr_movements:
         
         # check if nbr_match that made this match possible is a partial match.
         inconsistent_im_files = [ inconsistent_each_files.split(".")[0], inconsistent_each_files.split(".")[1] ]
      
         inconsistent_nbr_pixels = [ [], [] ]
         for im1or2 in range(2):
            for temp_shapeid in matched_by_nbr_movements[inconsistent_each_files][im1or2]:
               inconsistent_nbr_pixels[im1or2].extend( all_im_shapes[ int(inconsistent_im_files[im1or2]) - lowest_filenum ][temp_shapeid] )
      
         #image_functions.cr_im_from_pixels( inconsistent_im_files[0], directory, inconsistent_nbr_pixels[0] , pixels_rgb=(255,0,0) )
         #image_functions.cr_im_from_pixels( inconsistent_im_files[1], directory, inconsistent_nbr_pixels[1] , pixels_rgb=(0,0,255) )
      
         size_diff = same_shapes_functions.check_size_by_pixels( inconsistent_nbr_pixels[0], inconsistent_nbr_pixels[1], size_threshold=0.5  )
         if size_diff is True:
            cur_results[inconsistent_each_files] = False

   
   # removing wrong matches from current consecutive
   wrong_match = False
   for each_files in cur_results:
      if cur_results[each_files] is not True:
         consecutives_wrong_matches[consec_index] = each_files
         break
   

wrong_matches_dfile = consecutives_ddir + "wrong_matches.data"
with open(wrong_matches_dfile, 'wb') as fp:
   # # { consecutive index number: each_files, ... }
   pickle.dump(consecutives_wrong_matches, fp)
fp.close()

possible_partial_dfile = consecutives_ddir + "possible_partial_matches.data"
with open(possible_partial_dfile, 'wb') as fp:
   # # { consecutive index number: each_files, ... }
   pickle.dump(possible_partial_matches, fp)
fp.close()

possible_partial_dfile = consecutives_ddir + "consecutives_movements.data"
with open(possible_partial_dfile, 'wb') as fp:
   # # { consecutive index number: each_files, ... }
   pickle.dump(all_consec_movements, fp)
fp.close()



   


