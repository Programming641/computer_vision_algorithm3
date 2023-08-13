
from libraries import image_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir
import pickle
import sys
import math
from PIL import Image


im_file = '11'
directory = "videos/street3/resized/min"

pixch_shapes_color = ( 255, 0, 0 )

# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'


disappeared_dir = top_shapes_dir + directory + "pixch/ch_shapes/disappeared/"
disappeared_shapes_file = disappeared_dir + "data/" + im_file + ".data"
with open (disappeared_shapes_file, 'rb') as fp:
   # [ 'shapeid', 'shapeid', ... ]
   disappeared_shapes = pickle.load(fp)
fp.close()

intnl_spixcShp_shapes_file = top_shapes_dir + directory + "shapes/intnl_spixcShp/data/" + im_file + "shapes.data"
with open (intnl_spixcShp_shapes_file, 'rb') as fp:
   # { "shapeid": [ pixel indexes ], ... }
   image_shapes = pickle.load(fp)
fp.close()


original_image = Image.open(top_images_dir + directory + im_file + ".png")
image_width, image_height = original_image.size


for shapeid in disappeared_shapes:
   pixch_shape_pixels = image_shapes[ shapeid ]
   
   for pixel in pixch_shape_pixels:
   
      y = math.floor( int(pixel) / image_width)
      x  = int(pixel) % image_width

      original_image.putpixel( (x , y) , pixch_shapes_color )


original_image.show( )











