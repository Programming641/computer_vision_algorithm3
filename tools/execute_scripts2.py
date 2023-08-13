'''
   supported scripts.
   
   algorithms/spixc/find_internal_spixc_shapes.py
   
   algorithms/pixch/findim_pixch.py
   algorithms/pixch/find_mid_changed_shapes.py
   algorithms/pixch/find_staying_shapes.py
   algorithms/pixch/find_mid_changed_shapes_matches.py
   algorithms/pixch/find_most_changed_shapes.py
   algorithms/pixch/most_ch_shapes_frm_whichShp_in_prev_frm.py
   algorithms/pixch/verify_mid_ch_shapes_matches.py
   algorithms/pixch/verify_most_ch_shapes_matches.py
   algorithms/pixch/verify_staying_shapes.py
   
   algorithms/styLshape/find_staying_Lshp_btwn_frames.py
   algorithms/styLshape/find_styLshp_wo_pixch_btwn_frames.py
   algorithms/styLshape/verify_styLshp_wo_pixch.py
   
   algorithms/scnd_stage/shape_nbrs_matches_from_only_Nfnd_pixch_sty2.py
   algorithms/scnd_stage/verify_s_nbrs_m_frm_only_Nfnd_pixch_sty.py
   algorithms/scnd_stage/cross_check_all_LL_algo_acrs_cur_files.py
   
   

   how to use   
   fill directory, execute_script

'''

import glob, os, sys
from libraries.cv_globals import proj_dir, top_images_dir, top_shapes_dir, top_pixch_dir, styLshapes, styLshapes_wo_pixch
from libraries.cv_globals import snd_stg_alg_shp_nbrs_dir, scnd_stg_all_files
import winsound



directory = "videos/street6/resized/min"
if directory != "" and directory[-1] != '/':
   directory +='/'

execute_script = "algorithms/scnd_stage/cross_check_all_LL_algo_acrs_cur_files.py"
execute_filepath = top_images_dir + directory


# does this script require 2 files as input files?
single_file_execution = None

skip_files_by_num = []
skip_files_by_names = []


def create_skip_files( filepath, skip_filenames=None ):
   global skip_files_by_num, skip_files_by_names
   
   
   
   if not os.path.exists(filepath ):
      return

   # getting already executed files
   for file in os.listdir(filepath):
      if skip_filenames is None:
         break
      # file is a filename in the directory. not the filepath.
      if os.path.isdir(file):
         continue
      
      
      
      file1num_end = file.find(".", 0)
      #first number starts at index 0 of the filename and ends just before the first period
      file1num = file[ 0: file1num_end ]
      
      if "result" in skip_filenames:
         file2num_end = file.find("result")
      elif "shapes" in skip_filenames:
         file1num_end = file.find("shapes")
         file1num = file[ 0: file1num_end ]
         
         #file2num is not used anyway. so just random number for it
         file2num_end = file1num_end
      
      elif "mid_ch" in skip_filenames or "most_ch" in skip_filenames or "pixch/sty_shapes" in filepath or \
           "pixch/ch_shapes/ch_from" in filepath or top_pixch_dir + "ch_shapes/mid_ch_sty" in filepath or \
           "styLshapes" in filepath or styLshapes_wo_pixch in filepath or "only_nfnd_pixch_sty2" in filepath or scnd_stg_all_files in filepath:
         # find_mid_changed_shapes file name is -> image_filename + "." + image_filename2 + "." + main_filename + "mid_ch.data"
         # find_most_changed_shapes file name is -> image_filename + "." + image_filename2 + "." + main_filename + "most_ch.data"
         # pixch/find_staying_shapes file name is -> image_filename2 + "." + image_filename + "." + image_filename + ".data"
         # pixch/most_ch_shapes_frm_whichShp_in_prev_frm file name -> im1file + "." + im2file + "." + im2file + ".data"

         if "mid_ch" in skip_filenames and "mid_ch" not in file:
            continue
         if "most_ch" in skip_filenames and "most_ch" not in file:
            continue
         
         if "pixch/ch_shapes/ch_from" in filepath and "verified" in skip_filenames and "verified" not in file:
            continue
         
         if "pixch/sty_shapes" in filepath and "verified" in skip_filenames and "verified" not in file:
            continue
         
         if top_pixch_dir + "ch_shapes/mid_ch_sty" in filepath and "verified" in skip_filenames and "verified" not in file:
            continue
         
         if styLshapes_wo_pixch in filepath and "verified" in skip_filenames and "verified" not in file:
            continue
         
         if "only_nfnd_pixch_sty2" in filepath or scnd_stg_all_files in filepath and "verify" in execute_script and file.count(".") != 2:
            continue
         
         # second filename starts right after first filename + period
         file2num_end = file.find(".", file1num_end + 1 )
      
      file2num = file[ file1num_end + 1: file2num_end ]
      skip_files_by_num.append( (file1num, file2num ) )



