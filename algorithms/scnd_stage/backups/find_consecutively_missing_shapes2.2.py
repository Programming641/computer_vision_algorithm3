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
                           
      result_shapes[each_file] = set()
      result_shapes[prev_im1file + "." + cur_im1file ] = set()
      
   
   
      for each_shapes in all_matches_so_far[each_file]:
         
         found_shapes = { True for temp_shapes in prev_file_shapes if each_shapes[0] == temp_shapes[1] }      
         if len( found_shapes ) == 0:
            # current image1 shape not found in previous image2 shape. so find it by common matched neighbor.
            
            for cur_im1nbr in im1shapes_neighbors[ each_shapes[0] ]:
               if len( im1shapes[ cur_im1nbr ] ) < frth_smallest_pixc:
                  continue
                  
               # one_to_one_m_shapes[prev_im1file + "." + cur_im1file]  -> ('57125', '57529') or [ [image1 shapes], [image2 shapes] ]
               prev_common_nbrs_found = [ temp_shapes for temp_shapes in one_to_one_m_shapes[prev_im1file + "." + cur_im1file] \
                                             if ( type( temp_shapes ) is tuple and cur_im1nbr == temp_shapes[1] ) or 
                                             ( type( temp_shapes ) is list and cur_im1nbr in temp_shapes[1] )  ]
               if len( prev_common_nbrs_found ) >= 1:
                  # cur_im1nbr is the common matched neighbor.
                  # missing previous image1 shape is likely to be neighbor to this common matched neighbor
                  # check if possible_prev_im1match is a match with each_shapes[0]
                     
                  # prev_common_nbr_found -> [ ( '5555', '4444' ) ] or [[['49346', '42963'], ['50140']]]
                  #                          [ [['51481', '56319', '49529'], ['57125']], [['56319'], ['57125', '51925']] ]
                  
                  done_possible_pre_im1shapes = []
                  
                  for prev_common_nbr_found in prev_common_nbrs_found:

                     prev_found_matched_im1nbrs = set()
                     prev_found_matched_im2nbrs = set()
                     if type( prev_common_nbr_found ) is tuple:
                        prev_found_matched_im1nbrs.add( prev_common_nbr_found[0] )
                        prev_found_matched_im2nbrs.add( prev_common_nbr_found[1] )
                     elif type( prev_common_nbr_found ) is list:
                        prev_found_matched_im1nbrs |= set( prev_common_nbr_found[0] )
                        prev_found_matched_im2nbrs |= set( prev_common_nbr_found[1] )
                        
                     temp_im1pixels = set()
                     for prev_found_matched_im1nbr in prev_found_matched_im1nbrs:
                        temp_im1pixels |= prev_im1shapes[ prev_found_matched_im1nbr ]

                     temp_im2pixels = set()
                     for prev_found_matched_im2nbr in prev_found_matched_im2nbrs:
                        temp_im2pixels |= prev_im2shapes[ prev_found_matched_im2nbr ]
                     
                     if len( temp_im1pixels ) > ( im_width * im_height ) / 50 or len( temp_im2pixels ) > ( im_width * im_height ) / 50:
                        continue
                     
                     prev_fnd_m_im1nbrs_boundaries = pixel_shapes_functions.get_boundary_pixels( temp_im1pixels ) 
                     prev_fnd_m_im2nbrs_boundaries = pixel_shapes_functions.get_boundary_pixels( temp_im2pixels )
                     
                     
                     for prev_found_matched_im1nbr in prev_found_matched_im1nbrs:
                        
                        for possible_prev_im1match in prev_im1shapes_nbrs[ prev_found_matched_im1nbr ]:
                           
                           if len( prev_im1shapes[ possible_prev_im1match ] ) < frth_smallest_pixc or possible_prev_im1match in done_possible_pre_im1shapes:
                              continue
                           
                           done_possible_pre_im1shapes.append( possible_prev_im1match )
                           
                           if prev_im1shapes_clrs[ possible_prev_im1match ] != im1shapes_colors[ each_shapes[0] ]:
                              continue

                           size_diff = check_shape_size( possible_prev_im1match, each_shapes[0], prev_im1shapes, im1shapes, size_threshold=1 )
                           if size_diff is True:
                              continue
                           
                           print("possible_prev_im1match " + possible_prev_im1match + " each_shapes[0] " + each_shapes[0] )
                           
                           result =   pixel_shapes_functions.check_shape_attached_near( prev_fnd_m_im1nbrs_boundaries, prev_im1shapes_boundaries[possible_prev_im1match], 
                                                                                        prev_fnd_m_im2nbrs_boundaries, im1shapes_boundaries[each_shapes[0]], im1.size )

                           if result is not True:
                              continue

                           prev_im1nbr_shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( prev_im1shapes[ possible_prev_im1match ], im_width, param_shp_type=1 )  
                           im1nbr_shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( im1shapes[ each_shapes[0] ], im_width, param_shp_type=1 )  
                     
                           # matching from smaller shape.
                           if len( prev_im1shapes[ possible_prev_im1match ] ) > len( im1shapes[ each_shapes[0]] ):
                              im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( im1nbr_shp_coord_xy, prev_im1nbr_shp_coord_xy, match_threshold=0.6 )
                           else:
                              im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( prev_im1nbr_shp_coord_xy, im1nbr_shp_coord_xy, match_threshold=0.6 )

                           if im1im2nbr_match is not True:
                              continue     

                           result_shapes[prev_im1file + "." + cur_im1file ].add( ( possible_prev_im1match, each_shapes[0] ) )
                           
      sys.exit()

      for prev_each_shapes in prev_file_shapes:
      
         found_shapes = { True for temp_shapes in all_matches_so_far[each_file] if prev_each_shapes[1] == temp_shapes[0] }      
         if len( found_shapes ) == 0:
            # previous image2 shape is not found in current image1
            
            for prev_im2nbr in prev_im2shapes_nbrs[ prev_each_shapes[1] ]:
               if len( prev_im2shapes[ prev_im2nbr ] ) < frth_smallest_pixc:
                  continue
                  
               # one_to_one_m_shapes[prev_im1file + "." + cur_im1file]  -> ('57125', '57529') or [ [image1 shapes], [image2 shapes] ]
               cur_common_nbrs_found = [ temp_shapes for temp_shapes in one_to_one_m_shapes[each_file] \
                                             if ( type( temp_shapes ) is tuple and prev_im2nbr == temp_shapes[0] ) or 
                                             ( type( temp_shapes ) is list and prev_im2nbr in temp_shapes[0] )  ]
               if len( cur_common_nbrs_found ) >= 1:
                  # prev_im2nbr is the common matched neighbor.
                  # missing previous image1 shape is likely to be neighbor to this common matched neighbor
                  # check if possible_prev_im1match is a match with prev_each_shapes[0]
                     
                  # cur_common_nbr_found -> [ ( '5555', '4444' ) ] or [[['49346', '42963'], ['50140']]]
                  #                          [ [['51481', '56319', '49529'], ['57125']], [['56319'], ['57125', '51925']] ]
                  
                  done_possible_im2shapes = []
                  for cur_common_nbr_found in cur_common_nbrs_found:

                     cur_found_matched_im1nbrs = set()
                     cur_found_matched_im2nbrs = set()
                     if type( cur_common_nbr_found ) is tuple:
                        cur_found_matched_im1nbrs.add( cur_common_nbr_found[0] )
                        cur_found_matched_im2nbrs.add( cur_common_nbr_found[1] )
                     elif type( cur_common_nbr_found ) is list:
                        cur_found_matched_im1nbrs |= set( cur_common_nbr_found[0] )
                        cur_found_matched_im2nbrs |= set( cur_common_nbr_found[1] )
                        
                     temp_im1pixels = set()
                     for cur_found_matched_im1nbr in cur_found_matched_im1nbrs:
                        temp_im1pixels |= im1shapes[ cur_found_matched_im1nbr ]

                     temp_im2pixels = set()
                     for cur_found_matched_im2nbr in cur_found_matched_im2nbrs:
                        temp_im2pixels |= im2shapes[ cur_found_matched_im2nbr ]
                     
                     if len( temp_im1pixels ) > ( im_width * im_height ) / 50 or len( temp_im2pixels ) > ( im_width * im_height ) / 50:
                        continue                    
                     
                     cur_fnd_m_im1nbrs_boundaries = pixel_shapes_functions.get_boundary_pixels( temp_im1pixels )                         
                     cur_fnd_m_im2nbrs_boundaries = pixel_shapes_functions.get_boundary_pixels( temp_im2pixels )
                        
                     for cur_found_matched_im2nbr in cur_found_matched_im2nbrs:
                        
                        for possible_im2match in im2shapes_neighbors[ cur_found_matched_im2nbr ]:
                           
                           if len( im2shapes[ possible_im2match ] ) < frth_smallest_pixc or possible_im2match in done_possible_im2shapes:
                              continue
                           
                           done_possible_im2shapes.append( possible_im2match )
                        
                           if im2shapes_colors[ possible_im2match ] != im1shapes_colors[ prev_each_shapes[1] ]:
                              continue

                           size_diff = check_shape_size( prev_each_shapes[1], possible_im2match, im1shapes, im2shapes, size_threshold=1 )
                           if size_diff is True:
                              continue
                           
                           result =   pixel_shapes_functions.check_shape_attached_near( cur_fnd_m_im1nbrs_boundaries, im1shapes_boundaries[ prev_each_shapes[1] ], 
                                                                                        cur_fnd_m_im2nbrs_boundaries, im2shapes_boundaries[possible_im2match], im1.size )

                           if result is not True:
                              continue

                           im1nbr_shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( im1shapes[ prev_each_shapes[1] ], im_width, param_shp_type=1 )  
                           im2nbr_shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( im2shapes[ possible_im2match ], im_width, param_shp_type=1 )  
                     
                           # matching from smaller shape.
                           if len( im1shapes[ prev_each_shapes[1] ] ) > len( im2shapes[ possible_im2match ] ):
                              im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( im1nbr_shp_coord_xy, prev_im1nbr_shp_coord_xy, match_threshold=0.6 )
                           else:
                              im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( prev_im1nbr_shp_coord_xy, im1nbr_shp_coord_xy, match_threshold=0.6 )

                           if im1im2nbr_match is not True:
                              continue     

                           result_shapes[ each_file ].add( ( prev_each_shapes[1], possible_im2match ) )



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



