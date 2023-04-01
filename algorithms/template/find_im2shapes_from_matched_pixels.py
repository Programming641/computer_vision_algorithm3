

from PIL import Image
import re, pickle
import math
import shutil

import os, sys
from libraries.cv_globals import top_shapes_dir, top_images_dir, frth_smallest_pixc
from libraries import read_files_functions, image_functions, pixel_shapes_functions, pixel_functions



directory = "videos/street3/resized/min"
im1file = "11"
im2file = "12"
shapes_type = "intnl_spixcShp"


if len(sys.argv) > 1:
   im1file = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   im2file = sys.argv[1][0: len( sys.argv[1] ) - 4 ]

   directory = sys.argv[3]

   print("execute script findim_pixch.py. file1 " + im1file + " file2 " + im2file + " directory " + directory )




# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

pixel_template_dir = top_shapes_dir + directory + "template/" + "pixels/"
pixel_template_ddir = pixel_template_dir + "data/"
pixel_template_file = pixel_template_ddir + im1file + "." + im2file + ".data"


pixel_shape_tmpl_dir = pixel_template_dir + "shapes/"
pixel_shape_tmpl_ddir = pixel_shape_tmpl_dir + "data/"
pixel_shape_tmpl_imdir = pixel_shape_tmpl_dir + im1file + "." + im2file + "/"


if os.path.exists(pixel_shape_tmpl_dir ) == False:
   os.makedirs(pixel_shape_tmpl_dir )
if os.path.exists(pixel_shape_tmpl_ddir ) == False:
   os.makedirs(pixel_shape_tmpl_ddir )
# delete and create folder
if os.path.exists(pixel_shape_tmpl_imdir) == True:
   shutil.rmtree(pixel_shape_tmpl_imdir)
os.makedirs(pixel_shape_tmpl_imdir)




with open (pixel_template_file, 'rb') as fp:
   # [[{'2577': 173.46, 'nbrs': ['2985'], 'im2pixels': [182, 183]}, {'2577': 173.46, 'nbrs': ['2985'], 'im2pixels': [ 1790, 1791]}, ... ], ... ]
   # [ [ { image1shapeid: matched score, "nbrs": [ image1 shape neighbors ], "im2pixels" : [ image2 pixels ] }, ... ], ... ]
   # if there are multiple {} then they all have the same image1shapeid with the same score but different nbrs or im2pixels.
   template_pixels = pickle.load(fp)
fp.close()


if shapes_type == "normal":

   # return value form is
   # shapes[shapes_id][pixel_index] = {}
   # shapes[shapes_id][pixel_index]['x'] = x
   # shapes[shapes_id][pixel_index]['y'] = y
   im1shapes = read_files_functions.rd_shapes_file(im1file, directory)
   for im1shapeid in im1shapes:
      im1shapes[im1shapeid] = list( im1shapes[im1shapeid].keys() )
   im2shapes = read_files_functions.rd_shapes_file(im2file, directory)
   for im2shapeid in im2shapes:
      im2shapes[im1shapeid] = list( im2shapes[im2shapeid].keys() )

   im1shapes_neighbors_path = top_shapes_dir + directory + "shape_nbrs/" + im1file + "_shape_nbrs.txt"
   im2shapes_neighbors_path = top_shapes_dir + directory + "shape_nbrs/" + im2file + "_shape_nbrs.txt"  



elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/internal/"

   shapes_dfile = s_pixcShp_intnl_dir + "shapes/" + im1file + "shapes.data"
   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()
   im2shapes_dfile = s_pixcShp_intnl_dir + "shapes/" + im2file + "shapes.data"
   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()  

   im1shapes_neighbors_path = s_pixcShp_intnl_dir + "shape_nbrs/" + im1file + "_shape_nbrs.txt"
   im2shapes_neighbors_path = s_pixcShp_intnl_dir + "shape_nbrs/" + im2file + "_shape_nbrs.txt"


# {"shapeid": ["nbr_shapeid", "nbr_shapeid", ...], ...  }
im1shape_nbrs = read_files_functions.rd_dict_k_v_l(im1file, directory, im1shapes_neighbors_path)
im2shape_nbrs = read_files_functions.rd_dict_k_v_l(im2file, directory, im2shapes_neighbors_path)

