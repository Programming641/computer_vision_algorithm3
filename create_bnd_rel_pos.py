
import tkinter
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions
from libraries import same_shapes_btwn_frames
from libraries import read_files_functions


im1file = "2clrgrp"

directory = "videos/hanger"

im2file = "3clrgrp"

filenames = [ im1file, im2file ]



# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

rel_pos_filepath = "shapes/" + directory + im1file[0:1] + "." + im2file[0:1] + im1file[1: len(im1file) ] + "_rel_pos.txt"

# returned value has below form
# shapes[shapes_id][pixel_index] = {}
# shapes[shapes_id][pixel_index]['x'] = x
# shapes[shapes_id][pixel_index]['y'] = y
im1s_pindexes = read_files_functions.rd_shapes_file(im1file, directory)


im2s_pindexes = read_files_functions.rd_shapes_file(im2file, directory)

match_results = []
for im1_shapeid in im1s_pindexes:

   print("im1_shapeid " + im1_shapeid + " pixel count " + str( len(im1s_pindexes[im1_shapeid]) ) )
   
   if len(im1s_pindexes[im1_shapeid]) < 12:
      continue
   
   # boundary_pixels has the following form
   # {1: {'x': 0, 'y': 234}, 2: {'x': 61, 'y': 221}, {'x': 177, 'y': 319}, 16679: {'x': 178, 'y': 229}}
   # containing coordinates of boundary pixels
   im1bnd_pixels = pixel_shapes_functions.get_boundary_pixels(im1s_pindexes[im1_shapeid] )
   
   print("im1_boundary_pixels count " + str( len( im1bnd_pixels ) ) )

   for im2_shapeid in im2s_pindexes:
   
      print("im2_shapeid " + im2_shapeid + " pixel count " + str( len(im2s_pindexes[im2_shapeid]) ) )
      
      if len(im2s_pindexes[im2_shapeid]) < 12:
         continue

      #if im1_shapeid != "1440" or im2_shapeid != "26028":
      #   continue
      
      im2bnd_pixels = pixel_shapes_functions.get_boundary_pixels(im2s_pindexes[im2_shapeid] )
      
      print("im2_boundary_pixels count " + str( len( im2bnd_pixels ) ) )
   
      # match shapes based on relative positions of boundary pixels
      bnd_rel_result = same_shapes_btwn_frames.boundary_rel_pos(im1bnd_pixels, im2bnd_pixels, filenames, directory)
      
      print("boundary_rel_result")
      print(bnd_rel_result)
      print()
      
      match_results.append( [ im1_shapeid, im2_shapeid, bnd_rel_result ] )

rel_pos_file = open( rel_pos_filepath, "w")
rel_pos_file.write( str( match_results ) )

rel_pos_file.close()









