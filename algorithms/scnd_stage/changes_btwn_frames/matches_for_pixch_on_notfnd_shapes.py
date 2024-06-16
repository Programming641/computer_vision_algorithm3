
from libraries import  cv_globals, pixel_shapes_functions, pixel_functions, image_functions, same_shapes_functions


from PIL import ImageTk, Image
import os, sys
import pickle
import copy
import math
import shutil

from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files
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
   sys.exit(1)

elif shapes_type == "intnl_spixcShp":

   shapes_dir = top_shapes_dir + directory  + "shapes/"


else:
   print("ERROR at " + str( os.path.basename(__file__) ) + " shapes_type " + shapes_type + " is not supported")
   sys.exit(1)


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


def check_shape_size( param1shapes_len, param2shapes_len, size_threshold=1 ):
   # check if size is too different
      
   im1_2pixels_diff = abs( param1shapes_len - param2shapes_len )
   if im1_2pixels_diff != 0:
      if param1shapes_len > param2shapes_len:
         if im1_2pixels_diff / param2shapes_len > size_threshold:
            return True
      else:
         if im1_2pixels_diff / param1shapes_len > size_threshold:
            return True

   return False      



def find_matches( im1connected_notfnd_shp_pixch, im2connected_notfnd_shp_pixch, swapped, im_notfnd_shapes, im_shapes ):

   for each_im1pixch_notfnd_shapes in im1connected_notfnd_shp_pixch:
      if len( im1connected_notfnd_shp_pixch[each_im1pixch_notfnd_shapes] ) < frth_smallest_pixc:
         continue
      
      #image_functions.cr_im_from_pixels( "1", directory, im1connected_notfnd_shp_pixch[each_im1pixch_notfnd_shapes] )
      
      # get image2 connected pixch on not found shapes that overlap most pixels with each_im1pixch_notfnd_shapes
      for each_im2pixch_notfnd_shapes in im2connected_notfnd_shp_pixch:
         if len( im2connected_notfnd_shp_pixch[each_im2pixch_notfnd_shapes] ) < frth_smallest_pixc:
            continue
         
         #image_functions.cr_im_from_pixels( "2", directory, im2connected_notfnd_shp_pixch[each_im2pixch_notfnd_shapes] )
         
         size_diff = check_shape_size( len( im1connected_notfnd_shp_pixch[each_im1pixch_notfnd_shapes] ), len( im2connected_notfnd_shp_pixch[each_im2pixch_notfnd_shapes] ) )
         if size_diff is True:
            continue
         
         
         overlapped_pixels = im1connected_notfnd_shp_pixch[each_im1pixch_notfnd_shapes].intersection( im2connected_notfnd_shp_pixch[each_im2pixch_notfnd_shapes] )
         
         if len( overlapped_pixels ) / len( im1connected_notfnd_shp_pixch[each_im1pixch_notfnd_shapes] ) >= 0.5:
            # get shapes for each connected pixels

            matched_im1shapes = set() 
            for im1notfnd_shape in im_notfnd_shapes[0]:
               found_pixels = set( im_shapes[0][ im1notfnd_shape ] ).intersection( im1connected_notfnd_shp_pixch[each_im1pixch_notfnd_shapes] )

               
               if len( found_pixels ) >= 1:
                  matched_im1shapes.add( im1notfnd_shape )
           
            matched_im2shapes = set()
            for im2notfnd_shape in im_notfnd_shapes[1]:
               found_pixels = set( im_shapes[1][ im2notfnd_shape ] ).intersection( im2connected_notfnd_shp_pixch[each_im2pixch_notfnd_shapes] )
               
               if len( found_pixels ) >= 1:
                  matched_im2shapes.add( im2notfnd_shape )           
            
            if swapped is False and [ matched_im1shapes, matched_im2shapes ] not in result_matches[ each_files ]:
               result_matches[ each_files ].append( [ matched_im1shapes, matched_im2shapes ] )
            elif swapped is True and [ matched_im2shapes, matched_im1shapes ] not in result_matches[ each_files ]:
               result_matches[ each_files ].append( [ matched_im2shapes, matched_im1shapes ] )






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

   im1 = Image.open(top_images_dir + directory + cur_im1file + ".png" )
   if ref_imagefile_op is False:
      
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
   
   #image_functions.cr_im_from_pixels( cur_im1file, directory, im1notfnd_pixch )
   #image_functions.cr_im_from_pixels( cur_im2file, directory, im2notfnd_pixch )


   im1notfnd_shapes = set( im1shapes.keys() ).difference( all_im1found_shapes )
   im2notfnd_shapes = set( im2shapes.keys() ).difference( all_im2found_shapes )                 
   
   
   # get connected pixel changes on not found shapes.
   # {  64150: {64690, 65230, 64150}, 8103: {8103}, ... }
   im1connected_notfnd_shp_pixch = pixel_functions.find_shapes( im1notfnd_pixch, im_size )
   for im1connected_shapeid in im1connected_notfnd_shp_pixch:
      im1connected_notfnd_shp_pixch[ im1connected_shapeid ] = { temp_pixel for temp_pixel in im1connected_notfnd_shp_pixch[ im1connected_shapeid ] }
         
   im2connected_notfnd_shp_pixch = pixel_functions.find_shapes( im2notfnd_pixch, im_size )
   for im2connected_shapeid in im2connected_notfnd_shp_pixch:
      im2connected_notfnd_shp_pixch[ im2connected_shapeid ] = { temp_pixel for temp_pixel in im2connected_notfnd_shp_pixch[ im2connected_shapeid ] }
   
   find_matches( im1connected_notfnd_shp_pixch, im2connected_notfnd_shp_pixch, False, [ im1notfnd_shapes, im2notfnd_shapes ], [ im1shapes, im2shapes ] )
   find_matches( im2connected_notfnd_shp_pixch, im1connected_notfnd_shp_pixch, True, [ im2notfnd_shapes, im1notfnd_shapes ], [ im2shapes, im1shapes ] )



ch_btwn_frames_ddir = top_shapes_dir + directory + scnd_stg_ch_btwn_frames_dir + "/data/"
if os.path.exists(ch_btwn_frames_ddir ) == False:
   os.makedirs(ch_btwn_frames_ddir )


ch_btwn_frames_dfile = ch_btwn_frames_ddir + "4.data"
with open(ch_btwn_frames_dfile, 'wb') as fp:
   pickle.dump(result_matches, fp)
fp.close()

'''
with open(all_matches_so_far_dfile, 'wb') as fp:
   pickle.dump(all_matches_so_far, fp)
fp.close()
'''