# it takes so much time to see what shape contains the specific pixel, we prepare pixel and shapeid pair.
# { pixel: shapeid, pixel: shapeid, ... }
im2shape_by_pixel = {}
for im2shapeid, pixels in im2shapes.items():
   for pixel in pixels:
      im2shape_by_pixel[pixel] = im2shapeid






results = []
for shapeid_list in template_pixels:
   # shapeid_list -> [{'2577': 173.46, 'nbrs': ['2985'], 'im2pixels': [182, 183]}, {'2577': 173.46, 'nbrs': ['2985'], 'im2pixels': [ 1790, 1791]}, ... ]
   cur_shapeid_results = []
   for one_shapeid in shapeid_list:
      # one_shapeid -> {'2577': 173.46, 'nbrs': ['2985'], 'im2pixels': [182, 183]}
      
      # get all image2 shapeids that have im2pixels from one_shapeid
      im2shapeids = set()
      for im2pixel in one_shapeid["im2pixels"]:
         im2shapeids.add( im2shape_by_pixel[str(im2pixel)] )
      
      
      # now that I have all im2shapeids, check if they are neighbors to each other. but here is one thing to 
      # consider. example. there are 4 shapes, 1, 2, 3, 4.
      # 1 and 2 are neighbors to each other. 3 and 4 are neighbors to each other. but 1 and 2 are not neighbors to
      # 3 and 4 and vice versa.
      # should all shapes are neighbors all together? or can I take them if they have at least one neighbor?
      # I go with the at least one neighbor for now.
      
      all_neighbors = set()
      for im2shapeid in im2shapeids:
         # see if current im2shapeid has neighbors in im2shapeids
         found_neighbors = [ shape for shape in im2shapeids if shape in im2shape_nbrs[im2shapeid]  ]         

         all_neighbors |= set( found_neighbors )
         
      
      if len(all_neighbors) == 0:
         continue

      cur_im1shapeid = [ key for key in one_shapeid.keys() if key != "nbrs" or key != "im2pixels" ][0]
      
      cur_shapeid_results.append( { cur_im1shapeid: one_shapeid[cur_im1shapeid], "nbrs": one_shapeid["nbrs"], "im2shapeids": all_neighbors } )
      
   
   results.append( cur_shapeid_results )



with open(pixel_shape_tmpl_ddir  + im1file + "." + im2file + ".data", 'wb') as fp:
   pickle.dump(results, fp)
fp.close()


# now recreate images
progress_counter = len( results )
for result in results:
   print( str( progress_counter ) + " remaining" )
   progress_counter -= 1

   # result -> [{'2577': 173.46, 'nbrs': ['2985'], 'im2shapeids': { '2182', '185', '5419', '162', '166'}}, 
   #            {'2577': 173.46, 'nbrs': ['2985'], 'im2shapeids': { '1777', '1779', '166'}}]
   for each_shapeid in result:
      # each_shapeid -> {'2577': 173.46, 'nbrs': ['2985'], 'im2shapeids': { '1777', '1779', '166'}}
      
      cur_im1shapes = []
      cur_im1shapeid = [ key for key in each_shapeid.keys() if key != "nbrs" or key != "im2pixels" ][0]
      cur_im1shapes.append( cur_im1shapeid )
      cur_im1shapes.extend( each_shapeid["nbrs"] )
      

      save_filepath = pixel_shape_tmpl_imdir + "im1." + cur_im1shapeid + ".png"
                  
      # creating image for each shapeid inside each_LRUD_shapes or should I combine all shapes inside each_LRUD_shapes?     
      image_functions.cr_im_from_shapeslist2( im1file, directory, cur_im1shapes, save_filepath=save_filepath )

      save_filepath = pixel_shape_tmpl_imdir + "im1." + cur_im1shapeid + "im2shapes.png"
                  
      # creating image for each shapeid inside each_LRUD_shapes or should I combine all shapes inside each_LRUD_shapes?     
      image_functions.cr_im_from_shapeslist2( im2file, directory, each_shapeid["im2shapeids"], save_filepath=save_filepath ) 



























