
import copy
import shapes_functions
import read_files_functions
import pixel_functions


def process_neighbor(current_shape, member_shape):

   global repeating_shapes_pattern
   
   current_shape_neighbors = {}
   member_shape_neighbors = {}
   
   # looping all shapes with their neighbor shapes
   for current_shape_id in shape_neighbors:
      # getting neighbors of current_shape
      if current_shape == current_shape_id:   
         # neighbors of current shape
         for shape_neighbor in shape_neighbors[current_shape_id]:

            if not shape_neighbor in already_processed_shapes:
               for color_shape_id in shapes_colors:

                  if shape_neighbor == color_shape_id:      
                     current_shape_neighbors[shape_neighbor] = {}
                     current_shape_neighbors[shape_neighbor]['r'] = shapes_colors[color_shape_id]['r']
                     current_shape_neighbors[shape_neighbor]['g'] = shapes_colors[color_shape_id]['g']               
                     current_shape_neighbors[shape_neighbor]['b'] = shapes_colors[color_shape_id]['b']


      elif member_shape == current_shape_id:
         # neighbors of current shape
         for shape_neighbor in shape_neighbors[current_shape_id]:  
         
            if not shape_neighbor in already_processed_shapes:
               for color_shape_id in shapes_colors:

                  if shape_neighbor == color_shape_id:      
                     member_shape_neighbors[shape_neighbor] = {}
                     member_shape_neighbors[shape_neighbor]['r'] = shapes_colors[color_shape_id]['r']
                     member_shape_neighbors[shape_neighbor]['g'] = shapes_colors[color_shape_id]['g']                
                     member_shape_neighbors[shape_neighbor]['b'] = shapes_colors[color_shape_id]['b']



   for current_shape_neighbor in current_shape_neighbors:

      r = current_shape_neighbors[current_shape_neighbor]['r']
      g = current_shape_neighbors[current_shape_neighbor]['g']
      b = current_shape_neighbors[current_shape_neighbor]['b']       
      current_shape_neighbor_rgb = r, g, b, 255

      for member_shape_neighbor in member_shape_neighbors:
      
         r = member_shape_neighbors[member_shape_neighbor]['r']
         g = member_shape_neighbors[member_shape_neighbor]['g']
         b = member_shape_neighbors[member_shape_neighbor]['b']       
         member_shape_neighbor_rgb = r, g, b, 255

         already_processed_shapes.append(current_shape_neighbor)
         already_processed_shapes.append(member_shape_neighbor)

         total_difference = pixel_functions.compute_appearance_difference( current_shape_neighbor_rgb, member_shape_neighbor_rgb)

         if total_difference <= appearance_difference_threshold:

            repeating_shapes_pattern[repeating_shapes_pattern_counter].append(current_shape_neighbor)
            repeating_shapes_pattern[repeating_shapes_pattern_counter].append(member_shape_neighbor)

            process_neighbor(current_shape_neighbor, member_shape_neighbor)


   already_processed_shapes.append(current_shape)
   already_processed_shapes.append(member_shape)






filename = "birdcopy face color group"

directory = "bird"

# directory is specified but does not contain /
if directory != "" and directory.find('/') == -1:
   directory +='/'

# for creating repeating shape pattern file
repeating_shapes_pattern_filename = "shapes/" + filename + " with repeating pattern shapes.txt"


# return value
# shapes_colors[shape_id] = { 'r': r, 'g': g, 'b': b }
# { shape_id: { 'r': r, 'g': g, 'b': b } }
shapes_colors = shapes_functions.get_shapes_colors(filename, directory)


# return value
# { shape_id: [ neighbor id1 , neighbor_id2....] }
shape_neighbors = shapes_functions.find_direct_shape_neighbors(filename, directory)


same_color_pairs = read_files_functions.read_same_color_pairs_file(filename, directory)

repeating_shapes_pattern = {}
repeating_shapes_pattern_counter = 1

appearance_difference_threshold = 10

already_processed_shapes = []

current_pair_counter = 1
        
