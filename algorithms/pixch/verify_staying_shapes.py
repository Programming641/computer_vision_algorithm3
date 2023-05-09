
from libraries import pixel_functions, read_files_functions, pixel_shapes_functions, same_shapes_functions

from PIL import Image
import math
import os, sys
import winsound
import pickle

from libraries.cv_globals import top_shapes_dir, top_images_dir, frth_smallest_pixc, Lshape_size, third_smallest_pixc, internal

im1file = '14'
im2file = "15"

directory = "videos/street3/resized/min"
shapes_type = "intnl_spixcShp"


# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

original_image = Image.open(top_images_dir + directory + im1file + ".png")
im_width, im_height = original_image.size

pixch_dir = top_shapes_dir + directory + "pixch/"
pixch_sty_shapes_dir = pixch_dir + "sty_shapes/"
sty_shapes_ddir = pixch_sty_shapes_dir + "data/"

sty_shapes1_dfile = sty_shapes_ddir + im1file + "." + im2file + "." + im1file + ".data"
sty_shapes2_dfile = sty_shapes_ddir + im1file + "." + im2file + "." + im2file + ".data"

with open (sty_shapes1_dfile, 'rb') as fp:
   # [('1270', '2072'), ('2062', '2062'), ... ]
   # [ ( image1 shapeid, image2 shapeid ), ... ]
   sty_shapes1 = pickle.load(fp)
fp.close()

with open (sty_shapes2_dfile, 'rb') as fp:
   # [('1270', '2072'), ('2062', '2062'), ... ]
   # [ ( image1 shapeid, image2 shapeid ), ... ]
   sty_shapes2 = pickle.load(fp)
fp.close()

all_staying_shapes = set()
for sty_shape in sty_shapes1:
   all_staying_shapes.add( sty_shape )
for sty_shape in sty_shapes2:
   all_staying_shapes.add( sty_shape )

print( len( all_staying_shapes ) )


if shapes_type == "normal":
   print("shapes_type normal is not supported in " + os.path.basename(__file__) )
   sys.exit()
   

elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"

   shapes_dir = s_pixcShp_intnl_dir + "shapes/"
   shapes_dfile = shapes_dir + im1file + "shapes.data"
   im2shapes_dfile = shapes_dir + im2file + "shapes.data"

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


   shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + im1file + "_shape_nbrs.txt"
   im2shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + im2file + "_shape_nbrs.txt"



# {'79999': ['71555', '73953', ...], ...}
im1shapes_neighbors = read_files_functions.rd_dict_k_v_l(im1file, directory, shape_neighbors_file)
im2shapes_neighbors = read_files_functions.rd_dict_k_v_l(im2file, directory, im2shape_neighbors_file)

im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im1file, directory, shapes_type=shapes_type)
im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im2file, directory, shapes_type=shapes_type)


verified_matches = same_shapes_functions.verify_matches( all_staying_shapes, [ im1shapes, im2shapes ], [ im1shapes_colors, im2shapes_colors ], 
                   [ im1shapes_neighbors, im2shapes_neighbors ], im_width  )


'''
# this time, check if shapes locations match
# image1 shape1 and its neighbor, let's call it image1 neighbor1
# get where image1 nighbor1 is attached at image1 shape1
# image1 shape1 matched pair image2 shape1
# image1 neighbor1 matched pair image2 neighbor1
# see if image2 neighbor1 attachment location of image2 shape1 is the same as the attachment location of image1 neighbor1 and image1 shape1
for sty_shapes in all_staying_shapes:
   temp = set()
   temp.add( sty_shapes )
   found = temp.intersection( verified_shapes )
   
   if len( found ) == 1:
      continue
   
   if sty_shapes[0] != "78049":
      continue
   
   
   
   for im1shape_nbr in im1shapes_neighbors[sty_shapes[0]]:
      # found_sty_im1nbrs contain neighbors of image1 shape in sty_shapes 
      found_sty_im1nbrs = [ temp_shapes for temp_shapes in all_staying_shapes if temp_shapes[0] == im1shape_nbr ]
      
      for found_sty_im1nbr in found_sty_im1nbrs:
         
         _attached_near = pixel_shapes_functions.check_shape_attached_near( im1shapes_boundaries[sty_shapes[0]], im1shapes_boundaries[found_sty_im1nbr[0]],
                                                                                     im2shapes_boundaries[sty_shapes[1]], im2shapes_boundaries[found_sty_im1nbr[1]],
                                                                                     original_image.size )
         
         _nbr_attached_near = pixel_shapes_functions.check_shape_attached_near( im1shapes_boundaries[found_sty_im1nbr[0]], im1shapes_boundaries[sty_shapes[0]],
                                                                                     im2shapes_boundaries[found_sty_im1nbr[1]], im2shapes_boundaries[sty_shapes[1]],
                                                                                     original_image.size )         
         
         if _attached_near is True and _nbr_attached_near is True:
            
            if im1shapes_colors[ found_sty_im1nbr[0] ] != im2shapes_colors[ found_sty_im1nbr[1] ]:
               continue
            
            im1shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( im1shapes[found_sty_im1nbr[0]], im_width, param_shp_type=1 )  
            im2shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( im2shapes[found_sty_im1nbr[1]], im_width, param_shp_type=1 )
   
            im1_im2_nbr_match = same_shapes_functions.match_shape_while_moving_it( im1shp_coord_xy, im2shp_coord_xy )
            im2_im1_nbr_match = same_shapes_functions.match_shape_while_moving_it( im2shp_coord_xy, im1shp_coord_xy )
            if im1_im2_nbr_match is True and im2_im1_nbr_match is True:   
               print("matched shapes")
               print( sty_shapes )
               print( found_sty_im1nbr )
               
               verified_shapes.add( sty_shapes )
               verified_shapes.add( found_sty_im1nbr )

'''


print( len( verified_matches ) )


with open(sty_shapes_ddir + im1file + "." + im2file + "verified.data", 'wb') as fp:
   pickle.dump(verified_matches, fp)
fp.close()









frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)






