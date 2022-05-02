#
# algorithm for determining the closest match with the color group uses how far away the RGB value is from original
#
#

import sys
from PIL import Image
import re

filename = "bird01"

directory = "bird"

# directory is specified but does not contain /
if directory != "" and directory[-1] != "/":
   directory +='/'


original_image = Image.open("images/" + directory + filename + ".png")
original_pixel = original_image.getdata()
image_size = original_image.size


def get_closest_color(image_pixel):

    file = open("data\list of colors3.txt")

    lines = file.readlines()

    #dictionary for storing color group name and rgb values. this is needed after finding the image pixel's closest color group
    color_group_dict = {}



    # initializing dictionary for storing total difference value for every matching pixel with particular color group.
    difference_dict = {}

    for line in lines: 

       hex_pattern = '#[a-zA-Z0-9]{6}'
       hex_Num = re.search( hex_pattern , line)
       
       if not hex_Num:
          continue

       
       hex_rm = hex_Num.group().replace("#", "")
       
       red_color_group = int( hex_rm[0:2], 16 )
       green_color_group = int( hex_rm[2:4], 16 )
       blue_color_group = int( hex_rm[4:6], 16 )
           
       if len(image_pixel) == 3:
          image_red, image_green, image_blue = image_pixel
       else:
          image_red, image_green, image_blue, alpha = image_pixel
         
       red_difference = abs(image_red - red_color_group)
       green_difference = abs(image_green - green_color_group)
       blue_difference = abs(image_blue - blue_color_group)
            
       total_difference = red_difference + green_difference + blue_difference

       average = total_difference / 3

       # exclude 0 or negatie values because 0 or negative values mean that difference is smaller than average.
       red_how_far = exclude_negative_Num( red_difference - average )
       green_how_far = exclude_negative_Num( green_difference - average )
       blue_how_far = exclude_negative_Num( blue_difference - average )

       total_appearance_difference = total_difference + red_how_far * 1.3 + green_how_far * 1.3 + blue_how_far * 1.3

       #populating all color group hex number and values
       color_group_dict[hex_Num] = [red_color_group, green_color_group, blue_color_group]

       difference_dict[hex_Num] = total_appearance_difference

    # key_min has the color group hex number that has the closest match for the image pixel
    key_min = min(difference_dict, key=difference_dict.get)

    return color_group_dict[key_min]
        
    file.close()    


def exclude_negative_Num(num):

    if num > 0:
       return num
    else:
       return 0





debug = False


#image_size[0] is image width
for y in range(image_size[1]):
   print("y is " + str(y))

   for x in range(image_size[0]):
   


        # converting for the getdata(). y is the row that you want to get data for
        new_x = (y * image_size[0])+ x

        red, green, blue = get_closest_color(original_pixel[new_x])

        original_image.putpixel( (x,y), (red, green, blue))
        
        if debug == True:
           break
        
   if debug == True:
       break


original_image.save("images/" + directory + filename + "clrgrp.png")









