#
# algorithm for determining the closest match with the color group uses how far away the RGB value is from original
#
#

from PIL import Image
import math

from collections import OrderedDict

image_filename = 'easy image to analyze for practice3'

directory = ""

# directory is specified but does not contain /
if directory != "" and directory.find('/') == -1:
   directory +='/'


original_image = Image.open("images/" + directory + image_filename + ".png")
original_pixel = original_image.getdata()
image_size = original_image.size


# shapes[shape's index value ] = [ pixel index1, pixel index2, .... ]
shapes = OrderedDict()



def compute_appearance_difference(current_pix, compare_pixel):

   original_red, original_green, original_blue = current_pix

   compare_red, compare_green, compare_blue = compare_pixel
    
   red_difference = abs(original_red - compare_red)
   green_difference = abs(original_green - compare_green)
   blue_difference = abs(original_blue - compare_blue)
    
   total_difference = red_difference + green_difference + blue_difference

   average = total_difference / 3

   # exclude 0 or negatie values because 0 or negative values mean that difference is smaller than average.
   red_how_far = exclude_negative_Num( red_difference - average )
   green_how_far = exclude_negative_Num( green_difference - average )
   blue_how_far = exclude_negative_Num( blue_difference - average )

   total_appearance_difference = total_difference + red_how_far * 1.3 + green_how_far * 1.3 + blue_how_far * 1.3

   return total_appearance_difference

def exclude_negative_Num(num):

   if num > 0:
      return num
   else:
      return 0



def get_neighbor_pixels(pixel_index):

   # list for storing neighbor index numbers
   neighbors = []

   # assigning the positions for comparing neighbor pixels. starting with top going clockwise.
   ignore_neighbor_position_dict = { 'top' : False, 'top_right' : False, 'right' : False, 'bottom_right': False, 'bottom': False, 'bottom_left' : False, 'left': False, 'top_left': False }

   y = math.floor(pixel_index / image_size[0])

   x  = pixel_index % image_size[0]

   #  ----------------------------------------------------      determining current pixel's position      ----------------------------------------------------
   
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
    
   #  ----------------------------------------------------      determining current pixel's position     END     -------------------------------------------------

   if ignore_neighbor_position_dict['top'] == False:   
      top_neighbor = current_pixel_index - image_size[0]
      neighbors.append(top_neighbor)


   if ignore_neighbor_position_dict['top_right'] == False:     
      top_right_neighbor = current_pixel_index - image_size[0] + 1
      neighbors.append(top_right_neighbor)


   if ignore_neighbor_position_dict['right'] == False:  
      right_neighbor = current_pixel_index + 1
      neighbors.append(right_neighbor)

   if ignore_neighbor_position_dict['bottom_right'] == False:
      bottom_right_neighbor = current_pixel_index + image_size[0] + 1
      neighbors.append(bottom_right_neighbor)      

   if ignore_neighbor_position_dict['bottom'] == False:
      bottom_neighbor = current_pixel_index + image_size[0]
      neighbors.append(bottom_neighbor)   

   if ignore_neighbor_position_dict['bottom_left'] == False:    
      bottom_left_neighbor = current_pixel_index + image_size[0] - 1 
      neighbors.append(bottom_left_neighbor) 

   if ignore_neighbor_position_dict['left'] == False:   
      left_neighbor =    current_pixel_index - 1
      neighbors.append(left_neighbor) 

   if ignore_neighbor_position_dict['top_left'] == False:  
      top_left_neighbor =  current_pixel_index - image_size[0] - 1
      neighbors.append(top_left_neighbor) 

   return neighbors





