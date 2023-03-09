from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir
from libraries import read_files_functions
from PIL import Image
import os, sys
import math
import re



def get_image_areas( im_file, directory ):

   # needed for creating image areas
   image = Image.open(top_images_dir + directory + im_file + ".png")
   im_width, im_height = image.size
   
   # image width can not have decimal point values because decimal point value creates number less than the actual image width or height.
   # so divider has to be the one that can exactly divide image width or height
   
   # divide image into columns and rows
   image_dividers = [ 5, 6, 7, 8, 9, 4, 10, 11, 12, 13 ]
   
   image_divider = None
   for temp_divider in image_dividers:
      if im_width % temp_divider == 0 and im_height % temp_divider == 0:
         
         im_area_width = round(im_width / temp_divider)
         im_area_height = round(im_height / temp_divider)
         
         image_divider = temp_divider
         
         break
   
   if not image_divider:
      print("ERROR at get_image_areas method. No image divider found")
      sys.exit()
   
   image_areas = []
   
   column_num = 0
   for column_num in range(0, image_divider):
      for row_num in range(0, image_divider):
         if row_num == 0:
            left = 0
            right = im_area_width
         else:
            left = (im_area_width * row_num) + 1
            right = (im_area_width * row_num) + im_area_width
         
         if column_num == 0:
            top = 0
            bottom = im_area_height
         else:
            top = ( column_num * im_area_height ) + 1
            bottom = ( column_num * im_area_height ) + im_area_height
      
         temp = {}
         temp[row_num + 1 + ( column_num * image_divider ) ] = {'left': left, 'right': right, 'top': top, 'bottom': bottom }
      
         image_areas.append(temp)

   return image_areas




# this function is to get following image data
# counts of shapes in the image
# how many shapes there are in the image that consist of small numbers of pixels
def get_image_stats(imfile, directory):
   # {{{ }}} one dictionary containing two nested dictionaries
   # shapes[shapes_id][pixel_index] = {}
   # shapes[shapes_id][pixel_index]['x'] = x
   # shapes[shapes_id][pixel_index]['y'] = y
   imshapes = read_files_functions.rd_shapes_file(imfile, directory )
   
   imshapes_counts = len( imshapes )
   
   #print("image shapes counts: " + str( imshapes_counts ) )
   
   # contains each shape's pixel counts
   # {'shapeid': pixel count, 'shapeid': pixel count, .... }
   shapes_counts = {}
   
   for shapeid in imshapes:

      shapes_counts[shapeid] = len( imshapes[shapeid] )

   
   # creating pixel count statistics
   # { pixel count : counts of shapes that have this pixel count, pixel count: counts of shapes that have this pixel count, ... }
   pixel_counts = {}
   
   pixel_counts_w_shapes = { }
   
   for shapeid in shapes_counts:
      cur_pcount = shapes_counts[shapeid]
      
      
      
      if len( pixel_counts ) == 0:
         pixel_counts[ cur_pcount ] = 1
         
         pixel_counts_w_shapes[ cur_pcount ] = [ shapeid ]
   
      elif cur_pcount in pixel_counts.keys():
         #cur_pcount is found in pixel_counts. add 1
         pixel_counts[ cur_pcount ]  += 1
         
         pixel_counts_w_shapes[ cur_pcount ].append( shapeid )
      
      else:
         #cur_pcount is not found in pixel_counts. create this pixel count
         pixel_counts[ cur_pcount ] = 1

         pixel_counts_w_shapes[ cur_pcount ] = [ shapeid ]
   
   pixel_counts = dict( sorted(pixel_counts.items(), key=lambda i: i[1], reverse= True) )
   #print( pixel_counts )

   return pixel_counts_w_shapes


