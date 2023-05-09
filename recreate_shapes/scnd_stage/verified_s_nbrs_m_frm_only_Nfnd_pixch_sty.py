
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
im1file = "14"
im2file = "15"
# if target directory is shape_nbrs_matches, make target_dir emtpy, 
# if it's for only_nfnd_pixch_sty. write "/only_nfnd_pixch_sty/" in target_dir
target_dir = "/only_nfnd_pixch_sty/"
shapes_type = "intnl_spixcShp"


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'


only_nfnd_pixch_sty_Dir = top_shapes_dir + directory + snd_stg_alg_shp_nbrs_dir + target_dir

image_dir = only_nfnd_pixch_sty_Dir + im1file + "." + im2file + "/"
# delete and create folder
if os.path.exists(image_dir) == True:
   shutil.rmtree(image_dir)
os.makedirs(image_dir)


scnd_stage_alg_shp_dfile = only_nfnd_pixch_sty_Dir + im1file + "." + im2file + ".data"
with open (scnd_stage_alg_shp_dfile, 'rb') as fp:
   # [[['3120', '11916'], ['4712', '11515']], [['3294', '2085'], ['4510', '4516']], ... ]
   # [ [ [ image1 shapeids ], [ image2 shapeids ] ], ... ]
   scnd_stage_alg_shp = pickle.load(fp)
fp.close()



for each_scnd_stg_shp_nbrs in scnd_stage_alg_shp:
   # each_scnd_stg_shp_nbrs -> [['3294', '2085'], ['4510', '4516']]
   
   if "49710" in each_scnd_stg_shp_nbrs[0]:
      print( each_scnd_stg_shp_nbrs )
      sys.exit()
   
   save_im1fpath = image_dir + each_scnd_stg_shp_nbrs[0][0] + "im" + im1file + ".png"
   image_functions.cr_im_from_shapeslist2( im1file, directory, each_scnd_stg_shp_nbrs[0], save_filepath=save_im1fpath , shapes_rgb=(255, 0, 0 ) )
   
   save_im2fpath = image_dir + each_scnd_stg_shp_nbrs[0][0] + "im" + im2file + ".png"

   image_functions.cr_im_from_shapeslist2( im2file, directory, each_scnd_stg_shp_nbrs[1], save_filepath=save_im2fpath , shapes_rgb=(0, 0, 255 ) )  
       

   







































