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


# shapes_pixels 
# [ [ shapeid, ( rgb ), {( xy ), ( xy ), ... } ], [ shapeid, ( rgb ), { ( xy ), ( xy ), ... } ], ... ]
# 
# directly_UD is directly up or down. if it is true, it goes directly up or down with left or right value 0.
def move_pixels( shapes_pixels, move_direction, directly_UD, step, move_total, notfnd_shapes, notfnd_shapes_by_pindex, notfnd_shapes_clrs, notfnd_shapes_nbrs ):


   # {"matched count": [ ( shape from shapes_pixels, its matched not found shapeid ), ( another matched shape from shapes_pixels, 
   #                       its matched not found shapeid ), ... ], "matched count": [ ... ] }
   matched_shapes = {}

   
   for move_LR in range( 0, move_total, step ):

      if directly_UD is False and move_LR == 0:
         continue

      move_x = None
      if "left" in move_direction.lower():
         # subtract from x
         if move_LR != 0:
            move_x = move_LR * -1
         else:
            move_x = 0
      
      elif "right" in move_direction.lower():
         # add to x
         if move_LR != 0:
            move_x = move_LR
         else:
            move_x = 0
         
      
      for move_UD in range( 0, move_total, step ):
         move_y = None
         
         if "up" in move_direction.lower():
            # subtract from y
            if move_UD != 0:
               move_y = move_UD * -1
            else:
               move_y = 0
         
         elif "down" in move_direction.lower():
            # add to y
            if move_UD != 0:
               move_y = move_UD
            else:
               move_y = 0
         
         


         all_shapes_matched_notf_shapes = []
         
         # matched_notfnd_shapes have to be neighbors
         matched_notf_shapes_w_nbrs = []
        
         
         for shape_pixels in shapes_pixels:
            
            debug_pixels = set()
            
            cur_matched_shape_notf_shapes = []
            
            # { shapeid: how many pixels have been found, ... }
            pixel_found_from_notfnd_shapes = {}         
            for xy in shape_pixels[2]:
               _xy = ( xy[0] + move_x, xy[1] + move_y )

               # check if pixel is out of the image
               if _xy[0] < 0 or _xy[0] >= im_width or _xy[1] < 0 or _xy[1] >= im_height:
                  continue
               
               debug_pixels.add( _xy )
               
               pindex = pixel_functions.convert_xy_to_pindex( _xy, im_width )
               
               # check if current shape's color is the same as not found image's pixel
               if shape_pixels[1] != notfnd_shapes_clrs[ notfnd_shapes_by_pindex[ str(pindex) ] ]:
                  continue
               
               if notfnd_shapes_by_pindex[ str(pindex) ] not in pixel_found_from_notfnd_shapes.keys():
                  pixel_found_from_notfnd_shapes[ notfnd_shapes_by_pindex[ str(pindex) ] ] = 1
               else:
                  pixel_found_from_notfnd_shapes[ notfnd_shapes_by_pindex[ str(pindex) ] ] += 1

            #image_functions.cr_im_from_pixels( "10", directory, debug_pixels, save_filepath=None , pixels_rgb=None )


            
            for not_found_shapeid in pixel_found_from_notfnd_shapes:
               if len( notfnd_shapes[ not_found_shapeid ] ) < third_smallest_pixc:
                  continue
               
               # check if 60% or more pixels of not found shape matched or already found shape
               if pixel_found_from_notfnd_shapes[ not_found_shapeid ] / len( notfnd_shapes[ not_found_shapeid ] ) >= 0.6 or \
                  pixel_found_from_notfnd_shapes[ not_found_shapeid ] / len( shape_pixels[2] ) >= 0.7:
                  
                  matched_notfnd_shapes = []
                  matched_notfnd_shapes.append( shape_pixels[0] )
                  matched_notfnd_shapes.append( not_found_shapeid )
                  matched_notfnd_shapes.append( len( shape_pixels[2] ) )
                  matched_notfnd_shapes.append( pixel_found_from_notfnd_shapes[ not_found_shapeid ] )
                  
                  cur_matched_shape_notf_shapes.append( matched_notfnd_shapes )

            if len( cur_matched_shape_notf_shapes ) >= 1:
               all_shapes_matched_notf_shapes.append( cur_matched_shape_notf_shapes )
         
         

         # all_shapes_matched_notf_shapes -> [[['55672', '54887', 94, 50]], [['55292', '54496', 44, 20]], [['57316', '3704', 14, 20], ['57316', '43307', 8, 10], ... ]]
         # [ [ each already found shape's neighbor's list  [ already found shape's neighbor shapeid, matched not found shapeid, 
         #     already found shape's neighbor pixels, matched pixels ]   ] ]
         
         for each_matched_shape_notf_shapes in all_shapes_matched_notf_shapes:
            # each_matched_shape_notf_shapes -> [['57316', '3704', 14, 30], ['57316', '43307', 8, 21], ... ]
            
            for each_notf_shape in each_matched_shape_notf_shapes:
               notfnd_shape_nbrs = notfnd_shapes_nbrs[ each_notf_shape[1] ]
               
               for ano_each_m_shape_notf_shapes in all_shapes_matched_notf_shapes:
                  
                  for ano_each_notf_shape in ano_each_m_shape_notf_shapes:
                     if ano_each_notf_shape[1] in notfnd_shape_nbrs:
                        cur_m_notf_shapes_w_nbrs = []
                        cur_m_notf_shapes_w_nbrs.append( each_notf_shape[0] )   # already matched shape's neighbor
                        cur_m_notf_shapes_w_nbrs.append( each_notf_shape[1] )   # not found shape
                        cur_m_notf_shapes_w_nbrs.append( each_notf_shape[2] )   # already matched shape's neighbor pixels count
                        cur_m_notf_shapes_w_nbrs.append( each_notf_shape[3] )   # not found shape's matched pixels count
                        
                        matched_notf_shapes_w_nbrs.append( cur_m_notf_shapes_w_nbrs )
                        
                        cur_m_notf_shapes_w_nbrs = []
                        cur_m_notf_shapes_w_nbrs.append( ano_each_notf_shape[0] ) # already matched shape's neighbor
                        cur_m_notf_shapes_w_nbrs.append( ano_each_notf_shape[1] ) # not found shape
                        cur_m_notf_shapes_w_nbrs.append( ano_each_notf_shape[2] ) # already matched shape's neighbor pixels count
                        cur_m_notf_shapes_w_nbrs.append( ano_each_notf_shape[3] ) # not found shape's matched pixels count
                        
                        matched_notf_shapes_w_nbrs.append( cur_m_notf_shapes_w_nbrs )
                  

         # matched_notf_shapes_w_nbrs may contain same matched pairs. take only unique pairs.
         # examples.
         # [['51686', '51699', 191, 99], ['57316', '53280', 4719, 2632], ['57316', '53280', 4719, 2632], ['51686', '51699', 191, 99]]
         # [ [ already matched shape's neighbor, matched not found shape, already matched shape's neighbor pixels count, matched not found shape's pixels count ] ]

         cur_matched_shapes_count = 0
         cur_matched_shapes_total = 0
         cur_matched_shapes = set()   
         
         already_done_pairs = set()
         for each_shape_notf_shapes in matched_notf_shapes_w_nbrs:
            # each_shape_notf_shapes -> ['51686', '51699', 191, 136]
            
            if tuple(each_shape_notf_shapes) in already_done_pairs:
               continue
            
            # alrd_matched_shape_found includes each_shape_notf_shapes itself
            alrd_matched_shape_found = [ temp_shapes for temp_shapes in matched_notf_shapes_w_nbrs if temp_shapes[0] == each_shape_notf_shapes[0] ]
            if len( alrd_matched_shape_found ) > 1:
               notf_shapes_len = 0
               for each_shape in alrd_matched_shape_found:
                  # each_shape has the same already matched shape's neighbor
                  notf_shapes_len += each_shape[3]
               
               if notf_shapes_len / each_shape_notf_shapes[2] >= 0.65:
                  cur_matched_shapes_total +=  notf_shapes_len / each_shape_notf_shapes[2] 
                  
                  for each_shape in alrd_matched_shape_found:
                     cur_matched_shapes_count += 1
                     cur_matched_shapes.add( ( each_shape[1], each_shape[0] ) )
                     already_done_pairs.add( tuple(each_shape) )
                  
            else:
               # alrd_matched_shape_found does not contain multiple each_shape_notf_shapes with same already matched_shape's neighbor
            
               # notf_shape_found includes each_shape_notf_shapes itself
               notf_shape_found = [ temp_shapes for temp_shapes in matched_notf_shapes_w_nbrs if temp_shapes[1] == each_shape_notf_shapes[1] ]
            
               if len( notf_shape_found ) >= 1:
                  alrd_fshp_nbr_len = 0
                  for each_shape in notf_shape_found:
                     # each_shape has the same not found shape
                     alrd_fshp_nbr_len += each_shape[2]
               
                  if each_shape_notf_shapes[3] / alrd_fshp_nbr_len >= 0.65:
                     cur_matched_shapes_total += each_shape_notf_shapes[3] / alrd_fshp_nbr_len 
                     
                     for each_shape in notf_shape_found:
                        cur_matched_shapes_count += 1
                        cur_matched_shapes.add( ( each_shape[1], each_shape[0] ) )
                        already_done_pairs.add( tuple(each_shape) )
            
            
            
         if cur_matched_shapes_count < 2:
            continue
         
         cur_matched_shapes_total *= cur_matched_shapes_count
         matched_shapes[ cur_matched_shapes_total ] = cur_matched_shapes            
         
            
         
      
   return matched_shapes     





