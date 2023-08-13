from libraries import pixel_functions, read_files_functions, pixel_shapes_functions, image_functions, same_shapes_functions

from PIL import Image
import math
import os, sys
import winsound, time
import pickle

from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, frth_smallest_pixc



im1file = '14'
im2file = "15"
shapes_type = "intnl_spixcShp"
directory = "videos/street3/resized/min"

if len(sys.argv) > 1:
   im1file = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   im2file = sys.argv[1][0: len( sys.argv[1] ) - 4 ]
   directory = sys.argv[3]
   
   shapes_type = "intnl_spixcShp"

   print("execute script algorithms/pixch/most_ch_shapes_frm_whichShp_in_prev_frm.py. file1 " + im1file + " file2 " + im2file + " directory " + directory )



# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

pixch_ddir = top_shapes_dir + directory + "pixch/data/"
pixch_shapes_file = pixch_ddir + im1file + "." + im2file + "." + im2file + "most_ch.data"
with open (pixch_shapes_file, 'rb') as fp:
   # ['23', '52', '56', ... ]
   # [ most pixels changed shapes ]
   im2pixch_shapes = pickle.load(fp)
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
   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()


   im2shapes_dfile = shapes_dir + im2file + "shapes.data"   
   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()

   for shapeid in im2shapes:
      pixels = []
      
      for pindex in im2shapes[shapeid]:
         xy = pixel_functions.convert_pindex_to_xy( pindex, im_width )
         
         pixels.append( xy )
      
      im2shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels(pixels)
      im2shapes[shapeid] = pixels


   im1shape_neighbors_filepath = s_pixcShp_intnl_dir + "shape_nbrs/" + im1file + "_shape_nbrs.txt"
   im2shape_neighbors_filepath = s_pixcShp_intnl_dir + "shape_nbrs/" + im2file + "_shape_nbrs.txt"


im1shapes_neighbors = read_files_functions.rd_dict_k_v_l(im1file, directory, im1shape_neighbors_filepath)
im2shapes_neighbors = read_files_functions.rd_dict_k_v_l(im2file, directory, im2shape_neighbors_filepath)

im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im1file, directory, shapes_type=shapes_type)
im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im2file, directory, shapes_type=shapes_type)

im1shape_by_pindex = {}
for im1shapeid in im1shapes:
   for im1pindex in im1shapes[im1shapeid]:
      im1shape_by_pindex[im1pindex] = im1shapeid


for shapeid in im1shapes:
   pixels = []
   for pindex in im1shapes[shapeid]:
      xy = pixel_functions.convert_pindex_to_xy( pindex, im_width )
         
      pixels.append( xy )
      
   im1shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels(pixels)
   im1shapes[shapeid] = pixels


im1shapes_in_shp_coord = {}
for shapeid in im1shapes:
   if len( im1shapes[shapeid] ) < frth_smallest_pixc:
      continue
   
   im1shapes_in_shp_coord[shapeid] = pixel_shapes_functions.get_shape_pos_in_shp_coord( im1shapes[shapeid], im_width, param_shp_type=1 )


all_shapes_matches = []

