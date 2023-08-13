import tkinter
from PIL import ImageTk, Image
from libraries import btwn_amng_files_functions, read_files_functions, pixel_shapes_functions, same_shapes_functions, pixel_functions, image_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files
from libraries.cv_globals import frth_smallest_pixc
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


shapes_m_types_dir = top_shapes_dir + directory + scnd_stg_all_files + "/shp_match_types/"
one_to_one_matched_dfile = shapes_m_types_dir + "data/matched_pixels.data"
with open (one_to_one_matched_dfile, 'rb') as fp:
      # image file num: [ ('57125', '57529'), ... ]
      # or 
      # image file num: [ [ [image1 shapes], [image2 shapes] ], ... ]
   one_to_one_m_shapes = pickle.load(fp)
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




result_shapes = {}

prev_file_shapes = None
prev_filename = None
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
for each_file in all_matches_so_far:
   print( each_file )
   
   result_shapes[ each_file ] = set()
   
   cur_im1file = each_file.split(".")[0]
   cur_im2file = each_file.split(".")[1]

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
         im1shapes_by_pindex[temp_p] = shapeid
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im1shapes[shapeid] = cur_pixels
   

   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()


   im2shapes_by_pindex = {}
   for shapeid in im2shapes:
      cur_pixels = set()
      
      for temp_p in im2shapes[shapeid]:
         im2shapes_by_pindex[temp_p] = shapeid
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
      prev_im2shapes_by_pindex = im2shapes_by_pindex
   
   else:
   
      done_im1_each_shapes = []
      for each_shapes in all_matches_so_far[each_file]:
      
         if each_shapes[0] in done_im1_each_shapes:
            continue
         '''
         if each_shapes[0] != "66101" or each_file != "11.12":
            continue
         '''
         done_im1_each_shapes.append( each_shapes[0] )
         
         found_shapes = { True for temp_shapes in prev_file_shapes if each_shapes[0] == temp_shapes[1] }      
         if len( found_shapes ) == 0:
            # current image1 shape not found in previous image2 shape. so find it by common matched neighbor.
            
            prev_found_neighbor_matches = []
            for cur_im1nbr in im1shapes_neighbors[ each_shapes[0] ]:
               if len( im1shapes[ cur_im1nbr ] ) < frth_smallest_pixc:
                  continue
                  
               prev_common_nbrs_found = [ temp_shapes for temp_shapes in all_matches_so_far[prev_filename] if cur_im1nbr == temp_shapes[1]   ]
               if len( prev_common_nbrs_found ) >= 1:
                  
                  prev_found_neighbor_matches.append( prev_common_nbrs_found )
               

            if len( prev_found_neighbor_matches ) >= 2:
               # 2 or more neighbor matches found
               # not found previous image file image1 shape is likely to be neighbor to these multiple matched neighbors as well
               
               prev_fnd_nbr_m_all_im1shapes = set()
               possible_match_im1nbrs = []
               for prev_found_neighbor_match in prev_found_neighbor_matches:
                  # prev_found_neighbor_match -> [ ( "111", "222" ), ( "112", "222" ), ( "113", "222"), ... ]
                  
                  prev_fnd_nbr_m_all_im1shapes |= set( [ temp_shapes[0] for temp_shapes in prev_found_neighbor_match ] )

                  cur_fnd_nbr_m_im1shapes = [ temp_shapes[0] for temp_shapes in prev_found_neighbor_match ]
                  cur_done_shapes = []
                  for cur_fnd_nbr_m_im1shape in cur_fnd_nbr_m_im1shapes:
                     
                     for prev_im1nbr in prev_im1shapes_nbrs[ cur_fnd_nbr_m_im1shape ]:
                        if prev_im1nbr not in prev_fnd_nbr_m_all_im1shapes and len( prev_im1shapes[ prev_im1nbr ] ) >= frth_smallest_pixc and prev_im1nbr not in cur_done_shapes:
                           if prev_im1shapes_clrs[ prev_im1nbr ] != im1shapes_colors[ each_shapes[0] ]:
                              continue
                           
                           possible_match_im1nbrs.append( prev_im1nbr )
                           
                           cur_done_shapes.append( prev_im1nbr )

               
               done_im1nbrs = []
               more_possible_m_im1nbrs = {}
               for possible_match_im1nbr in possible_match_im1nbrs:
                  if possible_match_im1nbr in done_im1nbrs:
                     continue
                  done_im1nbrs.append( possible_match_im1nbr )
                  
                  im1nbr_count = possible_match_im1nbrs.count( possible_match_im1nbr )
                  
                  if im1nbr_count / len( prev_found_neighbor_matches ) > 0.5:
                     more_possible_m_im1nbrs[ possible_match_im1nbr ] = im1nbr_count
                     

               if len( more_possible_m_im1nbrs ) >= 1:
                  highest_match_count = max( more_possible_m_im1nbrs.values() )
               
               matched_shapes = set()
               for im1nbr_shapeid in more_possible_m_im1nbrs:
                  if more_possible_m_im1nbrs[ im1nbr_shapeid ] < highest_match_count:
                     continue                
                  
                  matched_shapes.add( im1nbr_shapeid )
               
               if len( matched_shapes ) > 1:
                  # if there are multiple matched shapes, then the shape that is closest to the each_shapes[0] in size is the match
                  final_matched_shape = None
                  # closest is the 0. 0 is the perfect size match. farther away from 0 the bigger the size difference
                  closest_size = None
                  closest_shapes = set()
                  for matched_shape in matched_shapes:
                     if closest_size is None:
                        closest_size = abs( len( prev_im1shapes[ matched_shape ] ) - len( im1shapes[ each_shapes[0] ] ) )
                        closest_shapes.add( matched_shape )
                     else:
                        cur_size = abs( len( prev_im1shapes[ matched_shape ] ) - len( im1shapes[ each_shapes[0] ] ) )
                        cur_size_distance_from_0 = cur_size - closest_size
                        
                        # if cur_size_distance_from_0 is negative value, this means that cur_size is closer to 0. if it's positive, cur_size is farther from 0.
                        if cur_size_distance_from_0 < 0:
                           closest_size = cur_size
                           closest_shapes = { matched_shape }
                        
                        elif cur_size_distance_from_0 == 0:
                           # cur_size and closest_size has the same value
                           closest_shapes.add( matched_shape )
                 

                  for closest_shape in closest_shapes:
                     result_shapes[ prev_filename ].add( ( closest_shape, each_shapes[0] ) )
                        
                  
               elif len( matched_shapes ) == 1:
                  result_shapes[ prev_filename ].add( ( list(matched_shapes)[0], each_shapes[0] ) )
                  


      


      prev_file_shapes = all_matches_so_far[each_file]
      prev_filename = each_file

      prev_im1shapes = im1shapes
      prev_im2shapes = im2shapes
      prev_im1shapes_nbrs = im1shapes_neighbors
      prev_im2shapes_nbrs = im2shapes_neighbors
      
      prev_im1shapes_clrs = im1shapes_colors
      prev_im2shapes_clrs = im2shapes_colors

      prev_im1shapes_by_pindex = im1shapes_by_pindex
      prev_im2shapes_by_pindex = im2shapes_by_pindex



