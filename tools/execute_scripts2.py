

import glob, os, sys
from libraries.cv_globals import proj_dir, top_images_dir, top_shapes_dir, top_pixch_dir, styLshapes, styLshapes_wo_pixch
from libraries.cv_globals import snd_stg_alg_shp_nbrs_dir, scnd_stg_all_files



execute_script = sys.argv[0]

print("execute_script " +  execute_script )

directory = sys.argv[1]
if directory != "" and directory[-1] != '/':
   directory +='/'

execute_filepath = top_images_dir + directory


# does this script require 2 files as input files?
single_file_execution = False

skip_files_by_num = []
skip_files_by_names = []

def create_skip_files( filepath, skip_filenames=None ):
   
   if not os.path.exists(filepath ):
      return

   # getting already executed files
   for file in os.listdir(filepath):
      if skip_filenames is None:
         break
      # file is a filename in the directory
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
      
      elif "most_ch" in skip_filenames or "pixch/sty_shapes" in filepath or \
           "styLshapes" in filepath or styLshapes_wo_pixch in filepath or "only_nfnd_pixch_sty2" in filepath or scnd_stg_all_files in filepath:
         # pixch/find_staying_shapes file name is -> image_filename2 + "." + image_filename + "." + image_filename + ".data"
         
         if "most_ch" in skip_filenames and "most_ch" not in file:
            continue
         
         if "pixch/sty_shapes" in filepath and "verified" in skip_filenames and "verified" not in file:
            continue
         
         if styLshapes_wo_pixch in filepath and "verified" in skip_filenames and "verified" not in file:
            continue
         
         if ( "only_nfnd_pixch_sty2" in filepath or scnd_stg_all_files in filepath ) and "verify" in execute_script and file.count(".") != 2:
            continue
         
        
         
         # second filename starts right after first filename + period
         file2num_end = file.find(".", file1num_end + 1 )
      
      else:
         # pixch/find_pixch_shapes_matches.py which has data file like this 25.26.data
         # template/match_by_whole_image_pixels_template.py  data file example -> 25.26.data

         # second filename starts right after first filename + period
         file2num_end = file.find(".", file1num_end + 1 )        
      
      file2num = file[ file1num_end + 1: file2num_end ]
      skip_files_by_num.append( (file1num, file2num ) )



if "findim_pixch.py" in execute_script:
   create_skip_files( top_shapes_dir + directory + top_pixch_dir, "result" )
   
elif "find_internal_spixc_shapes" in execute_script:
   create_skip_files( top_shapes_dir + directory + "spixc_shapes/data/", ".data" )
   single_file_execution = True
   
elif "pixch/find_staying_shapes" in execute_script:
   create_skip_files( top_shapes_dir + directory + top_pixch_dir + "sty_shapes/data/", ".data" )

elif "pixch/find_pixch_shapes.py" in execute_script:
   create_skip_files( top_shapes_dir + directory + top_pixch_dir + "data/", "most_ch" )

elif "pixch/verify_staying_shapes" in execute_script:
   create_skip_files( top_shapes_dir + directory + top_pixch_dir + "sty_shapes/data/", "verified" )

elif "pixch/find_pixch_shapes_matches.py" in execute_script:
   create_skip_files( top_shapes_dir + directory + top_pixch_dir + "ch_shapes/pixch_shapes/data/", ".data" )

elif "styLshape/find_staying_Lshp_btwn_frames" in execute_script:
   create_skip_files( top_shapes_dir + directory + styLshapes + "/intnl_spixcShp/data/", ".data" )

elif "styLshape/find_styLshp_wo_pixch_btwn_frames" in execute_script:
   create_skip_files( top_shapes_dir + directory + styLshapes_wo_pixch + "/intnl_spixcShp/data/", ".data" )

elif "styLshape/verify_styLshp_wo_pixch" in execute_script:
   create_skip_files( top_shapes_dir + directory + styLshapes_wo_pixch + "/intnl_spixcShp/data/", "verified" )

elif "template/match_by_whole_image_pixels_template" in execute_script:
   create_skip_files( top_shapes_dir + directory + "template/image_pixels/data/", ".data" )
   

elif "scnd_stage/shape_nbrs_matches_from_only_Nfnd_pixch_sty2" in execute_script:
   create_skip_files( top_shapes_dir + directory + snd_stg_alg_shp_nbrs_dir + "/only_nfnd_pixch_sty2/", ".data" )

elif "scnd_stage/verify_s_nbrs_m_frm_only_Nfnd_pixch_sty" in execute_script:
   create_skip_files( top_shapes_dir + directory + snd_stg_alg_shp_nbrs_dir + "/only_nfnd_pixch_sty2/", ".data" )

elif "scnd_stage/cross_check_all_LL_algo_acrs_cur_files" in execute_script:
   create_skip_files( top_shapes_dir + directory + scnd_stg_all_files + "/data/", ".data" )




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
      if single_file_execution is False and ( skip1n2files[0] == file1num and ( skip1n2files[1] == file2num or file2num in skip1n2files[1] ) ):
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
   
   if "find_mid_changed_shapes" in execute_script or "pixch/find_staying_shapes" in execute_script or "pixch/find_pixch_shapes.py" in execute_script or \
      "scnd_stage/shape_nbrs_matches_from_only_Nfnd_pixch_sty2" in execute_script:
      for execute_count in range(2):
         if execute_count == 0:
            if "find_mid_changed_shapes" in execute_script or "pixch/find_pixch_shapes.py" in execute_script:
               sys.argv = [ file, file2name, file, directory ]
            elif "pixch/find_staying_shapes" in execute_script or "scnd_stage/shape_nbrs_matches_from_only_Nfnd_pixch_sty2" in execute_script:
               sys.argv = [ file, file2name, True, directory ]
            
         
         elif execute_count == 1:
            if "find_mid_changed_shapes" in execute_script or "pixch/find_pixch_shapes.py" in execute_script:
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
   

   
   
   
   
   
   
   
   
   
   
   
   
   
   
   