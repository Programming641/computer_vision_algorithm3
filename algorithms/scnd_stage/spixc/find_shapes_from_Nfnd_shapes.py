
from libraries import  cv_globals, pixel_shapes_functions, pixel_functions, image_functions, same_shapes_functions


from PIL import ImageTk, Image
import os, sys
import pickle
import copy
import math
import shutil

from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files
from libraries.cv_globals import scnd_stg_spixc_dir

directory = "videos/street3/resized/min1"

if len( sys.argv ) >= 2:
   directory = sys.argv[1]

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



shapes_dir = top_shapes_dir + directory  + "shapes/"

sys.setrecursionlimit(5000)


def get_connected_spixc_shapes( spixc_shape, im_shapes_neighbors, nfnd_spixc_shapes, connected_shapes=None ):

   for shape_nbr in im_shapes_neighbors[ spixc_shape ]:
      
      if shape_nbr in nfnd_spixc_shapes:
         
         if connected_shapes is None:
            connected_shapes = set()
            connected_shapes.add( spixc_shape )
            connected_shapes.add( shape_nbr )
            
            get_connected_spixc_shapes( shape_nbr, im_shapes_neighbors, nfnd_spixc_shapes, connected_shapes )
         
         elif shape_nbr in connected_shapes:
            continue
      
         elif shape_nbr not in connected_shapes:
            connected_shapes.add( shape_nbr )
            
            get_connected_spixc_shapes( shape_nbr, im_shapes_neighbors, nfnd_spixc_shapes, connected_shapes )
            

   return connected_shapes




def size_is_too_diff( param_im1shapeid, param_im2shapeid, param_im1shapes, param_im2shapes, size_num=1, len_provided=False ):
   # check if size is too different
   
   if len_provided is False:
      im1shapes_total = len( param_im1shapes[param_im1shapeid] )
      im2shapes_total = len( param_im2shapes[param_im2shapeid] )
   else:
      im1shapes_total = param_im1shapeid
      im2shapes_total = param_im2shapeid
      
   im1_2pixels_diff = abs( im1shapes_total - im2shapes_total )
   if im1_2pixels_diff != 0:
      if im1shapes_total > im2shapes_total:
         if im1_2pixels_diff / im2shapes_total > size_num:
            return True
      else:
         if im1_2pixels_diff / im1shapes_total > size_num:
            return True

   return False     



if "min" in directory:
   min_colors = True
else:
   min_colors = False