result_shapes = {}

prev_file_shapes = None
prev_filename = None
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
for each_file in all_matches_so_far:
   print( each_file )
   
   cur_im1file = each_file.split(".")[0]
   cur_im2file = each_file.split(".")[1]
   
   result_shapes[each_file] = set()

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

   im1shapes_by_pindex = {}
   for shapeid in im1shapes:
      cur_pixels = set()
      for temp_p in im1shapes[shapeid]:
         im1shapes_by_pindex[ temp_p ] = shapeid
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im1shapes[shapeid] = cur_pixels

   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()

   for shapeid in im2shapes:
      cur_pixels = set()
      
      for temp_p in im2shapes[shapeid]:
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im2shapes[shapeid] = cur_pixels


   im1shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + cur_im1file + "_shape_nbrs.txt"
   im2shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + cur_im2file + "_shape_nbrs.txt"

   # {'79999': ['71555', '73953', ...], ...}
   im1shapes_neighbors = read_files_functions.rd_dict_k_v_l(cur_im1file, directory, im1shape_neighbors_file)
   im2shapes_neighbors = read_files_functions.rd_dict_k_v_l(cur_im2file, directory, im2shape_neighbors_file)

   im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im1file, directory, shapes_type=shapes_type, min_colors=True)
   im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im2file, directory, shapes_type=shapes_type, min_colors=True)

  
   if prev_file_shapes is None:
      prev_file_shapes = all_matches_so_far[each_file]
      prev_filename = each_file
      
      prev_im1shapes = im1shapes
      prev_im2shapes = im2shapes
      prev_im1shapes_nbrs = im1shapes_neighbors
      prev_im2shapes_nbrs = im2shapes_neighbors
      
      prev_im1shapes_clrs = im1shapes_colors
      prev_im2shapes_clrs = im2shapes_colors
      
      
      prev_im1shapes_by_pindex = im1shapes_by_pindex
   
   else:
      prev_im1file = prev_filename.split(".")[0]
      prev_im2file = prev_filename.split(".")[1]

   
      for each_shapes in all_matches_so_far[each_file]:
         if len( im1shapes[ each_shapes[0] ] ) < frth_smallest_pixc:
            continue

         
         found_shapes = { True for temp_shapes in prev_file_shapes if each_shapes[0] == temp_shapes[1] }      
         if len( found_shapes ) == 0:
            # current image1 shape not found in previous image2 shape
            
            # get all direct neighbors that are already matched.
            already_matched_shapes = set()
            already_matched_shapes.add(  each_shapes[0] )
            for im1nbr in im1shapes_neighbors[ each_shapes[0] ]:
               im1nbr_found = { True for temp_shapes in all_matches_so_far[each_file] if im1nbr == temp_shapes[0] }
               
               if len( im1nbr_found ) >= 1 and len( im1shapes[ im1nbr ] ) >= frth_smallest_pixc:
                  already_matched_shapes.add( im1nbr )
            
            if len( already_matched_shapes ) == 1:
               # no already matched neighbors are found. skip this
               continue
            
            
            # [ [ shapeid, ( rgb ), {( xy ), ( xy ), ... } ], [ shapeid, ( rgb ), { ( xy ), ( xy ), ... } ], ... ]
            already_matched_shp_pixels = []
            for temp_shape in already_matched_shapes:
               shape_rgb_and_pixels = [ temp_shape ]
               
               shape_rgb_and_pixels.append( im1shapes_colors[ temp_shape ] )
               shape_rgb_and_pixels.append( im1shapes[ temp_shape ] )
               
               already_matched_shp_pixels.append( shape_rgb_and_pixels )


            leftUp_results = move_pixels( already_matched_shp_pixels, "left_up", True, 2, 16, prev_im1shapes, prev_im1shapes_by_pindex, prev_im1shapes_clrs, prev_im1shapes_nbrs )
            leftDown_results = move_pixels( already_matched_shp_pixels, "left_down", True, 2, 16, prev_im1shapes, prev_im1shapes_by_pindex, prev_im1shapes_clrs, prev_im1shapes_nbrs )
            rightUp_results = move_pixels( already_matched_shp_pixels, "right_up", False, 2, 16, prev_im1shapes, prev_im1shapes_by_pindex, prev_im1shapes_clrs, prev_im1shapes_nbrs )
            rightDown_results = move_pixels( already_matched_shp_pixels, "right_down", False, 2, 16, prev_im1shapes, prev_im1shapes_by_pindex, prev_im1shapes_clrs, prev_im1shapes_nbrs )

            
            # get the highest matched shapes
            highest_match_count = 0
            highest_match = None
            for each_results in [ leftUp_results, leftDown_results, rightUp_results, rightDown_results ]:
               for each_match_count in each_results:
                  if each_match_count > highest_match_count:
                     highest_match_count = each_match_count
                     highest_match = each_results[ highest_match_count ]

            if highest_match is not None:
               
               verified_shapes = shapes_results_functions.verify_matches( highest_match, [ prev_im1shapes, im1shapes ] , [ prev_im1shapes_clrs, im1shapes_colors  ], 
                                                     [ prev_im1shapes_nbrs, im1shapes_neighbors ], im_width )
               if len( verified_shapes ) >= 1:
                  result_shapes[prev_im1file + "." + cur_im1file ] |= verified_shapes




      prev_file_shapes = all_matches_so_far[each_file]
      prev_filename = each_file

      prev_im1shapes = im1shapes
      prev_im2shapes = im2shapes
      prev_im1shapes_nbrs = im1shapes_neighbors
      prev_im2shapes_nbrs = im2shapes_neighbors
      
      prev_im1shapes_clrs = im1shapes_colors
      prev_im2shapes_clrs = im2shapes_colors

      prev_im1shapes_by_pindex = im1shapes_by_pindex



