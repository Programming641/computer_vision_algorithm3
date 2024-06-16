
from libraries import  cv_globals, pixel_shapes_functions, pixel_functions, image_functions, same_shapes_functions


from PIL import ImageTk, Image
import os, sys
import pickle
import copy
import math
import shutil

from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files
from libraries.cv_globals import scnd_stg_ch_btwn_frames_dir, pixch_sty_dir


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
   sys.exit(1)

elif shapes_type == "intnl_spixcShp":

   shapes_dir = top_shapes_dir + directory + "shapes/"


else:
   print("ERROR at " + str( os.path.basename(__file__) ) + " shapes_type " + shapes_type + " is not supported")
   sys.exit(1)

shapes_m_types_dir = top_shapes_dir + directory + scnd_stg_all_files + "/shp_match_types/"
one_to_one_matched_dfile = shapes_m_types_dir + "data/matched_pixels.data"
with open (one_to_one_matched_dfile, 'rb') as fp:
      # image file num: [ ('57125', '57529'), ... ]
      # or 
      # image file num: [ [ [ [image1 shapes], [image2 shapes] ] ], ... ]
   one_to_one_m_shapes = pickle.load(fp)
fp.close()



def find_separating_shapes( im_shapes, im_shape_num, search_im_shapes ):
   if im_shape_num == "im2":
      # 0 is im1, 1 is im2
      im_shape_num = 1
      search_in_im_num = 0
      
   elif im_shape_num == "im1":
      im_shape_num = 0
      search_in_im_num = 1


   for im_shapeid in im_shapes:
      if len( im_shapes[im_shapeid] ) < frth_smallest_pixc:
         continue

      pixch_in_im_shape = set( im_shapes[im_shapeid] ).intersection( pixch )      
      cur_im_shape_wo_pixch = set( im_shapes[im_shapeid] ).difference( pixch_in_im_shape )
      
      if len( pixch_in_im_shape ) > len( cur_im_shape_wo_pixch ):
         continue
      
      check_not_found = [ temp_shapes for temp_shapes in all_matches_so_far[ each_files ] if temp_shapes[im_shape_num] == im_shapeid ]
      if len( check_not_found ) == 0:
         # im_shapeid is not found yet

         found_staying_shapes = [ temp_shapes for temp_shapes in all_sty_shapes if temp_shapes[im_shape_num] == im_shapeid ]
         if len( found_staying_shapes ) == 1:
            
            pixch_in_im_shape = set( search_im_shapes[ found_staying_shapes[0][search_in_im_num] ] ).intersection( pixch )            
            cur_im_shape_wo_pixch = set( search_im_shapes[ found_staying_shapes[0][search_in_im_num] ] ).difference( pixch_in_im_shape )

            if len( pixch_in_im_shape ) > len( cur_im_shape_wo_pixch ):
               continue
            
            cur_im_shapes = pixel_functions.find_shapes( cur_im_shape_wo_pixch, im_size )
            
            im_shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( im_shapes[ im_shapeid ], im_width, param_shp_type=0 )  

            for search_im_shapeid in cur_im_shapes:
               
               search_im_shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( cur_im_shapes[ search_im_shapeid ], im_width, param_shp_type=0 )  
                     
               # matching from smaller shape.
               if len( cur_im_shapes[ search_im_shapeid ] ) > len( im_shapes[ im_shapeid ] ):
                  im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( im_shp_coord_xy, search_im_shp_coord_xy, match_threshold=0.6 )
               else:
                  im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( search_im_shp_coord_xy, im_shp_coord_xy, match_threshold=0.6 )

               if im1im2nbr_match is not True:  
                  continue
               
               #image_functions.cr_im_from_pixels( "26", directory, cur_im_shapes[ search_im_shapeid ] )
               
               if im_shape_num == 0:
                  result_matches[each_files].append( ( im_shapeid, found_staying_shapes[0][search_in_im_num] ) )
               elif im_shape_num == 1:
                  result_matches[each_files].append( ( found_staying_shapes[0][search_in_im_num], im_shapeid ) )
               
               break
               
            
         
         elif len( found_staying_shapes ) >= 2:
            # search_im_shapes has multiple shapes match with im_shapeid

            pixch_in_im_shapes = set()
            fnd_sty_shapes_pixels = set()
            cur_im_shapes_wo_pixch = set()
            for found_staying_shape in found_staying_shapes:
               
               pixch_in_im_shapes |= set( search_im_shapes[ found_staying_shape[search_in_im_num] ] ).intersection( pixch )
               fnd_sty_shapes_pixels |= set( search_im_shapes[ found_staying_shape[search_in_im_num] ] )
               
            cur_im_shapes_wo_pixch |= fnd_sty_shapes_pixels.difference( pixch_in_im_shapes )
            
            if len( pixch_in_im_shapes ) > len( cur_im_shapes_wo_pixch ):
               continue

            cur_im_shapes = pixel_functions.find_shapes( cur_im_shapes_wo_pixch, im_size )            

            im_shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( im_shapes[ im_shapeid ], im_width, param_shp_type=0 )  

            for search_im_shapeid in cur_im_shapes:
               
               search_im_shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( cur_im_shapes[ search_im_shapeid ], im_width, param_shp_type=0 )  
                     
               # matching from smaller shape.
               if len( cur_im_shapes[ search_im_shapeid ] ) > len( im_shapes[ im_shapeid ] ):
                  im1im2match = same_shapes_functions.match_shape_while_moving_it( im_shp_coord_xy, search_im_shp_coord_xy, match_threshold=0.6 )
               else:
                  im1im2match = same_shapes_functions.match_shape_while_moving_it( search_im_shp_coord_xy, im_shp_coord_xy, match_threshold=0.6 )

               if im1im2match is not True:  
                  continue
               
               if im_shape_num == 0:
                  
                  for found_staying_shape in found_staying_shapes:
                     result_matches[each_files].append( ( im_shapeid, found_staying_shape[ search_in_im_num ] ) )
                     
               elif im_shape_num == 1:
                  for found_staying_shape in found_staying_shapes:
                     result_matches[each_files].append( ( found_staying_shape[ search_in_im_num ] , im_shapeid ) )
               
               break            
            







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

   sty_shapes_dir = top_shapes_dir + directory + pixch_sty_dir + "/"
   sty_shapes_file1 = sty_shapes_dir + "data/" + cur_im1file + "." + cur_im2file + "." + cur_im1file + ".data"
   with open (sty_shapes_file1, 'rb') as fp:
      # [('1270', '2072'), ('2062', '2062'), ... ]
      # [ ( image1 shapeid, image2 shapeid ), ... ]
      sty_shapes1 = pickle.load(fp)
   fp.close()

   sty_shapes_file2 = sty_shapes_dir + "data/" + cur_im1file + "." + cur_im2file + "." + cur_im2file + ".data"
   with open (sty_shapes_file2, 'rb') as fp:
      # [('1270', '2072'), ('2062', '2062'), ... ]
      # [ ( image1 shapeid, image2 shapeid ), ... ]
      sty_shapes2 = pickle.load(fp)
   fp.close()
   
   all_sty_shapes = set( sty_shapes2 )
   all_sty_shapes |= set( sty_shapes1 )

   find_separating_shapes( im2shapes, "im2", im1shapes )
   find_separating_shapes( im1shapes, "im1", im2shapes )



ch_btwn_frames_ddir = top_shapes_dir + directory + scnd_stg_ch_btwn_frames_dir + "/data/"
if os.path.exists(ch_btwn_frames_ddir ) == False:
   os.makedirs(ch_btwn_frames_ddir )


ch_btwn_frames_dfile = ch_btwn_frames_ddir + "1.data"

for each_files in result_matches:
   for each_shapes in result_matches[ each_files ]:
      all_matches_so_far[ each_files ].add( each_shapes )



with open(ch_btwn_frames_dfile, 'wb') as fp:
   pickle.dump(result_matches, fp)
fp.close()


with open(all_matches_so_far_dfile, 'wb') as fp:
   pickle.dump(all_matches_so_far, fp)
fp.close()
