# create images from the given shapes.
# in_shapes are the list containing shapeids
# [ shapeid1, shapeid2, ..... ]
# save_filepath is the full path of the new image
# background_rgb -> (R, G, B) R,G,B values are integer
def cr_im_from_shapeslist( imfname, imdir, in_shapes, save_filepath=None , background_rgb=None ):

   if save_filepath == None:
      print("ERROR. save filepath is not specified.")
      sys.exit()

   shapes_filename = imfname + "_shapes.txt"

   # directory is specified but does not contain /
   if imdir != "" and imdir[-1] != ('/'):
      imdir +='/'


   # shapes file has the rule for its filename. Its filename consists of name of the image shape + shapes.txt.
   # so to extract the shapes image name only, you just remove last space + shapes.txt
   original_image_filename = shapes_filename[:-11]

   if os.path.exists(top_shapes_dir + imdir + "shapes/" + shapes_filename[:-4]) == False:
      os.makedirs(top_shapes_dir + imdir + "shapes/" + shapes_filename[:-4])



   original_image = Image.open(top_images_dir + imdir + original_image_filename + ".png")

   image_width, image_height = original_image.size
   
   if not background_rgb:
      new_image = Image.new('RGB', (image_width, image_height) )
   else:
      new_image = Image.new('RGB', (image_width, image_height), background_rgb )

   original_image_data = original_image.getdata()



   shapes_file = open(top_shapes_dir + imdir + "shapes/" + shapes_filename)
   shapes_file_contents = shapes_file.read()


   # single pixel pattern
   # ( then comes [0-9]{1, len(str(image_width * image_height))} then comes , then comes 
   # space then comes [ then comes [0-9]{1,len(str(image_width * image_height))} then comes ] then comes )

   single_pixel_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}, \[[0-9]{1,' + \
                           str(len(str(image_width * image_height))) + '}\]\)'
                           
   match = re.findall(single_pixel_pattern, shapes_file_contents)

   for shape in match:

      # getting shape index number
      shapeindex_ptn = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}'
      
      shapeindex = re.match(shapeindex_ptn, shape)
      
      shapeindex = shapeindex.group().replace("(", "")
      
      # current image shape is not in the given shapes list
      if not shapeindex in in_shapes:
         continue

      if len(original_image_data[ int(shapeindex) ]) == 3:
         original_image_red, original_image_green, original_image_blue = original_image_data[ int(shapeindex) ]
      else:
         original_image_red, original_image_green, original_image_blue, alpha = original_image_data[ int(shapeindex) ]
      y = math.floor( int(shapeindex) / image_width)
      x  = int(shapeindex) % image_width 


      new_image.putpixel( (x, y) , (original_image_red, original_image_green, original_image_blue) )


   '''
    ( then comes [0-9]{1, len(str(image_width * image_height))} then comes , then comes space then comes [ then comes 
    GROUPSTART [0-9]{1,len(str(image_width * image_height))} then comes , then comes space GROUPEND then comes [0-9]{1,len(str(image_width * image_height))} 
    then comes ] then comes )

    GROUPSTART (      GROUPEND )
   '''
   multiple_pixel_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}, \[(?:[0-9]{1,' + str(len(str(image_width * image_height))) + \
                             '},\s{1})+[0-9]{1,' + str(len(str(image_width * image_height))) + '}\]\)'
   match = re.findall(multiple_pixel_pattern, shapes_file_contents)


   # match contains all shapes
   for shape in match:

      shapes_id_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '},'
      match_temp = re.search(shapes_id_pattern, shape)
      shapeid = match_temp.group().strip('(,')

      if not shapeid in in_shapes:
         continue

      pixels_list_pattern = '\[.*\]'
      pixels_index_string = re.findall(pixels_list_pattern, shape)

      shape_pixel_counter = 0 


      #pixels_index_string contains one shape
      # pixels_index_string is a list but contains only one string
      for one_string in pixels_index_string:
      
         # one_string is a one string. removing unnecessary characters leaving only the numbers
         one_string_stripped = one_string.strip('[, ]')
         # split each number by ,
         one_string_list = one_string_stripped.split(',')

         # now iterate over all pixel index numbers
         for pixel_index in one_string_list:
            shape_pixel_counter += 1
            pixel_index = int(pixel_index)
         
            if len(original_image_data[pixel_index ]) == 3:
               original_image_red, original_image_green, original_image_blue = original_image_data[pixel_index ]
            else:
               original_image_red, original_image_green, original_image_blue, alpha = original_image_data[pixel_index ]
            y = math.floor(pixel_index / image_width)
            x  = pixel_index % image_width    


            new_image.putpixel( (x, y) , (original_image_red, original_image_green, original_image_blue) )


   
   new_image.save(save_filepath)
      
   shapes_file.close() 