for each_files in result_shapes:
      
   if each_files not in all_matches_so_far.keys():
      all_matches_so_far[ each_files ] = result_shapes[ each_files ]
      
   else:
      for each_shapes in result_shapes[ each_files ]:
         if each_shapes not in all_matches_so_far[ each_files ]:
            all_matches_so_far[ each_files ].add( each_shapes )  



missed_shapes_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/consecutive_missed/data/"
added_missed2_dfile = missed_shapes_ddir + "2.data"
if os.path.exists(added_missed2_dfile):
   with open (added_missed2_dfile, 'rb') as fp:
      added_missed2_shapes = pickle.load(fp)
   fp.close()
   
   for each_files in added_missed2_shapes:
      if each_files in result_shapes.keys():
         for each_shapes in added_missed2_shapes[each_files]:
            if each_shapes not in result_shapes[each_files]:
               result_shapes[each_files].add( each_shapes )
         
      else:
         result_shapes[each_files] = added_missed2_shapes[each_files]   



if os.path.exists(missed_shapes_ddir ) == False:
   os.makedirs(missed_shapes_ddir )

missed_shapes2_dfile = missed_shapes_ddir + "2.data"
with open(missed_shapes2_dfile, 'wb') as fp:
   pickle.dump(result_shapes, fp)
fp.close()

'''
with open(all_matches_so_far_dfile, 'wb') as fp:
   pickle.dump(all_matches_so_far, fp)
fp.close()
'''



















