





#  parameter in and out is a dictionary with following form.
#    pixels[pixel_counter] = {}
#    pixels[pixel_counter] ['x'] = x
#    pixels[pixel_counter] ['y'] = y
    
def get_boundary_pixels(pixels_dict):


   pixel_boundaries = {}


   # first, we are going to get boundaries horizontally



   smallest_y = min(int(d['y']) for d in pixels_dict.values())
   largest_y = max(int(d['y']) for d in pixels_dict.values())

   print("smallest y value " + str(smallest_y))
   print("largest y value " + str(largest_y))
 
 
 

   pixel_counter = 1



   # for loop for going from smallest y value to the largest y value
   # this means going from very top pixel to very bottom pixel
   #  for y in range(start, stop) stop value is excluded
   for y in range(smallest_y, largest_y + 1):

      # pixel_ids_with_current_y_values contains all xy coordinate pairs that have the current running y value.
      pixel_ids_with_current_y_values = [k for k in pixels_dict  if (int(pixels_dict[k]['y'])) == y]
      
      first = True
      
      
      # we first obtain all x values for the current running y value
      x_values_list_in_current_y = []
      
      
      '''
      -------------------        boundary finding algorithm            ---------------------------
      
      With current running y value, boundary is where there is no consecutive x values. This means there is no more 
      neighbor x values on the right or left side.  The " boundary left side " has missing x values on the " left " ( no more smaller x values )
      The " boundary right side " has missing x values on the " right " ( missing neighbor larger x values for a while )
      finally, the smallest and largest x values are the farthest of all pixels in the current running y value.
      '''
      
      # key is the coordinate pair id.  
      for key in pixel_ids_with_current_y_values:
      
         # putting all x values for all xy coordinates that have current running y vaule
         x_values_list_in_current_y.append(pixels_dict[key]['x'])

      
      # we need to sort x values so that we can work with neighbor x values
      x_values_list_in_current_y.sort()
      
      # this is for getting the largest x value in current running y. largest x value is the last one in current running y because
      # x values are sorted from smallest to largest
      x_counter_in_current_running_y = 1
      
      x_numbers_in_current_running_y = len(x_values_list_in_current_y)


      for x_value in x_values_list_in_current_y:
 
         print(" y value is " + str(y) )
         print(x_value)
         
         # boundary is also on smallest y and largest y because very top and very bottom will be the boundaries
         # this is for the very top
         if y == smallest_y:
            pixel_boundaries[pixel_counter] = {}
            pixel_boundaries[pixel_counter]['x'] = x_value
            pixel_boundaries[pixel_counter]['y'] = y                 

    
         # boundary is also on smallest y and largest y because very top and very bottom will be the boundaries
         # this is for the bottom
         if y == largest_y:
            pixel_boundaries[pixel_counter] = {}
            pixel_boundaries[pixel_counter]['x'] = x_value
            pixel_boundaries[pixel_counter]['y'] = y                 
         
         # checking to see if x value is the last one in current running y
         if x_counter_in_current_running_y == x_numbers_in_current_running_y:
         
            pixel_boundaries[pixel_counter] = {}
            pixel_boundaries[pixel_counter]['x'] = x_value
            pixel_boundaries[pixel_counter]['y'] = y                


         # smallest x value and largest x value in the current running y value are the farthest boundary pixels
         # x values are sorted, so smallest x value in current running y is the first x value
         if first != False:
         
            pixel_boundaries[pixel_counter] = {}
            pixel_boundaries[pixel_counter]['x'] = x_value
            pixel_boundaries[pixel_counter]['y'] = y            
            
            first = False
            
         else:
         
             # if two consecutive pixels are right next to each other, the difference of them should produce 1
             if abs( x_value - previous_x_value ) > 1:
                # boundary is found
                
                print("boundary found. current x value is " + str(x_value))
                print("previous x value is " + str(previous_x_value))

                if x_value - previous_x_value < 0:
                   # result is negative, this means current x value is smaller ( it is on the left relative to previous )
                   # then, current x value is the boundary pixel " on the left side "

                   pixel_boundaries[pixel_counter] = {}
                   pixel_boundaries[pixel_counter]['x'] = x_value
                   pixel_boundaries[pixel_counter]['y'] = y
                

                else:

                   # result is positive, this means current x value is larger than previous ( it is on the right relative 
                   # to previous ). Then, current x value is the boundary pixel " on the right side " relative to previous

                   pixel_boundaries[pixel_counter] = {}
                   pixel_boundaries[pixel_counter]['x'] = x_value
                   pixel_boundaries[pixel_counter]['y'] = y
                
                
         previous_x_value = x_value               

         pixel_counter += 1
         x_counter_in_current_running_y += 1











   # -----------------------------          now this is for getting boundaries vertically        ----------------------------------------



   smallest_x = min(int(d['x']) for d in pixels_dict.values())
   largest_x = max(int(d['x']) for d in pixels_dict.values())

   print("smallest x value " + str(smallest_y))
   print("largest x value " + str(largest_y))
 

   pixel_counter = 1

   # for loop for going from smallest y value to the largest y value
   # this means going from very top pixel to very bottom pixel
   #  for y in range(start, stop) stop value is excluded
   for x in range(smallest_x, largest_x + 1):

      # pixel_ids_with_current_x_values contains all xy coordinate pairs that have the current running x value.
      pixel_ids_with_current_x_values = [k for k in pixels_dict  if (int(pixels_dict[k]['x'])) == x]
      
      first = True
      y_counter_in_current_running_x = 1
      
      # we first obtain all y values for the current running x value
      y_values_list_in_current_x = []
      
      
      '''
      -------------------        boundary finding algorithm            ---------------------------
      
      With current running x value, boundary is where there is no consecutive y values. This means there is no more 
      neighbor y values on the top or bottom.  The " boundary top side " has missing y values on the " top " ( no more smaller y values )
      The " boundary bottom side " has missing y values on the " bottom " ( missing neighbor larger y values) 
      '''
      
      # key is the coordinate pair id.  
      for key in pixel_ids_with_current_x_values:
      
         # putting all y values for all xy coordinates that have current running x vaule
         y_values_list_in_current_x.append(pixels_dict[key]['y'])

      
      # we need to sort x values so that we can work with neighbor x values
      y_values_list_in_current_x.sort()
      
      print(" y values list when x is " + str(x))
      print( y_values_list_in_current_x )
	  

      for y_value in y_values_list_in_current_x:
 
         print(" y value is " + str(y_value) )
         print(x)
         
         print("current y counter is " + str(y_counter_in_current_running_x) )
         print(" current y count is " + str(len(y_values_list_in_current_x) ) )        
         
         # check if current y value is the last one in the current running y
         if y_counter_in_current_running_x == len(y_values_list_in_current_x):
         

         
            pixel_boundaries[pixel_counter] = {}

            pixel_boundaries[pixel_counter]['x'] = x
            pixel_boundaries[pixel_counter]['y'] = y_value

            print("boundary found. current y value is " + str(y_value) + " x value is " + str(x))

         
         
         # for the current running x value (all pixels vertically ), first y is the very top pixel which should be boundary
         if first == True:
         
            print("boundary found. current y value is " + str(y_value) + " x value is " + str(x))
      
            pixel_boundaries[pixel_counter] = {}

            pixel_boundaries[pixel_counter]['x'] = x
            pixel_boundaries[pixel_counter]['y'] = y_value 
 
            previous_y_value = y_value
            first = False
         else:          

            # if two consecutive pixels are right next to each other, the difference of them should produce 1
            if abs( y_value - previous_y_value ) > 1:
               # boundary is found
                
               print("boundary found. current y value is " + str(y_value) + " x value is " + str(x))


               pixel_boundaries[pixel_counter] = {}

               pixel_boundaries[pixel_counter]['x'] = x
               pixel_boundaries[pixel_counter]['y'] = y_value                
                
         previous_y_value = y_value    

         pixel_counter += 1
         y_counter_in_current_running_x += 1




      print(" end of current x ")

      print("")





   return pixel_boundaries