for same_color_pairs_key in same_color_pairs:

   # not processing single pair shapes because they do not have repeating shape patterns
   if len(same_color_pairs[same_color_pairs_key]) <= 1:
      continue

   print(" current running pair " + str(current_pair_counter))

   first_pair = True
   # this list is for storing member pairs of current running pair
   member_pairs_list = []
   
   # this is for looping all member pairs
   member_pairs_list_index = 0
   member_pair_shape_index = 0

   current_direct_neighbors = {}

   # pair is each pair of multiple pairs of the same colors
   # example ['8240', '8354']
   for pair in same_color_pairs[same_color_pairs_key]:
   
      # checking if both shapes of the current pair ( I don't think there is any instance that only one shape of the pair is not processed
      # because both shapes of the pair are processed
      for rpt_shapes_ptn_key in repeating_shapes_pattern:
         if pair[0] in repeating_shapes_pattern[rpt_shapes_ptn_key] and pair[1] in repeating_shapes_pattern[rpt_shapes_ptn_key]:
            continue
   
      # getting first pair as the current running pair
      # this pair compares with pairs that have the same color as the current running pair
      if first_pair == True:
         current_pair = pair
         first_pair = False
      elif first_pair == False:
         member_pairs_list.append(pair)  

   # outer loop is for looping thruogh all current pair which is the first pair of every same_color_pairs
   # this loop is for looping through all meber pairs of current pair
   for member_pair in member_pairs_list:

       repeating_shapes_pattern[repeating_shapes_pattern_counter] = []
       repeating_shapes_pattern[repeating_shapes_pattern_counter].append(current_pair[0])
       repeating_shapes_pattern[repeating_shapes_pattern_counter].append(current_pair[1])

       # checking if both shapes of the member_pair is already processed
       for rpt_shapes_ptn_key in repeating_shapes_pattern:
          if member_pair[0] in repeating_shapes_pattern[rpt_shapes_ptn_key] and member_pair[1] in repeating_shapes_pattern[rpt_shapes_ptn_key]:
             break

       repeating_shapes_pattern[repeating_shapes_pattern_counter].append(member_pair[0])  
       repeating_shapes_pattern[repeating_shapes_pattern_counter].append(member_pair[1])  
      
       # we now need to get direct neighbors of current running pair
       # looping all shapes with their neighbor shapes
       for current_shape_id in shape_neighbors:
         
          # getting direct neighbors of both shapes of the current running pair
          # this is assuming that placement of attachment (which shape is attached to which shape ) does not matter as long as
          # repeating shapes pattern occurs in the same repeating shapes group
          if current_shape_id in current_pair:

             # getting direct neighbors of both shapes of the current running pair
             # neighbors of current shape
             for shape_neighbor in shape_neighbors[current_shape_id]:   
                if not shape_neighbor in already_processed_shapes:            
                   current_direct_neighbors[shape_neighbor] = {}

          # we also need to get direct neighbors of member pair of current running pair
          elif current_shape_id in member_pair:
          
             member_pair_neighbors = {}

             # neighbors of current shape
             for shape_neighbor in shape_neighbors[current_shape_id]:
                if not shape_neighbor in already_processed_shapes:
                   # getting all neighbors of both shapes of the current member_pair
                   member_pair_neighbors[shape_neighbor] = {}

       # now we have direct neighbors of current running pair and member pair
       for current_pair_neighbor in current_direct_neighbors:
          # getting current_pair_neighbor's color
          for color_shape_id in shapes_colors:

             if current_pair_neighbor == color_shape_id:
                current_direct_neighbors[current_pair_neighbor]['r'] = shapes_colors[color_shape_id]['r']
                current_direct_neighbors[current_pair_neighbor]['g'] = shapes_colors[color_shape_id]['g']
                current_direct_neighbors[current_pair_neighbor]['b'] = shapes_colors[color_shape_id]['b']

       for member_pair_neighbor in member_pair_neighbors:
          # getting member_pair_neighbor's color
          for color_shape_id in shapes_colors:

             if member_pair_neighbor == color_shape_id:
                member_pair_neighbors[member_pair_neighbor]['r'] = shapes_colors[color_shape_id]['r']
                member_pair_neighbors[member_pair_neighbor]['g'] = shapes_colors[color_shape_id]['g']
                member_pair_neighbors[member_pair_neighbor]['b'] = shapes_colors[color_shape_id]['b']


       # now we have colors of direct neighbors of current running pair and member pairs
       # looping through all direct neighbors of both shapes of the current_pair
       for current_pair_neighbor in current_direct_neighbors:
          
          r = current_direct_neighbors[current_pair_neighbor]['r']
          g = current_direct_neighbors[current_pair_neighbor]['g']
          b = current_direct_neighbors[current_pair_neighbor]['b']       
          current_pair_neighbor_rgb = r, g, b, 255

          # looping through all neighbors of both shapes of the current member_pair
          for member_pair_neighbor in member_pair_neighbors:

             r = member_pair_neighbors[member_pair_neighbor]['r']
             g = member_pair_neighbors[member_pair_neighbor]['g']
             b = member_pair_neighbors[member_pair_neighbor]['b']
             member_pair_neighbor_rgb = r,g,b, 255

             total_difference = pixel_functions.compute_appearance_difference( current_pair_neighbor_rgb, member_pair_neighbor_rgb)

             if total_difference <= appearance_difference_threshold:

                repeating_shapes_pattern[repeating_shapes_pattern_counter].append(current_pair_neighbor)
                repeating_shapes_pattern[repeating_shapes_pattern_counter].append(member_pair_neighbor)

                process_neighbor(current_pair_neighbor, member_pair_neighbor)
                already_processed_shapes.append(current_pair_neighbor)
                already_processed_shapes.append(member_pair_neighbor)           


       repeating_shapes_pattern_counter += 1

   current_pair_counter += 1


# deleting all values of list that are all included in another bigger list
shapes_copy = copy.deepcopy(repeating_shapes_pattern)   

for key1 in shapes_copy:

      for key2 in shapes_copy:
         if not key1 == key2 and len(shapes_copy[key2]) >= len(shapes_copy[key1]):
            # check if shapes_copy[key2] contains all elements of shapes_copy[key1]
            result =  all(elem in shapes_copy[key2]  for elem in shapes_copy[key1])

            if result:
               # yes it contains all elements
               if key1 in repeating_shapes_pattern:
                  repeating_shapes_pattern.pop(key1)
                  continue


f = open(repeating_shapes_pattern_filename, "w")
f.write(str(repeating_shapes_pattern))
f.close()













