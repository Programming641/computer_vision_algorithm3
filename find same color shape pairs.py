

import shapes_functions
import pixel_functions


filename = "birdcopy face color group"

directory = "bird"

# directory is specified but does not contain /
if directory != "" and directory.find('/') == -1:
   directory +='/'

# for creating repeating shape pattern file
sampe_color_pair_filename = "shapes/" + filename + " with same color pairs.txt"


# return value
# shapes_colors[shape_id] = { 'r': r, 'g': g, 'b': b }
# { shape_id: { 'r': r, 'g': g, 'b': b } }
shapes_colors = shapes_functions.get_shapes_colors(filename, directory)


# return value
# { shape_id: [ neighbor id1 , neighbor_id2....] }
shape_neighbors = shapes_functions.find_direct_shape_neighbors(filename, directory)

# shape_pairs contains all shapes with all their direct neighbors in pair
# we need to get shape pair with their colors
# shape pair is the direct neighbors
# { 1: [{ shape_id1: { 'r': r, 'g': g, 'b': b } }, { shape_id2: { 'r': r, 'g': g, 'b': b } ], 2: 
# [{ shape_id3: { 'r': r, 'g': g, 'b': b } }, { shape_id4: { 'r': r, 'g': g, 'b': b } .... } ]
# more general form
# 1 is outer dict keys
# [ ] is outer dict value
# [ {}, {} ] list value contains shape_ids in dict
# [ { dict key : { } }, { dict_key2 : { } } ]
shape_pairs = {}
shape_pair_counter = 1
pair_list_index = 0


# looping all shapes with their neighbor shapes
for current_shape_id in shape_neighbors:

   # neighbors of current shape
   for shape_neighbor in shape_neighbors[current_shape_id]:

      shape_pairs[shape_pair_counter] = []
      
      for color_shape_id in shapes_colors:

         if current_shape_id == color_shape_id:

            temp_dict = { current_shape_id: {} }
            shape_pairs[shape_pair_counter].append(temp_dict)
            shape_pairs[shape_pair_counter][pair_list_index][current_shape_id]['r'] = shapes_colors[color_shape_id]['r']
            shape_pairs[shape_pair_counter][pair_list_index][current_shape_id]['g'] = shapes_colors[color_shape_id]['g']
            shape_pairs[shape_pair_counter][pair_list_index][current_shape_id]['b'] = shapes_colors[color_shape_id]['b']
            
            pair_list_index += 1
         elif color_shape_id == shape_neighbor:
         
            temp_dict = { shape_neighbor: {} }
            shape_pairs[shape_pair_counter].append(temp_dict)
            shape_pairs[shape_pair_counter][pair_list_index][shape_neighbor]['r'] = shapes_colors[color_shape_id]['r']
            shape_pairs[shape_pair_counter][pair_list_index][shape_neighbor]['g'] = shapes_colors[color_shape_id]['g']
            shape_pairs[shape_pair_counter][pair_list_index][shape_neighbor]['b'] = shapes_colors[color_shape_id]['b']      
            
            pair_list_index += 1        
            
            
         if pair_list_index == 2:
            shape_pair_counter += 1
            pair_list_index = 0
            break

# removing duplicates
result = {}
for key,value in shape_pairs.items():
    if value not in result.values():
        result[key] = value

shape_pairs = result

# ----------------      find same color pair algorithm      -----------------------
# current shape1 in pair compares with another shape1 in pair
# current shape2 in pair compares with another shape2 in pair
# current shape1 in pair compares with another shape2 in pair
# current shape2 in pair compares with another shape1 in pair
# if both are within the appearance_difference_threshold, comparing shape pair has the same color as the current running pair

appearance_difference_threshold = 10

# { shape pair number : [ [ shape_id1, shape_id2 ] , [shape_id3, shape_id4 ] .... ] , shape pair number :
# [ [ shape_id1, shape_id2 ], [shape_id3, shape_id4], .... ]
same_color_pairs = {}

pair_shape_counter = 1

shape_pair_list = []
      