boundary_shapes = {1: {6: {'x': 197, 'y': 32}, 7: {'x': 198, 'y': 32}, 8: {'x': 199, 'y': 32}, 9: {'x': 200, 'y': 32}}, 2: {10: {'x': 203, 'y': 32}, 11: {'x': 204, 'y': 32}, 12: {'x': 205, 'y': 32}, 13: {'x': 206, 'y': 32}}, 3: {14: {'x': 184, 'y': 33}, 15: {'x': 185, 'y': 33}, 20: {'x': 183, 'y': 34}, 21: {'x': 184, 'y': 34}, 22: {'x': 185, 'y': 34}, 23: {'x': 182, 'y': 35}, 25: {'x': 181, 'y': 36}, 26: {'x': 182, 'y': 36}, 27: {'x': 183, 'y': 36}, 28: {'x': 180, 'y': 37}, 29: {'x': 181, 'y': 37}, 30: {'x': 179, 'y': 38}, 31: {'x': 180, 'y': 38}}}


pixels =  {1: {'x': 179, 'y': 38}, 2: {'x': 180, 'y': 37}, 3: {'x': 180, 'y': 38}, 4: {'x': 181, 'y': 36}, 5: {'x': 181, 'y': 37}, 7: {'x': 182, 'y': 36}, 8: {'x': 183, 'y': 34}, 9: {'x': 183, 'y': 36}, 11: {'x': 184, 'y': 34}, 12: {'x': 185, 'y': 33}, 13: {'x': 185, 'y': 34}, 14: {'x': 186, 'y': 33}, 15: {'x': 187, 'y': 33}, 6: {'x': 182, 'y': 35}, 10: {'x': 184, 'y': 33}, 27: { 'x': 182, 'y': 37}, 22: { 'x': 181, 'y': 38}, 29: { 'x': 184, 'y': 35}}


return_values = get_boundary_pixels(pixels)


print(return_values)




































'''
determine_base_shapes(boundary_shapes)



# input parameter is boundary_shapes returned by get_boundary_shapes function
# boundary_shapes contains boundary shape number, pixel number, xy values
# form is shown below
# boundary shapes[ boundary shape number ][ pixel number ]['x']
# boundary shapes[ boundary shape number ][ pixel number ]['y']
def determine_base_shapes( boundary_shapes ):
'''






















































































