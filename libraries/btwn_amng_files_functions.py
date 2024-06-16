from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir
from libraries import pixel_shapes_functions, pixel_functions
from PIL import Image
import os, sys
import math
import re
import pickle

# btwn_frames_files -> [ "1.6", "20.5", "12.14", "14.15", "15.16", "1.5" ]
# this function put btwn_frames_files in order
# the order is that the small number file comes first.
# example. 10.11 -> 11.12 -> 12.13 ...
# if there are multiple same numbers before the comma, then the smallest second number after the comma should come first
# example. 10.11 -> 10.12 -> 10.13 ...
def put_btwn_frames_files_in_order( btwn_frames_files ):
   ordered_btwn_frames_files = []
   def num_come_before_after( number1, number2 ):
      num_bef_aft = None
      if number1 > number2:
         # number1 is bigger than number2 so number1 should come after number2
         num_bef_aft = 1
      elif number1 == number2:
         num_bef_aft = 2
      elif number1 < number2:
         # btwn_frames_file's first number is smaller
         num_bef_aft = 0

      return num_bef_aft

   def process_num_diffs( num_diff, num_closest_diff ):
      # when num_diff and num_closest_diff are both positive numbers, then the one closer
      # to 0 is the number that should come right before first_num. so the first_num should come right after
      # that number.           
      # closer to 0 is the smaller number
      if num_diff > 0 and num_closest_diff > 0:
         if num_diff < num_closest_diff:
            # num_diff is closer to 0 so btwn_frames_file number should come after the ordered_number
            return 0
            
         #elif num_closest_diff < num_diff:
            # num_closest_diff is closer to 0 so btwn_frames_file number should come after the closest_num

      elif num_diff == 0:
         return 2                      


      #elif num_diff > 0 and num_closest_diff < 0:
         # ordered_list number is positive and closest number is negative
         # It passed all the test data without implementing this condition but I don't know why it works...
            
      #elif num_diff < 0 and num_closest_diff > 0:
         # ordered_list number is negative and closest number is postive
         # It passed all the test data without implementing this condition but I don't know why it works...



   for btwn_frames_file in btwn_frames_files:
   
      if len( ordered_btwn_frames_files ) == 0:
         ordered_btwn_frames_files.append( btwn_frames_file )
      
      else:
      
         first_num_lastindex = btwn_frames_file.find(".")
         first_num = int( btwn_frames_file[0: first_num_lastindex] )
         second_num = int( btwn_frames_file[first_num_lastindex + 1: len( btwn_frames_file )] )
      
         # find current one's first number's closest first number from ordered_btwn_frames_files
         closest_first_num = closest_first_bef_aft = closest_sec_bef_aft = closest_sec_num = None
         closest_num = None
         closest_num_lindex = None
         for list_index, ordered_number in enumerate( ordered_btwn_frames_files ):
         
            ordered_list_first_num_lindex = ordered_number.find(".")
            ordered_list_first_num = int( ordered_number[0: ordered_list_first_num_lindex] )
            ordered_list_sec_num = int( ordered_number[ ordered_list_first_num_lindex + 1: len( ordered_number )] )
            if closest_num is None:
               # closest number initialization
               closest_first_num = ordered_list_first_num
               closest_sec_num = ordered_list_sec_num
               closest_num = ordered_number
               closest_num_lindex = list_index
            
               closest_first_bef_aft = num_come_before_after( first_num, ordered_list_first_num )
               closest_sec_bef_aft = num_come_before_after( second_num, ordered_list_sec_num )
         
            else:

               first_num_diff = first_num - ordered_list_first_num
               first_num_closest_diff = first_num - closest_first_num
            
               # if return value is 0, ordered_number should become the closest_number
               # if return value is 1, closest_number is still the closest.
               # if return value is 2, ordered_numer and closest number are the same            
               cur_closest = process_num_diffs( first_num_diff, first_num_closest_diff )
            
               if cur_closest == 0:
                  closest_first_num = ordered_list_first_num
                  closest_first_bef_aft = num_come_before_after( first_num, ordered_list_first_num )
                  closest_num = ordered_number
                  closest_num_lindex = list_index
               elif cur_closest == 2:
                  sec_num_diff = second_num - ordered_list_sec_num
                  sec_num_closest_diff = second_num - closest_sec_num
                  cur_sec_closest = process_num_diffs( sec_num_diff, sec_num_closest_diff )
               
                  if cur_sec_closest == 0:
                     closest_first_num = ordered_list_first_num
                     closest_first_bef_aft = num_come_before_after( first_num, ordered_list_first_num )
                     closest_sec_bef_aft = num_come_before_after( second_num, ordered_list_sec_num )
                     closest_num = ordered_number
                     closest_num_lindex = list_index                  

               

         # now that all numbers of ordered_btwn_frames_files have been checked
      
         if closest_first_bef_aft == 1:
            # btwn_frames_file number should come after
            ordered_btwn_frames_files.insert( closest_num_lindex + 1, btwn_frames_file )
         elif closest_first_bef_aft == 0:
            # btwn_frames_file number should come before
            ordered_btwn_frames_files.insert( closest_num_lindex, btwn_frames_file )
         else:
            # btwn_frames_file first number is the same. so check second number
            if closest_sec_bef_aft == 1:
               # btwn_frames_file number should come after
               ordered_btwn_frames_files.insert( closest_num_lindex + 1, btwn_frames_file )
            else:
               # number with the same first and second shouldn't exist. so if not bigger then it's smaller

               ordered_btwn_frames_files.insert( closest_num_lindex, btwn_frames_file )   


   return ordered_btwn_frames_files



