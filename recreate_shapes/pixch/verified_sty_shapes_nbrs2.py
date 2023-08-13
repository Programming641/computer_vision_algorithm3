# find matches between pixel change shape boundaries and large shape boundaries

from PIL import Image
import re, pickle
import shutil

import os, sys
from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, pixch_sty_dir
from libraries import read_files_functions, pixel_shapes_functions, image_functions


directory = "videos/street3/resized/min"

im1file = "14"
im2file = "15"
shapes_type = "intnl_spixcShp"

# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

nxt_im1 = str( int(im1file) + 1 )
nxt_im2 = str( int(im2file) + 1 )

sty_shapes_nbrs_dir = top_shapes_dir + directory + pixch_sty_dir + "/nbrs/"
sty_shapes_file = sty_shapes_nbrs_dir + "data/" + im1file + "." + im2file + "verified.data"
with open (sty_shapes_file, 'rb') as fp:
   # [ [ [ ['21455', '12641'], ['22257', '13043'] ], [ ['22257', '13043'], ['25045', '13044'] ] ], ... ]
   # [ [ [ [ image1 shapeid, image1 neighbor ], [ image2 shapeid, image2 neighbor ] ], [ [ next image1 shapeid, next image1 neighbor ], 
   #       [ next image2 shapeid, next image2 neighbor ] ]   ], ... ]
   sty_shapes_nbrs = pickle.load(fp)
fp.close()

sty_shapes_nbrs_imdir = sty_shapes_nbrs_dir + im1file + "." + im2file + "verified/"
# delete and create folder
if os.path.exists(sty_shapes_nbrs_imdir) == True:
   shutil.rmtree(sty_shapes_nbrs_imdir)
os.makedirs(sty_shapes_nbrs_imdir)



for each_sty_shapes_nbrs in sty_shapes_nbrs:
   # [[['34489', '29754'], ['35356', '18959']], [['35356', '18959'], ['34163', '19360']]]

   save_im1fpath = sty_shapes_nbrs_imdir + each_sty_shapes_nbrs[0][0][0] + "." + each_sty_shapes_nbrs[0][1][0]  + \
                   each_sty_shapes_nbrs[1][1][0] + "im1.png"
   image_functions.cr_im_from_shapeslist2( im1file, directory, each_sty_shapes_nbrs[0][0], save_filepath=save_im1fpath , shapes_rgb=(255,0,0) )

   save_im2fpath = sty_shapes_nbrs_imdir + each_sty_shapes_nbrs[0][0][0] + "." + each_sty_shapes_nbrs[0][1][0]  + \
                   each_sty_shapes_nbrs[1][1][0] + "im2.png"
   image_functions.cr_im_from_shapeslist2( im2file, directory, each_sty_shapes_nbrs[0][1], save_filepath=save_im2fpath , shapes_rgb=(0,0,255) )

   save_im3fpath = sty_shapes_nbrs_imdir + each_sty_shapes_nbrs[0][0][0] + "." + each_sty_shapes_nbrs[0][1][0]  + \
                   each_sty_shapes_nbrs[1][1][0] + "im3.png"
   image_functions.cr_im_from_shapeslist2( nxt_im2, directory, each_sty_shapes_nbrs[1][1], save_filepath=save_im3fpath , shapes_rgb=(0,255,0) )
















