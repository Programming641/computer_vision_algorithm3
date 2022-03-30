#
# algorithm for determining the closest match with the color group uses how far away the RGB value is from original
#
#
from libraries import pixel_functions

from PIL import Image
import math

from collections import OrderedDict


image_filename = 'blue1_clr_grp'

directory = ""

# directory is specified but does not contain /
if directory != "" and directory.find('/') == -1:
   directory +='/'


original_image = Image.open("images/" + directory + image_filename + ".png")
original_pixel = original_image.getdata()
image_size = original_image.size


# shapes[shape's index value ] = [ pixel index1, pixel index2, .... ]
shapes = OrderedDict()

def get_neighbor_pixels(pixel_index):

   # list for storing neighbor index numbers
   neighbors = []

   # assigning the positions for comparing neighbor pixels. starting with top going clockwise.
   ignore_neighbor_position_dict = { 'top' : False, 'top_right' : False, 'right' : False, 'bottom_right': False, 'bottom': False, 'bottom_left' : False, 'left': False, 'top_left': False }

   y = math.floor(pixel_index / image_size[0])

   x  = pixel_index % image_size[0]
   
   # determining if the current pixel is the leftmost pixel
   # no need to compare with top left, left, bottom left
   if x == 0:
 
      ignore_neighbor_position_dict['top_left'] = True
      ignore_neighbor_position_dict['left'] = True
      ignore_neighbor_position_dict['bottom_left'] = True
    
   # determing the first row
   # no need to compare with top left, top, top right
   if pixel_index <= image_size[0] -1:
      ignore_neighbor_position_dict['top_left'] = True
      ignore_neighbor_position_dict['top'] = True
      ignore_neighbor_position_dict['top_right'] = True  

   # determining the rightmost pixel. x counts from 0 to width - 1
   # no need to compare with top right, right, bottom right
   if x == image_size[0] - 1:
      ignore_neighbor_position_dict['top_right'] = True
      ignore_neighbor_position_dict['right'] = True
      ignore_neighbor_position_dict['bottom_right'] = True

   # determining last row . y counts from 0 to height - 1
   # no need to compare with bottom left, bottom, bottom right
   if y == image_size[1] - 1:
      ignore_neighbor_position_dict['bottom_left'] = True
      ignore_neighbor_position_dict['bottom'] = True
      ignore_neighbor_position_dict['bottom_right'] = True

   if ignore_neighbor_position_dict['top'] == False:   
      top_neighbor = pixel_index - image_size[0]
      neighbors.append(top_neighbor)


   if ignore_neighbor_position_dict['top_right'] == False:     
      top_right_neighbor = pixel_index - image_size[0] + 1
      neighbors.append(top_right_neighbor)


   if ignore_neighbor_position_dict['right'] == False:  
      right_neighbor = pixel_index + 1
      neighbors.append(right_neighbor)

   if ignore_neighbor_position_dict['bottom_right'] == False:
      bottom_right_neighbor = pixel_index + image_size[0] + 1
      neighbors.append(bottom_right_neighbor)      

   if ignore_neighbor_position_dict['bottom'] == False:
      bottom_neighbor = pixel_index + image_size[0]
      neighbors.append(bottom_neighbor)   

   if ignore_neighbor_position_dict['bottom_left'] == False:    
      bottom_left_neighbor = pixel_index + image_size[0] - 1 
      neighbors.append(bottom_left_neighbor) 

   if ignore_neighbor_position_dict['left'] == False:   
      left_neighbor =    pixel_index - 1
      neighbors.append(left_neighbor) 

   if ignore_neighbor_position_dict['top_left'] == False:  
      top_left_neighbor =  pixel_index - image_size[0] - 1
      neighbors.append(top_left_neighbor) 

   return neighbors





