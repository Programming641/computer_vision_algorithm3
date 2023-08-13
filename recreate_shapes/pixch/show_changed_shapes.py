
from libraries import image_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir
import pickle
import sys
import math
from PIL import Image


pixch_imfile = "10"
pixch_im1 = "10"
pixch_im2 = "11"
# changed_shp_type -> most_ch or mid_ch
changed_shp_type = "mid_ch"
directory = "videos/street3/resized/min"

pixch_shapes_color = ( 255, 0, 0 )

# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'


pixch_shapes_file = top_shapes_dir + directory + "pixch/data/" + pixch_im1 + "." + pixch_im2 + "." + pixch_imfile + changed_shp_type + ".data"

intnl_spixcShp_shapes_file = top_shapes_dir + directory + "shapes/intnl_spixcShp/data/" + pixch_imfile + "shapes.data"

with open (pixch_shapes_file, 'rb') as fp:
   # [ 'shapeid', 'shapeid', ... ]
   pixch_shapes = pickle.load(fp)
fp.close()


with open (intnl_spixcShp_shapes_file, 'rb') as fp:
   # { "shapeid": [ pixel indexes ], ... }
   image_shapes = pickle.load(fp)
fp.close()


original_image = Image.open(top_images_dir + directory + pixch_imfile + ".png")
image_width, image_height = original_image.size


for pixch_shapeid in pixch_shapes:
   pixch_shape_pixels = image_shapes[ pixch_shapeid ]
   
   for pixel in pixch_shape_pixels:
   
      y = math.floor( int(pixel) / image_width)
      x  = int(pixel) % image_width

      original_image.putpixel( (x , y) , pixch_shapes_color )


original_image.show( )