if "findim_pixch.py" in execute_script:
   create_skip_files( top_shapes_dir + directory + top_pixch_dir, "result" )
   single_file_execution = False
   
elif "find_internal_spixc_shapes" in execute_script:
   create_skip_files( top_shapes_dir + directory + "shapes/intnl_spixcShp/data/", "shapes.data" )
   single_file_execution = True
   
elif "find_mid_changed_shapes_matches" in execute_script:
   create_skip_files( top_shapes_dir + directory + top_pixch_dir + "ch_shapes/mid_ch_sty/data/", ".data" )
   single_file_execution = False
   
elif "find_mid_changed_shapes" in execute_script:
   create_skip_files( top_shapes_dir + directory + top_pixch_dir + "data/", "mid_ch" )
   single_file_execution = False
   
elif "pixch/find_staying_shapes" in execute_script:
   create_skip_files( top_shapes_dir + directory + top_pixch_dir + "sty_shapes/data/", ".data" )
   single_file_execution = False

elif "pixch/find_most_changed_shapes" in execute_script:
   create_skip_files( top_shapes_dir + directory + top_pixch_dir + "data/", "most_ch" )
   single_file_execution = False

elif "pixch/most_ch_shapes_frm_whichShp_in_prev_frm" in execute_script:
   create_skip_files( top_shapes_dir + directory + top_pixch_dir + "ch_shapes/ch_from/data/", ".data" )
   single_file_execution = False

elif "pixch/verify_mid_ch_shapes_matches" in execute_script:
   create_skip_files( top_shapes_dir + directory + top_pixch_dir + "ch_shapes/mid_ch_sty/data", "verified" )
   single_file_execution = False

elif "pixch/verify_most_ch_shapes_matches" in execute_script:
   create_skip_files( top_shapes_dir + directory + top_pixch_dir + "ch_shapes/ch_from/data/", "verified" )
   single_file_execution = False

elif "pixch/verify_staying_shapes" in execute_script:
   create_skip_files( top_shapes_dir + directory + top_pixch_dir + "sty_shapes/data/", "verified" )
   single_file_execution = False

elif "styLshape/find_staying_Lshp_btwn_frames" in execute_script:
   create_skip_files( top_shapes_dir + directory + styLshapes + "/intnl_spixcShp/data/", ".data" )
   single_file_execution = False

elif "styLshape/find_styLshp_wo_pixch_btwn_frames" in execute_script:
   create_skip_files( top_shapes_dir + directory + styLshapes_wo_pixch + "/intnl_spixcShp/data/", ".data" )
   single_file_execution = False

elif "styLshape/verify_styLshp_wo_pixch" in execute_script:
   create_skip_files( top_shapes_dir + directory + styLshapes_wo_pixch + "/intnl_spixcShp/data/", "verified" )
   single_file_execution = False

elif "scnd_stage/shape_nbrs_matches_from_only_Nfnd_pixch_sty2" in execute_script:
   create_skip_files( top_shapes_dir + directory + snd_stg_alg_shp_nbrs_dir + "/only_nfnd_pixch_sty2/", ".data" )
   single_file_execution = False

elif "scnd_stage/verify_s_nbrs_m_frm_only_Nfnd_pixch_sty" in execute_script:
   create_skip_files( top_shapes_dir + directory + snd_stg_alg_shp_nbrs_dir + "/only_nfnd_pixch_sty2/", ".data" )
   single_file_execution = False