# btwn_files -> ['10.11.10.data', '10.11.11.data', '11.12.11.data', '11.12.12.data', '12.13.12.data', '12.13.13.data']
def put3btwn_files_in_order( btwn_files ):
   ordered_files = []
   while len( btwn_files ) >= 1:
      # loop until every file is processed
      
      # first priority smallest number
      first_priority_sm_num = min( [ int( file.split(".")[0] ) for file in btwn_files ] )
   
      # get files that have first priority smallest number
      fst_priority_sm_files = [ file for file in btwn_files if int( file.split(".")[0] ) == first_priority_sm_num ]

      fst_file_main_num = int( fst_priority_sm_files[0].split(".")[2] )
      snd_file_main_num = int( fst_priority_sm_files[1].split(".")[2] )

      # of these first priority smallest number files, get file that has the smaller main file
      # there should be exactly two files in the fst_priority_sm_files
      if len( fst_priority_sm_files ) != 2:
         print("ERROR in " + os.path.basename(__file__) + " there should be only two file1 file2 named files" )
         sys.exit(1)
      else:
         if fst_file_main_num < snd_file_main_num:
            ordered_files.append( fst_priority_sm_files[0] )
            ordered_files.append( fst_priority_sm_files[1] )
         else:
            ordered_files.append( fst_priority_sm_files[1] )
            ordered_files.append( fst_priority_sm_files[0] )            

         btwn_files.remove( fst_priority_sm_files[0] )
         btwn_files.remove( fst_priority_sm_files[1] )
      
      
   return ordered_files


def get_btwn_files_nums( lowest_filenum, highest_filenum ):
   all_btwn_files_nums = []
   for cur_num in range( int( lowest_filenum ), int( highest_filenum ) ):
      im1_filenum = str( cur_num )
      im2_filenum = str( cur_num + 1 )

      all_btwn_files_nums.append( im1_filenum + "." + im2_filenum )

   return all_btwn_files_nums

# imdir is directory under top_images_dir
def get_low_highest_filenums( imdir ):

   imdir_contents = os.listdir(top_images_dir + imdir)
   im_files = set()
   for each_content in imdir_contents:
      if os.path.isfile(os.path.join(top_images_dir + imdir, each_content)):
         if ".png" not in each_content:
            continue
         # file looked after has number.png format
         filenum = each_content.replace(".png", "")
         if filenum.isnumeric():
            im_files.add( int(filenum) )
   
   return ( min(im_files), max(im_files) )





