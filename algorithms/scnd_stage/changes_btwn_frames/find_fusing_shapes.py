
from libraries import  cv_globals, pixel_shapes_functions, pixel_functions, image_functions, same_shapes_functions


from PIL import ImageTk, Image
import os, sys
import pickle
import copy
import math
import shutil

from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files
from libraries.cv_globals import scnd_stg_ch_btwn_frames_dir, scnd_stg_spixc_dir


directory = "videos/street6/resized/min"
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

shapes_dir = top_shapes_dir + directory  + "shapes/"


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



def find_fusing_shapes( cur_im_shape_num, im_notfnd_shapes , im_shapes , search_im_notfnd_pixch, im_shapes_colors  ):

   if cur_im_shape_num == "im2":
      cur_im_notfnd_shapes = im_notfnd_shapes[1]
      search_im_notfnd_shapes = im_notfnd_shapes[0]
      
      cur_im_shapes = im_shapes[1]
      search_im_shapes = im_shapes[0]
      
      cur_im_shapes_colors = im_shapes_colors[1]
      search_im_shapes_colors = im_shapes_colors[0]
   
   else:
      cur_im_notfnd_shapes = im_notfnd_shapes[0]
      search_im_notfnd_shapes = im_notfnd_shapes[1]
      
      cur_im_shapes = im_shapes[0]
      search_im_shapes = im_shapes[1]
      
      cur_im_shapes_colors = im_shapes_colors[0]
      search_im_shapes_colors = im_shapes_colors[1]


   for cur_im_notfnd_shape in cur_im_notfnd_shapes:
      if len( cur_im_shapes[ cur_im_notfnd_shape ] ) < frth_smallest_pixc:
         continue
         
      # {'20440', '21520', '20982', '19361', ... }
      cur_im_notfnd_pixch_shape = set( cur_im_shapes[ cur_im_notfnd_shape ] ).intersection( search_im_notfnd_pixch )
      
      # get all image1 shapes that are inside or connected to cur_im_notfnd_pixch_shape
      touching_im_shapes = set()
      search_im_notfnd_is_fnd= False
      for search_im_notfnd_shape in search_im_notfnd_shapes:
         
         touching_pixels = set( search_im_shapes[ search_im_notfnd_shape ] ).intersection( cur_im_notfnd_pixch_shape )
         if len( touching_pixels ) >= 1:
            if min_colors is True:
               if search_im_shapes_colors[ search_im_notfnd_shape ] != cur_im_shapes_colors[ cur_im_notfnd_shape ]:
                  continue
            else:
               appear_diff = pixel_functions.compute_appearance_difference(search_im_shapes_colors[ search_im_notfnd_shape ], cur_im_shapes_colors[ cur_im_notfnd_shape ] )
               if appear_diff is True:
                  # different appearance
                  continue
               
            touching_im_shapes.add( search_im_notfnd_shape )
            
            break
         

         for pindex in search_im_shapes[ search_im_notfnd_shape ]:
            # [28137, 28138, 28678, ... ]
            neighbor_pixels = pixel_functions.get_nbr_pixels( pindex, im_size )
            
            neighbor_pixels = { pixel for pixel in neighbor_pixels }
            
            connected_pixels = neighbor_pixels.intersection( cur_im_notfnd_pixch_shape )
            if len( connected_pixels ) >= 1:
               if min_colors is True:
                  if search_im_shapes_colors[ search_im_notfnd_shape ] != cur_im_shapes_colors[ cur_im_notfnd_shape ]:
                     continue
               else:
                  appear_diff = pixel_functions.compute_appearance_difference(search_im_shapes_colors[ search_im_notfnd_shape ], cur_im_shapes_colors[ cur_im_notfnd_shape ] )
                  if appear_diff is True:
                     # different appearance
                     continue
               
               touching_im_shapes.add( search_im_notfnd_shape )
               
               search_im_notfnd_is_fnd = True
               break
   
         if search_im_notfnd_is_fnd is True:
            break
      
      if len( touching_im_shapes ) >= 1:
         #image_functions.cr_im_from_shapeslist2( "2", directory, [cur_im_notfnd_shape], shapes_rgb=(0,255,0) )
         #image_functions.cr_im_from_shapeslist2( "1", directory, touching_im_shapes , shapes_rgb=( 255, 0, 255 ) )
         matched_shapes = set()
         for touching_im_shape in touching_im_shapes:

            search_im_shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( search_im_shapes[ touching_im_shape ], im_width, param_shp_type=0 )  
            cur_im_shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( cur_im_shapes[cur_im_notfnd_shape ] , im_width, param_shp_type=0 )  
                     
            # matching from touching shape.
            im1im2match = same_shapes_functions.match_shape_while_moving_it( search_im_shp_coord_xy, cur_im_shp_coord_xy, match_threshold=0.5 )

            if im1im2match is not True:                  
               continue
            
            matched_shapes.add( touching_im_shape )
         
         matched_pixels = set()
         for matched_shape in matched_shapes:
            matched_pixels |= set( search_im_shapes[ matched_shape ] )
         
         if len( matched_pixels ) / len( cur_im_shapes[ cur_im_notfnd_shape ] ) >= 0.6:
            for matched_shape in matched_shapes:
               if cur_im_shape_num == "im2":
                  result_matches[ each_files ].append( ( matched_shape, cur_im_notfnd_shape ) )
               else:
                  result_matches[ each_files ].append( ( cur_im_notfnd_shape, matched_shape ) )



if "min" in directory:
   min_colors = True
else:
   min_colors = False


result_matches = {}
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
frth_smallest_pixc = None
for each_files in all_matches_so_far:
   print(each_files)

   result_matches[each_files] = []
   
   cur_im1file = each_files.split(".")[0]
   cur_im2file = each_files.split(".")[1]

   if ref_imagefile_op is False:
      im1 = Image.open(top_images_dir + directory + cur_im1file + ".png" )
      im_size = im1.size
      im_width, im_height = im_size
      
      frth_smallest_pixc = cv_globals.get_frth_smallest_pixc( im_size )
      
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


   im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im1file, directory, min_colors=min_colors)
   im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im2file, directory, min_colors=min_colors)

   im1notfnd_shapes = set( im1shapes.keys() ).difference( all_im1found_shapes )
   im2notfnd_shapes = set( im2shapes.keys() ).difference( all_im2found_shapes )


   find_fusing_shapes( "im2", [ im1notfnd_shapes, im2notfnd_shapes ] , [ im1shapes, im2shapes ], im2notfnd_pixch, [ im1shapes_colors, im2shapes_colors ] )
   find_fusing_shapes( "im1", [ im1notfnd_shapes, im2notfnd_shapes ] , [ im1shapes, im2shapes ], im1notfnd_pixch, [ im1shapes_colors, im2shapes_colors ] )                    
   
   

            



ch_btwn_frames_ddir = top_shapes_dir + directory + scnd_stg_ch_btwn_frames_dir + "/data/"
if os.path.exists(ch_btwn_frames_ddir ) == False:
   os.makedirs(ch_btwn_frames_ddir )


ch_btwn_frames_dfile = ch_btwn_frames_ddir + "2.data"

for each_files in result_matches:
   for each_shapes in result_matches[ each_files ]:
      all_matches_so_far[ each_files ].add( each_shapes )



with open(ch_btwn_frames_dfile, 'wb') as fp:
   pickle.dump(result_matches, fp)
fp.close()


with open(all_matches_so_far_dfile, 'wb') as fp:
   pickle.dump(all_matches_so_far, fp)
fp.close()
















