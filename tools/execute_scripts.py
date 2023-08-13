'''
   supported scripts.
   algorithms/fundamental/putpix_into_clrgrp.py
   find_edges.py
   algorithms/fundamental/find_shapes.py
   help_lib/create_shape_locations.py
   help_lib/create_shape_neighbors.py
   find_rpt_ptn_shapes.py
   combine_rpt_ptn_shapes_wk.py

   how to use
   fill directory, execute_script

'''

import glob, os, sys
from libraries.cv_globals import proj_dir, top_images_dir, top_shapes_dir
import winsound

#   ---------------       user input begin      -------------------
directory = "videos/penguin2/resized/min"
execute_script = "algorithms/fundamental/find_shapes.py"
# if execute_script is "putpix_into_clrgrp.py" then, please enter clrgrp_type. choices for clrgrp_type -> min or clrgrp
clrgrp_type = "min"
#   ---------------       user input end        -------------------


if directory != "" and directory[-1] != '/':
   directory +='/'



execute_filepath = None

skip_files_by_num = []

def create_skip_files( filepath, skip_filename=None ):
   global skip_files_by_num
   
   
   if not os.path.exists(filepath ):
      return

   # getting already executed files
   for file in os.listdir(filepath):
      if skip_filename is None:
         break
      # file is a filename in the directory. not the filepath.
      if os.path.isdir(file) or skip_filename not in file:
         continue
   
      temp_num = [x for x in list(file) if x.isdigit()] 

      num = ""
      for i in range( 0, len( temp_num ) ):
         num += temp_num[i]
      
      skip_files_by_num.append( num )




if  "putpix_into_clrgrp.py" in execute_script:

   execute_filenames = "png"
   
   create_skip_files( top_images_dir + directory + clrgrp_type , ".png" )
   
   execute_filepath = top_images_dir + directory

      

if  "find_edges.py" in execute_script or "find_shapes.py" in execute_script or "create_shape_locations.py" in execute_script or \
    "create_shape_neighbors.py" in execute_script or "find_rpt_ptn_shapes.py" in execute_script or "combine_rpt_ptn_shapes_wk.py" in execute_script:

   execute_filenames = "png"
   
   if "find_edges.py" in execute_script:
      create_skip_files( top_shapes_dir + directory + "edges", "clrgrp.png" )
   elif "find_shapes.py" in execute_script:
      create_skip_files( top_shapes_dir + directory + "shapes", "shapes.txt" )
   elif "create_shape_locations.py" in execute_script:
      create_skip_files( top_shapes_dir + directory + "locations/", "_loc.data" )
   elif "create_shape_neighbors.py" in execute_script:
      create_skip_files( top_shapes_dir + directory + "shape_nbrs/", "_shape_nbrs.txt" )
   elif "find_rpt_ptn_shapes.py" in execute_script:
      create_skip_files( top_shapes_dir + directory + "rpt_ptn/", "_rpt_ptn_shapes.txt" )
   elif "combine_rpt_ptn_shapes_wk.py" in execute_script:
      create_skip_files( top_shapes_dir + directory + "rpt_ptn/", "_combi_rpt_ptn_shapes.txt" )
   
   execute_filepath = top_images_dir + directory



for file in os.listdir(execute_filepath):
   
   if execute_filenames not in file:
      continue   

   if "putpix_into_clrgrp.py" not in execute_script:
      sys.argv = [ file , directory ]
   else:
      sys.argv = [ file , directory, clrgrp_type ]
   
   print("file " + file )
   
   temp_num = [x for x in list(file) if x.isdigit()] 

   num = ""
   for i in range( 0, len( temp_num ) ):
      num += temp_num[i]
   
   if num in skip_files_by_num:
      print(directory + " skipping current file " + file )
      continue
   
   
   exec(open(proj_dir + execute_script).read())
   print()
   

frequency = 2000  # Set Frequency To 2500 Hertz
duration = 5000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)




















