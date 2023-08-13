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
partially_matched_shapes = {}

prev_file_shapes = None
prev_filename = None
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
for each_file in all_matches_so_far:
   print( each_file )
   
   result_shapes[ each_file ] = set()
   partially_matched_shapes[ each_file ] = set()
   
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
         done_im1_each_shapes.append( each_shapes[0] )
         
         
         found_shapes = { True for temp_shapes in prev_file_shapes if each_shapes[0] == temp_shapes[1] }      
         if len( found_shapes ) == 0:
            # current image1 shape not found in previous image2 shape. so find it by common matched neighbor.
            
            for cur_im1nbr in im1shapes_neighbors[ each_shapes[0] ]:
               if len( im1shapes[ cur_im1nbr ] ) < frth_smallest_pixc:
                  continue
                  
               # one_to_one_m_shapes[prev_filename]  -> ('57125', '57529') or [ [image1 shapes], [image2 shapes] ]
               prev_common_nbrs_found = [ temp_shapes for temp_shapes in one_to_one_m_shapes[prev_filename] \
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
                     
                     im1shape_average_pix = pixel_shapes_functions.get_shape_average_pixel( temp_im1pixels , im_width, pixel_xy=True )
                     # rounding to whole number
                     im1shape_average_pix = ( round( im1shape_average_pix[0] ), round( im1shape_average_pix[1] ) )
                     im2shape_average_pix = pixel_shapes_functions.get_shape_average_pixel( temp_im2pixels , im_width, pixel_xy=True )
                     im2shape_average_pix = ( round( im2shape_average_pix[0] ), round( im2shape_average_pix[1] ) )  


                     debug_pixels = set()
         
                     prev_im1shapes_in_relpos = {}
                     for prev_im2nfnd_shape_pix in prev_im2shapes[each_shapes[0]]:
               
                        diff_x = prev_im2nfnd_shape_pix[0] - im2shape_average_pix[0]
                        diff_y = prev_im2nfnd_shape_pix[1] - im2shape_average_pix[1]
               
                        relpos_pix = ( im1shape_average_pix[0] + diff_x, im1shape_average_pix[1] + diff_y )

                        if relpos_pix[0] >= im_width or relpos_pix[0] < 0:
                           # pixel out of image range
                           continue
                        if relpos_pix[1] < 0 or relpos_pix[1] >= im_height:
                           continue
            
                        debug_pixels.add( relpos_pix )
                        pindex = pixel_functions.convert_xy_to_pindex( relpos_pix, im_width )
            
                        if prev_im1shapes_by_pindex[str(pindex)] in prev_im1shapes_in_relpos.keys():
                           prev_im1shapes_in_relpos[ prev_im1shapes_by_pindex[str(pindex)] ] += 1
                        else:
                           prev_im1shapes_in_relpos[ prev_im1shapes_by_pindex[str(pindex)] ] = 1

                        #save_filepath = top_shapes_dir + directory + scnd_stg_all_files + "/relpos_nbr/temp/temp.png"
                        #image_functions.cr_im_from_pixels( cur_im2file, directory, debug_pixels, save_filepath=save_filepath , pixels_rgb=None )

                     partially_matched_prev_im1shapes = set()
                     partially_matched_prev_im1shapes_len = 0
                     
                     for prev_im1shapeid in prev_im1shapes_in_relpos:
                        if prev_im2shapes_clrs[ each_shapes[0] ] != prev_im1shapes_clrs[ prev_im1shapeid ] or len( prev_im1shapes[ prev_im1shapeid ] ) < frth_smallest_pixc:
                           continue
                        
                        size_diff = check_shape_size( each_shapes[0], prev_im1shapeid, prev_im2shapes, prev_im1shapes, size_threshold=5 )
                        if size_diff is True:
                           # size is too different
                           continue        
            
                        #image_functions.cr_im_from_shapeslist2( cur_im2file, directory,  [ prev_im1shapeid ], save_filepath=None , shapes_rgb=None, input_im=save_filepath )
            
                        if prev_im1shapes_in_relpos[prev_im1shapeid] > len( prev_im1shapes[prev_im1shapeid] ) * 0.2:
                           # partially matched shape
                           partially_matched_prev_im1shapes.add( prev_im1shapeid )
                           partially_matched_prev_im1shapes_len += prev_im1shapes_in_relpos[prev_im1shapeid]
                  
                     if partially_matched_prev_im1shapes_len / len( prev_im2shapes[each_shapes[0]] ) >= 0.6:
                        for partially_m_prev_im1shapeid in partially_matched_prev_im1shapes:
                              result_shapes[prev_filename].add( (partially_m_prev_im1shapeid, each_shapes[0]) )
                     
                     
                     if partially_matched_prev_im1shapes_len / len( prev_im2shapes[each_shapes[0]] ) >= 0.4:
                        for partially_m_prev_im1shapeid in partially_matched_prev_im1shapes:
                              partially_matched_shapes[prev_filename].add( (partially_m_prev_im1shapeid, each_shapes[0]) )


                    
                     
                     for prev_found_matched_im1nbr in prev_found_matched_im1nbrs:
                        
                        for possible_prev_im1match in prev_im1shapes_nbrs[ prev_found_matched_im1nbr ]:

                           
                           if len( prev_im1shapes[ possible_prev_im1match ] ) < frth_smallest_pixc or possible_prev_im1match in done_possible_pre_im1shapes:
                              continue
                           
                           done_possible_pre_im1shapes.append( possible_prev_im1match )
                           
                           debug_pixels = set()
         
                           prev_im2shapes_in_relpos = {}
                           for im1not_found_shape_pix in prev_im1shapes[possible_prev_im1match]:
               
                              diff_x = im1not_found_shape_pix[0] - im1shape_average_pix[0]
                              diff_y = im1not_found_shape_pix[1] - im1shape_average_pix[1]
               
                              relpos_pix = ( im2shape_average_pix[0] + diff_x, im2shape_average_pix[1] + diff_y )

                              if relpos_pix[0] >= im_width or relpos_pix[0] < 0:
                                 # pixel out of image range
                                 continue
                              if relpos_pix[1] < 0 or relpos_pix[1] >= im_height:
                                 continue
            
                              debug_pixels.add( relpos_pix )
                              pindex = pixel_functions.convert_xy_to_pindex( relpos_pix, im_width )
            
                              if prev_im2shapes_by_pindex[str(pindex)] in prev_im2shapes_in_relpos.keys():
                                 prev_im2shapes_in_relpos[ prev_im2shapes_by_pindex[str(pindex)] ] += 1
                              else:
                                 prev_im2shapes_in_relpos[ prev_im2shapes_by_pindex[str(pindex)] ] = 1

                              #save_filepath = top_shapes_dir + directory + scnd_stg_all_files + "/relpos_nbr/temp/temp.png"
                              #image_functions.cr_im_from_pixels( cur_im2file, directory, debug_pixels, save_filepath=save_filepath , pixels_rgb=None )


                           for prev_im2shapeid in prev_im2shapes_in_relpos:
                              if prev_im1shapes_clrs[ possible_prev_im1match ] != prev_im2shapes_clrs[ prev_im2shapeid ] or len( prev_im2shapes[ prev_im2shapeid ] ) < frth_smallest_pixc:
                                 continue
            
                              size_diff = check_shape_size( possible_prev_im1match, prev_im2shapeid, prev_im1shapes, prev_im2shapes, size_threshold=2.5 )
                              if size_diff is True:
                                 # size is too different
                                 continue        
            
                              #image_functions.cr_im_from_shapeslist2( cur_im2file, directory,  [ prev_im2shapeid ], save_filepath=None , shapes_rgb=None, input_im=save_filepath )
            
                              if prev_im2shapes_in_relpos[prev_im2shapeid] > len( prev_im2shapes[prev_im2shapeid] ) * 0.6:
                                 result_shapes[prev_filename].add( (possible_prev_im1match, prev_im2shapeid) )
                  
                              elif prev_im2shapes_in_relpos[prev_im2shapeid] > len( prev_im1shapes[possible_prev_im1match] ) * 0.6:
                                 result_shapes[prev_filename].add( (possible_prev_im1match, prev_im2shapeid) )


      for prev_each_shapes in prev_file_shapes:
      
         found_shapes = { True for temp_shapes in all_matches_so_far[each_file] if prev_each_shapes[1] == temp_shapes[0] }      
         if len( found_shapes ) == 0:
            # previous image2 shape is not found in current image1
            
            for prev_im2nbr in prev_im2shapes_nbrs[ prev_each_shapes[1] ]:
               if len( prev_im2shapes[ prev_im2nbr ] ) < frth_smallest_pixc:
                  continue
                  
               # one_to_one_m_shapes[prev_filename]  -> ('57125', '57529') or [ [image1 shapes], [image2 shapes] ]
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
                     
                     im1shape_average_pix = pixel_shapes_functions.get_shape_average_pixel( temp_im1pixels , im_width, pixel_xy=True )
                     # rounding to whole number
                     im1shape_average_pix = ( round( im1shape_average_pix[0] ), round( im1shape_average_pix[1] ) )
                     im2shape_average_pix = pixel_shapes_functions.get_shape_average_pixel( temp_im2pixels , im_width, pixel_xy=True )
                     im2shape_average_pix = ( round( im2shape_average_pix[0] ), round( im2shape_average_pix[1] ) )  


                     debug_pixels = set()
         
                     cur_im2shapes_in_relpos = {}
                     for prev_im2nfnd_shape_pix in prev_im2shapes[prev_each_shapes[1]]:
               
                        diff_x = prev_im2nfnd_shape_pix[0] - im1shape_average_pix[0]
                        diff_y = prev_im2nfnd_shape_pix[1] - im1shape_average_pix[1]
               
                        relpos_pix = ( im2shape_average_pix[0] + diff_x, im2shape_average_pix[1] + diff_y )

                        if relpos_pix[0] >= im_width or relpos_pix[0] < 0:
                           # pixel out of image range
                           continue
                        if relpos_pix[1] < 0 or relpos_pix[1] >= im_height:
                           continue
            
                        debug_pixels.add( relpos_pix )
                        pindex = pixel_functions.convert_xy_to_pindex( relpos_pix, im_width )
            
                        if im2shapes_by_pindex[str(pindex)] in cur_im2shapes_in_relpos.keys():
                           cur_im2shapes_in_relpos[ im2shapes_by_pindex[str(pindex)] ] += 1
                        else:
                           cur_im2shapes_in_relpos[ im2shapes_by_pindex[str(pindex)] ] = 1

                        #save_filepath = top_shapes_dir + directory + scnd_stg_all_files + "/relpos_nbr/temp/temp.png"
                        #image_functions.cr_im_from_pixels( cur_im2file, directory, debug_pixels, save_filepath=save_filepath , pixels_rgb=None )

                     partially_matched_im2shapes = set()
                     partially_matched_im2shapes_len = 0
                     
                     for cur_im2shapeid in cur_im2shapes_in_relpos:
                        if im1shapes_colors[ prev_each_shapes[1] ] != im2shapes_colors[ cur_im2shapeid ] or len( im2shapes[ cur_im2shapeid ] ) < frth_smallest_pixc:
                           continue
                        
                        size_diff = check_shape_size( prev_each_shapes[1], cur_im2shapeid, im1shapes, im2shapes, size_threshold=5 )
                        if size_diff is True:
                           # size is too different
                           continue        
            
                        #image_functions.cr_im_from_shapeslist2( cur_im2file, directory,  [ cur_im2shapeid ], save_filepath=None , shapes_rgb=None, input_im=save_filepath )
            
                        if cur_im2shapes_in_relpos[cur_im2shapeid] > len( im2shapes[cur_im2shapeid] ) * 0.2:
                           # partially matched shape
                           partially_matched_im2shapes.add( cur_im2shapeid )
                           partially_matched_im2shapes_len += cur_im2shapes_in_relpos[cur_im2shapeid]
                  
                     if partially_matched_im2shapes_len / len( im1shapes[prev_each_shapes[1]] ) >= 0.6:
                        for partially_m_im2shapeid in partially_matched_im2shapes:
                              result_shapes[each_file].add( (prev_each_shapes[1], partially_m_im2shapeid ) )
                     
                     
                     if partially_matched_im2shapes_len / len( im1shapes[prev_each_shapes[1]] ) >= 0.4:
                        for partially_m_im2shapeid in partially_matched_im2shapes:
                              partially_matched_shapes[each_file].add( (prev_each_shapes[1], partially_m_im2shapeid ) )


                     
                     
                     for cur_found_matched_im2nbr in cur_found_matched_im2nbrs:
                        
                        for possible_im2match in im2shapes_neighbors[ cur_found_matched_im2nbr ]:
                           
                           if len( im2shapes[ possible_im2match ] ) < frth_smallest_pixc or possible_im2match in done_possible_im2shapes:
                              continue
                           
                           done_possible_im2shapes.append( possible_im2match )
                           
                           debug_pixels = set()
         
                           im1shapes_in_relpos = {}
                           for possible_im2match_pix in im2shapes[possible_im2match]:
               
                              diff_x = possible_im2match_pix[0] - im2shape_average_pix[0]
                              diff_y = possible_im2match_pix[1] - im2shape_average_pix[1]
               
                              relpos_pix = ( im1shape_average_pix[0] + diff_x, im1shape_average_pix[1] + diff_y )

                              if relpos_pix[0] >= im_width or relpos_pix[0] < 0:
                                 # pixel out of image range
                                 continue
                              if relpos_pix[1] < 0 or relpos_pix[1] >= im_height:
                                 continue
            
                              debug_pixels.add( relpos_pix )
                              pindex = pixel_functions.convert_xy_to_pindex( relpos_pix, im_width )
            
                              if im1shapes_by_pindex[str(pindex)] in im1shapes_in_relpos.keys():
                                 im1shapes_in_relpos[ im1shapes_by_pindex[str(pindex)] ] += 1
                              else:
                                 im1shapes_in_relpos[ im1shapes_by_pindex[str(pindex)] ] = 1

                              #save_filepath = top_shapes_dir + directory + scnd_stg_all_files + "/relpos_nbr/temp/temp.png"
                              #image_functions.cr_im_from_pixels( cur_im2file, directory, debug_pixels, save_filepath=save_filepath , pixels_rgb=None )


                           for im1shapeid in im1shapes_in_relpos:
                              if im2shapes_colors[ possible_im2match ] != im1shapes_colors[ im1shapeid ] or len( im1shapes[ im1shapeid ] ) < frth_smallest_pixc:
                                 continue
            
                              size_diff = check_shape_size( possible_im2match, im1shapeid, im2shapes, im1shapes, size_threshold=2.5 )
                              if size_diff is True:
                                 # size is too different
                                 continue        
           
                              #image_functions.cr_im_from_shapeslist2( cur_im2file, directory,  [ im1shapeid ], save_filepath=None , shapes_rgb=None, input_im=save_filepath )
            
                              if im1shapes_in_relpos[im1shapeid] > len( im1shapes[im1shapeid] ) * 0.6:
                                 result_shapes[each_file].add( (im1shapeid, possible_im2match) )
                  
                              elif im1shapes_in_relpos[im1shapeid] > len( im2shapes[possible_im2match] ) * 0.6:
                                 result_shapes[each_file].add( (im1shapeid, possible_im2match) )
      


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

for each_files in partially_matched_shapes:
      
   if each_files not in all_matches_so_far.keys():
      all_matches_so_far[ each_files ] = partially_matched_shapes[ each_files ]
      
   else:
      for each_shapes in partially_matched_shapes[ each_files ]:
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


partially_matched_dfile = missed_shapes_ddir + "partially_matched.data"
if os.path.exists(partially_matched_dfile):
   with open (partially_matched_dfile, 'rb') as fp:
      partially_m_shapes = pickle.load(fp)
   fp.close()
   
   for each_files in partially_m_shapes:
      if each_files in partially_matched_shapes.keys():
         for each_shapes in partially_m_shapes[each_files]:
            if each_shapes not in partially_matched_shapes[each_files]:
               partially_matched_shapes[each_files].add( each_shapes )
         
      else:
         partially_matched_shapes[each_files] = partially_m_shapes[each_files]   


if os.path.exists(missed_shapes_ddir ) == False:
   os.makedirs(missed_shapes_ddir )

missed_shapes2_dfile = missed_shapes_ddir + "2.data"
with open(missed_shapes2_dfile, 'wb') as fp:
   pickle.dump(result_shapes, fp)
fp.close()

with open(partially_matched_dfile, 'wb') as fp:
   pickle.dump(partially_matched_shapes, fp)
fp.close()

with open(all_matches_so_far_dfile, 'wb') as fp:
   pickle.dump(all_matches_so_far, fp)
fp.close()




















