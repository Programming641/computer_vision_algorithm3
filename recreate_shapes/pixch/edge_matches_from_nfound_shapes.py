import re
import math
import os, sys
import shutil
import pickle

from PIL import Image

from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir
from libraries import image_functions, read_files_functions

main_filename = "10"
image_filename = "10"
image_filename2 = "11"
directory = "videos/street3/resized/min"
shapes_type = "intnl_spixcShp"


# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'







pixch_edge_dir = top_shapes_dir + directory + "pixch/edge/"
pixch_edge_dfile = pixch_edge_dir + image_filename + "." + image_filename2 + "." + main_filename + ".data"
with open (pixch_edge_dfile, 'rb') as fp:
   # {'74749': [{(351, 181), ... }, {(353, 181), ... }]}
   # { image1shapeid: [ { matched image1 edges }, { matched image2 edges } ], ... }
   pixch_edges = pickle.load(fp)
fp.close()


imdir = pixch_edge_dir + image_filename + "." + image_filename2 + "/"
# delete and create folder
if os.path.exists(imdir) == True:
   shutil.rmtree(imdir)
os.makedirs(imdir)



for im1shapeid in pixch_edges:
   
   im1save_filepath = imdir + im1shapeid + ".png"
   image_functions.cr_im_from_pindexes( image_filename, directory, pixch_edges[im1shapeid][0], save_filepath=im1save_filepath , pixels_rgb=(255, 0, 0 ) )

   im2save_filepath = imdir + im1shapeid + "im2edges.png"
   image_functions.cr_im_from_pindexes( image_filename2, directory, pixch_edges[im1shapeid][1], save_filepath=im2save_filepath , pixels_rgb=(0, 0, 255 ) )

