elif "scnd_stage/cross_check_all_LL_algo_acrs_cur_files" in execute_script:
   create_skip_files( top_shapes_dir + directory + scnd_stg_all_files + "/data/", ".data" )
   single_file_execution = False





# find last file. last file will be the largest filenumber. largest filenumber won't have any more files to compare with.
largest_filenum = None
for file in os.listdir(execute_filepath):
   if ".png" not in file:
         continue
      
   temp_num = [x for x in list(file) if x.isdigit()] 

   filenum = ""
   for i in range( 0, len( temp_num ) ):
      filenum += temp_num[i]

   if largest_filenum == None:
      largest_filenum = int( filenum )

   if int( filenum ) > largest_filenum:
      largest_filenum = int( filenum )


for file in os.listdir(execute_filepath):
   if ".png" not in file:
         continue
      
   print("file " + file )
   
   temp_num = [x for x in list(file) if x.isdigit()] 

   filenum = ""
   for i in range( 0, len( temp_num ) ):
      filenum += temp_num[i]
   
   if filenum == str( largest_filenum ) and single_file_execution is False:
      print("skip current file")
      continue
   
   
   file1num = filenum
   file2num = str( int( file1num ) + 1 )
   
   skip = False
   for skip1n2files in skip_files_by_num:
      if single_file_execution is False and ( skip1n2files[0] == file1num and skip1n2files[1] == file2num ):
         skip = True
         break
      
      if single_file_execution is True and skip1n2files[0] == file1num:
         skip = True
         break
   
   if skip:
      print("skip current file")
      print()
      continue
   
   filename_after_num_start = file.find( file1num ) + len( file1num )
   filename_after_num_end = len( file )
   filename_after_num = file[ filename_after_num_start: filename_after_num_end ]
   
   filename_before_num_end = file.find( file1num )
   filename_before_num = file[0: filename_before_num_end ]
   
   rest_of_filename = filename_before_num + filename_after_num
   
   file2name = filename_before_num + file2num + filename_after_num
   
   
   sys.argv = [ file, file2name, rest_of_filename, directory ]
   
   if "find_mid_changed_shapes" in execute_script or "pixch/find_staying_shapes" in execute_script or "pixch/find_most_changed_shapes" in execute_script or \
      "scnd_stage/shape_nbrs_matches_from_only_Nfnd_pixch_sty2" in execute_script:
      for execute_count in range(2):
         if execute_count == 0:
            if "find_mid_changed_shapes" in execute_script or "pixch/find_most_changed_shapes" in execute_script:
               sys.argv = [ file, file2name, file, directory ]
            elif "pixch/find_staying_shapes" in execute_script or "scnd_stage/shape_nbrs_matches_from_only_Nfnd_pixch_sty2" in execute_script:
               sys.argv = [ file, file2name, True, directory ]
            
         
         elif execute_count == 1:
            if "find_mid_changed_shapes" in execute_script or "pixch/find_most_changed_shapes" in execute_script:
               sys.argv = [ file, file2name, file2name, directory ]
            elif "pixch/find_staying_shapes" in execute_script or "scnd_stage/shape_nbrs_matches_from_only_Nfnd_pixch_sty2" in execute_script:
               sys.argv = [ file, file2name, False, directory ]
            
         
         exec(open(proj_dir + execute_script).read())
   
   else:
      # pixch/findim_pixch.py
      # pixch/most_ch_shapes_frm_whichShp_in_prev_frm
      # pixch/verify_most_ch_shapes_matches
      # pixch/verify_staying_shapes
      # styLshape/find_staying_Lshp_btwn_frames
      # styLshape/find_styLshp_wo_pixch_btwn_frames
      # styLshape/verify_styLshp_wo_pixch
      # scnd_stage/verify_s_nbrs_m_frm_only_Nfnd_pixch_sty
      # scnd_stage/cross_check_all_LL_algo_acrs_cur_files
      # pixch/verify_mid_ch_shapes_matches
      exec(open(proj_dir + execute_script).read())
   
   
   
frequency = 2000  # Set Frequency To 2500 Hertz
duration = 5000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)


 
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   