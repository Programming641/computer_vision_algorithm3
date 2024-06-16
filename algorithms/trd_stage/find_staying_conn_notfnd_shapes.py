
from libraries import  btwn_amng_files_functions, pixel_shapes_functions, pixel_functions, image_functions, same_shapes_functions
from libraries import cv_globals

from PIL import ImageTk, Image
import os, sys
import pickle
import copy
import math
import shutil

from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files
from libraries.cv_globals import scnd_stg_spixc_dir, scnd_stg_ch_btwn_frames_dir

shapes_type = "intnl_spixcShp"
directory = "videos/street3/resized/min1"

if len( sys.argv ) >= 2:
   directory = sys.argv[1]

# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

if shapes_type == "normal":
   print("ERROR. shapes_type normal is not supported")
   sys.exit(1)

elif shapes_type == "intnl_spixcShp":

   shapes_dir = top_shapes_dir + directory  + "shapes/"


else:
   print("ERROR at " + str( os.path.basename(__file__) ) + " shapes_type " + shapes_type + " is not supported")
   sys.exit(1)



across_all_files_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/data/"
across_all_files_dfile = across_all_files_ddir + "all_files.data"
with open (across_all_files_dfile, 'rb') as fp:
   acrs_all_files_shapes = pickle.load(fp)
fp.close()

all_matches_so_far_dfile = across_all_files_ddir + "all_matches.data"
if os.path.exists( all_matches_so_far_dfile ):
   with open (all_matches_so_far_dfile, 'rb') as fp:
      all_matches_so_far = pickle.load(fp)
   fp.close()

else:
   all_matches_so_far = acrs_all_files_shapes



spixc_dir = top_shapes_dir + directory + scnd_stg_spixc_dir
spixc_shapes_dfile = spixc_dir + "/data/" + "1.data"
with open (spixc_shapes_dfile, 'rb') as fp:
   # { '10.11': [ [ [ im1shapes ], [ im2shapes ] ], ...  ], ... }
   spixc_shapes = pickle.load(fp)
fp.close()


ch_btwn_frames_ddir = top_shapes_dir + directory + scnd_stg_ch_btwn_frames_dir + "/data/"
ch_btwn_frames4_dfile = ch_btwn_frames_ddir + "4.data"
with open (ch_btwn_frames4_dfile, 'rb') as fp:
   # { '10.11': [ [ [ im1shapes ], [ im2shapes ] ], ...  ], ... }
   pixch_on_notfnd_shapes = pickle.load(fp)
fp.close()

image_template_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/image_template/data/"
multi_shapes_by_img_tmpl_dfile = image_template_ddir + "verified_multi1.data"  
with open (multi_shapes_by_img_tmpl_dfile, 'rb') as fp:
   # {'1.2': [[{'52800', '68452'}, ['56042', '68454']]], '2.3': [[['37593', '33271'], {'32189', '33271', ... }], 
   #         [['42525', '36043'], {'32802', '35504', ... }], ... ], ... }
   multi_shapes_by_img_tmpl = pickle.load(fp)
fp.close()


third_stage_notfnd_shapes_dir = top_shapes_dir + directory + "trd_stage/notfnd_shapes/"
third_st_notfnd_shapes_ddir = third_stage_notfnd_shapes_dir + "data/"



def find_staying_notfnd_shapes( im_conn_notfnd_shapes, im_shapes, im_shapeids_by_pindex, im_notfnd_shapes ):
   im_pixel_total = 0
   matched_pixel_count = 0
   matched_shapes = set()
   
   
   for im_conn_notfnd_shape in im_conn_notfnd_shapes:
      im_pixel_total += len( im_shapes[ im_conn_notfnd_shape ] )
      
      for notfnd_shape_pixel in im_shapes[ im_conn_notfnd_shape ]:

         for im_shape_at_same_pixel in im_shapeids_by_pindex[ notfnd_shape_pixel ]:
            if im_shape_at_same_pixel in im_notfnd_shapes:
               matched_pixel_count += 1
               matched_shapes.add( im_shape_at_same_pixel )
            
   
   if im_pixel_total >= frth_smallest_pixc:
      match_threshold = 0.55
   elif im_pixel_total >= third_smallest_pixc:
      match_threshold = 0.65
      
   if matched_pixel_count / im_pixel_total >= match_threshold:
      
      return [ im_conn_notfnd_shapes, matched_shapes ]
      

   else:
      return []




