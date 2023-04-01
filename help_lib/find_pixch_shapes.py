#
from libraries import pixel_functions

from PIL import Image
import math
import os, sys
import winsound

from collections import OrderedDict
from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir

if proj_dir != "" and proj_dir[-1] != "/":
   proj_dir +='/'



def do_find( image_filename, image_filename2, directory ):

   # check if directory's last directory is "pixch". if not add pixch directory to it
   if directory[-1] != "/":
      add_slash = True
      pixch_word_len = 5
      pixch_word_end = len( directory )
   else:
      add_slash = False
      pixch_word_len = 6
      pixch_word_end = len( directory ) - 1    # excluding "/"
   
   pixch_word_start = len( directory ) - pixch_word_len
   
   pixch_word = directory[ pixch_word_start: pixch_word_end ]
  
   if pixch_word == "pixch":
      if add_slash is True:
         directory += "/"
   else:
      if add_slash is True:
         directory += "/pixch/"
      else:
         directory += "pixch/"


   # pixel change image contains pixel change color and backgound color. this is needed to exclude background color
   pixch_color = ( 0, 255 , 0 )

   target_im_shapes_dir = top_shapes_dir + directory + "shapes/"

   if os.path.exists(target_im_shapes_dir ) == False:
      os.makedirs(target_im_shapes_dir)
   
   original_image = Image.open(top_images_dir + directory + image_filename + "." + image_filename2 + ".png")
   original_pixel = original_image.getdata()
   image_size = original_image.size

   # shapes[shape's index value ] = [ pixel index1, pixel index2, .... ]
   shapes = OrderedDict()

   #image_size[0] is width
   for y in range(image_size[1]):
      print("y is " + str(y))

      for x in range(image_size[0]):
      
         # converting for the getdata(). y is the row that you want to get data for. current_pixel_index is the current pixel's index number
         current_pixel_index = (y * image_size[0])+ x
      
         # make sure it is pixel change, and not background pixel
         if not original_pixel[current_pixel_index] == pixch_color:
            continue

         # initializing current pixel' shape number. This 
         current_shape_id = None
      
         # this is needed for checking if pixel has same color with every pixels in the confirmed shapes
         cur_shape_containing_confirmed_shapes = None
      
         cur_pixel_neighbors = pixel_functions.get_nbr_pixels(current_pixel_index, image_size)      

         # check if current pixel is in other pixel's shapes.
         if len(shapes) != 0:
            # last in first out
            for shape_id, shapes_lists in reversed(shapes.items()):
               if current_pixel_index in shapes_lists:
                  # current pixel is found in existing shape. current shape will be this found shape
                  current_shape_id = shape_id
               
                  cur_shape_containing_confirmed_shapes = shapes_lists


         # current pixel was not found in all shapes so create its own shape
         if current_shape_id == None:     
            # create shape with current pixel's number as shape's id
            current_shape_id = current_pixel_index
            # make sure to put current pixel in current pixel shape
         
            shapes[current_shape_id] = [current_shape_id]


         cur_shape_pixel_RGB = original_pixel[current_shape_id]



         # iterating each one of current pixel's unfound neighbors
         for neighbor in cur_pixel_neighbors:
         
            neighbor_shape_found, cur_shape_nei_shape_appearance = False, False
            neighbor_shape_index = None  
         
            cur_nbr_containing_shapes = []
            # check if this neighbor is already in the shape
            for shape_id, shapes_lists in reversed(shapes.items()):
               # iterating all neighbor shapes
               if neighbor in shapes_lists:
                  
                  # check if neighbor is already in the same shape as current_pixel_index
                  if shape_id == current_shape_id:
                     neighbor_shape_found = True 
                     break
                  
                  cur_nbr_containing_shapes = shapes_lists
                               
                  neighbor_shape_index = shape_id                
                              


            if cur_nbr_containing_shapes:
               # neighbor is found in neighbor_shape_index
               # check if all pixels in the  neighbor_shape_index have same same as current_shape_id
               # merge two shapes only if they all have the same color
               # merging all pixels in neighbor shape into current shape

               all_pixels_same_clr = None
               for cur_nbr_containing_pixel in cur_nbr_containing_shapes:
                  for cur_shape_pixel in shapes[current_shape_id]:
               
                     clrch, brit_thres, brit_ch_v = pixel_functions.compute_appearance_difference(original_pixel[cur_nbr_containing_pixel] ,
                                                    original_pixel[cur_shape_pixel], 30 )
                  
                     # color changed is true or color did not change but brightness is not within threshold
                     if clrch or ( not clrch and not brit_thres ):
                        all_pixels_same_clr = False
                        break

                  if all_pixels_same_clr == False:
                     break
                  
               if all_pixels_same_clr != False:
                  shapes[current_shape_id].extend(shapes[neighbor_shape_index])
               
                  shapes.pop(neighbor_shape_index)       


            if  neighbor_shape_found == False:

               neighbor_pixel_RGB = original_pixel[neighbor]

               # make sure all pixels have same color as neighbor, then you can put neighbor in current_shape_id shape
               all_pixels_same_clr = None
               if cur_shape_containing_confirmed_shapes:
                  for pixels in cur_shape_containing_confirmed_shapes:
                     clrch, brit_thres, brit_ch_v = pixel_functions.compute_appearance_difference(original_pixel[pixels], neighbor_pixel_RGB, 30 )
                 
                     if clrch or ( not clrch and not brit_thres ):
                        all_pixels_same_clr = False
                        break
               
                  if all_pixels_same_clr != False:
                  
                     # neighbor pixel will be added to current shape
                     shapes[current_shape_id].append(neighbor)                 
            


   file = open(target_im_shapes_dir + image_filename + "." + image_filename2 + "_shapes.txt", 'w')
   file.write(str(shapes))
   file.close()


   frequency = 2500  # Set Frequency To 2500 Hertz
   duration = 1000  # Set Duration To 1000 ms == 1 second
   winsound.Beep(frequency, duration)



if __name__ == '__main__':
   im1file = ""
   im2file = ""
   directory = ""
   
   do_find( im1file, im2file, directory )










