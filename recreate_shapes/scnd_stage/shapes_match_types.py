
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


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'


shapes_m_types_dir = top_shapes_dir + directory + scnd_stg_all_files + "/shp_match_types/"
matched_pixels_dfile = shapes_m_types_dir + "data/matched_pixels.data"
with open (matched_pixels_dfile, 'rb') as fp:
   matched_pixels = pickle.load(fp)
fp.close()

not_classified_dfile = shapes_m_types_dir + "data/not_classified.data"
with open (not_classified_dfile, 'rb') as fp:
   not_classified_shapes = pickle.load(fp)
fp.close()



for filename in matched_pixels:
   print( filename )

   im1file = filename.split(".")[0]
   im2file = filename.split(".")[1]
   
   matched_pixels_imdir = shapes_m_types_dir + im1file + "." + im2file + "/"

   # delete and create folder
   if os.path.exists(matched_pixels_imdir) == True:
      shutil.rmtree(matched_pixels_imdir)
   os.makedirs(matched_pixels_imdir)

   im_pixels_counter = 1
   for each_file_shapes in matched_pixels[filename]:
      # each_file_shapes -> ('57125', '57529')
      # or 
      # [ [image1 shapes], [image2 shapes] ]

      if type( each_file_shapes ) is tuple :
         # ('57125', '57529')
         cur_image_name = matched_pixels_imdir + each_file_shapes[0] + "." + each_file_shapes[1]
         
         save_im1fpath = cur_image_name + "im1.png"
         image_functions.cr_im_from_shapeslist2( im1file, directory, [ each_file_shapes[0] ], save_filepath=save_im1fpath , shapes_rgb=(255, 0, 0 ) )

         save_im2fpath = cur_image_name + ".im2.png"
         image_functions.cr_im_from_shapeslist2( im2file, directory, [ each_file_shapes[1] ], save_filepath=save_im2fpath , shapes_rgb=(0, 0, 255 ) )       

      elif type( each_file_shapes[0] ) is list:

         save_im1fpath = matched_pixels_imdir + str( im_pixels_counter ) + ".im1.png"
         image_functions.cr_im_from_shapeslist2( im1file, directory, each_file_shapes[0], save_filepath=save_im1fpath )

         save_im2fpath = matched_pixels_imdir + str( im_pixels_counter ) + ".im2.png"
         image_functions.cr_im_from_shapeslist2( im2file, directory, each_file_shapes[1], save_filepath=save_im2fpath )

         im_pixels_counter += 1


not_classified_dir = shapes_m_types_dir + "not_classified/"
if os.path.exists(not_classified_dir ) == False:
   os.makedirs(not_classified_dir )

for filename in not_classified_shapes:
   print( filename )

   im1file = filename.split(".")[0]
   im2file = filename.split(".")[1]
   
   not_classified_imdir = not_classified_dir + im1file + "." + im2file + "/"

   # delete and create folder
   if os.path.exists(not_classified_imdir) == True:
      shutil.rmtree(not_classified_imdir)
   os.makedirs(not_classified_imdir)


   for each_file_shapes in not_classified_shapes[ filename ]:

      cur_image_name = not_classified_imdir + each_file_shapes[0] + "." + each_file_shapes[1]
      
      save_im1fpath = cur_image_name + "im1.png"
      image_functions.cr_im_from_shapeslist2( im1file, directory, [ each_file_shapes[0] ], save_filepath=save_im1fpath , shapes_rgb=(255, 0, 0 ) )

      save_im2fpath = cur_image_name + ".im2.png"
      image_functions.cr_im_from_shapeslist2( im2file, directory, [ each_file_shapes[1] ], save_filepath=save_im2fpath , shapes_rgb=(0, 0, 255 ) )   











