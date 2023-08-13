
from libraries import pixel_functions, read_files_functions, pixel_shapes_functions, image_functions

from PIL import Image
import math
import os, sys
import shutil
import pickle

from libraries.cv_globals import top_shapes_dir, top_images_dir, frth_smallest_pixc, Lshape_size, internal

main_filename = "10"
image_filename = '10'
image_filename2 = "11"

directory = "videos/street3/resized/min"
top_edge_dir = "videos/street3/resized/"
shapes_type = "intnl_spixcShp"


# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

pixch_dir = top_shapes_dir + directory + "pixch/"
pixch_edge_dir = pixch_dir + "edge/"
shapes_matches_dfile = pixch_edge_dir + image_filename + "." + image_filename2 + "." + main_filename + "shapes.data"
with open (shapes_matches_dfile, 'rb') as fp:
   # {'68957': [['69348'], ['70946']], '71152': [[], []], '71336': [['69348', '71342', ... ], ['70946']]}
   # { im1shapeid used for finding edge matches: [ [ image1 shapeids that matched with edges ], [ image2 shapeids that matched with edges ] ], ... }
   shapes_matches = pickle.load(fp)
fp.close()


shapes_matches_imdir = pixch_edge_dir + image_filename + "." + image_filename2 + "." + main_filename + "shapes/"
# delete and create folder
if os.path.exists(shapes_matches_imdir) == True:
   shutil.rmtree(shapes_matches_imdir)
os.makedirs(shapes_matches_imdir)






if shapes_type == "normal":

   # we need to get every pixel of the shapes
   # return value form is
   # shapes[shapes_id][pixel_index] = {}
   # shapes[shapes_id][pixel_index]['x'] = x
   # shapes[shapes_id][pixel_index]['y'] = y
   im1shapes = read_files_functions.rd_shapes_file(image_filename, directory)
   
elif shapes_type == "intnl_spixcShp":   
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"
   
   shapes_dir = s_pixcShp_intnl_dir + "shapes/"
   shapes_dfile = shapes_dir + image_filename + "shapes.data"
   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()   

   im2shapes_dfile = shapes_dir + image_filename2 + "shapes.data"
   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes_pixels = pickle.load(fp)
   fp.close()   










for edge_id in shapes_matches:
   save_filepath = shapes_matches_imdir + edge_id + ".png"
   image_functions.cr_im_from_shapeslist2( image_filename, directory, shapes_matches[edge_id][0], save_filepath=save_filepath , shapes_rgb=(255,0,0) )
   
   save_filepath = shapes_matches_imdir + edge_id + "im2.png"
   image_functions.cr_im_from_shapeslist2( image_filename, directory, shapes_matches[edge_id][0], save_filepath=save_filepath , shapes_rgb=(0,0,255) )   

































