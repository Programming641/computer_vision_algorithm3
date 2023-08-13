import tkinter
from PIL import ImageTk, Image
from libraries import btwn_amng_files_functions, read_files_functions, pixel_shapes_functions, same_shapes_functions, pixel_functions, image_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files
from libraries.cv_globals import frth_smallest_pixc
import pickle
import sys, pathlib, os



shapes_type = "intnl_spixcShp"
directory = "videos/street3/resized/min"


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



def check_shape_size( param_im1shapeid, param_im2shapeid, param_shapes, param_ano_shapes ):
   # check if size is too different
   im1shapes_total = len( param_shapes[param_im1shapeid] )
   im2shapes_total = len( param_ano_shapes[param_im2shapeid] )
      
   im1_2pixels_diff = abs( im1shapes_total - im2shapes_total )
   if im1_2pixels_diff != 0:
      if im1shapes_total > im2shapes_total:
         if im1_2pixels_diff / im2shapes_total > 1:
            return True
      else:
         if im1_2pixels_diff / im1shapes_total > 1:
            return True

   return False      


verified_shapes = {}

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

   im1shapes_boundaries = {}
   for shapeid in im1shapes:
      cur_pixels = set()
      for temp_p in im1shapes[shapeid]:
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
   for shapeid in im2shapes:
      cur_pixels = set()
      
      for temp_p in im2shapes[shapeid]:
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

  
   if prev_file_shapes is None:
      prev_file_shapes = all_matches_so_far[each_file]
      prev_filename = each_file
      
      prev_im1shapes = im1shapes
      prev_im2shapes = im2shapes
      prev_im1shapes_nbrs = im1shapes_neighbors
      prev_im2shapes_nbrs = im2shapes_neighbors
      
      prev_im1shapes_clrs = im1shapes_colors
      prev_im2shapes_clrs = im2shapes_colors
      
      prev_im1shapes_boundaries = im1shapes_boundaries
      prev_im2shapes_boundaries = im2shapes_boundaries
   
   else:
      prev_im1file = prev_filename.split(".")[0]
      prev_im2file = prev_filename.split(".")[1]
                           
      verified_shapes[prev_im2file + "." +  cur_im2file ] = []
      verified_shapes[prev_im1file + "." + cur_im1file ] = []
      
   
   
      for each_prev_shapes in prev_file_shapes:
         
         found_shapes = { True for temp_shapes in all_matches_so_far[each_file] if each_prev_shapes[1] == temp_shapes[0] }      

         if len( found_shapes ) == 0:
            # each_prev_shapes image2 not found in current all_matches_so_far. so find it.
            
            already_done_shapes = []
            for not_found_prev_im2shape_nbr in prev_im2shapes_nbrs[each_prev_shapes[1]]:
               found_cur_nbrs_matches = [ temp_shapes for temp_shapes in all_matches_so_far[each_file] if temp_shapes[0] == not_found_prev_im2shape_nbr ]
               
               for found_cur_nbr_match in found_cur_nbrs_matches:
                  
                  for possible_match_im2nbr in im2shapes_neighbors[found_cur_nbr_match[1]]:
                     # possible_match_im2nbr may be the match with each_prev_shapes[1]
                     if possible_match_im2nbr in already_done_shapes or len( im2shapes[possible_match_im2nbr] ) < frth_smallest_pixc:
                        continue
                     
                     already_done_shapes.append( possible_match_im2nbr )
                     
                     # check if size is too different
                     size_too_diff = check_shape_size( each_prev_shapes[1], possible_match_im2nbr, prev_im2shapes, im2shapes )
                     if size_too_diff is True:
                        continue                        
                     
                     if prev_im2shapes_clrs[ each_prev_shapes[1] ] != im2shapes_colors[possible_match_im2nbr]:
                        continue                     

                     prev_shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( prev_im2shapes[ each_prev_shapes[1] ], im_width, param_shp_type=1 )  
                     cur_shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( im2shapes[possible_match_im2nbr], im_width, param_shp_type=1 )                     
                     
                     # matching from bigger shape.
                     if len( prev_im2shapes[ each_prev_shapes[1] ] ) > len( im2shapes[possible_match_im2nbr] ):
                        prev_cur_match = same_shapes_functions.match_shape_while_moving_it( prev_shp_coord_xy, cur_shp_coord_xy )
                     else:
                        prev_cur_match = same_shapes_functions.match_shape_while_moving_it( cur_shp_coord_xy, prev_shp_coord_xy )

                     if prev_cur_match is not True:
                        continue


                     im2shp_nbrs = set()
                     for temp_nbr in im2shapes_neighbors[possible_match_im2nbr]:
                        if len( im2shapes[temp_nbr] ) < frth_smallest_pixc:
                           continue
                           
                        im2shp_nbrs.add( temp_nbr )
                     
                     prev_im2shp_nbrs = set()
                     for temp_nbr in prev_im2shapes_nbrs[each_prev_shapes[1]]:
                        if len( prev_im2shapes[temp_nbr] ) < frth_smallest_pixc:
                           continue

                        prev_im2shp_nbrs.add( temp_nbr )
                    
                     matched_nbrs = 0
                     smaller_neighbor_len = 0
                     if len( im2shp_nbrs ) > len( prev_im2shp_nbrs ):
                        smaller_neighbor_len = len( prev_im2shp_nbrs )
                     else:
                        smaller_neighbor_len = len( im2shp_nbrs )                     
                    
                  
                     for im2shp_nbr in im2shp_nbrs:
                     
                        for prev_im2shp_nbr in prev_im2shp_nbrs:
                           
                           if im2shapes_colors[ im2shp_nbr ] != prev_im2shapes_clrs[prev_im2shp_nbr]:
                              continue                           
                        
                           size_too_diff = check_shape_size( im2shp_nbr, prev_im2shp_nbr, im2shapes, prev_im2shapes )
                           if size_too_diff is True:
                              continue                  

                           cur_shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( im2shapes[ im2shp_nbr ], im_width, param_shp_type=1 )  
                           prev_shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( prev_im2shapes[prev_im2shp_nbr], im_width, param_shp_type=1 )                     
                     
                           # matching from bigger shape.
                           if len( im2shapes[ im2shp_nbr ] ) > len( prev_im2shapes[prev_im2shp_nbr] ):
                              prev_cur_match = same_shapes_functions.match_shape_while_moving_it( cur_shp_coord_xy, prev_shp_coord_xy )
                           else:
                              prev_cur_match = same_shapes_functions.match_shape_while_moving_it( prev_shp_coord_xy, cur_shp_coord_xy )

                           if prev_cur_match is True:
                              matched_nbrs += 1
                              
                              break
                                 
                     if matched_nbrs < 2:
                        continue
   
                     if matched_nbrs / smaller_neighbor_len >= 0.6:
                        # 33% or more of neighbors matched

                        verified_shapes[ prev_im2file + "." +  cur_im2file ].append( ( each_prev_shapes[1], possible_match_im2nbr ) )




      if len( verified_shapes[prev_im2file + "." +  cur_im2file ] ) == 0:
         verified_shapes.pop( prev_im2file + "." +  cur_im2file )



      for each_cur_shapes in all_matches_so_far[each_file]:

         found_shapes = { True for temp_shapes in prev_file_shapes if each_cur_shapes[0] == temp_shapes[1] }      

         if len( found_shapes ) == 0:
            # each_cur_shapes image1 not found in prev_file_shapes image2. so find it.
            # each_cur_shapes image1 neighbors and neighbors of prev_file_shapes image2 that matches each_cur_shapes image1 should have
            # fairly the same neighbors
            
            already_done_shapes = []
            for not_found_im1shape_nbr in im1shapes_neighbors[each_cur_shapes[0]]:
               found_prev_nbrs_matches = [ temp_shapes for temp_shapes in prev_file_shapes if temp_shapes[1] == not_found_im1shape_nbr ]
               
               for found_prev_nbr_match in found_prev_nbrs_matches:
                  
                  for possible_match_im1nbr in prev_im1shapes_nbrs[found_prev_nbr_match[0]]:
                     # possible_match_im1nbr may be the match with each_cur_shapes[0]
                     if possible_match_im1nbr in already_done_shapes or len( prev_im1shapes[possible_match_im1nbr] ) < frth_smallest_pixc:
                        continue
                                          
                     already_done_shapes.append( possible_match_im1nbr )

                     
                     # check if size is too different
                     size_too_diff = check_shape_size( each_cur_shapes[0], possible_match_im1nbr, im1shapes, prev_im1shapes )
                     if size_too_diff is True:
                        continue                        
                     
                     if im1shapes_colors[ each_cur_shapes[0] ] != prev_im1shapes_clrs[possible_match_im1nbr]:
                        continue                     

                     cur_shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( im1shapes[ each_cur_shapes[0] ], im_width, param_shp_type=1 )  
                     prev_shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( prev_im1shapes[possible_match_im1nbr], im_width, param_shp_type=1 )                     
                     
                     # matching from bigger shape.
                     if len( im1shapes[ each_cur_shapes[0] ] ) > len( prev_im1shapes[possible_match_im1nbr] ):
                        prev_cur_match = same_shapes_functions.match_shape_while_moving_it( cur_shp_coord_xy, prev_shp_coord_xy )
                     else:
                        prev_cur_match = same_shapes_functions.match_shape_while_moving_it( prev_shp_coord_xy, cur_shp_coord_xy )

                     if prev_cur_match is not True:
                        continue

                     prev_im1nbrs = set()
                     for temp_nbr in prev_im1shapes_nbrs[possible_match_im1nbr]:
                        
                        if len( prev_im1shapes[temp_nbr] ) < frth_smallest_pixc:
                           continue
                           
                        prev_im1nbrs.add( temp_nbr )
                     
                     
                     im1shapes_nbrs = set()
                     for temp_nbr in im1shapes_neighbors[each_cur_shapes[0]]:
                        if len( im1shapes[temp_nbr] ) < frth_smallest_pixc:
                           continue

                        im1shapes_nbrs.add( temp_nbr )
                    
                     matched_nbrs = 0
                     smaller_neighbor_len = 0
                     if len( prev_im1nbrs ) > len( im1shapes_nbrs ):
                        smaller_neighbor_len = len( im1shapes_nbrs )
                     else:
                        smaller_neighbor_len = len( prev_im1nbrs )                     
                     
                     #image_functions.cr_im_from_shapeslist2( prev_im1file, directory, prev_im1nbrs, save_filepath=None , shapes_rgb=None )
                     #image_functions.cr_im_from_shapeslist2( cur_im1file, directory, im1shapes_nbrs, save_filepath=None , shapes_rgb=None )

                     for prev_im1nbr in prev_im1nbrs:
                     
                        for im1nbr in im1shapes_nbrs:
                           
                           if im1shapes_colors[ im1nbr ] != prev_im1shapes_clrs[prev_im1nbr]:
                              continue                           
                        
                           size_too_diff = check_shape_size( im1nbr, prev_im1nbr, im1shapes, prev_im1shapes )
                           if size_too_diff is True:
                              continue                  

                           cur_shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( im1shapes[ im1nbr ], im_width, param_shp_type=1 )  
                           prev_shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( prev_im1shapes[prev_im1nbr], im_width, param_shp_type=1 )                     
                     
                           # matching from bigger shape.
                           if len( im1shapes[ im1nbr ] ) > len( prev_im1shapes[prev_im1nbr] ):
                              prev_cur_match = same_shapes_functions.match_shape_while_moving_it( cur_shp_coord_xy, prev_shp_coord_xy )
                           else:
                              prev_cur_match = same_shapes_functions.match_shape_while_moving_it( prev_shp_coord_xy, cur_shp_coord_xy )

                           if prev_cur_match is True:
                                 matched_nbrs += 1
                              
                                 break

                     
                     if matched_nbrs < 2:
                        continue
   
                     if matched_nbrs / smaller_neighbor_len >= 0.6:
                        # 33% or more of neighbors matched

                        verified_shapes[ prev_im1file + "." +  cur_im1file ].append( ( possible_match_im1nbr, each_cur_shapes[0] ) )



      prev_file_shapes = all_matches_so_far[each_file]
      prev_filename = each_file

      prev_im1shapes = im1shapes
      prev_im2shapes = im2shapes
      prev_im1shapes_nbrs = im1shapes_neighbors
      prev_im2shapes_nbrs = im2shapes_neighbors
      
      prev_im1shapes_clrs = im1shapes_colors
      prev_im2shapes_clrs = im2shapes_colors

      prev_im1shapes_boundaries = im1shapes_boundaries
      prev_im2shapes_boundaries = im2shapes_boundaries




