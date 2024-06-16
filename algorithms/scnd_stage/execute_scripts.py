import sys, traceback, os
from libraries.cv_globals import top_shapes_dir, snd_stg_alg_shp_nbrs_dir, styLshapes, styLshapes_wo_pixch, internal, scnd_stg_all_files


print("entered directory. algorithms/scnd_stage")

directory = sys.argv[1]
if directory[-1] != "/":
   directory += "/"

exec_scriptnames = [  "cross_check_all_low_level_algo_acrs_all_files.py", "find_shapes_match_types.py", "match_neighbor_by_relpos_shp_nbr.py", 
                     "find_shapes_from_Nfnd_shapes_by_relpos.py", "find_consecutively_missing_shapes2.py", "find_consecutively_missing_shapes3.py",
                     "find_consecutively_missing_shapes4.py", "find_nbr_matches_from_Nfnd_shapes.py", "find_consecutively_missing_shapes5.py",
                     "find_shapes_from_Nfnd_shapes.py", "find_shapes_from_Nfnd_shapes_by_relpos2.py", "find_shapes_from_Nfnd_shapes_by_relpos3.py",
                     "verify_shapes_from_Nfnd_shapes_by_relpos3.py", "find_moving_together_shapes.py", "correct_wrong_matches.py", 
                     "find_multi_shapes_match_by_img_tmpl.py", "verify_multishapes_by_img_tmpl.py", "spixc/execute_scripts.py",
                     "changes_btwn_frames/execute_scripts.py", "finish_scnd_stage.py"
                      ]

across_all_files_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/data/"

shapes_m_types_dir = top_shapes_dir + directory + scnd_stg_all_files + "/shp_match_types/"
shapes_m_types_ddir = shapes_m_types_dir + "data/"

relpos_nbr_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/relpos_nbr/data/"
relpos_nbr_dfile = relpos_nbr_ddir + "1.data"

missed_shapes_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/consecutive_missed/data/"
missed_shapes2_dfile = missed_shapes_ddir + "2.data"

missed_shapes3_dfile = missed_shapes_ddir + "3.data"

possible_matches_dfile = missed_shapes_ddir + "possible_matches.data"

nbr_match_dfile = across_all_files_ddir + "nbr_matches.data"

possible_matches5_dfile = missed_shapes_ddir + "5.data"

possibe_matches_dir = top_shapes_dir + directory + scnd_stg_all_files + "/possible_matches/data/"
possible_matches1_dfile = possibe_matches_dir + "1.data"

relpos_nbr2_dfile = relpos_nbr_ddir + "2.data"

relpos_nbr3_dfile = relpos_nbr_ddir + "3.data"

verified_relpos_nbr3_dfile = relpos_nbr_ddir + "verified3.data"

move_together_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/move_together/data/"
move_together_dfile = move_together_ddir + "move_together.data"

correct_matches_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/correct_matches/data/"
correct_matches_dfile = correct_matches_ddir + "1.data"

image_template_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/image_template/data/"
image_template_shapes_dfile = image_template_ddir + "multi1.data"  

verified_img_tmpl_shapes_dfile = image_template_ddir + "verified_multi1.data"  

script_result_associate = { "cross_check_all_low_level_algo_acrs_all_files.py": across_all_files_ddir + "all_files.data", 
                            "find_shapes_match_types.py": shapes_m_types_ddir + "matched_pixels.data", 
                            "match_neighbor_by_relpos_shp_nbr.py": across_all_files_ddir + "verified2.data", 
                            "find_shapes_from_Nfnd_shapes_by_relpos.py": relpos_nbr_dfile, 
                            "find_consecutively_missing_shapes2.py": missed_shapes2_dfile, "find_consecutively_missing_shapes3.py": missed_shapes3_dfile,
                            "find_consecutively_missing_shapes4.py": possible_matches_dfile, "find_nbr_matches_from_Nfnd_shapes.py": nbr_match_dfile, 
                            "find_consecutively_missing_shapes5.py": possible_matches5_dfile, "find_shapes_from_Nfnd_shapes.py": possible_matches1_dfile,
                            "find_shapes_from_Nfnd_shapes_by_relpos2.py": relpos_nbr2_dfile, "find_shapes_from_Nfnd_shapes_by_relpos3.py": relpos_nbr3_dfile,
                            "verify_shapes_from_Nfnd_shapes_by_relpos3.py": verified_relpos_nbr3_dfile, "find_moving_together_shapes.py": move_together_dfile,
                            "correct_wrong_matches.py": correct_matches_dfile, "find_multi_shapes_match_by_img_tmpl.py": image_template_shapes_dfile, 
                            "verify_multishapes_by_img_tmpl.py": verified_img_tmpl_shapes_dfile, "spixc/execute_scripts.py": "", 
                            "changes_btwn_frames/execute_scripts.py": "", "finish_scnd_stage.py": "" }
                            
                            
                            
                            


for exec_scriptname in exec_scriptnames:
   
   try:
      cur_dirname = "algorithms/scnd_stage/"
      
      # check if this script is already executed
      if os.path.exists( script_result_associate[ exec_scriptname ] ) and "execute_script" not in exec_scriptname:
         # this script is already executed
         print("skip " + exec_scriptname )
         continue   
   
   
      print("executing " + cur_dirname + exec_scriptname )
      cur_execute_script = cur_dirname + exec_scriptname

      with open(cur_execute_script) as exec_script:
         exec(exec_script.read())   

   except Exception as e:
      print("error occurred in " + cur_execute_script )
      print( traceback.format_exc() )
         
      sys.exit(1)
         

































