
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
main_fname = "13"
im1file = "12"
im2file = "13"

shapes_type = "intnl_spixcShp"


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'


scnd_stage_alg_shpDir = top_shapes_dir + directory + snd_stg_alg_shp_nbrs_dir + "/only_nfnd_pixch_sty/"

image_dir = scnd_stage_alg_shpDir + im1file + "." + im2file + "." + main_fname + "/"
# delete and create folder
if os.path.exists(image_dir) == True:
   shutil.rmtree(image_dir)
os.makedirs(image_dir)


scnd_stage_alg_shp_dfile = scnd_stage_alg_shpDir + im1file + "." + im2file + "." + main_fname + ".data"
with open (scnd_stage_alg_shp_dfile, 'rb') as fp:
   # [[['3120', '11916'], ['4712', '11515']], [['3294', '2085'], ['4510', '4516']], ... ]
   # [ [ [ image1 shapeids ], [ image2 shapeids ] ], ... ]
   scnd_stage_alg_shp = pickle.load(fp)
fp.close()

if main_fname == im2file:
   im2file = im1file

if shapes_type == "normal":
   print("shapes_type normal is not supported in this script ( shp_nbrs_mtch_frm_Nfnd_pixch_sty.py ) ")
   sys.exit()
   
elif shapes_type == "intnl_spixcShp":   
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"
   
   shapes_dir = s_pixcShp_intnl_dir + "shapes/"
   shapes_dfile = shapes_dir + main_fname + "shapes.data"

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


for each_scnd_stg_shp_nbrs in scnd_stage_alg_shp:
   # each_scnd_stg_shp_nbrs -> [['3294', '2085'], ['4510', '4516']]
   
   save_im1fpath = image_dir + each_scnd_stg_shp_nbrs[0][0] + "im" + main_fname + ".png"
   image_functions.cr_im_from_shapeslist2( main_fname, directory, each_scnd_stg_shp_nbrs[0], save_filepath=save_im1fpath , shapes_rgb=(255, 0, 0 ) )
   
   save_im2fpath = image_dir + each_scnd_stg_shp_nbrs[0][0] + "im" + im2file + ".png"

   image_functions.cr_im_from_shapeslist2( im2file, directory, each_scnd_stg_shp_nbrs[1], save_filepath=save_im2fpath , shapes_rgb=(0, 0, 255 ) )  
       

   







































