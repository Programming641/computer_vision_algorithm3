# matching in both direction 
# example.  given the files 10.11.10 and 10.11.11
# shapes matched from 10 to 11. are in 10.11.10. shapes matched from 11 to 10 are in 10.11.11
# shapes matched in both directions
from PIL import Image
import pickle
import math
import copy, shutil
import os, sys
from libraries.cv_globals import top_temp_dir, top_shapes_dir, top_images_dir, internal, pixch_sty_dir, snd_stg_alg_shp_nbrs_dir
from libraries.cv_globals import frth_smallest_pixc, Lshape_size, third_smallest_pixc
from libraries import read_files_functions, pixel_shapes_functions, image_functions, pixel_functions, same_shapes_functions
import winsound


directory = "videos/street3/resized/min"
im1file = "11"
im2file = "12"

shapes_type = "intnl_spixcShp"


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'


scnd_stage_alg_shpDir = top_shapes_dir + directory + snd_stg_alg_shp_nbrs_dir + "/only_nfnd_pixch_sty2/"

image1_2_1_dir = scnd_stage_alg_shpDir + im1file + "." + im2file + "." + im1file + "/"
# delete and create folder
if os.path.exists(image1_2_1_dir) == True:
   shutil.rmtree(image1_2_1_dir)
os.makedirs(image1_2_1_dir)

image1_2_2_dir = scnd_stage_alg_shpDir + im1file + "." + im2file + "." + im2file + "/"
# delete and create folder
if os.path.exists(image1_2_2_dir) == True:
   shutil.rmtree(image1_2_2_dir)
os.makedirs(image1_2_2_dir)

scnd_stage_alg_shp_dfile = scnd_stage_alg_shpDir + im1file + "." + im2file + "." + im1file + ".data"
with open (scnd_stage_alg_shp_dfile, 'rb') as fp:
   # [[['3120', '11916'], ['4712', '11515']], [['3294', '2085'], ['4510', '4516']], ... ]
   # [ [ [ image1 shapeids ], [ image2 shapeids ] ], ... ]
   scnd_stage_alg_shp1 = pickle.load(fp)
fp.close()

scnd_stage_alg_shp_dfile = scnd_stage_alg_shpDir + im1file + "." + im2file + "." + im2file + ".data"
with open (scnd_stage_alg_shp_dfile, 'rb') as fp:
   # [[['3120', '11916'], ['4712', '11515']], [['3294', '2085'], ['4510', '4516']], ... ]
   # [ [ [ image1 shapeids ], [ image2 shapeids ] ], ... ]
   scnd_stage_alg_shp2 = pickle.load(fp)
fp.close()


if shapes_type == "normal":
   print("shapes_type normal is not supported in this script ( shp_nbrs_mtch_frm_Nfnd_pixch_sty.py ) ")
   sys.exit()
   
elif shapes_type == "intnl_spixcShp":   
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"
   
   shapes_dir = s_pixcShp_intnl_dir + "shapes/"
   shapes_dfile = shapes_dir + im1file + "shapes.data"

   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()   

   im2shapes_dfile = shapes_dir + im2file + "shapes.data"
   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()   


for each_shape_match in scnd_stage_alg_shp1:
   # each_shape_match -> [['62436', '73262', '75268'], ['67217', '75643', '65662']]
   im1save_fpath = image1_2_1_dir + each_shape_match[0][0] + ".png"
   image_functions.cr_im_from_shapeslist2( im1file, directory, each_shape_match[0], save_filepath=im1save_fpath , shapes_rgb=(255, 0, 0 ) )
   
   im2save_fpath = image1_2_1_dir + each_shape_match[0][0] + "im2.png"
   image_functions.cr_im_from_shapeslist2( im2file, directory, each_shape_match[1], save_filepath=im2save_fpath , shapes_rgb=(0, 0, 255 ) )


for each_shape_match in scnd_stage_alg_shp2:
   # each_shape_match -> [['62436', '73262', '75268'], ['67217', '75643', '65662']]
   im1save_fpath = image1_2_2_dir + each_shape_match[0][0] + ".png"
   image_functions.cr_im_from_shapeslist2( im1file, directory, each_shape_match[0], save_filepath=im1save_fpath , shapes_rgb=(255, 0, 0 ) )
   
   im2save_fpath = image1_2_2_dir + each_shape_match[0][0] + "im2.png"
   image_functions.cr_im_from_shapeslist2( im2file, directory, each_shape_match[1], save_filepath=im2save_fpath , shapes_rgb=(0, 0, 255 ) )











































