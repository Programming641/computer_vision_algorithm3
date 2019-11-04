#
# algorithm for determining the closest match with the color group uses how far away the RGB value is from original
#
#

from PIL import Image


from collections import OrderedDict



original_image = Image.open("images/bird01.png")
original_pixel = original_image.getdata()
image_size = original_image.size


already_compared_pixels = []

# shapes[shape's index value ] = [ pixel index1, pixel index2, .... ]
shapes = OrderedDict()


def compute_appearance_difference(current_pix, compare_pixel):

   original_red, original_green, original_blue, alpha = current_pix

   compare_red, compare_green, compare_blue, alpha = compare_pixel
    
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












#image_size[0] is width
for y in range(image_size[1]):
   print("y is " + str(y))


   for x in range(image_size[0]):
   
      # assigning the positions for comparing neighbor pixels. starting with top going clockwise.
      neighbor_position_dict = { 'top' : False, 'top_right' : False, 'right' : False, 'bottom_right': False, 'bottom': False, 'bottom_left' : False, 'left': False, 'top_left': False }

   
      # converting for the getdata(). y is the row that you want to get data for. current_pixel_index is the current pixel's index number
      current_pixel_index = (y * image_size[0])+ x    

      if current_pixel_index == 377:
         debug = True	  
      
      # initializing current pixel' shape number. This 
      current_pixel_shape = None
      
      
      total_appearance_difference_threshold = 55
      
      # check if current pixel is in other pixel's shapes.
      if len(shapes) != 0:
        # last in first out
        for shape_id, value_list in reversed(shapes.items()):
          for values in value_list:
             if values == current_pixel_index:
                current_pixel_shape = shape_id

      # if current pixel is not in other pixel's shape, then create shape based on current pixel's index number
      if current_pixel_shape == None:
         current_pixel_shape = current_pixel_index
         # make sure to put current pixel in current pixel shape
         shapes[current_pixel_shape] = [current_pixel_shape]
		 


      
#  ----------------------------------------------------      determining current pixel's position      ----------------------------------------------------
   
      # determining if the current pixel is the leftmost pixel
      # no need to compare with top left, left, bottom left
      if x == 0:
         neighbor_position_dict['top_left'] = True
         neighbor_position_dict['left'] = True
         neighbor_position_dict['bottom_left'] = True


      # determing the first row
      # no need to compare with top left, top, top right
      if current_pixel_index <= image_size[0] -1:
         neighbor_position_dict['top_left'] = True
         neighbor_position_dict['top'] = True
         neighbor_position_dict['top_right'] = True

        

      # determining the rightmost pixel. x counts from 0 to width - 1
      # no need to compare with top right, right, bottom right
      if x == image_size[0] - 1:
         neighbor_position_dict['top_right'] = True
         neighbor_position_dict['right'] = True
         neighbor_position_dict['bottom_right'] = True

      # determining last row . y counts from 0 to height - 1
      # no need to compare with bottom left, bottom, bottom right
      if y == image_size[1] - 1:
         neighbor_position_dict['bottom_left'] = True
         neighbor_position_dict['bottom'] = True
         neighbor_position_dict['bottom_right'] = True
    
#  ----------------------------------------------------      determining current pixel's position     END     -------------------------------------------------

    
      #getting current pixel RGB values
      current_pixel_RGB = original_pixel[current_pixel_index]

