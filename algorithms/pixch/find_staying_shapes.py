# if most of pixel changes occur near the shape boundaries and not inside the shape, then the shape
# moved only a little
from libraries import pixel_functions, read_files_functions, pixel_shapes_functions

from PIL import Image
import math
import os, sys
import winsound
import pickle

from libraries.cv_globals import top_shapes_dir, top_images_dir, frth_smallest_pixc, Lshape_size, internal

image_filename = '14'
image_filename2 = "15"
swap_filename = True

directory = "videos/street3/resized/min"
shapes_type = "intnl_spixcShp"


if len(sys.argv) >= 2:
   # excluding .png extension 
   image_filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   image_filename2 = sys.argv[1][0: len( sys.argv[1] ) - 4 ]
   swap_filename = sys.argv[2]
   directory = sys.argv[3]
   
   print("execute find_mid_changed_shapes.py " + directory + " " + image_filename + " " + str(swap_filename) )



# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

original_image = Image.open(top_images_dir + directory + image_filename + ".png")
im_width, im_height = original_image.size

pixch_dir = top_shapes_dir + directory + "pixch/"
pixch_dfile = pixch_dir + "data/"  + image_filename + "." + image_filename2 + ".data"
with open (pixch_dfile, 'rb') as fp:
   # [ strings of pixel indexes ]
   pixch = pickle.load(fp)
fp.close()

if swap_filename is True:
   temp_finame = image_filename
   image_filename = image_filename2
   image_filename2 = temp_finame





pixch_sty_shapes_dir = pixch_dir + "sty_shapes/"
if os.path.exists(pixch_sty_shapes_dir ) == False:
   os.makedirs(pixch_sty_shapes_dir)
sty_shapes_ddir = pixch_sty_shapes_dir + "data/"
if os.path.exists(sty_shapes_ddir ) == False:
   os.makedirs(sty_shapes_ddir)



set_pixch = set()
# for searching near boundary pixels in pixch, convert list of string pixels to set of (x,y)
for pixel in pixch:
   xy = pixel_functions.convert_pindex_to_xy( pixel, im_width )
   set_pixch.add( xy )


# { shapeid: [(379, 154), (380, 154), (379, 155), (379, 156), ... ], ... }
shapes_boundaries = {}
if shapes_type == "normal":
   # return value form is
   # shapes[shapes_id][pixel_index] = {}
   # shapes[shapes_id][pixel_index]['x'] = x
   # shapes[shapes_id][pixel_index]['y'] = y
   im_shapes = read_files_functions.rd_shapes_file(image_filename, directory)

   for shapeid in im_shapes:
      shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels( im_shapes[shapeid] )

   for shapeid in im_shapes:
      cur_pixels = set()
      for pixel in im_shapes[shapeid].keys():
         xy = pixel_functions.convert_pindex_to_xy( pixel, im_width )
         cur_pixels.add( xy )
      
      im_shapes[shapeid] = cur_pixels


   
elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"
   shapes_dir = s_pixcShp_intnl_dir + "shapes/"

   shapes_dfile = shapes_dir + image_filename + "shapes.data"
   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im_shapes = pickle.load(fp)
   fp.close()

   for shapeid in im_shapes:
      cur_pixels = set()
      for pixel in im_shapes[shapeid]:
         xy = pixel_functions.convert_pindex_to_xy( pixel, im_width )
         cur_pixels.add( xy )
      
      im_shapes[shapeid] = cur_pixels

   for shapeid in im_shapes:
      shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels( im_shapes[shapeid] )


   im2shapes_dfile = shapes_dir + image_filename2 + "shapes.data"
   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()
   
   
   


# prepare im2shapes for searching shape by pixel index number
im2shapes_by_pindex = {}
for shapeid in im2shapes:
   for pindex in im2shapes[shapeid]:
      im2shapes_by_pindex[pindex] = shapeid


im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(image_filename, directory, shapes_type=shapes_type, min_colors=True)
im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(image_filename2, directory, shapes_type=shapes_type, min_colors=True)

