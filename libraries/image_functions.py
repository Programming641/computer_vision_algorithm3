from libraries.cv_globals import top_shapes_dir, top_images_dir, internal
from libraries import read_files_functions
from PIL import Image
import os, sys
import math
import re
import pickle



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

# shapes_type
# normal is the one created by find_shapes
# intnl_spixcShp are shapes that incorporate internal small pixel count shapes
def get_image_stats(imfile, directory, shapes_type=None):

   imshapes = None
   if shapes_type == "normal":
      # {{{ }}} one dictionary containing two nested dictionaries
      # shapes[shapes_id][pixel_index] = {}
      # shapes[shapes_id][pixel_index]['x'] = x
      # shapes[shapes_id][pixel_index]['y'] = y
      imshapes = read_files_functions.rd_shapes_file(imfile, directory )
   
   elif shapes_type == "intnl_spixcShp":
      s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"   
      shapes_dir = s_pixcShp_intnl_dir + "shapes/"   
      shapes_dfile = shapes_dir + imfile + "shapes.data"

      with open (shapes_dfile, 'rb') as fp:
         # { '79999': ['79999', ... ], ... }
         # { 'shapeid': [ pixel indexes ], ... }
         imshapes = pickle.load(fp)
      fp.close() 
   
   else:
      print("ERROR at libraries/image_functions/get_image_stats. shapes_type " + shapes_type + " is not supported.")
      sys.exit()


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
# this function reads shapes file which are created by find_shapes.py. so this does not use shapes that incorporate
# internal small pixel count shapes
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


# this function incorporates internal small pixel count shapes and reads shapes file from 
# top_shapes_dir/videos/video_filename/image_directory/shapes/intnl_s_pixcShp/data
def cr_im_from_shapeslist2( imfname, imdir, in_shapes, save_filepath=None , shapes_rgb=None ):

   original_image = Image.open(top_images_dir + imdir + imfname + ".png")
   original_pixel = original_image.getdata()
   image_width, image_height = original_image.size
   
   if shapes_rgb is None:
      shapes_rgb = ( 255, 0, 0 )

   
   # read shapes file
   shapes_intnl_s_pixcShp_dfile = top_shapes_dir + imdir + "shapes/intnl_spixcShp/data/" + imfname + "shapes.data"

   with open (shapes_intnl_s_pixcShp_dfile, 'rb') as fp:
      # { 'shapeid': [ pixel indexes ], ... }
      im_shapes_w_intl_spixcShp = pickle.load(fp)
   fp.close()


   for pixch_shapeid in in_shapes:
      pixch_shape_pixels = im_shapes_w_intl_spixcShp[ pixch_shapeid ]
   
      for pixel in pixch_shape_pixels:
   
         y = math.floor( int(pixel) / image_width)
         x  = int(pixel) % image_width

         original_image.putpixel( (x , y) , shapes_rgb )

   if save_filepath is not None:
      original_image.save( save_filepath )
   elif save_filepath is None:
      original_image.show()









# image data is a list of rgb values placed at each pixel index
# [ ( rgb at pixel index 0 ), ( rgb at pixel index 1 ), ... ]
# return image data which has the same form as input image data
def move_image_up( image_data, move_amount, image_size ):
   last_image_index = ( image_size[0] * image_size[1] ) - 1
   move_image_up = []
   
   for image_index in range( 0, last_image_index + ( move_amount * image_size[0] ) + 1 ):
      y = math.floor( int(image_index) / image_size[0])
      x  = int(image_index) % image_size[0] 
   
      if y - move_amount >= 0 and y < image_size[1]:
         # get rid of rows that have been moved outside through top side of the image
         move_image_up.append( image_data[image_index] )
   
      elif y >= image_size[1]:
         # current row is leftover rows after moving rows up
         move_image_up.append( ( 255, 0, 0 ) )

   return move_image_up


def move_image_down( image_data, move_amount, image_size ):

   last_image_index = ( image_size[0] * image_size[1] ) - 1
   move_image_down = []
   
   replace_top_rows = True
   for image_index in range( 0, last_image_index + 1 ):
      y = math.floor( int(image_index) / image_size[0])
      x  = int(image_index) % image_size[0] 
      
      if y - move_amount < 0:
         if replace_top_rows is True:
            for temp_index in range( 0, image_size[0] * move_amount ):
               # top rows that will move down will be replaced by non image color in their rows.
               move_image_down.append( ( 255, 0, 0 ) )
            
            replace_top_rows = False
         
         if replace_top_rows is False:
            move_image_down.append( image_data[image_index] )
         
   
      elif y + move_amount < image_size[1]:
         move_image_down.append( image_data[image_index] )


   return move_image_down



def move_image_left( image_data, move_amount, image_size ):
   last_image_index = ( image_size[0] * image_size[1] ) - 1

   move_image_left = []

   for image_index in range( 0, last_image_index + 1 ):
      y = math.floor( int(image_index) / image_size[0])
      x  = int(image_index) % image_size[0] 
         
      if x - move_amount >= 0 and x < image_size[0]:
         # get rid of columns that have been moved outside through left side of the image
         move_image_left.append( image_data[image_index] )
   
      if x == image_size[0] - 1:
         for leftover_pixel in range( 0, move_amount ):
            # current column is leftover columns after moving columns left
            move_image_left.append( ( 255, 0, 0 ) )

   return move_image_left



def move_image_right( image_data, move_amount, image_size ):
   last_image_index = ( image_size[0] * image_size[1] ) - 1

   move_image_right = []
   

   for image_index in range( 0, last_image_index + 1 ):
      y = math.floor( int(image_index) / image_size[0])
      x  = int(image_index) % image_size[0] 
         
      if x + move_amount < image_size[0]:
         # right column will be moved out of the image by the "right" amount
         move_image_right.append( image_data[image_index] )
      elif x == image_size[0] - 1:
         # at the last column on the current row, put non-image color at the front as much as pixels have been moved to the right
         for right_pixel in range( image_size[0] * y , ( image_size[0] * y ) + move_amount ):
            move_image_right.insert( right_pixel , ( 0, 0, 255 ) )

   return move_image_right



















































