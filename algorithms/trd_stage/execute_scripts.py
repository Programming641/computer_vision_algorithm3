import sys, traceback

print("entered directory. algorithms/trd_stage")

cur_dirname = "algorithms/trd_stage/"

exec_scriptnames = [ "find_staying_conn_notfnd_shapes.py", "find_shapes_movement2.2.py", "find_consecutives.py", "find_all_consecutives.py",
                     "fix_consecutives.py", "find_wrong_matches_from_consecutives.py", "attach_with_direct_neighbors.py" ]



for exec_scriptname in exec_scriptnames:
   print("executing " + cur_dirname + exec_scriptname )
   try:
      cur_execute_script = cur_dirname + exec_scriptname

      with open(cur_execute_script) as exec_script:
         exec(exec_script.read())   

   except Exception as e:
      print("error occurred in " + cur_execute_script )
      print( traceback.format_exc() )
         
      sys.exit(1)
         

































