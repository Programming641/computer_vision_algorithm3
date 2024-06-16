import tkinter
from PIL import ImageTk, Image
from libraries import btwn_amng_files_functions, pixel_shapes_functions, same_shapes_functions, pixel_functions, image_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files
import pickle
import sys, pathlib, os



shapes_type = "intnl_spixcShp"
directory = sys.argv[1]


# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

   
across_all_files_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/data/"
all_matches_so_far_dfile = across_all_files_ddir + "all_matches.data"
if os.path.exists( all_matches_so_far_dfile ):
   with open (all_matches_so_far_dfile, 'rb') as fp:
      all_matches_so_far = pickle.load(fp)
   fp.close()



def check_shape_size( param_im1shapeid, param_im2shapeid, param_shapes, param_ano_shapes, size_threshold=1 ):
   # check if size is too different
   im1shapes_total = len( param_shapes[param_im1shapeid] )
   im2shapes_total = len( param_ano_shapes[param_im2shapeid] )
      
   im1_2pixels_diff = abs( im1shapes_total - im2shapes_total )
   if im1_2pixels_diff != 0:
      if im1shapes_total > im2shapes_total:
         if im1_2pixels_diff / im2shapes_total > size_threshold:
            return True
      else:
         if im1_2pixels_diff / im1shapes_total > size_threshold:
            return True

   return False      


def get_rest_of_files( done_filename ):
   done_first_file = done_filename.split(".")[0]
   
   all_files = list( all_matches_so_far.keys() )
   # removing already done files
   done_files = [done_filename]
   for each_file in all_files:
      each_file_first_file = each_file.split(".")[0]
      
      if int( each_file_first_file ) < int( done_first_file ):
         done_files.append( each_file )
   
   for remove_file in done_files:
      all_files.remove( remove_file )
      
   if len( all_files ) >= 2:
      # make sure that all_files are in the order. 10.11 -> 11.12 -> 12.13 -> 13.14 -> 14.15 ....
      prev_filename = None
      for each_files in all_files:
         if prev_filename is None:
            prev_filename = each_files
         else:
            prev_first_file = prev_filename.split(".")[0]
            cur_first_file = each_files.split(".")[0]
         
            if int( prev_first_file ) > int( cur_first_file ):
               print("ERROR in " + os.path.basename(__file__) + " all_files is not in order" )
               sys.exit(1)
      
            prev_filename = each_files

   return all_files


def find_match_from_next_file( next_file, image2shape ):

   found_shapes = [ temp_shapes for temp_shapes in all_matches_so_far[next_file] if temp_shapes[0] == image2shape ]

   return found_shapes



result_shapes = []

prev_file_shapes = None
prev_filename = None
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
for each_file in all_matches_so_far:
   
   cur_im1file = each_file.split(".")[0]
   cur_im2file = each_file.split(".")[1]

   if ref_imagefile_op is False:
      im1 = Image.open(top_images_dir + directory + cur_im1file + ".png" )
      im_size = im1.size
      im_width, im_height = im_size
      
      ref_imagefile_op = True

  
   if prev_file_shapes is None:
      prev_file_shapes = all_matches_so_far[each_file]
      prev_filename = each_file
      

   
   else:
      
   
   
      for each_shapes in all_matches_so_far[each_file]:
         already_done = { True for temp_shapes in result_shapes if each_file in temp_shapes.keys() and each_shapes in temp_shapes[ each_file ] }
         
         if len( already_done ) >= 1:
            continue
         
         
         found_shapes = [ temp_shapes for temp_shapes in prev_file_shapes if temp_shapes[1] == each_shapes[0] ]
         
         if len( found_shapes ) >= 1:
            # one to one match or combining type of match.
            
            cur_matches = {prev_filename: found_shapes}
            cur_matches[ each_file ] = [each_shapes]
            

            rest_of_files = get_rest_of_files( each_file )
            
            next_image2shape = found_shapes[0][1]
            
            # find current match's further consecutives.
            for next_file in rest_of_files:
               
               further_found_shapes = find_match_from_next_file( next_file, next_image2shape )
               if len( further_found_shapes ) >= 1:
                  
                  cur_matches[ next_file ] = further_found_shapes
                  
                  next_image2shape = further_found_shapes[0][1]

         
            result_shapes.append( cur_matches )



      prev_file_shapes = all_matches_so_far[each_file]
      prev_filename = each_file




consecutives_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/consecutives/data/"
if os.path.exists(consecutives_ddir ) == False:
   os.makedirs(consecutives_ddir )

consecutives2_dfile = consecutives_ddir + "2.data"
with open(consecutives2_dfile, 'wb') as fp:
   pickle.dump(result_shapes, fp)
fp.close()



