#image_size[0] is width
for y in range(image_size[1]):
   print("y is " + str(y))


   for x in range(image_size[0]):
   


   
      # converting for the getdata(). y is the row that you want to get data for. current_pixel_index is the current pixel's index number
      current_pixel_index = (y * image_size[0])+ x    

      # initializing current pixel' shape number. This 
      current_pixel_shape = None
      
      
      total_appearance_difference_threshold = 55
      
      cur_pixel_neighbors = get_neighbor_pixels(current_pixel_index)


      merge_neighbors_list = []


      #getting current pixel RGB values
      current_pixel_RGB = original_pixel[current_pixel_index]
      

      # check if current pixel is in other pixel's shapes.
      if len(shapes) != 0:
         # last in first out
         for shape_id, shapes_lists in reversed(shapes.items()):
            for shapes_pixel in shapes_lists:
               if shapes_pixel == current_pixel_index:
                  # current pixel is found in existing shape. current shape will be this found shape
                  current_pixel_shape = shape_id



      # current pixel was not in any of the shapes. Now determine if any of the current pixel's neighbors are already in shape
      if current_pixel_shape == None:
      
         # iterating each one of current pixel's neighbors
         for neighbor in cur_pixel_neighbors:
         
               # look for neighbor pixel in all existing shapes
               for neighbor_shape_id, shapes_lists in reversed(shapes.items()):
                  for shapes_pixel in shapes_lists:
                     if shapes_pixel == neighbor:
                        # neighbor pixel is found
                     
                        neighbor_pixel_RGB = original_pixel[neighbor]
                        appearance_difference = compute_appearance_difference(current_pixel_RGB, neighbor_pixel_RGB)
              
                        # check to see if total appearance difference value is within the threshold. if so, current pixel's shape will be this neighbor's shape and it will be put in 
                        # this neighbor's shape.
                        if total_appearance_difference_threshold - appearance_difference >= 0:      
                        
                           print(" current running pixel " + str(current_pixel_index) + " was not found in all existing shapes but its neighor " + str(neighbor) + " was already in shape " + 
                           str(neighbor_shape_id) + " and has similar appearance to current pixel. so append current pixel to this neighbor's shape. This shape will be current shape.")
                           current_pixel_shape = neighbor_shape_id
                           
                           # before merging, make sure it is not already in the current shape
                           if not current_pixel_index in shapes[neighbor_shape_id]:
                              shapes[neighbor_shape_id].append(current_pixel_index)
                        
      else:

         # current pixel is already in existing shape. Now check if its neighbors are alreay in shape as well.
         # if neighbors are already in shape and have similar appearance, then merge both shapes.
         
         # iterating each one of current pixel's neighbors
         for neighbor in cur_pixel_neighbors:
         
               # look for neighbor pixel in all existing shapes
               for neighbor_shape_id, shape_list in reversed(shapes.items()):
               
                  if neighbor_shape_id != current_pixel_shape:
                     for shape_pixels in shape_list:
                        if shape_pixels == neighbor:
                           # neighbor pixel is found
                     
                           neighbor_pixel_RGB = original_pixel[neighbor]
                           current_shape_RGB = original_pixel[current_pixel_shape]
                           appearance_difference = compute_appearance_difference(current_shape_RGB, neighbor_pixel_RGB)
              
                           # check if neighbor shape and current pixel shapes are similar in appearnce. if they are, merge both shapes into one shape.
                           if total_appearance_difference_threshold - appearance_difference >= 0:
                           
                              print(" adding neighbor_shape_id " + str(neighbor_shape_id) + " to be deleted" )
                              merge_neighbors_list.append(neighbor_shape_id)
                              merge_neighbor_pixels = shapes[ neighbor_shape_id ]
                           
                              print("merging neighbor pixels to current shape  " + str(current_pixel_shape) )
                           
                              for merge_neighbor_pixel in merge_neighbor_pixels:
                                 # before merging, make sure it is not already in the current shape
                                 if not merge_neighbor_pixel in shapes[current_pixel_shape]:
                                    shapes[current_pixel_shape].append(merge_neighbor_pixel)
   
      if merge_neighbors_list:
         # deleting duplicate shape ids
         merge_neighbors_list = list( dict.fromkeys(merge_neighbors_list) )
         for merged_neighbor in merge_neighbors_list:
            shapes.pop(merged_neighbor)


      # all current pixel's neighbors did not have similar appearance to it, so create its own shape
      if current_pixel_shape == None:     
         # create shape with current pixel's number as shape's id
         current_pixel_shape = current_pixel_index
         # make sure to put current pixel in current pixel shape
         
         print(" creating new shape " + str(current_pixel_shape) )
         
         shapes[current_pixel_shape] = [current_pixel_shape]




      # iterating each one of current pixel's neighbors
      for neighbor in cur_pixel_neighbors:
      
         # current pixel's top neighbor can be found by subtrating image width from current pixel index number
         neighbor_pixel_RGB = original_pixel[neighbor]
      
         neighbor_pixel_index = neighbor
      
         # what's returned is total appearance difference value
         appearance_difference = compute_appearance_difference(current_pixel_RGB, neighbor_pixel_RGB)
              
         # check to see if total appearance difference value is within the threshold. if so, this neighbor pixel will be put in current pixel's shape
         if total_appearance_difference_threshold - appearance_difference >= 0:

            # before adding this neighbor pixel to current shape, make sure that it also has similar appearance with the 
            # pixel shape id's RGB because if it does not then it means that appearance is gradually changing its appearance.
            # If the appearance is gradually changing and no longer look similar with the shape id's pixels, then it should not
            # be put in the same shape as the current pixel shape id.
            current_pixel_shape_RGB = original_pixel[current_pixel_shape]
                  
            appearance_difference = compute_appearance_difference(current_pixel_shape_RGB, neighbor_pixel_RGB)
                  
            if total_appearance_difference_threshold - appearance_difference >= 0:
            
               # before putting this pixel to current shape, make sure it is not already in current shape
               if not neighbor_pixel_index in shapes[current_pixel_shape]:
                  shapes[current_pixel_shape].append(neighbor_pixel_index)

