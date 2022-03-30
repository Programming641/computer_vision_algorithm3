#
# algorithm for determining the closest match with the color group uses how far away the RGB value is from original
#
#

import sys
from PIL import Image
import re

filename = "hanger001_color_group"

directory = "videos/hanger"

# directory is specified but does not contain /
if directory != "" and directory.find('/') == -1:
   directory +='/'


original_image = Image.open("images/" + directory + filename + ".png")
original_pixel = original_image.getdata()
image_size = original_image.size


def get_closest_color(image_pixel):

    file = open("data\list of colors2.txt")

    lines = file.readlines()

    #dictionary for storing color group name and rgb values. this is needed after finding the image pixel's closest color group
    color_group_dict = {}



    # initializing dictionary for storing total difference value for every matching pixel with particular color group.
    difference_dict = {}

    for line in lines: 


       # first # then 6 alphanumerics. tab or space repeats 1 - 5 times. number repeats 1-3 times. tab or space 1-5 times ...
       tem_pattern = '#[a-zA-Z0-9]{6}\s{1,5}[0-9]{1,3}\s{1,5}[0-9]{1,3}\s{1,5}[0-9]{1,3}'
       temp_match = re.search( tem_pattern , line)
       
       if temp_match != None:
          
          hex_pattern = '#[a-zA-Z0-9]{6}'
          hex_Num = re.search( hex_pattern , temp_match.group())

          # remove hexedecimal number for extracting the RGB values
          hex_first_index = temp_match.group().find('#')
          # hex numbers consist of 7 characters including #
          hex_removed = temp_match.group()[ hex_first_index + 7 : ]

          RGB_pattern = '[0-9]{1,3}'
          RGB_color_group = re.findall( RGB_pattern, hex_removed )
          
          red_color_group, green_color_group, blue_color_group = RGB_color_group

          red_color_group = int(red_color_group)
          green_color_group = int(green_color_group)
          blue_color_group = int(blue_color_group)
           
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


original_image.save("images/" + directory + filename + "_clr_grp.png")