#image_size[0] is width
for y in range(image_size[1]):
   print("y is " + str(y))


   for x in range(image_size[0]):
   
   
      # converting for the getdata(). y is the row that you want to get data for. current_pixel_index is the current pixel's index number
      current_pixel_index = (y * image_size[0])+ x    

      # initializing current pixel' shape number. This 
      current_shape_id = None
      
      total_appearance_difference_threshold = 30
      
      cur_pixel_neighbors = get_neighbor_pixels(current_pixel_index)


      #getting current pixel RGB values
      current_pixel_RGB = original_pixel[current_pixel_index]
      

      # check if current pixel is in other pixel's shapes.
      if len(shapes) != 0:
         # last in first out
         for shape_id, shapes_lists in reversed(shapes.items()):
            for shapes_pixel in shapes_lists:
               if shapes_pixel == current_pixel_index:
                  # current pixel is found in existing shape. current shape will be this found shape
                  current_shape_id = shape_id


      # current pixel was not found in all shapes so create its own shape
      if current_shape_id == None:     
         # create shape with current pixel's number as shape's id
         current_shape_id = current_pixel_index
         # make sure to put current pixel in current pixel shape
         
         print(" creating new shape " + str(current_shape_id) )
         
         shapes[current_shape_id] = [current_shape_id]


      cur_shape_pixel_RGB = original_pixel[current_shape_id]



      # iterating each one of current pixel's unfound neighbors
      for neighbor in cur_pixel_neighbors:
         
         neighbor_shape_found, cur_pix_nei_shape_appearance, cur_shape_nei_shape_appearance = False, False, False
         neighbor_shape_index = None  
         
         # check if this neighbor is already in the shape
         for shape_id, shapes_lists in reversed(shapes.items()):
            # iterating all neighbor shapes
            for shapes_pixel in shapes_lists:
               # iterating all pixels in neighor shape
               
               if shapes_pixel == neighbor:    
                  neighbor_shape_found = True              
                  # check if this neighbor's shape id's appearance is the same. If it not, then it likely mean that
                  # appearance is gradually changing.
      
                  neighbor_shape_index = shape_id
                 
                  if neighbor_shape_index == current_shape_id:
                     continue
                 
                 
                  neighbor_shape_pixel_RGB = original_pixel[neighbor_shape_index]
      
                  appearance_difference = pixel_functions.compute_appearance_difference(current_pixel_RGB, neighbor_shape_pixel_RGB)
              
                  if total_appearance_difference_threshold - appearance_difference >= 0:
                     cur_pix_nei_shape_appearance = True
                     
                     print("current pixel " + str(current_pixel_index) + " neighbor shape pixel " + str(neighbor_shape_index) + 
                     " have similar appearance" )
         
                  appearance_difference = pixel_functions.compute_appearance_difference(cur_shape_pixel_RGB, neighbor_shape_pixel_RGB) 
                  if total_appearance_difference_threshold - appearance_difference >= 0:
                     # this is for avoiding mutating shapes dictionary during iteration
                     cur_shape_nei_shape_appearance = True
                     
                     print("current shape pixel " + str(current_shape_id) + " neighbor shape pixel " + str(neighbor_shape_index) +
                     " have same appearance" )


         if cur_shape_nei_shape_appearance == True:
            # avoiding mutating shapes dictionary during iteration
            # neighbor's shape and current shape need to be merged    
            
            # merging all pixels in neighbor shape into current shape
            for neighbor_pixels in shapes[neighbor_shape_index]:
               shapes[current_shape_id].append(neighbor_pixels)
               
            shapes.pop(neighbor_shape_index)       




         if  neighbor_shape_found == False:

            neighbor_pixel_RGB = original_pixel[neighbor]
            appearance_difference = pixel_functions.compute_appearance_difference(cur_shape_pixel_RGB, neighbor_pixel_RGB )
                 
            if total_appearance_difference_threshold - appearance_difference >= 0:

               # neighbor pixel will be added to current shape
               shapes[current_shape_id].append(neighbor)            
            
            
                 


file = open('shapes/' + image_filename + '_shapes.txt', 'w')
file.write(str(shapes))
file.close()








