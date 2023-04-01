# find stayed large shapes neighbors matches between frames
# After finding stayed large shapes, find their large shape neighbors and see if they have matches in the next frame.
import tkinter
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions, same_shapes_btwn_frames, read_files_functions, image_functions, pixel_functions
from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir
import pickle
import math
import winsound
import sys, os
import copy

filename1 = "11"
directory = "videos/street3/resized/min"
filename2 = "12"
filenames = [ filename1, filename2 ]
shapes_type = "intnl_spixcShp"

# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

original_image = Image.open(top_images_dir + directory + filename1 + ".png")
im_width, im_height = original_image.size


print("preparing data. please wait...")

styLshapes_Ddir = top_shapes_dir + directory + styLshapes + "/" + shapes_type + "/data/"
styLshapes_wo_pixch_Ddir = top_shapes_dir + directory + styLshapes_wo_pixch + "/" + shapes_type + "/data/"



im1shapes_boundaries = {}
im2shapes_boundaries = {}
if shapes_type == "normal":
   # returned value has below form
   # shapes[shapes_id][pixel_index] = {}
   # shapes[shapes_id][pixel_index]['x'] = x
   # shapes[shapes_id][pixel_index]['y'] = y
   im1shapes = read_files_functions.rd_shapes_file(filename1, directory)
   im2shapes = read_files_functions.rd_shapes_file(filename2, directory)  
   
   im1shapes_neighbors_path = top_shapes_dir + directory + "shape_nbrs/" + filename1 + "_shape_nbrs.txt"
   im2shapes_neighbors_path = top_shapes_dir + directory + "shape_nbrs/" + filename2 + "_shape_nbrs.txt"

   # get boundary pixels of all shapes
   for shapeid in im1shapes:
      im1shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels(im1shapes[shapeid] )
   
   # get boundary pixels of all shapes
   for shapeid in im2shapes:
      im2shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels(im2shapes[shapeid] )


elif shapes_type == "intnl_spixcShp":

   s_pixcShp_intnl_dir = top_shapes_dir + directory + spixc_shapes + "/" +  internal + "/"
   
   shapes_dir = s_pixcShp_intnl_dir + "shapes/"
   shapes_dfile = shapes_dir + filename1 + "shapes.data"
   im2shapes_dfile = shapes_dir + filename2 + "shapes.data"

   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()
   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()      

   im1shapes_neighbors_path = s_pixcShp_intnl_dir + "shape_nbrs/" + filename1 + "_shape_nbrs.txt"
   im2shapes_neighbors_path = s_pixcShp_intnl_dir + "shape_nbrs/" + filename2 + "_shape_nbrs.txt"

   # get boundary pixels of all shapes
   for shapeid in im1shapes:
      cur_shape_pixels = { }
      for pindex in im1shapes[shapeid]:
         cur_shape_pixels[pindex] = {}
            
         y = math.floor( int(pindex) / im_width)
         x  = int(pindex) % im_width 
      
         cur_shape_pixels[pindex]['x'] = x
         cur_shape_pixels[pindex]['y'] = y
      
      im1shapes[shapeid] = cur_shape_pixels

      # {1: {'x': 190, 'y': 30}, 2: {'x': 190, 'y': 31},.... }
      im1shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels(cur_shape_pixels )

      

   # get boundary pixels of all shapes
   for shapeid in im2shapes:
      cur_shape_pixels = { }
      for pindex in im2shapes[shapeid]:
         cur_shape_pixels[pindex] = {}
            
         y = math.floor( int(pindex) / im_width)
         x  = int(pindex) % im_width 
      
         cur_shape_pixels[pindex]['x'] = x
         cur_shape_pixels[pindex]['y'] = y
      
      im2shapes[shapeid] = cur_shape_pixels

      # {1: {'x': 190, 'y': 30}, 2: {'x': 190, 'y': 31},.... }
      im2shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels(cur_shape_pixels )


else:
   print("ERROR at " + str( os.path.basename(__file__) ) + " shapes_type " + shapes_type + " is not supported")
   sys.exit()


styLshapes1to2_dfile = styLshapes_Ddir + filename1 + "." + filename2 + ".data"
styLshapes_wo_pixch_dfile = styLshapes_wo_pixch_Ddir + filename1 + "." + filename2 + ".data"


with open (styLshapes1to2_dfile, 'rb') as fp:
   # [ ['21455', '22257'], ... ]
   # [ [ image1 shapeid, image2 shapeid ], ... ]
   styLshapes1to2 = pickle.load(fp)
fp.close()

with open (styLshapes_wo_pixch_dfile, 'rb') as fp:
   #  [ ['79999', '79936', ['78799', '78399', ... ] ], ... ]
   #  [ [ im1shapeid, im2shapeid, matched_pixels ], ... ]
   styLshapes_wo_pixch = pickle.load(fp)
fp.close()


# [ {"shapeid": ["nbr_shapeid", "nbr_shapeid", ...] }, ...  ]
im1shape_nbrs = read_files_functions.rd_dict_k_v_l(filename1, directory, im1shapes_neighbors_path)
im2shape_nbrs = read_files_functions.rd_dict_k_v_l(filename2, directory, im2shapes_neighbors_path)



all_styLshapes = []
for shapes  in styLshapes_wo_pixch:
   temp = [ shapes[0], shapes[1] ]
   
   if temp not in styLshapes1to2:
      all_styLshapes.append( temp )

