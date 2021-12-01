
import tkinter
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions
from libraries import video_algorithms
from libraries import read_files_functions
import math

filename = "hanger003_color_group"

directory = ""

filename2 = "hanger004_color_group"

# directory is specified but does not contain /
if directory != "" and directory.find('/') == -1:
   directory +='/'


original_image = Image.open("images/" + directory + filename + ".png")

image_width, image_height = original_image.size


compare_image = Image.open("images/" + directory + filename2 + ".png")

compare_image_width, compare_image_height = compare_image.size


# returned value has below form
# shapes[shapes_id][pixel_index] = {}
# shapes[shapes_id][pixel_index]['x'] = x
# shapes[shapes_id][pixel_index]['y'] = y
original_shapeIDs_with_all_indexes = read_files_functions.read_shapes_file(filename, directory)


compare_shapeIDs_with_all_indexes = read_files_functions.read_shapes_file(filename2, directory)

all_shape_match_results = []

# this is used for displaying closest matched images
root = tkinter.Tk()


for original_shape_id in original_shapeIDs_with_all_indexes:

   match_results = {}
   match_results[ int( original_shape_id ) ] = []
   
   cur_orig_shape_id = False

   print(" original_shape_id " + str(original_shape_id ) )
   
   if len(original_shapeIDs_with_all_indexes[original_shape_id]) < 12:
      continue

   # boundary_pixels has the following form
   # {1: {'x': 0, 'y': 234}, 2: {'x': 61, 'y': 221}, {'x': 177, 'y': 319}, 16679: {'x': 178, 'y': 229}}
   # containing coordinates of boundary pixels
   original_boundary_pixels = pixel_shapes_functions.get_boundary_pixels(original_shapeIDs_with_all_indexes[original_shape_id], int(original_shape_id) )

   for compare_shape_id in compare_shapeIDs_with_all_indexes:
   
      if len(compare_shapeIDs_with_all_indexes[compare_shape_id]) < 12:
         continue

      
      shape_ids = [ int(original_shape_id ), int (compare_shape_id ) ]

      if shape_ids[0] == 32836 :

         #print("compare_shape_id is " + str(compare_shape_id) )
      
         compare_boundary_pixels = pixel_shapes_functions.get_boundary_pixels(compare_shapeIDs_with_all_indexes[compare_shape_id], int(compare_shape_id) )
    
         # match shapes based on relative positions of boundary pixels
         boundary_rel_result = video_algorithms.boundary_rel_pos(original_boundary_pixels, compare_boundary_pixels, shape_ids)
      
         boundary_result = 0
         boundary_result = video_algorithms.process_boundaries(original_boundary_pixels, compare_boundary_pixels, shape_ids)
         result = 0
         result = video_algorithms.find_shapes_in_diff_frames(original_shapeIDs_with_all_indexes[original_shape_id], compare_shapeIDs_with_all_indexes[compare_shape_id],  "consecutive_count", shape_ids)
         print("real pixels result " + str(result) )
         print("boundary_result " + str(boundary_result) )
         if result or boundary_result:
               
            temp = {}
            match_result = 0
            if boundary_result:
               match_result += round( boundary_result )
            if result:
               match_result += round( result )
            if boundary_rel_result:
               match_result += round( boundary_rel_result * 1.6 )
            
            temp['compare_shape_id'] = compare_shape_id
            temp['value'] = match_result
            match_results[int (original_shape_id) ].append(temp)
          
            if not cur_orig_shape_id:
               # match_results will be added to the all_shape_match_results. match_results added here is a reference and not a value. so if you update match_results, the changes will be 
               # reflected in match_results inside all_shape_match_results as well. What this means is that you only need to add match_results once. Not each time temp is added to the match_results
               all_shape_match_results.append(match_results)
               cur_orig_shape_id = True
    

   if shape_ids[0] == 32836 :
      match_results[int (original_shape_id) ] = sorted(match_results[int (original_shape_id) ], key=lambda k: k['value'])
  
      closest_match = {}
      prev_compare_shapeid = None
      for matches in match_results[shape_ids[0]]:
         
         # closest_match initialization
         if not closest_match:
            closest_match[matches['compare_shape_id']] = matches['value']
            prev_compare_shapeid = matches['compare_shape_id']

         elif closest_match[prev_compare_shapeid] < matches['value']:
            closest_match.pop(prev_compare_shapeid)
            prev_compare_shapeid = matches['compare_shape_id']
            closest_match[prev_compare_shapeid] = matches['value']
               
      print(" original shape " + str(shape_ids[0]) + " closest match shape is " + str( prev_compare_shapeid ) )

      # displaying closest match images/

      window = tkinter.Toplevel(root)
      window.title( str(shape_ids[0]) + " " + str( prev_compare_shapeid ) )
    
      if prev_compare_shapeid:
         original_shape_file = "shapes/" + str(filename) + "_shapes/" + str(original_shape_id) + ".png"
         compare_shape_file = "shapes/" + str(filename2) + "_shapes/" + str(prev_compare_shapeid) + ".png"
   
         img = ImageTk.PhotoImage(Image.open(original_shape_file))
         img2 = ImageTk.PhotoImage(Image.open(compare_shape_file))
  
         label1 = tkinter.Label(window, image = img)
         label1.image = img
         label1.pack()
   
         label2 = tkinter.Label(window, image = img2 )
         label2.image = img2
         label2.pack()  
   
   
root.mainloop()



print("all_shape_match_results")
print(all_shape_match_results)












