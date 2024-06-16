
from PIL import Image
import pickle
import math
import copy, shutil
import os, sys
from libraries.cv_globals import top_temp_dir, top_shapes_dir, top_images_dir, internal, scnd_stg_all_files
from libraries import pixel_shapes_functions, image_functions, pixel_functions, same_shapes_functions
import winsound


directory = "videos/street3/resized/min1"
shapes_type = "intnl_spixcShp"
target_filename = "objects1"


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

obj_shapes_dir = top_shapes_dir + directory + "trd_stage/obj_shapes/"
obj_shapes_ddir = obj_shapes_dir + "data/"
obj_shapes_dfile = obj_shapes_ddir + target_filename + ".data"
with open (obj_shapes_dfile, 'rb') as fp:
   target_shapes = pickle.load(fp)
fp.close()


imdir = obj_shapes_dir + target_filename + "/"

for filename in target_shapes:
   print( filename )

   im1file = filename.split(".")[0]
   im2file = filename.split(".")[1]
   
   each_files_imdir = imdir + im1file + "." + im2file + "/"

   # delete and create folder
   if os.path.exists(each_files_imdir) == True:
      files_len = len( os.listdir(each_files_imdir) )
      print( str( files_len ) + " files before")
      
      shutil.rmtree(each_files_imdir)
   os.makedirs(each_files_imdir)
   
   # for target file: move_shapes2partial.data
   # [ [ source im1 shapeids, source im2 shapeids ], ... ]
   source_shapeids = []
   
   # source id is placed in the same index as the source shapeids.
   source_id_counter = []
   
   match_counter = 1
   for each_file_shapes in target_shapes[filename]:
      # [('61978', '79999'), {('79689', '79677'), ('79689', '66510'), ... }]
      # [ ( im1shapeid, im2shapeid ), { ( im1neighbor shapeid, im2neighbor shapeid ), ... } ]
      
      matched_shapes_fname = each_files_imdir + str( match_counter )

      if target_filename == "objects1":
         # algorithm: attach_with_direct_neighbors.py
         #    [ [ { im1shapeids }, { im2shapeids }, movement ], [ { im1shapeids }, { im2shapeids }, movement ], ... ]

         matched_shapes_imf1name = matched_shapes_fname + ".im1.png"
         matched_shapes_im2fname = matched_shapes_fname + ".im2.png"
         
         cur_im1shapes = set()
         cur_im2shapes = set()
         shapes_colors = image_functions.get_rgbs( start_r=100, start_g=20, start_b=20 )
         first = True
         for i, each_shapes in enumerate(each_file_shapes):
            if first is True:
               first = False
               image_functions.cr_im_from_shapeslist2( im1file, directory, each_shapes[0], save_filepath=matched_shapes_imf1name , shapes_rgbs=[shapes_colors[i]] )
               image_functions.cr_im_from_shapeslist2( im2file, directory, each_shapes[1], save_filepath=matched_shapes_im2fname, shapes_rgbs=[shapes_colors[i]] )  

            else:
               image_functions.cr_im_from_shapeslist2( im1file, directory, each_shapes[0], save_filepath=matched_shapes_imf1name , shapes_rgbs=[shapes_colors[i + 2]], input_im=matched_shapes_imf1name )
               image_functions.cr_im_from_shapeslist2( im2file, directory, each_shapes[1], save_filepath=matched_shapes_im2fname, shapes_rgbs=[shapes_colors[i + 2]], input_im=matched_shapes_im2fname ) 


      
      elif type(each_file_shapes[0]) is int:

         src_imfile = obj_shapes_dir + filename + "/" + each_file_shapes[0] + "." + each_file_shapes[1]
         src_im1file =  src_imfile + "im1.png"
         src_im2file = src_imfile + "im2.png"      
      

         result_name = each_file_shapes[0] + "." + each_file_shapes[1]

         save_im1fpath = each_files_imdir + result_name + "im1.png"
         shutil.copyfile(src_im1file, save_im1fpath)

         save_im2fpath = each_files_imdir + result_name + "im2.png"
         shutil.copyfile(src_im2file, save_im2fpath)


      elif type( each_file_shapes[0] ) is tuple:
         
         matched_shapes_imf1name = matched_shapes_fname + ".im1.png"
         
         image_functions.cr_im_from_shapeslist2( im1file, directory, [ each_file_shapes[0][0] ], save_filepath=matched_shapes_imf1name , shapes_rgbs=[(255,0,0)] )
         matched_shapes_im2fname = matched_shapes_fname + ".im2.png"
         image_functions.cr_im_from_shapeslist2( im2file, directory, [ each_file_shapes[0][1] ], save_filepath=matched_shapes_im2fname, shapes_rgbs=[(0,0,255)] )
         
         im1nbr_fname = matched_shapes_fname + ".nbr1.png"
         im1nbr_shapes = { temp_shapes[0] for temp_shapes in each_file_shapes[1] }
         image_functions.cr_im_from_shapeslist2( im1file, directory, im1nbr_shapes, save_filepath=im1nbr_fname , shapes_rgbs=[(0,255,0)] )

         im2nbr_fname = matched_shapes_fname + ".nbr2.png"
         im2nbr_shapes = { temp_shapes[1] for temp_shapes in each_file_shapes[1] }
         image_functions.cr_im_from_shapeslist2( im2file, directory, im2nbr_shapes, save_filepath=im2nbr_fname , shapes_rgbs=[(0,255,255)] )      


      elif len( each_file_shapes ) >= 3 and type( each_file_shapes[0] ) is list and type( each_file_shapes[1] ) is tuple and type( each_file_shapes[2] ) is tuple:
         # [ [ {im1shapes}, {im2shapes} ], (im1shapes average xy ), ( im2shapes average xy ) ]

         matched_shapes_imf1name = matched_shapes_fname + ".im1.png"
         
         image_functions.cr_im_from_shapeslist2( im1file, directory, each_file_shapes[0][0], save_filepath=matched_shapes_imf1name , shapes_rgbs=[(255,0,0)] )
         matched_shapes_im2fname = matched_shapes_fname + ".im2.png"
         image_functions.cr_im_from_shapeslist2( im2file, directory, each_file_shapes[0][1], save_filepath=matched_shapes_im2fname, shapes_rgbs=[(0,0,255)] )


         image_functions.cr_im_from_pixels( im1file, directory, [ each_file_shapes[1] ], save_filepath=matched_shapes_imf1name , pixels_rgb=(0,255,255), input_im=matched_shapes_imf1name )
         image_functions.cr_im_from_pixels( im2file, directory, [ each_file_shapes[2] ], save_filepath=matched_shapes_im2fname , pixels_rgb=(0,255,255), input_im=matched_shapes_im2fname )       


      elif len( each_file_shapes ) == 3 and type( each_file_shapes[0] ) is list and type( each_file_shapes[1] ) is set and type( each_file_shapes[2] ) is set:
         # [ [ {im1shapes}, {im2shapes} ], disappeared_pixels, appeared_pixels ]

         matched_shapes_imf1name = matched_shapes_fname + ".im1.png"
         
         image_functions.cr_im_from_shapeslist2( im1file, directory, each_file_shapes[0][0], save_filepath=matched_shapes_imf1name , shapes_rgbs=[(255,0,0)] )
         matched_shapes_im2fname = matched_shapes_fname + ".im2.png"
         image_functions.cr_im_from_shapeslist2( im2file, directory, each_file_shapes[0][1], save_filepath=matched_shapes_im2fname, shapes_rgbs=[(0,0,255)] )

         if len( each_file_shapes[1] ) >= 1:
            image_functions.cr_im_from_pixels( im1file, directory, each_file_shapes[1], save_filepath=matched_shapes_imf1name , pixels_rgb=(0,255,255), input_im=matched_shapes_imf1name )
         if len( each_file_shapes[2] ) >= 1:
            image_functions.cr_im_from_pixels( im2file, directory, each_file_shapes[2], save_filepath=matched_shapes_im2fname , pixels_rgb=(0,255,255), input_im=matched_shapes_im2fname )         



      elif len( each_file_shapes ) == 3 and type( each_file_shapes[0] ) is set and type( each_file_shapes[1] ) is set and type( each_file_shapes[2] ) is tuple:
         # [ { im1shapeids }, { im2shapeids }, movement ] or ( { im1shapeids }, { im2shapeids }, movement )
         
         print( str(match_counter) + " " + str(each_file_shapes[2]) )
         
         matched_shapes_imf1name = matched_shapes_fname + ".im1.png"
         
         image_functions.cr_im_from_shapeslist2( im1file, directory, each_file_shapes[0], save_filepath=matched_shapes_imf1name , shapes_rgbs=[(255,0,0)] )
         matched_shapes_im2fname = matched_shapes_fname + ".im2.png"
         image_functions.cr_im_from_shapeslist2( im2file, directory, each_file_shapes[1], save_filepath=matched_shapes_im2fname, shapes_rgbs=[(0,0,255)] )


      elif target_filename == "move_shapes2partial":
         # target file: move_shapes2partial.data
         # ( [ { neighbor im1 shapeids }, { neighbor im2 shapeids }, movement ] , source im1 shapeids, source im2 shapeids, matched movement pixels, 
         #                                               matched movement  )
         
         if [ each_file_shapes[1], each_file_shapes[2] ] not in source_shapeids: 
            source_shapeids.append( [ each_file_shapes[1], each_file_shapes[2] ] )
            
            cur_source_index = len( source_shapeids ) - 1
            
            cur_folder = each_files_imdir + str(cur_source_index) + "/"
            
            os.makedirs(cur_folder)

            source_id_counter.append(0)
            cur_shapes_counter = 0
         
         else:
            cur_source_index = source_shapeids.index( [ each_file_shapes[1], each_file_shapes[2] ] )
            
            cur_folder = each_files_imdir + str(cur_source_index) + "/"
            
            cur_shapes_counter = source_id_counter[cur_source_index]
         
         
         imfname_prefix = cur_folder + str(cur_shapes_counter)
         
         matched_shapes_imfname = imfname_prefix + ".nbr_im1.png"
         image_functions.cr_im_from_shapeslist2( im1file, directory, each_file_shapes[0][0], save_filepath=matched_shapes_imfname , shapes_rgbs=[(255,0,0)] )
         
         matched_shapes_imfname = imfname_prefix + ".nbr_im2.png"
         image_functions.cr_im_from_shapeslist2( im2file, directory, each_file_shapes[0][1], save_filepath=matched_shapes_imfname , shapes_rgbs=[(0,0,255)] )

         matched_shapes_imfname = imfname_prefix + "matched_pixels.png"
         image_functions.cr_im_from_pixels( im2file, directory, each_file_shapes[3], save_filepath=matched_shapes_imfname , pixels_rgb=(255,0,0) )
         
         source_id_counter[cur_source_index] += 1



      
      elif type( each_file_shapes ) is list and len( each_file_shapes[0] ) == 4:
         # [ im1shapes, disappeared_pixels, im1_lg_farthest_conn_pixels, im1_lg_far_conn_p_directions, 
         #   im2shapes, appeared_pixels, im2_lg_farthest_conn_pixels, im2_lg_far_conn_p_directions ]
         
         matched_shapes_imfname = matched_shapes_fname + ".im1.1.png"
         image_functions.cr_im_from_shapeslist2( im1file, directory, each_file_shapes[0][0], save_filepath=matched_shapes_imfname , shapes_rgbs=[(255,0,0)] )
         
         matched_shapes_imfname = matched_shapes_fname + ".im1.2.png"
         if len( each_file_shapes[0][1] ) >= 1:
            image_functions.cr_im_from_pixels( im1file, directory, each_file_shapes[0][1], save_filepath=matched_shapes_imfname , pixels_rgb=(0,255,255) )

         matched_shapes_imfname = matched_shapes_fname + ".im1.3.png"
         if len( each_file_shapes[0][2] ) >= 1:
            image_functions.cr_im_from_pixels( im1file, directory, each_file_shapes[0][2], save_filepath=matched_shapes_imfname , pixels_rgb=(0,255,255) )

         matched_shapes_imfname = matched_shapes_fname + ".im2.1.png"
         image_functions.cr_im_from_shapeslist2( im2file, directory, each_file_shapes[1][0], save_filepath=matched_shapes_imfname , shapes_rgbs=[(0,0,255)] )
         
         matched_shapes_imfname = matched_shapes_fname + ".im2.2.png"
         if len( each_file_shapes[1][1] ) >= 1:
            image_functions.cr_im_from_pixels( im2file, directory, each_file_shapes[1][1], save_filepath=matched_shapes_imfname , pixels_rgb=(0,255,255) )

         matched_shapes_imfname = matched_shapes_fname + ".im2.3.png"
         if len( each_file_shapes[1][2] ) >= 1:
            image_functions.cr_im_from_pixels( im2file, directory, each_file_shapes[1][2], save_filepath=matched_shapes_imfname , pixels_rgb=(0,255,255) )


      elif type( each_file_shapes[0] ) is set or type( each_file_shapes[0] ) is list:

         matched_shapes_imf1name = matched_shapes_fname + ".im1.png"
         
         image_functions.cr_im_from_shapeslist2( im1file, directory, each_file_shapes[0], save_filepath=matched_shapes_imf1name , shapes_rgbs=[(255,0,0)] )
         matched_shapes_im2fname = matched_shapes_fname + ".im2.png"
         image_functions.cr_im_from_shapeslist2( im2file, directory, each_file_shapes[1], save_filepath=matched_shapes_im2fname, shapes_rgbs=[(0,0,255)] )

                
      
      match_counter += 1



   files_len = len( os.listdir(each_files_imdir) )
   
   print( str( files_len ) + " files now")
   print()
   print()