progress_counter = len( im2pixch_shapes )
for im2pixch_shape in im2pixch_shapes:
   print( str( progress_counter ) + " remaining")
   progress_counter -= 1


   if len( im2shapes[im2pixch_shape] ) < frth_smallest_pixc:
      continue
   
   im2vicinity_pixels = pixel_shapes_functions.get_shape_vicinity_pixels( im2shapes_boundaries[im2pixch_shape], 15, original_image.size, 1 )

   # get image1 shapes that are in the im2vicinity_pixels
   im1shapes_in_vicinity = set()
   for im2vicinity_pixel in im2vicinity_pixels:
      im2pindex = pixel_functions.convert_xy_to_pindex( im2vicinity_pixel, im_width )
      im1shapes_in_vicinity.add( im1shape_by_pindex[str(im2pindex)] )

   
   im2shape_in_shp_coord = pixel_shapes_functions.get_shape_pos_in_shp_coord( im2shapes[im2pixch_shape], im_width, param_shp_type=1 )
   

   for im2pixch_neighbor in im2shapes_neighbors[im2pixch_shape]:
      if len( im2shapes[im2pixch_neighbor] ) < frth_smallest_pixc:
         continue
      
      im2shape_nbr_in_shp_coord = pixel_shapes_functions.get_shape_pos_in_shp_coord( im2shapes[im2pixch_neighbor], im_width, param_shp_type=1 )
      
      matched_im1shape = None
      # already_processed_mtch_im1nbrs will contain matched_im1nbrs that failed check_shape_attached_near.
      already_processed_mtch_im1nbrs = []
      for im1shape_in_vicinity in im1shapes_in_vicinity:
         if len( im1shapes[im1shape_in_vicinity] ) < frth_smallest_pixc:
            continue 

         # before checking shape neighbors for match, check if it can match with any of the vicinity image1 shapes
         if matched_im1shape is None:
            if im2shapes_colors[im2pixch_shape] == im1shapes_colors[im1shape_in_vicinity]:
               im2shape_match = same_shapes_functions.match_shape_while_moving_it( im2shape_in_shp_coord, im1shapes_in_shp_coord[im1shape_in_vicinity] )
               if im2shape_match is True:
                  matched_im1shape = im1shape_in_vicinity
                  continue
         else:
            matched_im1nbrs = set()
            attached_near = False
            matched_im1nbr = None
            
            for im1s_nbr_in_vicinity in im1shapes_in_vicinity:
               if im1s_nbr_in_vicinity == matched_im1shape or len( im1shapes[im1s_nbr_in_vicinity] ) < frth_smallest_pixc or \
                  im1s_nbr_in_vicinity not in im1shapes_neighbors[matched_im1shape]:
                  continue
                  
               if im2shapes_colors[im2pixch_neighbor] == im1shapes_colors[im1s_nbr_in_vicinity]:
                  nbr_temp_match = same_shapes_functions.match_shape_while_moving_it( im2shape_nbr_in_shp_coord, im1shapes_in_shp_coord[im1s_nbr_in_vicinity] )
                  nbr_temp2_match = same_shapes_functions.match_shape_while_moving_it( im1shapes_in_shp_coord[im1s_nbr_in_vicinity], im2shape_nbr_in_shp_coord )
                  if nbr_temp_match is True and nbr_temp2_match is True:
                     matched_im1nbrs.add( im1s_nbr_in_vicinity )
            

                  for _matched_im1nbr in matched_im1nbrs:
                     if _matched_im1nbr in already_processed_mtch_im1nbrs:
                        continue
                  
                     already_processed_mtch_im1nbrs.append( _matched_im1nbr )
                     # check if shapes are attached to im2pixch_shape close to each other.
                     _attached_near = pixel_shapes_functions.check_shape_attached_near( im2shapes_boundaries[im2pixch_shape], im2shapes_boundaries[im2pixch_neighbor],
                                                                                     im1shapes_boundaries[matched_im1shape], im1shapes_boundaries[_matched_im1nbr],
                                                                                     original_image.size )
               
                     if _attached_near is True:
                     
                        matched_im1nbr = _matched_im1nbr
                        attached_near = True
                        break
                  if attached_near is True:
                     break
                     
            if attached_near is not True:
               matched_im1shape = None
         
      
         if matched_im1shape is not None and attached_near is True:
            # match found but check if pixel size are not too different
            im1shapes_total = len( im1shapes[matched_im1shape] )
            im2shapes_total = len( im2shapes[im2pixch_shape] )
      
            im1_2pixels_diff = abs( im1shapes_total - im2shapes_total )
            if im1shapes_total > im2shapes_total:
               if im1_2pixels_diff / im2shapes_total > 1:
                 continue
            else:
               if im1_2pixels_diff / im1shapes_total > 1:
                  continue    
         
            all_shapes_matches.append( [ [matched_im1shape, matched_im1nbr], [im2pixch_shape, im2pixch_neighbor] ] )
            #image_functions.cr_im_from_shapeslist2( im2file, directory, [im2pixch_shape, im2pixch_neighbor], save_filepath=None , shapes_rgb=(255,0,0) )
            #image_functions.cr_im_from_shapeslist2( im1file, directory, [matched_im1shape, matched_im1nbr], save_filepath=None , shapes_rgb=(0,0,255) )


changed_shapes_dir = top_shapes_dir + directory + "pixch/ch_shapes/ch_from/"
if os.path.exists(changed_shapes_dir ) == False:
   os.makedirs(changed_shapes_dir )
changed_shapes_ddir = changed_shapes_dir + "data/"
if os.path.exists(changed_shapes_ddir ) == False:
   os.makedirs(changed_shapes_ddir )



with open(changed_shapes_ddir + im1file + "." + im2file + "." + im2file + ".data", 'wb') as fp:
   pickle.dump(all_shapes_matches, fp)
fp.close()


