for each_files in result_shapes:
      
   if each_files not in all_matches_so_far.keys():
      all_matches_so_far[ each_files ] = result_shapes[ each_files ]
      
   else:
      for each_shapes in result_shapes[ each_files ]:
         if each_shapes not in all_matches_so_far[ each_files ]:
            all_matches_so_far[ each_files ].add( each_shapes )  


missed_shapes_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/consecutive_missed/data/"
added_missed3_dfile = missed_shapes_ddir + "3.data"  
if os.path.exists(added_missed3_dfile):
   with open (added_missed3_dfile, 'rb') as fp:
      added_missed3_shapes = pickle.load(fp)
   fp.close()
   
   for each_files in added_missed3_shapes:
      if each_files in result_shapes.keys():
         for each_shapes in added_missed3_shapes[each_files]:
            if each_shapes not in result_shapes[each_files]:
               result_shapes[each_files].add( each_shapes )
         
      else:
         result_shapes[each_files] = added_missed3_shapes[each_files]   


if os.path.exists(missed_shapes_ddir ) == False:
   os.makedirs(missed_shapes_ddir )

missed_shapes2_dfile = missed_shapes_ddir + "3.data"
with open(missed_shapes2_dfile, 'wb') as fp:
   pickle.dump(result_shapes, fp)
fp.close()

with open(all_matches_so_far_dfile, 'wb') as fp:
   pickle.dump(all_matches_so_far, fp)
fp.close()





















