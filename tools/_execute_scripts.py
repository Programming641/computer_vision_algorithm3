'''
   ****    supported scripts in tools/execute_scripts.py.    ****
   
   algorithms/fundamental/putpix_into_clrgrp.py
   find_edges.py    not supported.
   algorithms/fundamental/find_shapes.py
   help_lib/crud_shape_locations.py
   help_lib/crud_shape_neighbors.py
   find_rpt_ptn_shapes.py   not supported.
   combine_rpt_ptn_shapes_wk.py   not supoorted.

   
   *****   supported scripts in tools/execute_scripts2.py    ****
   
   algorithms/spixc/find_internal_spixc_shapes.py
   
   algorithms/pixch/findim_pixch.py
   algorithms/pixch/find_staying_shapes.py
   algorithms/pixch/find_mid_changed_shapes.py
   
   algorithms/pixch/find_mid_changed_shapes_matches.py
   algorithms/pixch/find_pixch_shapes.py
   algorithms/pixch/most_ch_shapes_frm_whichShp_in_prev_frm.py
   algorithms/pixch/verify_mid_ch_shapes_matches.py
   algorithms/pixch/verify_most_ch_shapes_matches.py
   algorithms/pixch/verify_staying_shapes.py
   algorithms/pixch/find_pixch_shapes_matches.py
   
   algorithms/styLshape/find_staying_Lshp_btwn_frames.py
   algorithms/styLshape/find_styLshp_wo_pixch_btwn_frames.py
   algorithms/styLshape/verify_styLshp_wo_pixch.py
   
   algorithms/template/match_by_whole_image_pixels_template.py
   
   algorithms/scnd_stage/shape_nbrs_matches_from_only_Nfnd_pixch_sty2.py
   algorithms/scnd_stage/verify_s_nbrs_m_frm_only_Nfnd_pixch_sty.py
   algorithms/scnd_stage/cross_check_all_LL_algo_acrs_cur_files.py





'''

import glob, os, sys
from libraries.cv_globals import proj_dir, top_images_dir, top_shapes_dir
import winsound
import traceback


# for user input when directly executing tools/execute_scripts.py
# tools_exec_scripts_filenum -> run execute_scripts or execute_scripts2
tools_exec_scripts_filenum = 1
directory = "videos/street3/resized"
exec_scriptname = "algorithms/fundamental/putpix_into_clrgrp.py"
# if execute_script is "putpix_into_clrgrp.py" then, please enter clrgrp_type. choices for clrgrp_type are choices for list of colors data 
# files. 
clrgrp_type = "min1"
# ---------------------------------------------

exec_scriptnames = []
if len( sys.argv ) > 1:
   # executed from outside
   directory = sys.argv[1]
   clrgrp_type = sys.argv[2]
   
   exec_scriptnames = [ "algorithms/fundamental/putpix_into_clrgrp.py", "algorithms/fundamental/find_shapes.py", "help_lib/crud_shape_boundaries.py", "help_lib/crud_shape_locations.py",
                        "help_lib/crud_shape_neighbors.py" ]

   cur_executing_script = ""
   
   try:
   
      # executing tools/execute_scripts.py
      for exec_scriptname in exec_scriptnames:
         cur_executing_script = exec_scriptname
         
         print("executing algorithm " + cur_executing_script )
      
         if "putpix_into_clrgrp.py" in exec_scriptname:
            sys.argv = [ exec_scriptname , directory, clrgrp_type ]
         else:

            if directory != "" and directory[-1] != '/':
               directory +='/'
            
            if clrgrp_type not in directory:
               directory = directory + clrgrp_type
            
            sys.argv = [ exec_scriptname , directory ]

         with open("tools/execute_scripts.py") as exec_scripts:
            exec(exec_scripts.read())

   
      # executing tools/execute_scripts2.py
      exec_scriptnames = [ "algorithms/spixc/find_internal_spixc_shapes.py", "algorithms/pixch/findim_pixch.py", "algorithms/pixch/find_staying_shapes.py",
                           "algorithms/pixch/find_pixch_shapes.py",
                           "algorithms/pixch/verify_staying_shapes.py", "algorithms/pixch/find_pixch_shapes_matches.py", 
                           "algorithms/styLshape/find_staying_Lshp_btwn_frames.py",
                           "algorithms/styLshape/find_styLshp_wo_pixch_btwn_frames.py", "algorithms/styLshape/verify_styLshp_wo_pixch.py", 
                           "algorithms/template/match_by_whole_image_pixels_template.py",
                           "algorithms/scnd_stage/cross_check_all_LL_algo_acrs_cur_files.py" ]

      for exec_scriptname in exec_scriptnames:
         cur_executing_script = exec_scriptname
         
         print("executing algorithm " + cur_executing_script )
         
         sys.argv = [ exec_scriptname , directory ]

         with open("tools/execute_scripts2.py") as exec_scripts:
            exec(exec_scripts.read())

   except Exception as e:
      tb = sys.exc_info()[2]
      print("error occurred in " + cur_executing_script )
      print( traceback.format_exc() )
         
      sys.exit(1)
      


if len( exec_scriptnames ) == 0 and tools_exec_scripts_filenum == 1:
   # directly executing script
   if "putpix_into_clrgrp.py" in exec_scriptname:
      sys.argv = [ exec_scriptname , directory, clrgrp_type ]
   else:
      sys.argv = [ exec_scriptname , directory ]

   with open("tools/execute_scripts.py") as exec_scripts:
      exec(exec_scripts.read())   


elif len( exec_scriptnames ) == 0 and tools_exec_scripts_filenum == 2:
   # directly executing script
   sys.argv = [ exec_scriptname , directory ]

   with open("tools/execute_scripts2.py") as exec_scripts:
      exec(exec_scripts.read())   




   
   
frequency = 2000  # Set Frequency To 2500 Hertz
duration = 5000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)


 

