pixch_imdir = top_shapes_dir + directory + "pixch/"
pixch_data_dir = pixch_imdir + "data/"

shp_by_index_dir = shapes_dir + 'shapeids_by_pindex/'

lowest_filenum, highest_filenum = btwn_amng_files_functions.get_low_highest_filenums( directory )
im1 = Image.open(top_images_dir + directory + str(lowest_filenum) + ".png" )

frth_smallest_pixc = cv_globals.get_frth_smallest_pixc( im1.size )
third_smallest_pixc = cv_globals.get_third_smallest_pixc( im1.size )


result_shapes = {}
strict_result_shapes = {}
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
for each_files in all_matches_so_far:
   print(each_files)
   
   result_shapes[ each_files ] = []
   strict_result_shapes[each_files] = []
   
   cur_im1file = each_files.split(".")[0]
   cur_im2file = each_files.split(".")[1]

   if ref_imagefile_op is False:
      im1 = Image.open(top_images_dir + directory + cur_im1file + ".png" )

      im_size = im1.size
      im_width, im_height = im_size
      
      ref_imagefile_op = True


   shapes_dfile = shapes_dir + cur_im1file + "shapes.data"
   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()     

   for shapeid in im1shapes:
      cur_pixels = set()
      cur_xy_pixels = set()
      for pindex in im1shapes[ shapeid ]:
         cur_pixels.add( pindex )
      
      im1shapes[ shapeid ] = cur_pixels

   shp_by_index_dfile = shp_by_index_dir + cur_im1file + ".data"
   with open (shp_by_index_dfile, 'rb') as fp:
      # { pindex: { shapeids }, ... }
      im1shapeids_by_pindex = pickle.load(fp)
   fp.close()

   im2shapes_dfile = shapes_dir + cur_im2file + "shapes.data"
   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()   

   for shapeid in im2shapes:
      cur_pixels = set()
      for pindex in im2shapes[ shapeid ]:
         cur_pixels.add( pindex )
      
      im2shapes[ shapeid ] = cur_pixels

   shp_by_index_dfile2 = shp_by_index_dir + cur_im2file + ".data"
   with open (shp_by_index_dfile2, 'rb') as fp:
      # { pindex: { shapeids }, ... }
      im2shapeids_by_pindex = pickle.load(fp)
   fp.close()

   im1found_shapes = set()
   im2found_shapes = set()

   
   for each_shapes in all_matches_so_far[ each_files ]:
      im1found_shapes.add( each_shapes[0] )
      im2found_shapes.add( each_shapes[1] )

   
   for each_shapes in spixc_shapes[ each_files ]:
      for temp_im1shapeid in each_shapes[0]:
         im1found_shapes.add( temp_im1shapeid )
      
      for temp_im2shapeid in each_shapes[1]:
         im2found_shapes.add( temp_im2shapeid )
  

   for each_shapes in pixch_on_notfnd_shapes[ each_files ]:
      for temp_im1shapeid in each_shapes[0]:
         im1found_shapes.add( temp_im1shapeid )
      
      for temp_im2shapeid in each_shapes[1]:
         im2found_shapes.add( temp_im2shapeid )   


   for each_shapes in multi_shapes_by_img_tmpl[ each_files ]:
      for temp_im1shapeid in each_shapes[0]:
         im1found_shapes.add( temp_im1shapeid )
      
      for temp_im2shapeid in each_shapes[1]:
         im2found_shapes.add( temp_im2shapeid )      


   pixch_dfile = pixch_data_dir  + cur_im1file + "." + cur_im2file + ".data"
   with open (pixch_dfile, 'rb') as fp:
      # {'39773', '16485', '20100', '57958', ... }
      pixch = pickle.load(fp)
   fp.close()      


   im1notfnd_shapes = set( im1shapes.keys() ).difference( im1found_shapes )
   im2notfnd_shapes = set( im2shapes.keys() ).difference( im2found_shapes )
   
   #image_functions.cr_im_from_shapeslist2( cur_im1file, directory, im1notfnd_shapes, shapes_rgb=(255,0,0) )

   im1shape_neighbors_file = shapes_dir + "shape_nbrs/" + cur_im1file + "_shape_nbrs.data"
   im2shape_neighbors_file = shapes_dir + "shape_nbrs/" + cur_im2file + "_shape_nbrs.data"

   with open (im1shape_neighbors_file, 'rb') as fp:
      im1shapes_neighbors = pickle.load(fp)
   fp.close()     

   with open (im2shape_neighbors_file, 'rb') as fp:
      im2shapes_neighbors = pickle.load(fp)
   fp.close()     

   
   already_added_shapes = set()
   for notfnd_shape in im1notfnd_shapes:
      if notfnd_shape in already_added_shapes:
         continue
      im1conn_notfnd_shapes = pixel_shapes_functions.get_connected_shapes( notfnd_shape, im1shapes_neighbors, im1notfnd_shapes )
      if im1conn_notfnd_shapes is not None:
         all_im1pixels = set()
         for im1conn_notfnd_shape in im1conn_notfnd_shapes:
            all_im1pixels |= { pixel for pixel in im1shapes[im1conn_notfnd_shape] }
         
         im1changed_pixels = all_im1pixels.intersection( pixch )
         if len( im1changed_pixels ) > len(all_im1pixels) * 0.7:
            already_added_shapes |= im1conn_notfnd_shapes
            continue
         
         #image_functions.cr_im_from_shapeslist2( cur_im1file, directory, im1conn_notfnd_shapes, shapes_rgb=(0,255,0) )
         if len(all_im1pixels) >= third_smallest_pixc:         
            matched_results = find_staying_notfnd_shapes( im1conn_notfnd_shapes, im1shapes, im2shapeids_by_pindex, im2notfnd_shapes )
            if len( matched_results ) == 2:
               if matched_results not in result_shapes[ each_files ]:
                  result_shapes[ each_files ].append( matched_results )
            

         already_added_shapes |= im1conn_notfnd_shapes


   already_added_shapes = set()
   for notfnd_shape in im2notfnd_shapes:
      if notfnd_shape in already_added_shapes:
         continue
      im2conn_notfnd_shapes = pixel_shapes_functions.get_connected_shapes( notfnd_shape, im2shapes_neighbors, im2notfnd_shapes )
      if im2conn_notfnd_shapes is not None:
         all_im2pixels = set()
         for im2conn_notfnd_shape in im2conn_notfnd_shapes:
            all_im2pixels |= { pixel for pixel in im2shapes[im2conn_notfnd_shape] }
         
         im2changed_pixels = all_im2pixels.intersection( pixch )
         if len( im2changed_pixels ) > len(all_im2pixels) * 0.7:
            already_added_shapes |= im2conn_notfnd_shapes
            continue
            
         if len(all_im2pixels) >= third_smallest_pixc:
            matched_results = find_staying_notfnd_shapes( im2conn_notfnd_shapes, im2shapes, im1shapeids_by_pindex, im1notfnd_shapes )
            if len( matched_results ) == 2:
               matched_results = [ matched_results[1], matched_results[0] ]
            
               if matched_results not in result_shapes[ each_files ]:
                  result_shapes[ each_files ].append( matched_results )


         already_added_shapes |= im2conn_notfnd_shapes



third_stage_notfnd_shapes_dir = top_shapes_dir + directory + "trd_stage/notfnd_shapes/"
third_stage_notfnd_shapes_ddir = third_stage_notfnd_shapes_dir + "data/"
if os.path.exists(third_stage_notfnd_shapes_ddir ) == False:
   os.makedirs(third_stage_notfnd_shapes_ddir )


third_stage_notfnd_shapes_im1dfile = third_stage_notfnd_shapes_ddir + "staying.data"
with open(third_stage_notfnd_shapes_im1dfile, 'wb') as fp:
   pickle.dump(result_shapes, fp)
fp.close()


'''
with open(all_matches_so_far_dfile, 'wb') as fp:
   pickle.dump(all_matches_so_far, fp)
fp.close()
'''