# removing duplicates
for each_filenames in verified_shapes:
   cur_already_fnd_shapes = []
   cur_delete_indexes = []
   
   for lindex, cur_matched_shapes in enumerate( verified_shapes[each_filenames] ):
      
      if cur_matched_shapes in cur_already_fnd_shapes:
         # duplicate found
          cur_delete_indexes.append( lindex )
      else:
         cur_already_fnd_shapes.append( cur_matched_shapes )
      
      
   # now I have all indexes to be deleted
   cur_deleted = 0
   for cur_index in cur_delete_indexes:
      verified_shapes[each_filenames].pop( cur_index - cur_deleted )
      
      cur_deleted += 1

         
         
# adding verified_shapes to all_matches_so_far
for each_files in verified_shapes:
      
   if each_files not in all_matches_so_far.keys():
      all_matches_so_far[ each_files ] = verified_shapes[ each_files ]
      
   else:
      for each_shapes in verified_shapes[ each_files ]:
         if each_shapes not in all_matches_so_far[ each_files ]:
            all_matches_so_far[ each_files ].add( each_shapes )
         
      
missed_shapes_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/consecutive_missed/data/"
added_missed_dfile = missed_shapes_ddir + "7.data"
if os.path.exists(added_missed_dfile):
   with open (added_missed_dfile, 'rb') as fp:
      added_missed_shapes = pickle.load(fp)
   fp.close()
   
   for each_files in added_missed_shapes:
      if each_files in verified_shapes.keys():
         for each_shapes in added_missed_shapes[each_files]:
            if each_shapes not in verified_shapes[each_files]:
               verified_shapes[each_files].append( each_shapes )
         
      else:
         verified_shapes[each_files] = added_missed_shapes[each_files]      
    
      
if os.path.exists(missed_shapes_ddir ) == False:
   os.makedirs(missed_shapes_ddir )

missed_shapes_dfile = missed_shapes_ddir + "7.data"
with open(missed_shapes_dfile, 'wb') as fp:
   pickle.dump(verified_shapes, fp)
fp.close()
'''
with open(all_matches_so_far_dfile, 'wb') as fp:
   pickle.dump(all_matches_so_far, fp)
fp.close()
'''

















