from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir
from libraries import read_files_functions
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
         sys.exit()
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





