#  ----------------------------------------------------      start comparing with neighbor pixel              -------------------------------------------------



      if neighbor_position_dict['top'] == False:
      
         # current pixel's top neighbor can be found by subtrating image width from current pixel index number
         top_pixel_RGB = original_pixel[current_pixel_index - image_size[0]]
      
         top_pixel_index = current_pixel_index - image_size[0]
      
         # check if top neighbor pixel is already compared. if not, then execute compare.
         if top_pixel_index not in already_compared_pixels:

            # what's returned is total appearance difference value
            appearance_difference = compute_appearance_difference(current_pixel_RGB, top_pixel_RGB)
              
            # check to see if total appearance difference value is within the threshold. if so, this neighbor pixel will be put in current pixel's shape
            if total_appearance_difference_threshold - appearance_difference >= 0:

               # before putting this neighbor pixel in shape, check if it is already in the shape to avoid duplicates
               if (top_pixel_index in  shapes[current_pixel_shape] ) == False:
                  
				  # before adding this neighbor pixel to current shape, make sure that it also has similar appearance with the 
				  # pixel shape id's RGB because if it does not then it means that appearance is gradually changing its appearance.
				  # If the appearance is gradually changing and no longer look similar with the shape id's pixels, then it should not
				  # be put in the same shape as the current pixel shape id.
				  current_pixel_shape_RGB = original_pixel[current_pixel_shape]
				  
				  appearance_difference = compute_appearance_difference(current_pixel_shape_RGB, top_pixel_RGB)
				  
				  if total_appearance_difference_threshold - appearance_difference >= 0:
                     shapes[current_pixel_shape].append(top_pixel_index)

      
      
      
      if neighbor_position_dict['top_right'] == False:

         # top right neighbor pixel is next to the top neighbor pixel
         top_right_pixel_RGB = original_pixel[current_pixel_index - image_size[0] + 1 ]
         
         top_right_pixel_index = current_pixel_index - image_size[0] + 1

         # check if top right neighbor pixel is already compared. if not, then execute compare.
         if top_right_pixel_index not in already_compared_pixels:

           # what's returned is total appearance difference value
           appearance_difference = compute_appearance_difference(current_pixel_RGB, top_right_pixel_RGB)
          
           # check to see if total appearance difference value is within the threshold. if so, this neighbor pixel will be put in current pixel's shape
           if total_appearance_difference_threshold - appearance_difference >= 0:

              # before putting this neighbor pixel in shape, check if it is already in the shape.
              if (top_right_pixel_index in  shapes[current_pixel_shape] ) == False:
			  
				  # before adding this neighbor pixel to current shape, make sure that it also has similar appearance with the 
				  # pixel shape id's RGB because if it does not then it means that appearance is gradually changing its appearance.
				  # If the appearance is gradually changing and no longer look similar with the shape id's pixels, then it should not
				  # be put in the same shape as the current pixel shape id.
				  current_pixel_shape_RGB = original_pixel[current_pixel_shape]
				  
				  appearance_difference = compute_appearance_difference(current_pixel_shape_RGB, top_right_pixel_RGB)
				  
				  if total_appearance_difference_threshold - appearance_difference >= 0:
                     shapes[current_pixel_shape].append(top_right_pixel_index)
          
              


      if neighbor_position_dict['right'] == False:

         # right neighbor pixel is next to the current pixel
         right_pixel_RGB = original_pixel[current_pixel_index + 1 ]

         right_pixel_index = current_pixel_index + 1

         # check if right neighbor pixel is already compared. if not, then execute compare.
         if  right_pixel_index not in already_compared_pixels:

            # what's returned is total appearance difference value
            appearance_difference = compute_appearance_difference(current_pixel_RGB, right_pixel_RGB)
              
            # check to see if total appearance difference value is within the threshold. if so, this neighbor pixel will be put in current pixel's shape
            if total_appearance_difference_threshold - appearance_difference >= 0:
   
               # before putting this neighbor pixel in shape, check if it is already in the shape.               
               if (right_pixel_index in  shapes[current_pixel_shape] ) == False:   
			   
				  # before adding this neighbor pixel to current shape, make sure that it also has similar appearance with the 
				  # pixel shape id's RGB because if it does not then it means that appearance is gradually changing its appearance.
				  # If the appearance is gradually changing and no longer look similar with the shape id's pixels, then it should not
				  # be put in the same shape as the current pixel shape id.
				  current_pixel_shape_RGB = original_pixel[current_pixel_shape]
				  
				  appearance_difference = compute_appearance_difference(current_pixel_shape_RGB, right_pixel_RGB)
				  
				  if total_appearance_difference_threshold - appearance_difference >= 0:	  			                    
                     shapes[current_pixel_shape].append(right_pixel_index)





      if neighbor_position_dict['bottom_right'] == False:

         # bottom right neighbor pixel is next to the bottom
         bottom_right_pixel_RGB = original_pixel[current_pixel_index + image_size[0] + 1 ]


         bottom_right_pixel_index = current_pixel_index + image_size[0] + 1

         # check if top right neighbor pixel is already compared. if not, then execute compare.
         if bottom_right_pixel_index not in already_compared_pixels:

            # what's returned is total appearance difference value
            appearance_difference = compute_appearance_difference(current_pixel_RGB, bottom_right_pixel_RGB)
              
            # check to see if total appearance difference value is within the threshold. if so, this neighbor pixel will be put in current pixel's shape
            if total_appearance_difference_threshold - appearance_difference >= 0:
 
               # before putting this neighbor pixel in shape, check if it is already in the shape.   
               if (bottom_right_pixel_index in  shapes[current_pixel_shape] ) == False:     
			   
				  # before adding this neighbor pixel to current shape, make sure that it also has similar appearance with the 
				  # pixel shape id's RGB because if it does not then it means that appearance is gradually changing its appearance.
				  # If the appearance is gradually changing and no longer look similar with the shape id's pixels, then it should not
				  # be put in the same shape as the current pixel shape id.
				  current_pixel_shape_RGB = original_pixel[current_pixel_shape]
				  
				  appearance_difference = compute_appearance_difference(current_pixel_shape_RGB, bottom_right_pixel_RGB)
				  
				  if total_appearance_difference_threshold - appearance_difference >= 0:				                     
                     shapes[current_pixel_shape].append(bottom_right_pixel_index)






      if neighbor_position_dict['bottom'] == False:

         # bottom neighbor pixel is found by adding image width
         bottom_pixel_RGB = original_pixel[current_pixel_index + image_size[0] ]

         bottom_pixel_index = current_pixel_index + image_size[0]

         # check if top right neighbor pixel is already compared. if not, then execute compare.
         if bottom_pixel_index not in already_compared_pixels:
  
            # what's returned is total appearance difference value
            appearance_difference = compute_appearance_difference(current_pixel_RGB, bottom_pixel_RGB)
              
            # check to see if total appearance difference value is within the threshold. if so, this neighbor pixel will be put in current pixel's shape
            if total_appearance_difference_threshold - appearance_difference >= 0:
 
               # before putting this neighbor pixel in shape, check if it is already in the shape.   
               if (bottom_pixel_index in  shapes[current_pixel_shape] ) == False:   
			   
				  # before adding this neighbor pixel to current shape, make sure that it also has similar appearance with the 
				  # pixel shape id's RGB because if it does not then it means that appearance is gradually changing its appearance.
				  # If the appearance is gradually changing and no longer look similar with the shape id's pixels, then it should not
				  # be put in the same shape as the current pixel shape id.
				  current_pixel_shape_RGB = original_pixel[current_pixel_shape]
				  
				  appearance_difference = compute_appearance_difference(current_pixel_shape_RGB, bottom_pixel_RGB)
				  
				  if total_appearance_difference_threshold - appearance_difference >= 0:	                  
                     shapes[current_pixel_shape].append(bottom_pixel_index)





      if neighbor_position_dict['bottom_left'] == False:

         # bottom left neighbor pixel is by subtracting from bottom pixel
         bottom_left_pixel_RGB = original_pixel[current_pixel_index + image_size[0] - 1 ]

         bottom_left_pixel_index = current_pixel_index + image_size[0] - 1

         # check if top right neighbor pixel is already compared. if not, then execute compare.
         if bottom_left_pixel_index not in already_compared_pixels:

            # what's returned is total appearance difference value
            appearance_difference = compute_appearance_difference(current_pixel_RGB, bottom_left_pixel_RGB)
              
            # check to see if total appearance difference value is within the threshold. if so, this neighbor pixel will be put in current pixel's shape
            if total_appearance_difference_threshold - appearance_difference >= 0:

               # before putting this neighbor pixel in shape, check if it is already in the shape.   
               if (bottom_left_pixel_index in  shapes[current_pixel_shape] ) == False:        

				  # before adding this neighbor pixel to current shape, make sure that it also has similar appearance with the 
				  # pixel shape id's RGB because if it does not then it means that appearance is gradually changing its appearance.
				  # If the appearance is gradually changing and no longer look similar with the shape id's pixels, then it should not
				  # be put in the same shape as the current pixel shape id.
				  current_pixel_shape_RGB = original_pixel[current_pixel_shape]
				  
				  appearance_difference = compute_appearance_difference(current_pixel_shape_RGB, bottom_left_pixel_RGB)
				  
				  if total_appearance_difference_threshold - appearance_difference >= 0:	
                     shapes[current_pixel_shape].append(bottom_left_pixel_index)





      if neighbor_position_dict['left'] == False:

         # left neighbor pixel is by subtracting from current pixel
         left_pixel_RGB = original_pixel[current_pixel_index - 1 ]


         left_pixel_index = current_pixel_index - 1

         # check if top right neighbor pixel is already compared. if not, then execute compare.
         if left_pixel_index not in already_compared_pixels:

            # what's returned is total appearance difference value
            appearance_difference = compute_appearance_difference(current_pixel_RGB, left_pixel_RGB)
              
            # check to see if total appearance difference value is within the threshold. if so, this neighbor pixel will be put in current pixel's shape
            if total_appearance_difference_threshold - appearance_difference >= 0:
   
                # before putting this neighbor pixel in shape, check if it is already in the shape.                   
                if (left_pixel_index in  shapes[current_pixel_shape] ) == False:      

				  # before adding this neighbor pixel to current shape, make sure that it also has similar appearance with the 
				  # pixel shape id's RGB because if it does not then it means that appearance is gradually changing its appearance.
				  # If the appearance is gradually changing and no longer look similar with the shape id's pixels, then it should not
				  # be put in the same shape as the current pixel shape id.
				  current_pixel_shape_RGB = original_pixel[current_pixel_shape]
				  
				  appearance_difference = compute_appearance_difference(current_pixel_shape_RGB, left_pixel_RGB)
				  
				  if total_appearance_difference_threshold - appearance_difference >= 0:	
                     shapes[current_pixel_shape].append(left_pixel_index)




      if neighbor_position_dict['top_left'] == False:

         # top left neighbor pixel is by subtracting from top pixel
         top_left_pixel_RGB = original_pixel[current_pixel_index - image_size[0] - 1 ]

         top_left_pixel_index = current_pixel_index - image_size[0] - 1

         # check if this neighbor pixel is already compared. if not, then execute compare.
         if top_left_pixel_index not in already_compared_pixels:

            # what's returned is total appearance difference value
            appearance_difference = compute_appearance_difference(current_pixel_RGB, top_left_pixel_RGB)
              
            # check to see if total appearance difference value is within the threshold. if so, this neighbor pixel will be put in current pixel's shape
            if total_appearance_difference_threshold - appearance_difference >= 0:

                # before putting this neighbor pixel in shape, check if it is already in the shape.   
                if (top_left_pixel_index in  shapes[current_pixel_shape] ) == False:       

				  # before adding this neighbor pixel to current shape, make sure that it also has similar appearance with the 
				  # pixel shape id's RGB because if it does not then it means that appearance is gradually changing its appearance.
				  # If the appearance is gradually changing and no longer look similar with the shape id's pixels, then it should not
				  # be put in the same shape as the current pixel shape id.
				  current_pixel_shape_RGB = original_pixel[current_pixel_shape]
				  
				  appearance_difference = compute_appearance_difference(current_pixel_shape_RGB, top_left_pixel_RGB)
				  
				  if total_appearance_difference_threshold - appearance_difference >= 0:	
                     shapes[current_pixel_shape].append(top_left_pixel_index)





      # current pixel is compared
      already_compared_pixels.append(current_pixel_index)


#  ----------------------------------------------------      start comparing with neighbor pixel    END       -------------------------------------------------






file = open('bird01 shapes.txt', 'w')
file.write(str(shapes))
file.close()








