#
# algorithm for determining the closest match with the color group uses how far away the RGB value is from original
#
#

import sys, os
from PIL import Image
import re, pickle
from libraries import pixel_functions
from libraries.cv_globals import proj_dir, top_shapes_dir

if proj_dir != "" and proj_dir[-1] != "/":
   proj_dir +='/'

image_dir = proj_dir + "images/"

# -------------------       user input begin     ---------------------
# user input: filename, directory ( example. videos/cat/original ), 
filename = "1"
directory = "videos/monkey"
# types of color groups. choices are clrgrp ( for color group ), min ( for minimum )
clr_grp_type = "clrgrp3"
# -------------------       user input end       ---------------------


if len(sys.argv) >= 2:
   filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   directory = sys.argv[1]
   clr_grp_type = sys.argv[2]

   print("execute script putpix_into_clrgrp.py. filename " + filename + " directory " + directory + " clr_grp_type " + clr_grp_type )



# directory is specified but does not contain /
if directory != "" and directory[-1] != "/":
   directory +='/'


original_image = Image.open(image_dir + directory + filename + ".png")
original_pixel = original_image.getdata()
image_size = original_image.size

def get_closest_color(image_pixel, clrgrp_data):

   closest_color = None
   minimum_diff = None
   if len(image_pixel) == 3:
      image_red, image_green, image_blue = image_pixel
   else:
      image_red, image_green, image_blue, alpha = image_pixel
   
   for clrgrp_rgb in clrgrp_data:
      
      red_difference = abs(image_red - clrgrp_rgb[0])
      green_difference = abs(image_green - clrgrp_rgb[1])
      blue_difference = abs(image_blue - clrgrp_rgb[2])
            
      total_difference = red_difference + green_difference + blue_difference

      if closest_color is None:
         closest_color = clrgrp_rgb
         minimum_diff = total_difference
      elif total_difference < minimum_diff:
         closest_color = clrgrp_rgb
         minimum_diff = total_difference

   return closest_color
        
    



if "clrgrp" in clr_grp_type:
   color_filenum = clr_grp_type[6:7]
   clrgrp_file = open(proj_dir + "data/list_of_colors" + color_filenum + ".txt")
elif "min" in clr_grp_type:
   # example clr_grp_type is min1, min2, min3 and so on.
   color_filenum = clr_grp_type[3:4]
   clrgrp_file = open(proj_dir + "data/minimum_colors" + color_filenum + ".txt")
    
lines = clrgrp_file.readlines()
clrgrp_file.close()    

clrgrp_data = set()
for line in lines: 

   hex_pattern = '#[a-zA-Z0-9]{6}'
   hex_Num = re.search( hex_pattern , line)
       
   if not hex_Num:
      continue

       
   hex_rm = hex_Num.group().replace("#", "")
       
   r = int( hex_rm[0:2], 16 )
   g = int( hex_rm[2:4], 16 )
   b = int( hex_rm[4:6], 16 )

   clrgrp_data.add( (r, g, b) )




resulted_colors = set()

#image_size[0] is image width
for y in range(image_size[1]):
   if y % 10 == 0:
      print("\r" + "y is " + str(y), end="")

   for x in range(image_size[0]):
   
        # converting for the getdata(). y is the row that you want to get data for
        new_x = (y * image_size[0])+ x

        matched_color = get_closest_color(original_pixel[new_x], clrgrp_data)
        
        resulted_colors.add( matched_color )
        
        original_image.putpixel( (x,y), matched_color)
        
print()
print( "color variations " + str( len(resulted_colors) ) )

save_dirname = image_dir + directory + clr_grp_type 
if not os.path.exists(save_dirname):
   os.makedirs(save_dirname)

shapes_data_dir = top_shapes_dir + directory + clr_grp_type + "/data/"
if not os.path.exists(shapes_data_dir):
   os.makedirs(shapes_data_dir)
   
with open(shapes_data_dir + "color_variations.data", 'wb') as fp:
   pickle.dump(resulted_colors, fp)
fp.close()


original_image.save(save_dirname + "/" + filename + ".png")






