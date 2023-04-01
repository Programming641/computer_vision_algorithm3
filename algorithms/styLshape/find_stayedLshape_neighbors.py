# find stayed large shapes neighbors
# if neighbors are stayed large shapes themselves, combine them together
import tkinter
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions, same_shapes_btwn_frames, read_files_functions, image_functions, pixel_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir, styLshapes_w_nbrs, styLshapes, styLshapes_wo_pixch, internal
from libraries.cv_globals import Lshape_size
import pickle
import math
import winsound
import sys, os
import copy

filename1 = "12"
directory = "videos/street3/resized/min"
filename2 = "13"
shapes_type = "intnl_spixcShp"


# image_num -> data type is integer. 0 = image1, 1 = image2
def find_n_process_neighbor( cur_Lshape, image_num, cur_stayed_shapes, already_processed_neighbors ):
   if cur_Lshape in already_processed_neighbors or cur_Lshape in cur_stayed_shapes:
      return

   already_processed_neighbors.append( cur_Lshape )
   
   # get image1 shape's large shape neighbor
   if image_num == 0:
      neighbors =  im1shape_nbrs[ cur_Lshape[image_num] ]
   elif image_num == 1:
      neighbors = im2shape_nbrs[ cur_Lshape[image_num] ]
   else:
      print("ERROR at find_stayedLshape_neighbors.py:process_neighbors image_num " + str( image_num ) + " is not supported" )
      sys.exit()
   
   if len( neighbors ) <= 0:
      print("ERROR at find_stayedLshape_neighbors.py:process_neighbors all shape has to have neighbors")
      sys.exit()

   
   cur_neighbors = []
   for neighbor in neighbors:
      if image_num == 0:
         if len( im1shapes[neighbor] ) >= Lshape_size:
            cur_neighbors.append( neighbor )
      elif image_num == 1:
         if len( im2shapes[neighbor] ) >= Lshape_size:
            cur_neighbors.append( neighbor )

      
   if len( cur_neighbors ) == 0:
      return

   for cur_neighbor in cur_neighbors:
      cur_nbr_pairs = None
      if image_num == 0:   
         cur_nbr_pairs = [ shapes for shapes in all_styLshapes if cur_neighbor == shapes[image_num] ]

      
      elif image_num == 1:
         cur_nbr_pairs = [ shapes for shapes in all_styLshapes if cur_neighbor == shapes[image_num] ]


      if cur_nbr_pairs is not None and len(cur_nbr_pairs) >= 1:
         for cur_nbr_pair in cur_nbr_pairs:
            cur_stayed_shapes.append( cur_nbr_pair )
         
            find_n_process_neighbor( cur_nbr_pair, image_num, cur_stayed_shapes, already_processed_neighbors )






# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'


print("preparing data. please wait...")

styLshapes_Ddir = top_shapes_dir + directory + styLshapes + "/" + shapes_type + "/data/"
styLshapes_wo_pixch_Ddir = top_shapes_dir + directory + styLshapes_wo_pixch + "/" + shapes_type + "/data/"
styLshapes_w_neighbors_Ddir = top_shapes_dir + directory + styLshapes_w_nbrs + "/" + shapes_type + "/data/"
styLshapes1to2_dfile = styLshapes_Ddir + filename1 + "." + filename2 + ".data"
styLshapes_wo_pixch_dfile = styLshapes_wo_pixch_Ddir + filename1 + "." + filename2 + ".data"


with open (styLshapes1to2_dfile, 'rb') as fp:
   # [ ['21455', '22257'], ... ]
   # [ [ image1 shapeid, image2 shapeid ], ... ]
   styLshapes1to2 = pickle.load(fp)
fp.close()

with open (styLshapes_wo_pixch_dfile, 'rb') as fp:
   #  [ ['79999', '79936', ['78799', '78399', ... ] ], ... ]
   #  [ [ im1shapeid, im2shapeid, matched_pixels ], ... ]
   styLshapes_wo_pixch_data = pickle.load(fp)
fp.close()


all_styLshapes = []
for shapes  in styLshapes_wo_pixch_data:
   temp = [ shapes[0], shapes[1] ]
   
   if temp not in styLshapes1to2:
      all_styLshapes.append( temp )

all_styLshapes.extend( styLshapes1to2 )


if shapes_type == "normal":
   # returned value has below form
   # shapes[shapes_id][pixel_index] = {}
   # shapes[shapes_id][pixel_index]['x'] = x
   # shapes[shapes_id][pixel_index]['y'] = y
   im1shapes = read_files_functions.rd_shapes_file(filename1, directory)
   im2shapes = read_files_functions.rd_shapes_file(filename2, directory)   
   
   for im1shapeid in im1shapes:
      im1shapes[im1shapeid] = list( im1shapes[im1shapeid].keys() )
   for im2shapeid in im2shapes:
      im2shapes[im1shapeid] = list( im2shapes[im2shapeid].keys() )


   im1nbr_filepath = top_shapes_dir + directory + "shape_nbrs/" + filename1 + "_shape_nbrs.txt"
   im2nbr_filepath = top_shapes_dir + directory + "shape_nbrs/" + filename2 + "_shape_nbrs.txt"
   
elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"
   shapes_dir = s_pixcShp_intnl_dir + "shapes/"

   shapes_dfile = shapes_dir + filename1 + "shapes.data"
   im2shapes_dfile = shapes_dir + filename2 + "shapes.data"

   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()

   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()  

   
   im1nbr_filepath = s_pixcShp_intnl_dir + "shape_nbrs/" + filename1 + "_shape_nbrs.txt"
   im2nbr_filepath = s_pixcShp_intnl_dir + "shape_nbrs/" + filename2 + "_shape_nbrs.txt"



# {"shapeid": ["nbr_shapeid", "nbr_shapeid", ...], ...  }
im1shape_nbrs = read_files_functions.rd_dict_k_v_l(filename1, directory, im1nbr_filepath)
im2shape_nbrs = read_files_functions.rd_dict_k_v_l(filename2, directory, im2nbr_filepath)





print("data preparation complete. now main process begins")


all_stayed_shapes = {}
same_im1shapeids = []
for styLshape in all_styLshapes:
   cur_stayed_shapes = []
   already_processed_neighbors = []
   
   # find image1 shape's neighbors from stayed large shapes. put together all image1 shape's neighbors along with
   # image1 neighbor's matched image2 shapes
   find_n_process_neighbor( styLshape, 0, cur_stayed_shapes, already_processed_neighbors )

   
   if len(cur_stayed_shapes) >= 1:
      if styLshape not in cur_stayed_shapes:
         cur_stayed_shapes.insert(0, styLshape )
      
      # the image1 shapeid from first image1 image2 pair becomes the all_stayed_shapes's shapeid
      # because there may be multiple same image1 shapes, take count of it
      shapeid_count = same_im1shapeids.count( cur_stayed_shapes[0][0] )
      same_im1shapeids.append( cur_stayed_shapes[0][0] )
      all_stayed_shapes[ cur_stayed_shapes[0][0] + "." + str( shapeid_count + 1 ) ] = cur_stayed_shapes



if os.path.exists(styLshapes_w_neighbors_Ddir ) == False:
   os.makedirs(styLshapes_w_neighbors_Ddir)

styLshapes_w_neighbors_dfile = styLshapes_w_neighbors_Ddir + filename1 + "." + filename2 + ".data"
with open(styLshapes_w_neighbors_dfile, 'wb') as fp:
   pickle.dump(all_stayed_shapes, fp)
fp.close()



































































