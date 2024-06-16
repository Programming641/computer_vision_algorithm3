
from libraries import  read_files_functions, pixel_shapes_functions, pixel_functions, image_functions, same_shapes_functions


from PIL import ImageTk, Image
import os, sys
import pickle
import copy
import math
import shutil

from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files, frth_smallest_pixc, third_smallest_pixc
from libraries.cv_globals import scnd_stg_ch_btwn_frames_dir, scnd_stg_spixc_dir


directory = "videos/street3/resized/min1"
shapes_type = "intnl_spixcShp"
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
      # {'10.11': {('79935', '58671'), ('39441', '39842'), ('45331', '36516')}, '11.12': {('39842', '40243'), ('26336', '27137'), ... }, ... }
      all_matches_so_far = pickle.load(fp)
   fp.close()

else:
   all_matches_so_far = acrs_all_files_shapes


if shapes_type == "normal":
   print("ERROR. shapes_type normal is not supported")
   sys.exit()

elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"
   
   shapes_dir = s_pixcShp_intnl_dir + "shapes/"


else:
   print("ERROR at " + str( os.path.basename(__file__) ) + " shapes_type " + shapes_type + " is not supported")
   sys.exit()


relpos_nbr_dfile = top_shapes_dir + directory + scnd_stg_all_files + "/relpos_nbr/data/verified3.data"
with open (relpos_nbr_dfile, 'rb') as fp:
   relpos_nbr_shapes = pickle.load(fp)
fp.close()

spixc_dir = top_shapes_dir + directory + scnd_stg_spixc_dir
spixc_shapes_dfile = spixc_dir + "/data/" + "1.data"
with open (spixc_shapes_dfile, 'rb') as fp:
   # { '10.11': [ [ [ im1shapes ], [ im2shapes ] ], ...  ], ... }
   spixc_shapes = pickle.load(fp)
fp.close() 




