import sys

print("entered directory. algorithms/scnd_stage/spixc")

cur_dirname = "algorithms/scnd_stage/spixc/"

exec_scriptnames = [ "find_shapes_from_Nfnd_shapes.py" ]



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
         

































