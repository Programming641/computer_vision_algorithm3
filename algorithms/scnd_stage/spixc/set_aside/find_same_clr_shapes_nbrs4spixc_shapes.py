from libraries import read_files_functions
from libraries import pixel_shapes_functions
from libraries import pixel_functions

import os, sys
from libraries.cv_globals import proj_dir
import winsound
import pickle

top_shapes_dir = proj_dir + "/shapes/"

im_file = "25"

directory = "videos/giraffe/min"
shapes_dir = "videos/giraffe/min/s_pixc_shapes"


if len(sys.argv) > 1:
   im_file = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   
   location_fname = im_file + "_loc.txt"

   directory = sys.argv[1]

   print("execute script create_shape_neighbors.py. filename " + im_file + " directory " + directory )



# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'
if shapes_dir != "" and shapes_dir[-1] != ('/'):
   shapes_dir +='/'



nbr_directory = top_shapes_dir + shapes_dir + "same_clr_shapes/shape_nbrs/"

if not os.path.isdir(nbr_directory):
   os.makedirs(nbr_directory)


shape_neighbor_file = nbr_directory + im_file + "_shape_nbrs.data"

s_clr_shapes_folder = top_shapes_dir + shapes_dir + "same_clr_shapes/"
s_clr_shapes_file = s_clr_shapes_folder + im_file + ".data"

with open (s_clr_shapes_file, 'rb') as fp:
   # s_clr_shapes = {}
   # s_clr_shapes[shapeid] = { "shapeids": [ shapeid1, shapeid2,... ], "rgb": ( r, g, b ) }
   s_clr_shapes = pickle.load(fp)
fp.close()


nbr_filepath = top_shapes_dir + directory + "shape_nbrs/" + im_file + "_shape_nbrs.txt"
# [ {"shapeid": ["nbr_shapeid", "nbr_shapeid", ...] }, ...  ]
shape_nbrs = read_files_functions.rd_ldict_k_v_l(im_file, directory, nbr_filepath)

# shapes_colors = {}
# shapes_colors[shape_id] = { 'r': r, 'g': g, 'b': b }
shapes_colors = pixel_shapes_functions.get_all_shapes_colors( im_file, directory )

all_shape_nbrs = {}

debug = False
all_same_clr_shapes_len = len(s_clr_shapes) 
for s_clr_shapeid in s_clr_shapes:
   all_shape_nbrs[ s_clr_shapeid ] = []
   # cur_s_clr_shapes will get all current same color shapes including shapeid of s_clr_shapeid
   cur_s_clr_shapes = s_clr_shapes[s_clr_shapeid]["shapeids"]

   print("s_clr_shapeid " + s_clr_shapeid + " " +  str(all_same_clr_shapes_len) + " remaining" )

   s_clr_shape_counter = 0
   for cur_s_clr_shape in cur_s_clr_shapes:
      if s_clr_shape_counter == 0:
         all_shape_nbrs[ s_clr_shapeid ].append( [ cur_s_clr_shape ] )
      
      # getting neighbor shapes of cur_s_clr_shape
      cur_shape_nbrs = [ s_nbrs for s_nbrs in shape_nbrs if list(s_nbrs.keys())[0] == cur_s_clr_shape ][0]
      cur_neighbors = cur_shape_nbrs[ cur_s_clr_shape ]
      
      
      for cur_shape_nbr in cur_neighbors:
      
         if s_clr_shape_counter == 0:
            all_shape_nbrs[ s_clr_shapeid ][0].append( cur_shape_nbr )
            all_shape_nbrs[ s_clr_shapeid ][0].append( shapes_colors[ cur_shape_nbr ] )

            s_clr_shape_counter += 1
         else:
            # check if current shape neighbor has same color as any of its previous shape neighbors
            cur_shape_nbr_color = shapes_colors[ cur_shape_nbr ]
            
            nbr_clr_matched = False
            # loop all colors
            for nbr_clr_counter in range( 0, s_clr_shape_counter ):
               existing_nbr_color = [ nbr_color for nbr_color in all_shape_nbrs[ s_clr_shapeid ][ nbr_clr_counter ] if type( nbr_color ) is dict ]
               
               existing_nbr_color = existing_nbr_color[0]

               # make sure existing_nbr_color is a dictionary that only contains current running existing neighbor color 
               if len(existing_nbr_color) != 3 or not (type( existing_nbr_color ) is dict) and "r" in list( existing_nbr_color.keys() ) and "g" in list( existing_nbr_color.keys() ) \
                  and "b" in list( existing_nbr_color.keys() ):
                  print("ERROR. each same color shapes list should contain only one color that all neighbors in this list have")
                  sys.exit()
               
               clrch, brit_thres, brit_ch_v = pixel_functions.compute_appearance_difference(existing_nbr_color,
                                              cur_shape_nbr_color, 30 )
                  
               # color did not change and brightness is within threshold
               if not clrch and brit_thres:
                  # cur_shape_nbr_color is the same as existing_nbr_color
                  # so put cur_shape_nbr in the same list as nbr_clr_counter
                  all_shape_nbrs[ s_clr_shapeid ][ nbr_clr_counter ].append( cur_shape_nbr )
                  
                  if cur_s_clr_shape not in all_shape_nbrs[ s_clr_shapeid ][ nbr_clr_counter ]:
                     all_shape_nbrs[ s_clr_shapeid ][ nbr_clr_counter ].append( cur_s_clr_shape )
                  
                  nbr_clr_matched = True
                  break
            
            if not nbr_clr_matched:   
               # if processing reached this point, cur_shape_nbr has different color from any of the existing neighbor colors.
               # create new list for the new neighbor color
               all_shape_nbrs[ s_clr_shapeid ].append( [ cur_s_clr_shape ] )
               all_shape_nbrs[ s_clr_shapeid ][ s_clr_shape_counter ].append( cur_shape_nbr_color )
               all_shape_nbrs[ s_clr_shapeid ][ s_clr_shape_counter ].append( cur_shape_nbr )
            
               s_clr_shape_counter += 1
      
            
   all_same_clr_shapes_len -= 1   
            
with open(shape_neighbor_file, 'wb') as fp:
   pickle.dump(all_shape_nbrs, fp)
fp.close()


frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)