'''
# finished all processing for creating all shapes from entire image pixels
# Now it's time for dealing with problem1 which is described in the document.

# this process is to put together all shapes with similar appearance sitting right next to each other.
# If two shapes are both neighbors to each other and if they are in similar appearance, they will be merged into one shape

# comparing pixels will be done with both shapes ids' pixels

cur_shape_pixels = []
next_shape_pixels = []
shape_remove = []
for cur_shape_id, cur_shape_pixels_list in shapes.items():
   print("current shape id " + str(cur_shape_id) )

   # for each one of current shapes
   for cur_shape_pixels_ in cur_shape_pixels_list:
      cur_shape_pixels.append(cur_shape_pixels_)
      
   # for each one of current shapes, process all next shapes
   for next_shape_id, next_shape_pixels_list in shapes.items():
      
      for next_shape_pixels_ in next_shape_pixels_list:
         next_shape_pixels.append(next_shape_pixels_)     
      
      
      
      # we now have two shapes to compare
      
      cur_shape_RGB = original_pixel[cur_shape_id]
      next_shape_RGB = original_pixel[next_shape_id]
      
      appearance_difference = compute_appearance_difference(cur_shape_RGB, next_shape_RGB)
               
      if total_appearance_difference_threshold - appearance_difference >= 0:
      
         # both shapes have similar appearance, now we need to determine if they are neighbors
         # processing for each one of current shape pixels
         for cur_pixel in cur_shape_pixels:
            complete = False
            
            for next_shape_pixel in next_shape_pixels:
            
               if next_shape_pixel in get_neighbor_pixels(cur_pixel):
      
                  # one or more pixels are neighbors
                  # merging current shape pixels into next shape
                  for cur_pixel1 in cur_shape_pixels:
                     shapes[next_shape_id].append(cur_pixel1)
      
                  # for deleting merged shape
                  shape_remove.append(cur_shape_id)
                  
                  complete = True
                  
                  break

            if complete == True:
               break

      if complete == True:
         continue


for shape in shape_remove:
   shapes.pop(shape)

'''



file = open('shapes/' + image_filename + ' shapes.txt', 'w')
file.write(str(shapes))
file.close()








