
from PIL import Image
import pickle
import math
import copy, shutil
import os, sys
from libraries.cv_globals import top_temp_dir, top_shapes_dir, top_images_dir, internal, scnd_stg_all_files
from libraries.cv_globals import frth_smallest_pixc, Lshape_size, third_smallest_pixc
from libraries import read_files_functions, pixel_shapes_functions, image_functions, pixel_functions, same_shapes_functions
import winsound


directory = "videos/street3/resized/min"
shapes_type = "intnl_spixcShp"
file_num = "verified_multi1"


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'


image_template_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/image_template/data/"
image_template_dfile = image_template_ddir + file_num + ".data"
with open (image_template_dfile, 'rb') as fp:
   im_template_shapes = pickle.load(fp)
fp.close()     

imdir = top_shapes_dir + directory + scnd_stg_all_files + "/image_template/" + file_num + "/"

for filename in im_template_shapes:
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

   done_shapes_pairs = []
   img_counter = 1
   for each_shapes in im_template_shapes[filename]:
      if each_shapes in done_shapes_pairs:
         continue

      if type( each_shapes[0] ) is str:

         im1n2shp_pairs = set()
         cur_im1shape_pairs = { temp_shapes for temp_shapes in im_template_shapes[ filename ] if each_shapes[1] == temp_shapes[1] }
         cur_im2shape_pairs = { temp_shapes for temp_shapes in im_template_shapes[ filename ] if each_shapes[0] == temp_shapes[0] }
      
         im1n2shp_pairs |= cur_im1shape_pairs
         im1n2shp_pairs |= cur_im2shape_pairs
      
         all_im1shapes = { temp_shapes[0] for temp_shapes in im1n2shp_pairs }
         all_im2shapes = { temp_shapes[1] for temp_shapes in im1n2shp_pairs }
      
         for im1n2shp_pair in im1n2shp_pairs:
            done_shapes_pairs.append( im1n2shp_pair )
      
         im_filename = each_files_imdir + each_shapes[0] + "." + each_shapes[1]
      
         save_im1fpath = im_filename + "im1.png"
         image_functions.cr_im_from_shapeslist2( im1file, directory, all_im1shapes, save_filepath=save_im1fpath , shapes_rgb=(255, 0, 0 ) )      

         save_im2fpath = im_filename + "im2.png"
         image_functions.cr_im_from_shapeslist2( im2file, directory, all_im2shapes, save_filepath=save_im2fpath , shapes_rgb=(0, 0, 255 ) )           

      elif type( each_shapes[0] ) is list or type( each_shapes[1] ) is set:
         save_im1fpath = each_files_imdir + str( img_counter ) + "im1.png"
         image_functions.cr_im_from_shapeslist2( im1file, directory, each_shapes[0], save_filepath=save_im1fpath , shapes_rgb=(255, 0, 0 ) )   
         
         save_im2fpath = each_files_imdir + str( img_counter ) + "im2.png"
         image_functions.cr_im_from_shapeslist2( im2file, directory, each_shapes[1], save_filepath=save_im2fpath , shapes_rgb=(0, 0, 255 ) )   

         if filename == "14.15" and img_counter == 35:
            print( each_shapes )

        
         img_counter += 1
         


   files_len = len( os.listdir(each_files_imdir) )
   
   print( str( files_len ) + " files now")
   print()