for each_files in result_shapes:
      
   if each_files not in all_matches_so_far.keys():
      all_matches_so_far[ each_files ] = result_shapes[ each_files ]
      
   else:
      for each_shapes in result_shapes[ each_files ]:
         if each_shapes not in all_matches_so_far[ each_files ]:
            all_matches_so_far[ each_files ].add( each_shapes )  




possibe_matches_dir = top_shapes_dir + directory + scnd_stg_all_files + "/possible_matches/data/"
possibe_matches_file = possibe_matches_dir + "4.data"
if os.path.exists(possibe_matches_file):
   with open (possibe_matches_file, 'rb') as fp:
      added_missed_shapes = pickle.load(fp)
   fp.close()
   
   for each_files in added_missed_shapes:
      if each_files in result_shapes.keys():
         for each_shapes in added_missed_shapes[each_files]:
            if each_shapes not in result_shapes[each_files]:
               result_shapes[each_files].add( each_shapes )
         
      else:
         result_shapes[each_files] = added_missed_shapes[each_files]   



with open(possibe_matches_file, 'wb') as fp:
   pickle.dump(result_shapes, fp)
fp.close()

'''
with open(all_matches_so_far_dfile, 'wb') as fp:
   pickle.dump(all_matches_so_far, fp)
fp.close()
'''



















