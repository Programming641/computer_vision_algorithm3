from libraries import pixel_functions, image_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir

from PIL import Image
import math
import os, sys
import winsound
import glob

from collections import OrderedDict
from libraries.cv_globals import proj_dir, top_images_dir, top_shapes_dir


directory = "videos/monkey/"


# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

image_width = image_height = original_im_pixel = None


def check_image_color_mode():
   for dir_content in glob.glob( top_images_dir + directory + "*" ):

      if dir_content[ len( dir_content ) - 4: len( dir_content ) ] == ".png":
         cur_image = Image.open(dir_content)
         cur_im_pixel = cur_image.getdata()         
         if len( cur_im_pixel[0] ) == 4:
            print("ERROR at check_image_color_mode")
            sys.exit()
   
   print("all image color modes are OK")
         
         
all_file_nums = []
# loop all files and folders
for dir_content in glob.glob( top_images_dir + directory + "*" ):
   # dir_content -> C:\Users\Taichi\Documents\computer_vision/images/videos/street3/resized\51.png
   if not os.path.isfile(dir_content):
      # accept only files and not directory or anything else
      continue
   
   filename = dir_content.split("/")[-1]
   
   if "\\" in filename:
      filename = filename.split("\\")[-1]
   
   filename_num = filename[0: len( filename ) - 4 ]
   
   cur_image = cur_im_pixel = cur_image_width = cur_image_height = None
   if dir_content[ len( dir_content ) - 4: len( dir_content ) ] == ".png" and filename_num.isnumeric():
      # get only input image files and not other image files or anything else
      all_file_nums.append( int(filename_num) )
   
      if image_width is None and image_height is None and original_im_pixel is None:

         original_image = Image.open(dir_content)
         original_im_pixel = original_image.getdata()
         image_width, image_height = original_image.size
         
         if len( original_im_pixel[0] ) == 4:
            original_image = original_image.convert("RGB")
            original_image.save( dir_content )
            

      else:
         cur_image = Image.open(dir_content)
         cur_im_pixel = cur_image.getdata()
         cur_image_width, cur_image_height = cur_image.size      

         if len( cur_im_pixel[0] ) == 4:
            cur_image = cur_image.convert("RGB") 
            cur_image.save( dir_content )            
      
         if not ( image_width == cur_image_width and image_height == cur_image_height ):
            print("ERROR at image size")
            sys.exit(1)



print("all image size is OK")

all_file_nums.sort()
first_image_file = all_file_nums[0]
deleted_image_nums = []
prev_image = None
for file_num in all_file_nums:
   filename = str( file_num ) + ".png"
   cur_filepath = top_images_dir + directory + filename
   if prev_image == None:
      prev_image = Image.open( cur_filepath )
      prev_im_data = list( prev_image.getdata() )
   
   else:
      cur_image = Image.open( cur_filepath )
      cur_im_data = list( cur_image.getdata() )
      
      if prev_im_data == cur_im_data:
         # cur_image and prev_image are exactly the same image, so delete current image.
         os.remove( cur_filepath )
         deleted_image_nums.append( file_num )
      
      prev_im_data = cur_im_data
      

file_num_counter = first_image_file
# [ ( previous image file number, new image file number ), ... ]
reorder_file_nums = []
for file_num in all_file_nums:
   if file_num not in deleted_image_nums:
      reorder_file_nums.append( (file_num, file_num_counter) )
      file_num_counter += 1

for reorder_file_num in reorder_file_nums:
   image_dir = top_images_dir + directory
   prev_image_filename = image_dir + str(reorder_file_num[0]) + ".png"
   cur_image_filename = image_dir + str(reorder_file_num[1]) + ".png"
   
   os.rename(prev_image_filename, cur_image_filename) 
      

reorder_filepath = top_images_dir + directory + 'reorder_file_nums.txt'
reorder_file = open(reorder_filepath, 'w')
reorder_file_contents = "reordered file contents.\n"
reorder_file_contents += "[ ( previous image file number, new image file number ), ... ]\n"
reorder_file_contents +=  str( reorder_file_nums )
reorder_file.write( reorder_file_contents )
reorder_file.close()

check_image_color_mode( )

image_areas = image_functions.get_image_areas( str(first_image_file), directory )
if len( image_areas ) >= 1:
   print("image areas OK")





