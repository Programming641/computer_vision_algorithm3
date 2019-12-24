
import shapes_functions
import copy



def find_brightness_change(current_shape_id_color, current_neighbor_color):

   all_positive = False
   all_negative = False
   red_difference = current_shape_id_color['r'] - current_neighbor_color['r']
   green_difference = current_shape_id_color['g'] - current_neighbor_color['g']
   blue_difference = current_shape_id_color['b'] - current_neighbor_color['b']
  
   # make sure that all signs are the same otherwise it is considered color change
   # checking here for all positive signs
   if red_difference > 0 and green_difference > 0 and blue_difference > 0:
      all_positive = True
  
   # checking here for all negative signs
   if red_difference < 0 and green_difference < 0 and blue_difference < 0:
      all_negative = True
  

   # proceed to process if different signs are not present
   if all_negative == True or all_positive == True:
     
      average_difference = ( abs(red_difference) + abs(green_difference) + abs(blue_difference) ) / 3
      
      red_difference = average_difference - abs(red_difference)
      green_difference = average_difference - abs(green_difference)
      blue_difference = average_difference - abs(blue_difference)
      
      total_difference = abs(red_difference) + abs(green_difference) + abs(blue_difference)
      
      if total_difference <= brightness_threshold:
         # current neighbor has the brightness change from the current running shape
         return True


   return False

def process_neighbor(brightness_current_shape_id, neighbor):
   global shape_neighbors
   global shapes_colors
   global brightness_neighbors

   if neighbor in already_processed_neighbor:
      return

   # now, we need to find all neighbors of found neighbor
   for shape_id in shape_neighbors:
   
      if neighbor == shape_id:
       
         # we need to get rgb values for current running shape and neighbor's rgb values to see if only brightness changed
         # in here, we get color for current running shape id
         for shape_color_id in shapes_colors:
            if shape_id == shape_color_id:
               current_shape_id_color = shapes_colors[shape_color_id]
               break
           
         # getting all neighbors of current neighbor
         # neighbor_neighbor is each of neighbors in the list
         for neighbor_neighbor in shape_neighbors[shape_id]:
         
            # checking if current neighbor is not processed
            if not neighbor_neighbor in brightness_neighbors[brightness_current_shape_id]:
                

                # now we get colors for shape id's neighbors
                for shape_color_id in shapes_colors:
                   if neighbor_neighbor == shape_color_id:
                      current_neighbor_color  = shapes_colors[shape_color_id]
                      break               

                brightness_changed = find_brightness_change(current_shape_id_color, current_neighbor_color)

                if brightness_changed == True:
                   brightness_neighbors[brightness_current_shape_id].append(neighbor_neighbor)
                   process_neighbor(brightness_current_shape_id, neighbor_neighbor)

   already_processed_neighbor.append(neighbor)


filename = "brightness test"

directory = ""

# directory is specified but does not contain /
if directory != "" and directory.find('/') == -1:
   directory +='/'


brightness_change_filename = "shapes/" + filename + " with brightness change.txt"

already_processed_neighbor = []


shapes_colors = shapes_functions.get_shapes_colors(filename, directory)


shape_neighbors = shapes_functions.find_direct_shape_neighbors(filename, directory)


print(" real processing now begins" )

brightness_threshold = 10

# for storing neighbors that have brightness change
brightness_neighbors = {}

# looping all shapes with their neighbor shapes
for shape_id in shape_neighbors:

   if shape_id in already_processed_neighbor:
      continue

   # checking to see if shape is already processed
   for temp_shape_id in brightness_neighbors:
      if shape_id in brightness_neighbors[temp_shape_id]:
         continue

   # create brightness parent shape only if shape is not contained in any brightness shape
   brightness_neighbors[shape_id] = []
   
   # we need to get rgb values for current running shape and neighbor's rgb values to see if only brightness changed
   # in here, we get color for current running shape id
   for shape_color_id in shapes_colors:
      if shape_id == shape_color_id:
         current_shape_id_color = shapes_colors[shape_color_id]
         break

   # shape neighbors of current running shape
   # shape_neighbors[shape_id] contains the neighbors in the list type
   for neighbor in shape_neighbors[shape_id]:

      # now we get colors for shape id's neighbors
      for shape_color_id in shapes_colors:
         if neighbor == shape_color_id:
            current_neighbor_color  = shapes_colors[shape_color_id]
            break               

      brightness_changed = find_brightness_change(current_shape_id_color, current_neighbor_color)

      if brightness_changed == True:
         brightness_neighbors[shape_id].append(neighbor)
         # we now need to find neighbor's neighbors and see if neighbor's neighbors have brightness change
         process_neighbor(shape_id, neighbor)



                
   # for current running shape, there are no neighbors found that have brightness changed
   if len(brightness_neighbors[shape_id]) == 0:
      brightness_neighbors.pop(shape_id)

   already_processed_neighbor.append(shape_id)

f = open(brightness_change_filename, "w")
f.write(str(brightness_neighbors))
f.close()