result_matches = {}
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
fifth_s_pixc = smallest_pixc = None
for each_files in all_matches_so_far:
   print(each_files)
   
   result_matches[each_files] = []
   
   cur_im1file = each_files.split(".")[0]
   cur_im2file = each_files.split(".")[1]

   im1 = Image.open(top_images_dir + directory + cur_im1file + ".png" )
   if ref_imagefile_op is False:
      im_size = im1.size
      im_width, im_height = im_size
      
      fifth_s_pixc = cv_globals.get_fifth_s_pixc( im_size )
      smallest_pixc = cv_globals.get_smallest_pixc( im_size )
      
      ref_imagefile_op = True

   shapes_dfile = shapes_dir + cur_im1file + "shapes.data"
   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()     

   im2shapes_dfile = shapes_dir + cur_im2file + "shapes.data"
   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
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


   found_im1shapes = set( [ temp_shapes[0] for temp_shapes in all_matches_so_far[ each_files ] ] )
   nfnd_spixc_im1shapes = set()
   for temp_shape in im1shapes:
      if temp_shape not in found_im1shapes and len( im1shapes[ temp_shape ] ) < fifth_s_pixc and len( im1shapes[ temp_shape ] ) >= smallest_pixc:
         nfnd_spixc_im1shapes.add( temp_shape )


   found_im2shapes = set( [ temp_shapes[1] for temp_shapes in all_matches_so_far[ each_files ] ] )
   nfnd_spixc_im2shapes = set()
   for temp_shape in im2shapes:
      if temp_shape not in found_im2shapes and len( im2shapes[ temp_shape ] ) < fifth_s_pixc and len( im2shapes[ temp_shape ] ) >= smallest_pixc:
         nfnd_spixc_im2shapes.add( temp_shape )

   all_connected_spixc_im2shapes = []
   # get connected small pixel count shapes that are not found yet.
   for nfnd_spixc_im2shape in nfnd_spixc_im2shapes:
      connected_spixc_im2shapes = get_connected_spixc_shapes( nfnd_spixc_im2shape, im2shapes_neighbors, nfnd_spixc_im2shapes ) 
      if connected_spixc_im2shapes is not None and connected_spixc_im2shapes not in all_connected_spixc_im2shapes:
         
         temp_pixels = set()
         for connected_spixc_im2shape in connected_spixc_im2shapes:
            temp_pixels |= set( im2shapes[ connected_spixc_im2shape ] )
            
         if len( temp_pixels ) >= fifth_s_pixc:
            all_connected_spixc_im2shapes.append( connected_spixc_im2shapes )
   
   
   im1shapes_already_prcssed = []
   # get connected small pixel count shapes that are not found yet.
   for nfnd_spixc_im1shape in nfnd_spixc_im1shapes:

      # {33569, 29572, ...}
      connected_spixc_im1shapes = get_connected_spixc_shapes( nfnd_spixc_im1shape, im1shapes_neighbors, nfnd_spixc_im1shapes )
         
      if connected_spixc_im1shapes is not None:
         if connected_spixc_im1shapes in im1shapes_already_prcssed:
            continue
         #image_functions.cr_im_from_shapeslist2( cur_im1file, directory, connected_spixc_im1shapes, save_filepath=None , shapes_rgb=(255,0,0) )

         im1shapes_already_prcssed.append( connected_spixc_im1shapes )
         
         
         connected_im1shapes_pixels = set()
         # { pixel index: pixel color } 
         app_im1shapes_pixels = {}
         
         app_im1shapes_nbrs = set()
         for connected_spixc_im1shape in connected_spixc_im1shapes:
            app_im1shapes_nbrs |= set( im1shapes_neighbors[connected_spixc_im1shape] )
            
            for pindex in im1shapes[ connected_spixc_im1shape ]:
               app_im1shapes_pixels[ pindex ] = im1shapes_colors[connected_spixc_im1shape]
               
               xy = pixel_functions.convert_pindex_to_xy( pindex, im_width )
               connected_im1shapes_pixels.add( xy )
         
         if len( connected_im1shapes_pixels ) < fifth_s_pixc:
            continue    
         
         app_im1shapes_nbrs = app_im1shapes_nbrs.difference( connected_spixc_im1shapes )
         
         # [(370, 68), (371, 69), ... ]
         connected_im1shapes_boundaries = pixel_shapes_functions.get_boundary_pixels( connected_im1shapes_pixels )

         # { ( x, y ), ( x, y ), ... }
         vicinity_pixels = pixel_shapes_functions.get_shape_vicinity_pixels( connected_im1shapes_boundaries, 15, im_size, param_shp_type=1 )
         
         for each_connected_spixc_im2shapes in all_connected_spixc_im2shapes:
            
            # { pixel index: pixel color } 
            app_im2shapes_pixels = {}
            
            app_im2shapes_nbrs = set()
            
            cur_con_im2shapes_pixels = set()
            for connected_spixc_im2shape in each_connected_spixc_im2shapes:
               app_im2shapes_nbrs |= set( im2shapes_neighbors[connected_spixc_im2shape] )
               
               for pindex in im2shapes[ connected_spixc_im2shape ]:
                  app_im2shapes_pixels[pindex] = im2shapes_colors[connected_spixc_im2shape]
                  
                  xy = pixel_functions.convert_pindex_to_xy( pindex, im_width )
                  cur_con_im2shapes_pixels.add(xy)
            
            if len( cur_con_im2shapes_pixels ) < fifth_s_pixc:
               continue
            
            app_im2shapes_nbrs = app_im2shapes_nbrs.difference( each_connected_spixc_im2shapes )
            
            within_vicinity = cur_con_im2shapes_pixels.intersection( vicinity_pixels ) 
            if len( within_vicinity ) >= 1:
               # each_connected_spixc_im2shapes is within vicinity with the connected_spixc_im1shapes
               # so check if they are the match                            
                     
               # matching from smaller shape.
               if len( connected_im1shapes_pixels ) > len( cur_con_im2shapes_pixels ):
                  im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it2( app_im2shapes_pixels, app_im1shapes_pixels, im_size, min_colors, match_threshold=0.6 )
               else:
                  im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it2( app_im1shapes_pixels, app_im2shapes_pixels, im_size, min_colors, match_threshold=0.6 )
               if im1im2nbr_match is not True:                  
                  continue                 

               # get common neighbor that app_im1shapes_pixels and app_im2shapes_pixels are attached.
               # neighbor should be the one that connected_im1shapes_pixels are most attached at.
               most_attached_neighbors = None
               most_attached_pixels = None
               
               im1save_filepath = top_shapes_dir + directory + "temp/test1.png"
               #image_functions.cr_im_from_pixels( cur_im1file, directory, connected_im1shapes_pixels, pixels_rgb=(255, 0, 0 ), save_filepath=im1save_filepath )
               
               for app_im1shapes_nbr in app_im1shapes_nbrs:
                  
                  # common_matches can be multiple. app_im1shapes_nbr is a big shape that matched multiple small shapes
                  # multiple small shapes are neighbors of cur_con_im2shapes_pixels
                  common_matches = { temp_match for temp_match in all_matches_so_far[each_files] if temp_match[0] == app_im1shapes_nbr and temp_match[1] in app_im2shapes_nbrs }
                  if len( common_matches ) >= 1:
                     temp_im1nbr_pixels = set()
                     for pindex in im1shapes[app_im1shapes_nbr]:
                        xy = pixel_functions.convert_pindex_to_xy( pindex, im_width )
                        temp_im1nbr_pixels.add(xy)
                     
                     
                     app_im1shapes_nbr_pixels = pixel_shapes_functions.get_only_nbr_pixels( connected_im1shapes_boundaries, connected_im1shapes_pixels, im_size, input_xy=True )
                     app_im1attached_pixels = pixel_shapes_functions.get_attached_pixels( app_im1shapes_nbr_pixels, temp_im1nbr_pixels )  
                      
                     if most_attached_pixels is None or len(app_im1attached_pixels) > len(most_attached_pixels):
                        most_attached_pixels = app_im1attached_pixels
                        most_attached_neighbors = common_matches
               
               #image_functions.cr_im_from_shapeslist2( cur_im1file, directory, [list(most_attached_neighbors)[0][0]], input_im=im1save_filepath , shapes_rgb=(0,255,0) )
               if most_attached_neighbors is None:
                  continue
               
               temp_im2nbr_pixels = set()
               for each_nbr_match in most_attached_neighbors:
                  # ( 222, 333 )
                  for pindex in im2shapes[ each_nbr_match[1] ]:
                     xy = pixel_functions.convert_pindex_to_xy( pindex, im_width )
                     temp_im2nbr_pixels.add(xy)
               
               #image_functions.cr_im_from_pixels( cur_im2file, directory, cur_con_im2shapes_pixels, pixels_rgb=(0, 0, 255 ), save_filepath=im1save_filepath )  
               #image_functions.cr_im_from_pixels( cur_im2file, directory, temp_im2nbr_pixels, pixels_rgb=(0, 255, 0 ), input_im=im1save_filepath )  
               
               conn_im2shapes_boundaries = pixel_shapes_functions.get_boundary_pixels( cur_con_im2shapes_pixels )
               
               app_im2shapes_nbr_pixels = pixel_shapes_functions.get_only_nbr_pixels( conn_im2shapes_boundaries, cur_con_im2shapes_pixels, im_size, input_xy=True )
               app_2m1attached_pixels = pixel_shapes_functions.get_attached_pixels( app_im2shapes_nbr_pixels, temp_im2nbr_pixels )  

               #image_functions.cr_im_from_pixels( cur_im1file, directory, most_attached_pixels, pixels_rgb=(255, 0, 0 ) )
               #image_functions.cr_im_from_pixels( cur_im2file, directory, app_2m1attached_pixels, pixels_rgb=(0, 0, 255 ) )    

               attached_near = pixel_shapes_functions.check_shape_attached_near( connected_im1shapes_boundaries, most_attached_pixels, 
                                                                                 conn_im2shapes_boundaries, app_2m1attached_pixels, im_size )
               if attached_near is False:
                  continue
               
               result_matches[ each_files ].append( [ connected_spixc_im1shapes, each_connected_spixc_im2shapes ] )

               break
         



spixc_ddir = top_shapes_dir + directory + scnd_stg_spixc_dir + "/data/"
if os.path.exists(spixc_ddir ) == False:
   os.makedirs(spixc_ddir )


spixc_dfile = spixc_ddir + "1.data"
if os.path.exists(spixc_dfile):
   with open (spixc_dfile, 'rb') as fp:
      prev_spixc_shapes = pickle.load(fp)
   fp.close()
   
   for each_files in prev_spixc_shapes:
      if each_files in result_matches.keys():
         for each_shapes in prev_spixc_shapes[each_files]:
            if each_shapes not in result_matches[each_files]:
               result_matches[each_files].append( each_shapes )
         
      else:
         result_matches[each_files] = prev_spixc_shapes[each_files]   


with open(spixc_dfile, 'wb') as fp:
   pickle.dump(result_matches, fp)
fp.close()