stayed_shapes = []
for shapeid in shapes_boundaries:
   cur_shape_size = len( im_shapes[shapeid] )
   boundary_pix_len = len( shapes_boundaries[shapeid] )
   if cur_shape_size < frth_smallest_pixc:
      continue
      
   # if boundary is 50% or more of the whole pixels, then near_boundary_value is 0
   #                30% to less than 50% -> 1
   #                less than 30% -> 2
   near_boundary_value = None
   if boundary_pix_len / cur_shape_size >= 0.5:
      near_boundary_value = 0
   elif boundary_pix_len / cur_shape_size < 0.5 and boundary_pix_len / cur_shape_size >= 0.3:
      near_boundary_value = 1
   else:
      near_boundary_value = 2
   
   near_bnd_pixels = set()
   for boundary_pixel in shapes_boundaries[shapeid]:
      # shapes_boundaries[shapeid] -> [(379, 154), (380, 154), (379, 155), (379, 156), ... ]
      # cur_bnd_pixels -> [ (379, 154), ... ]
      cur_bnd_pixels = pixel_functions.get_vicinity_pixels( boundary_pixel, near_boundary_value, original_image.size )
      cur_bnd_pixels = set( cur_bnd_pixels )
      
      # keep in mind that near boundary pixels are not just pixels of the current shape. they will contain pixels of 
      # neighbor shapes "near the boundaries".
      near_bnd_pixels |= cur_bnd_pixels
         
   cur_shape_pixch_count = im_shapes[shapeid].intersection( set_pixch )
      
   near_bnd_pixch = near_bnd_pixels.intersection( set_pixch )

   cur_shape_pixch_percent = len( cur_shape_pixch_count ) / cur_shape_size
      
   # if shape's pixch are less than 50% and most of those pixch are near the boundaries then, this shape moved only 
   # a little
   if len( near_bnd_pixch ) > 0 and len( cur_shape_pixch_count ) > 0:
      if cur_shape_pixch_percent < 0.5 and len( near_bnd_pixch ) / len( cur_shape_pixch_count ) >= 0.8:
         # more than 80% of pixch are near the boundaries.
         
         # find image2 shape that matches the most with the current image1 shape
         # matched_im2shapes -> { im2shapeid: matched score, ... }
         matched_im2shapes = {}
         for im1xy in im_shapes[shapeid]:
            im1pindex = pixel_functions.convert_xy_to_pindex( im1xy, im_width )
            im1pindex = str(im1pindex)
            
            if not im2shapes_by_pindex[im1pindex] in matched_im2shapes.keys():
               # image2 shape that has current image1 pixel is not already added in matched_im2shapes yet.
               matched_im2shapeid = im2shapes_by_pindex[im1pindex]
               matched_im2shapes[ matched_im2shapeid ] = 1
            else:
               matched_im2shapeid = im2shapes_by_pindex[im1pindex]
               matched_im2shapes[ matched_im2shapeid ] += 1   
         
         highest_matched_count = max( [ matched_count for matched_count in matched_im2shapes.values() ] )
         most_matched_im2shape = [ shape for shape, matched_count in matched_im2shapes.items() if matched_count == highest_matched_count ][0]
         
         if im1shapes_colors[shapeid] == im2shapes_colors[most_matched_im2shape]:

            if swap_filename is False:
               stayed_shapes.append( (shapeid, most_matched_im2shape) )
            else:
               stayed_shapes.append( (most_matched_im2shape, shapeid) )
         

if swap_filename is False:
   with open(sty_shapes_ddir + image_filename + "." + image_filename2 + "." + image_filename + ".data", 'wb') as fp:
      pickle.dump(stayed_shapes, fp)
   fp.close()

else:
   with open(sty_shapes_ddir + image_filename2 + "." + image_filename + "." + image_filename + ".data", 'wb') as fp:
      pickle.dump(stayed_shapes, fp)
   fp.close()





frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)