result_matches = {}
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
for each_files in all_matches_so_far:
   print(each_files)

   result_matches[each_files] = []
   
   cur_im1file = each_files.split(".")[0]
   cur_im2file = each_files.split(".")[1]

   im1 = Image.open(top_images_dir + directory + cur_im1file + ".png" )
   if ref_imagefile_op is False:
      
      im_size = im1.size
      im_width, im_height = im_size
      
      ref_imagefile_op = True

   im1pixels = im1.getdata()
   im2 = Image.open(top_images_dir + directory + cur_im2file + ".png" )
   im2pixels = im2.getdata()


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


   pixch_imdir = top_shapes_dir + directory + "pixch/"
   pixch_data_dir = pixch_imdir + "data/"
   with open (pixch_data_dir  + cur_im1file + "." + cur_im2file + ".data", 'rb') as fp:
      #  { '54665', '65001', '29295', ... }
      pixch = pickle.load(fp)
   fp.close()

   all_im1found_shapes = set()
   all_im2found_shapes = set()
   for each_shapes in all_matches_so_far[ each_files ]:
      all_im1found_shapes.add( each_shapes[0] )
      all_im2found_shapes.add( each_shapes[1] )
   
   for each_shapes in relpos_nbr_shapes[ each_files ]:
      all_im1found_shapes |= set( each_shapes[0] )
      all_im2found_shapes |= set( each_shapes[1] )
   
   for each_shapes in spixc_shapes[ each_files ]:
      all_im1found_shapes |= set( each_shapes[0] )
      all_im2found_shapes |= set( each_shapes[1] )
 
   im1found_pixch = set()
   im2found_pixch = set()
   
   for each_im1shapeid in all_im1found_shapes:
      found_pixch = set( im1shapes[ each_im1shapeid ] ).intersection( pixch )
      im1found_pixch |= found_pixch
   for each_im2shapeid in all_im2found_shapes:
      found_pixch = set( im2shapes[ each_im2shapeid ] ).intersection( pixch )
      im2found_pixch |= found_pixch
   
   im1notfnd_pixch = pixch.difference( im1found_pixch )
   im2notfnd_pixch = pixch.difference( im2found_pixch )
   
   #image_functions.cr_im_from_pixels( "1", directory, im1notfnd_pixch )
   #image_functions.cr_im_from_pixels( "2", directory, im2notfnd_pixch )

   im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im1file, directory, shapes_type=shapes_type, min_colors=True)
   im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im2file, directory, shapes_type=shapes_type, min_colors=True)

   im1shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + cur_im1file + "_shape_nbrs.txt"
   im2shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + cur_im2file + "_shape_nbrs.txt"

   im1shapes_neighbors = read_files_functions.rd_dict_k_v_l(cur_im1file, directory, im1shape_neighbors_file)
   im2shapes_neighbors = read_files_functions.rd_dict_k_v_l(cur_im2file, directory, im2shape_neighbors_file)   

   im1notfnd_shapes = set( im1shapes.keys() ).difference( all_im1found_shapes )
   im2notfnd_shapes = set( im2shapes.keys() ).difference( all_im2found_shapes )                 
   
   
   # get most pixel changed shapes
   im1notfnd_mostpixch_shapes = set()
   im2notfnd_mostpixch_shapes = set()
   
   for im1notfnd_shape in im1notfnd_shapes:
      shape_pixch = set( im1shapes[ im1notfnd_shape ] ).intersection( im1notfnd_pixch )
      
      if len( shape_pixch ) / len( im1shapes[ im1notfnd_shape ] ) >= 0.5:
         im1notfnd_mostpixch_shapes.add( im1notfnd_shape )

   for im2notfnd_shape in im2notfnd_shapes:
      shape_pixch = set( im2shapes[ im2notfnd_shape ] ).intersection( im2notfnd_pixch )
      
      if len( shape_pixch ) / len( im2shapes[ im2notfnd_shape ] ) >= 0.5:
         im2notfnd_mostpixch_shapes.add( im2notfnd_shape )
   
   im1connected_shapes = []
   done_shapes = set()
   for im1notfnd_mostpixch_shape in im1notfnd_mostpixch_shapes:
      if im1notfnd_mostpixch_shape in done_shapes:
         continue
      connected_mostpixch_shapes = pixel_shapes_functions.get_connected_shapes( im1notfnd_mostpixch_shape, im1shapes_neighbors, im1notfnd_mostpixch_shapes )
      
      if connected_mostpixch_shapes is not None:
         #image_functions.cr_im_from_shapeslist2( "1", directory, connected_mostpixch_shapes, shapes_rgb=(0, 255, 0 ) )
         im1connected_shapes.append( connected_mostpixch_shapes )
         done_shapes |= connected_mostpixch_shapes
         

   im2connected_shapes = []
   done_shapes = set()
   for im2notfnd_mostpixch_shape in im2notfnd_mostpixch_shapes:
      if im2notfnd_mostpixch_shape in done_shapes:
         continue
      connected_mostpixch_shapes = pixel_shapes_functions.get_connected_shapes( im2notfnd_mostpixch_shape, im2shapes_neighbors, im2notfnd_mostpixch_shapes )
      
      if connected_mostpixch_shapes is not None:
         #image_functions.cr_im_from_shapeslist2( "2", directory, connected_mostpixch_shapes, shapes_rgb=(0, 255, 0 ) )
         im2connected_shapes.append( connected_mostpixch_shapes )
         done_shapes |= connected_mostpixch_shapes         
         
   
   for each_im1connected_shapes in im1connected_shapes:
      cur_im1connected_pixels = set()

      #image_functions.cr_im_from_shapeslist2( "1", directory, each_im1connected_shapes, shapes_rgb=(0, 255, 0 ) )
      
      for im1connected_shape in each_im1connected_shapes:
         cur_im1connected_pixels |= set( im1shapes[ im1connected_shape ] )
      
      if len( cur_im1connected_pixels ) < frth_smallest_pixc:
         continue
      
      for each_im2connected_shapes in im2connected_shapes:
         cur_im2connected_pixels = set()
         
         for im2connected_shape in each_im2connected_shapes:
            cur_im2connected_pixels |= set( im2shapes[ im2connected_shape ] )
         
         if len( cur_im2connected_pixels ) < frth_smallest_pixc:
            continue
         
         same_location_pixels = cur_im1connected_pixels.intersection( cur_im2connected_pixels )
         if len( same_location_pixels ) >= 1:
            
            #image_functions.cr_im_from_shapeslist2( "2", directory, each_im2connected_shapes, shapes_rgb=(0, 255, 0 ) )
            
            # { xy in string: shape color }
            all_im1shapes_pix = {}
         
            # [ ( x,y ), (x,y), ... ]
            im1shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( cur_im1connected_pixels, im_width, param_shp_type=0 )
            for xy in im1shp_coord_xy:
               # xy_str is start coordinate (0,0) xy.
               xy_str = str( xy[0] ) + "." + str( xy[1] )
            
               pindex = pixel_functions.convert_xy_to_pindex( xy, im_width )
               # xy_str with source pixel color
               all_im1shapes_pix[ xy_str ] = im1pixels[ pindex ]                
            

            # { xy in string: shape color }
            all_im2shapes_pix = {}
         
            # [ ( x,y ), (x,y), ... ]
            im2shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( cur_im2connected_pixels, im_width, param_shp_type=0 )
            for xy in im2shp_coord_xy:
               # xy_str is start coordinate (0,0) xy.
               xy_str = str( xy[0] ) + "." + str( xy[1] )
            
               pindex = pixel_functions.convert_xy_to_pindex( xy, im_width )
               # xy_str with source pixel color
               all_im2shapes_pix[ xy_str ] = im2pixels[ pindex ]         
   

            # matching from smaller shape.
            if len( cur_im1connected_pixels ) > len( cur_im2connected_pixels ):
               im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it2( all_im2shapes_pix, all_im1shapes_pix, im_size, match_threshold=0.55 )
            else:
               im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it2( all_im1shapes_pix, all_im2shapes_pix, im_size, match_threshold=0.55 )
            if im1im2nbr_match[0] is not True:                  
               continue       


            result_matches[ each_files ].append( [ each_im1connected_shapes, each_im2connected_shapes ] )




ch_btwn_frames_ddir = top_shapes_dir + directory + scnd_stg_ch_btwn_frames_dir + "/data/"
if os.path.exists(ch_btwn_frames_ddir ) == False:
   os.makedirs(ch_btwn_frames_ddir )


ch_btwn_frames_dfile = ch_btwn_frames_ddir + "3.data"
with open(ch_btwn_frames_dfile, 'wb') as fp:
   pickle.dump(result_matches, fp)
fp.close()

'''
with open(all_matches_so_far_dfile, 'wb') as fp:
   pickle.dump(all_matches_so_far, fp)
fp.close()
'''















