import sys

print("entered directory. algorithms/scnd_stage/changes_btwn_frames")

cur_dirname = "algorithms/scnd_stage/changes_btwn_frames/"

exec_scriptnames = [ "matches_for_shapes_that_separate.py", "find_fusing_shapes.py", "matches_for_pixch_on_notfnd_shapes.py" ]



for exec_scriptname in exec_scriptnames:
   print("executing " + cur_dirname + exec_scriptname )
   try:
      cur_execute_script = cur_dirname + exec_scriptname

      with open(cur_execute_script) as exec_script:
         exec(exec_script.read())   

   except Exception as e:
      tb = sys.exc_info()[2]
      print("error occurred in " + cur_execute_script )
      print("message:{0}".format(e.with_traceback(tb)))
         
      sys.exit(1)
         

