for shape_pair_counter in shape_pairs:

   # shape_pair contains two shapes in the list
   # example {'46650': {'r': 204, 'g': 102, 'b': 102}}
  
   print(" same color pair counter " + str(pair_shape_counter))  
   same_color_pairs[pair_shape_counter] = []
   current_first = True

   # shape_pair is one shape of the pair     
   for shape_pair in shape_pairs[shape_pair_counter]:
   
      for shape_id in shape_pair:

         # getting one shape of current pair      
         if current_first == True:
         
            current_shape1_id = shape_id
            current_shape1_red = shape_pair[shape_id]['r']
            current_shape1_green = shape_pair[shape_id]['g']         
            current_shape1_blue = shape_pair[shape_id]['b']           

            current_shape1_rgb = current_shape1_red, current_shape1_green, current_shape1_blue, 255
            
            shape_pair_list.append(shape_id)

            current_first = False

         # getting second shape of current pair
         else:
         
            current_shape2_id = shape_id
            current_shape2_red = shape_pair[shape_id]['r']
            current_shape2_green = shape_pair[shape_id]['g']         
            current_shape2_blue = shape_pair[shape_id]['b']           

            current_shape2_rgb = current_shape2_red, current_shape2_green, current_shape2_blue, 255       

            shape_pair_list.append(shape_id)



   # adding current shape pair to same_color_pairs
   same_color_pairs[pair_shape_counter].append(shape_pair_list)
   current_shape_list_index = 0

   # for putting another pair, empty the shape_pair_list
   shape_pair_list = []

   for compare_shape_pair_counter in shape_pairs:
   
      # for putting another pair, empty the shape_pair_list
      shape_pair_list = []   

      compare_first = True
      skip = False
      
      # compare_shape_pair is one shape of the pair
      for compare_shape_pair in shape_pairs[compare_shape_pair_counter]:
      
         
         for compare_shape_id in compare_shape_pair:
            
            # getting one shape of compare pair      
            if compare_first == True:
               compare_shape1_id = compare_shape_id
               compare_shape1_red = compare_shape_pair[compare_shape_id]['r']
               compare_shape1_green = compare_shape_pair[compare_shape_id]['g']         
               compare_shape1_blue = compare_shape_pair[compare_shape_id]['b']           

               compare_shape1_rgb = compare_shape1_red, compare_shape1_green, compare_shape1_blue, 255
                  
               shape_pair_list.append(compare_shape_id)
               compare_first = False

            # getting second shape of compare pair
            else:
               compare_shape2_id = compare_shape_id
               compare_shape2_red = compare_shape_pair[compare_shape_id]['r']
               compare_shape2_green = compare_shape_pair[compare_shape_id]['g']         
               compare_shape2_blue = compare_shape_pair[compare_shape_id]['b']           

               compare_shape2_rgb = compare_shape2_red, compare_shape2_green, compare_shape2_blue, 255

               shape_pair_list.append(compare_shape_id)
                  
      if compare_shape1_id == current_shape1_id or compare_shape1_id == current_shape2_id:
         if compare_shape2_id == current_shape1_id or compare_shape2_id == current_shape2_id:
            # current pair is compare pair. skip this comparing processing
            skip = True
            shape_pair_list = []

            same_color_pairs[pair_shape_counter].pop(current_shape_list_index)
            
      if not skip == True:
          total_difference1 = pixel_functions.compute_appearance_difference( current_shape1_rgb, compare_shape1_rgb)
          total_difference2 = pixel_functions.compute_appearance_difference( current_shape2_rgb, compare_shape1_rgb)
                
          # first compare current shape1 with compare shape1
          if total_difference1 <= appearance_difference_threshold:
                
             total_difference = pixel_functions.compute_appearance_difference( current_shape2_rgb, compare_shape2_rgb)
                   
             if total_difference <= appearance_difference_threshold:
                # compare pair is the repeating pattern with current pair

                same_color_pairs[pair_shape_counter].append(shape_pair_list)
                current_shape_list_index += 1

          elif total_difference2 <= appearance_difference_threshold:

             total_difference = pixel_functions.compute_appearance_difference( current_shape1_rgb, compare_shape2_rgb)

             if total_difference <= appearance_difference_threshold:
                # compare pair is the repeating pattern with current pair

                same_color_pairs[pair_shape_counter].append(shape_pair_list)
                current_shape_list_index += 1

          else:
             # current compare pair was not the repeating pattern with current running pair
             shape_pair_list = []

   if len(same_color_pairs[pair_shape_counter]) == 0:
      same_color_pairs.pop(pair_shape_counter)
   pair_shape_counter += 1


f = open(sampe_color_pair_filename, "w")
f.write(str(same_color_pairs))
f.close()



        