# shapes_dir example: C:\Users\Taichi\Documents\computer_vision\shapes\videos\street3\resized\min1\shapes\
# target_files: list of image file numbers to get image shapes for. [ 25, 26, 29 ] these image shapes will be returned
def get_all_image_shapes( shapes_dir, return_highest=False, convert_to_xy=False, target_files=None ):
   # [ lowest number image shapes, second lowest number image shapes, ... ]
   im_shapes = []
   
   
   
   target_im_dir = ""
   if convert_to_xy is True:
      # I need to get image size
      im_size = None
      
      def split_by_each_dir( param_path ):

         path_wk = param_path.split("/")
         split_path = []

         for each_dir in path_wk:
            backslash_splits = each_dir.split("\\")

            if len( backslash_splits ) >= 2:
               for backslash_split in backslash_splits:
                  split_path.append( backslash_split )
   
            else:
               split_path.append( each_dir )

         return split_path


      split_shapes_dirs = split_by_each_dir( shapes_dir )
      split_top_shapes_dir = split_by_each_dir( top_shapes_dir )

      common_dirs = set(split_shapes_dirs).intersection( set(split_top_shapes_dir) )
      split_shapes_dirs = [ temp_dir for temp_dir in split_shapes_dirs if temp_dir not in common_dirs ]

      found = True
      search_im_dir = top_images_dir
      while found is True:
         found = False
         for im_dir in os.listdir(search_im_dir):
            if im_dir == split_shapes_dirs[0]:
               split_shapes_dirs.pop(0)
               search_im_dir += im_dir + "/"
         
               found = True
        
         if found is False or len(split_shapes_dirs) == 0:
            target_im_dir = search_im_dir
            break
   
   shapes_files = os.listdir(shapes_dir)
   all_image_files = [ temp_fname for temp_fname in shapes_files if not os.path.isdir(shapes_dir + temp_fname) and "shapes.data" in temp_fname ]
   
   all_image_nums = [ int( temp_file.replace("shapes.data", "") ) for temp_file in all_image_files if temp_file.replace("shapes.data", "").isnumeric()  ]
   
   lowest_filenum = min(all_image_nums)
   highest_filenum = max(all_image_nums)
   
   ordered_shapes_files = []
   for cur_filenum in range( lowest_filenum, highest_filenum + 1 ):
      ordered_shapes_files.append( str(cur_filenum) + "shapes.data" )
   
   for cur_shape_file in ordered_shapes_files:
         
      if convert_to_xy is True and im_size is None:
         im1 = Image.open(target_im_dir + str(lowest_filenum) + ".png" )
         im_size = im1.size
      
      cur_fpath = shapes_dir + cur_shape_file
      with open (cur_fpath, 'rb') as fp:
         cur_im_shapes = pickle.load(fp)
      fp.close()
      
      if convert_to_xy is True:
         for shapeid in cur_im_shapes:
            pixels = set()
            for pindex in cur_im_shapes[shapeid]:
               xy = pixel_functions.convert_pindex_to_xy( pindex, im_size[0] )
               
               pixels.add(xy)
            
            cur_im_shapes[shapeid] = pixels
            
      im_shapes.append( cur_im_shapes )

   if return_highest is False:
      return im_shapes, lowest_filenum
   else:
      return im_shapes, lowest_filenum, highest_filenum


# im_dir example: videos\street3\resized\min1\
# target: "neighbors" -> gets image shapes neighbors data. "colors" -> gets image shapes colors
def get_all_im_target_data( im_dir, target, min_colors=None ):

   shapes_dir = top_shapes_dir + im_dir + "shapes/"
   min_filenum, highest_filenum = get_low_highest_filenums( im_dir )
   
   all_im_target_data = []
   for cur_im_num in range(min_filenum, highest_filenum + 1 ):
      
      if target == "neighbors":
         target_file = shapes_dir + "shape_nbrs/" + str(cur_im_num) + "_shape_nbrs.data"      
      elif target == "colors":
         target_data = pixel_shapes_functions.get_all_shapes_colors(str(cur_im_num), im_dir, min_colors=min_colors)
   
      if target == "neighbors":
         with open (target_file, 'rb') as fp:
            target_data = pickle.load(fp)
         fp.close()   
      
      all_im_target_data.append( target_data )

   return all_im_target_data



# im_dir example: C:\Users\Taichi\Documents\computer_vision\images\videos\street3\resized\min1\
def get_all_image_data( im_dir ):
   # [ lowest number image data, second lowest number image data, ... ]
   all_im_data = []
   
   im_dir_contents = os.listdir(im_dir)
   # make sure that files in order. ['25.png', '26.png', ..., 'test.png', ... ]
   im_dir_contents.sort()
   
   for cur_file in im_dir_contents:
      if "png" not in cur_file or ( not cur_file.replace(".png", "").isnumeric() ):
         # file has to be number.png
         continue
      
      im_obj = Image.open( im_dir + cur_file )
      all_im_data.append( im_obj.getdata() )

   return all_im_data



# total numbers to be counted down. this is the result of len( iterator such as list, set, or dictionary )
# cur_num is current number
def show_progress( total, cur_num, prev_num, remaining_chars="", in_step=1 ):

   max_len = len( str(total) )
   prev_len = len( str(prev_num) )
   
   cur_len = len(str(cur_num))
   if cur_len < prev_len:
      remaining_chars = ""
      remaining_len = max_len - cur_len
      for char_len in range( remaining_len ):   
         remaining_chars += " "
   

   if cur_num % in_step == 0:
      print("\r",cur_num, remaining_chars, " remaining", end="")

   if cur_num == in_step:
      # last 
      print( )

   return remaining_chars

