all_styLshapes.extend( styLshapes1to2 )


print("data preparation complete. now main process begins")

all_shape_match_results = []

# this is used for displaying closest matched images
root = tkinter.Tk()

Lshape_size = 50
for styLshape in all_styLshapes:

   
   cur_im1shape_neighbors = []
   for cur_im1s_nbr in im1shape_nbrs[ styLshape[0] ]:
      if len( im1shapes[cur_im1s_nbr] ) >= Lshape_size:
         cur_im1shape_neighbors.append( cur_im1s_nbr )
      
   if len( cur_im1shape_neighbors ) == 0:
      continue

   match_results = {}
   match_results[ styLshape[0] ] = []
   
   cur_orig_shape_id = False 
   

   cur_im2shape_neighbors = []
   for cur_im2s_nbr in im2shape_nbrs[ styLshape[1] ]:
      if len( im2shapes[cur_im2s_nbr] ) >= Lshape_size:
         cur_im2shape_neighbors.append( cur_im2s_nbr )
      
   if len( cur_im2shape_neighbors ) == 0:
      continue   
   
   print("current image1 shapeid " + styLshape[0] + " current image2 shapeid " + styLshape[1] )

   for cur_im1shape_neighbor in cur_im1shape_neighbors:
      # combine image1 shape and its neighbors and see if they match the image2 shape and its neighbors
      # current image1 shape's boundaries may likly have same keys as its neighbor's keys. so create new keys here
      # keys in boundaries are just incremental numbers so it's ok to create them.      
      temp_xy_values = im1shapes_boundaries[ styLshape[0] ].values()
      
      
      cur_im1boundaries = {}
      temp_num = 1
      for temp_xy_value in temp_xy_values:
         cur_im1boundaries[temp_num] = temp_xy_value
         temp_num += 1
      
     
      temp_xy_values = im1shapes_boundaries[ cur_im1shape_neighbor ].values()
      for temp_xy_value in temp_xy_values:
         cur_im1boundaries[temp_num] = temp_xy_value     
     
         temp_num += 1   
      
      print("current image1 shape's neighbor " + cur_im1shape_neighbor )


      for cur_im2shape_neighbor in cur_im2shape_neighbors:
         temp_xy_values = im2shapes_boundaries[ styLshape[1] ].values()

      
         cur_im2boundaries = {}
         temp_num = 1
         for temp_xy_value in temp_xy_values:
            cur_im2boundaries[temp_num] = temp_xy_value
            temp_num += 1
      
     
         temp_xy_values = im2shapes_boundaries[ cur_im2shape_neighbor ].values()
         for temp_xy_value in temp_xy_values:
            cur_im2boundaries[temp_num] = temp_xy_value     
     
            temp_num += 1        
   

         print("current image2 shape's neighbor " + cur_im2shape_neighbor )


   
         shape_ids = [ int(styLshape[0] ), int (styLshape[1] ) ]

         boundary_result = same_shapes_btwn_frames.process_boundaries(cur_im1boundaries, cur_im2boundaries, shape_ids, filenames)

         result = same_shapes_btwn_frames.find_shapes_in_diff_frames(im1shapes[ styLshape[0] ], im2shapes[styLshape[1]],  "consecutive_count", shape_ids)         
         
         print("real pixels result " + str(result) )
         print("boundary_result " + str(boundary_result) )         
         
         if result or boundary_result:
               
            temp = {}
            match_result = 0
            if boundary_result:
               match_result += round( boundary_result )
            if result:
               match_result += round( result )      
         
         
            temp['compare_shape_id'] = styLshape[1]
            temp['value'] = match_result
            temp['im1s_nbr'] = cur_im1shape_neighbor
            temp['im2s_nbr'] = cur_im2shape_neighbor
            match_results[styLshape[0] ].append(temp)
            
            if not cur_orig_shape_id:
               # match_results will be added to the all_shape_match_results. match_results added here is a reference and not a value. so if you update match_results, the changes will be 
               # reflected in match_results inside all_shape_match_results as well. What this means is that you only need to add match_results once. Not each time temp is added to the match_results
               all_shape_match_results.append(match_results)
               cur_orig_shape_id = True         
         
         
         print()
         

   match_results[styLshape[0] ] = sorted(match_results[styLshape[0] ], key=lambda k: k['value'])
 
   closest_match = {}
   prev_compare_shapeid = None
   for matches in match_results[str(shape_ids[0])]:
         
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
    
   if prev_compare_shapeid != None:
      original_shape_file = top_shapes_dir + directory + "shapes/intnl_spixcShp/" + str(filename1) + "/" + str(shape_ids[0]) + ".png"
      compare_shape_file = top_shapes_dir + directory + "shapes/intnl_spixcShp/" + str(filename2) + "/" + str(prev_compare_shapeid) + ".png"
   
      img = ImageTk.PhotoImage(Image.open(original_shape_file))
      img2 = ImageTk.PhotoImage(Image.open(compare_shape_file))
  
      label1 = tkinter.Label(window, image = img, bg="white")
      label1.image = img
      label1.pack()
   
      label2 = tkinter.Label(window, image = img2, bg="white" )
      label2.image = img2
      label2.pack()
      
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)      

root.mainloop()



print("all_shape_match_results")
print(all_shape_match_results)        
         
         
         
         
         



























