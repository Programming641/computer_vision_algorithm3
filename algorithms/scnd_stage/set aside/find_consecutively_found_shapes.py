import tkinter
from PIL import ImageTk, Image
from libraries import btwn_amng_files_functions, read_files_functions, pixel_shapes_functions, same_shapes_functions, pixel_functions, image_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files
from libraries.cv_globals import frth_smallest_pixc
import pickle
import sys, pathlib, os



shapes_type = "intnl_spixcShp"
directory = "videos/street3/resized/min"


# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'


if shapes_type == "normal":
   print("shapes_type normal is not supported in " + os.path.basename(__file__) )
   sys.exit()
   

elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"

   shapes_dir = s_pixcShp_intnl_dir + "shapes/"


def get_rest_of_files( done_filename ):
   done_first_file = done_filename.split(".")[0]
   
   rest_of_files = list( one_to_one_m_shapes.keys() )
   # removing already done files
   done_files = [done_filename]
   for each_file in rest_of_files:
      each_file_first_file = each_file.split(".")[0]
      
      if int( each_file_first_file ) < int( done_first_file ):
         done_files.append( each_file )
   
   for remove_file in done_files:
      rest_of_files.remove( remove_file )
      
   if len( rest_of_files ) >= 2:
      # make sure that rest_of_files are in the order. 10.11 -> 11.12 -> 12.13 -> 13.14 -> 14.15 ....
      prev_filename = None
      for each_files in rest_of_files:
         if prev_filename is None:
            prev_filename = each_files
         else:
            prev_first_file = prev_filename.split(".")[0]
            cur_first_file = each_files.split(".")[0]
         
            if int( prev_first_file ) > int( cur_first_file ):
               print("ERROR in " + os.path.basename(__file__) + " rest_of_files is not in order" )
               sys.exit()
      
            prev_filename = each_files

   return rest_of_files



def find_further_files_1to1shapes( param_shapes, done_filename, param_cur_found_shapes ):

   rest_of_files = get_rest_of_files( done_filename )
   if len( rest_of_files ) < 1:
      return

   found_shapes = [ temp_shapes for temp_shapes in one_to_one_m_shapes[ rest_of_files[0] ] if param_shapes[1] == temp_shapes[0] ]
   if len( found_shapes ) == 1:
            
      param_cur_found_shapes[ rest_of_files[0] ] = found_shapes[0]
            
      find_further_files_1to1shapes( found_shapes[0], rest_of_files[0], param_cur_found_shapes )




def find_further_files_brknUp_shapes( param_shapes, done_filename, param_cur_found_shapes ):
   # param_shapes -> ['13446', ['13848', '8233']]
   
   rest_of_files = get_rest_of_files( done_filename )
   if len( rest_of_files ) < 1:
      return

   
   # checking to see if all image2 shapes of param_shapes can be found
   im2shapes_found_len = 0
   all_found_shapes = [[], []]
   for im2shape in param_shapes[1]:
      found_shapes = [ temp_shapes for temp_shapes in one_to_one_m_shapes[ rest_of_files[0] ] if im2shape == temp_shapes[0] ]
      
      if len( found_shapes ) == 1:
         all_found_shapes[0].append( found_shapes[0][0] )
         all_found_shapes[1].append( found_shapes[0][1] )
      
         im2shapes_found_len += 1

      else:
         # was not found from one to one type of match. try combining type of match
         # combining type of match has multiple image1 shapes
         found_shapes = [ temp_shapes for temp_shapes in combining_m_shapes[ rest_of_files[0] ] if im2shape in temp_shapes[0] ]
         
         if len( found_shapes ) > 1:
            print("attention required in " + os.path.basename(__file__) + " multiple matches found for previous broken up into pieces " + 
                  "type of match image2 shape and combining type of match image1 shape. is this supported to happen?")
            sys.exit()         

         elif len( found_shapes ) == 1:
            all_found_shapes[0].append( im2shape )
            all_found_shapes[1].append( found_shapes[0][1] )
            im2shapes_found_len += 1
            
         else:
            # was not found from combining type of match. try broken up into pieces type of match
            # broken up type of match has multiple image2 shapes.
            found_shapes = [ temp_shapes for temp_shapes in brokenUp_m_shapes[ rest_of_files[0] ] if im2shape == temp_shapes[0] ]

            if len( found_shapes ) > 1:
               print("attention required in " + os.path.basename(__file__) + " multiple matches found for previous broken up into pieces " + 
                     "type of match image2 shape and combining type of match image1 shape. is this supported to happen?")
               sys.exit()         

            elif len( found_shapes ) == 1:
               all_found_shapes[0].append( im2shape )
               all_found_shapes[1].extend( found_shapes[0][1] )
               im2shapes_found_len += 1


   if im2shapes_found_len == len( param_shapes[1] ):

      param_cur_found_shapes[ rest_of_files[0] ] = all_found_shapes
     

def find_further_files_combining_shapes( param_shapes, done_filename, param_cur_found_shapes ):
   # param_shapes -> [['23513', '21125', '21121', '21106', '13521', '12709', '17921'], '21914']

   rest_of_files = get_rest_of_files( done_filename )
   if len( rest_of_files ) < 1:
      return

   # not implemented.


    
   
shapes_m_types_dir = top_shapes_dir + directory + scnd_stg_all_files + "/shp_match_types/"
one_to_one_matched_dfile = shapes_m_types_dir + "data/one_to_one.data"
with open (one_to_one_matched_dfile, 'rb') as fp:
   # {'10.11': [('37042', '43422'), ('40641', '43422'), ... ], ... }
   # { prev filename_cur filename: [ ( image1 shapeid, image2 shapeid), ... ], ... }
   one_to_one_m_shapes = pickle.load(fp)
fp.close()

combining_matched_dfile = shapes_m_types_dir + "data/combining.data"
with open (combining_matched_dfile, 'rb') as fp:
   # {'10.11': [[['38784', '38784', '38784', '38784'], '45572'], [['4436', '4436'], '8439'] ], ... }
   # { prev filename_cur filename: [ [ [ im1shapes ], im2shape ], ... ], ... }
   combining_m_shapes = pickle.load(fp)
fp.close()

brokenUp_matched_dfile = shapes_m_types_dir + "data/brokenUp.data"
with open (brokenUp_matched_dfile, 'rb') as fp:
   # {'10.11': [['45572', ['38784', '38784', '38784', '38784'] ], [ '8439', ['4436', '4436'] ], ... }
   # { prev filename_cur filename: [ [ im1shape, [ im2shapes ] ], ... ], ... }
   brokenUp_m_shapes = pickle.load(fp)
fp.close()
   

# [ { 10.11: ( image1, image2 ), 11.12: ( image1shapeid, image2shapeid ), ... }, ... ]
consecutively_found_shapes = []

prev_one_to_one = None
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
for each_file in one_to_one_m_shapes:
   print( each_file )
   
   cur_im1file = each_file.split(".")[0]
   cur_im2file = each_file.split(".")[1]

   cur_files_one_to_one = one_to_one_m_shapes[ each_file ]
   cur_files_combining = combining_m_shapes[ each_file ]
   cur_files_brokenUp = brokenUp_m_shapes[ each_file ]

   
   if prev_one_to_one is None:
      prev_one_to_one = cur_files_one_to_one
      prev_combining = cur_files_combining
      prev_brokenUp = cur_files_brokenUp
      prev_filename = each_file
   
   else:

      for prev_1to1_shape in prev_one_to_one:
         # prev_1to1_shape -> ('37042', '43422')
         
         cur_found_shapes = {}
         
         found_shapes = [ temp_shapes for temp_shapes in one_to_one_m_shapes[ each_file ] if temp_shapes[0] == prev_1to1_shape[1] ]
         
         if len( found_shapes ) == 1:
            cur_found_shapes[ prev_filename ] = prev_1to1_shape
            cur_found_shapes[ each_file ] = found_shapes[0]
            
            find_further_files_1to1shapes( found_shapes[0], each_file, cur_found_shapes )
            
         else:
            # prev_1to1_shape not found in one_to_one_m_shapes[ each_file ]. next, try to find prev_1to1_shape from combining_m_shapes[ each_file ]
            # combining type of match has multiple image2 shapes.
            # so if image2 shape of prev_1to1_shape is found in combining_m_shapes[ each_file ] image1 shape, that is a match.
            found_shapes = [ temp_shapes for temp_shapes in combining_m_shapes[ each_file ] if prev_1to1_shape[1] in temp_shapes[0]  ]
            
            if len( found_shapes ) > 1:
               print("attention required in " + os.path.basename(__file__) + " multiple matches found for previous one to one type of match " + 
                     " image2 shape and combining type of match image1 shape. is this supported to happen?")
               sys.exit()
            
            elif len( found_shapes ) == 1:
               cur_found_shapes[ prev_filename ] = prev_1to1_shape
               cur_found_shapes[ each_file ] = found_shapes[0]
               
            
            else:
               # prev_1to1_shape not found in combining_m_shapes[ each_file ]. next, try to find prev_1to1_shape from brokenUp_m_shapes[ each_file ]
               # broken up into pieces type of match has multiple image1 shapes and one image2 shape.
               # so if image2 shape of prev_1to1_shape is found in brokenUp_m_shapes[ each_file ] image1 shape, that is a match.
               found_shapes = [ temp_shapes for temp_shapes in brokenUp_m_shapes[ each_file ] if temp_shapes[0] == prev_1to1_shape[1] ]
               
               if len( found_shapes ) > 1:
                  print("attention required in " + os.path.basename(__file__) + " multiple matches found for previous one to one type of match " + 
                        " image2 shape and broken up into pieces type of match image1 shape. is this supported to happen?")
                  sys.exit()
            
               elif len( found_shapes ) == 1:
                  cur_found_shapes[ prev_filename ] = prev_1to1_shape
                  cur_found_shapes[ each_file ] = found_shapes[0]
                  

            
                  find_further_files_brknUp_shapes( found_shapes[0], each_file, cur_found_shapes )

         if len( cur_found_shapes ) != 0: 
            consecutively_found_shapes.append( cur_found_shapes )


      for prev_combining_shape in prev_combining:
         # prev_combining_shape -> [['38784', '38784', '38784', '38784'], '45572']
         cur_found_shapes = {}
         
         found_shapes = [ temp_shapes for temp_shapes in one_to_one_m_shapes[ each_file ] if temp_shapes[0] == prev_combining_shape[1] ]
         
         if len( found_shapes ) == 1:
            cur_found_shapes[ prev_filename ] = prev_combining_shape
            cur_found_shapes[ each_file ] = found_shapes[0]


            
            find_further_files_1to1shapes( found_shapes[0], each_file, cur_found_shapes )
            
         else:
            # prev_combining_shape not found in one_to_one_m_shapes[ each_file ]. next, try to find prev_combining_shape from combining_m_shapes[ each_file ]
            # combining type of match has multiple image1 shapes.
            # so if image2 shape of prev_combining_shape is found in combining_m_shapes[ each_file ] image1 shape, that is a match.
            found_shapes = [ temp_shapes for temp_shapes in combining_m_shapes[ each_file ] if prev_combining_shape[1] == temp_shapes[0]  ]       
         
            if len( found_shapes ) > 1:
               print("attention required in " + os.path.basename(__file__) + " multiple matches found for previous one to one type of match " + 
                     " image2 shape and combining type of match image1 shape. is this supported to happen?")
               sys.exit()
            
            elif len( found_shapes ) == 1:
               cur_found_shapes[ prev_filename ] = prev_combining_shape
               cur_found_shapes[ each_file ] = found_shapes[0]
            
            else:         
               # prev_combining_shape not found in combining_m_shapes[ each_file ]. next, try to find prev_combining_shape from brokenUp_m_shapes[ each_file ]
               # broken up into pieces type of match has multiple image2 shapes and one image1 shape.
               # so if image2 shape of prev_combining_shape is found in brokenUp_m_shapes[ each_file ] image1 shape, that is a match.
               found_shapes = [ temp_shapes for temp_shapes in brokenUp_m_shapes[ each_file ] if temp_shapes[0] == prev_combining_shape[1] ]
               
               if len( found_shapes ) > 1:
                  print("attention required in " + os.path.basename(__file__) + " multiple matches found for previous one to one type of match " + 
                        " image2 shape and broken up into pieces type of match image1 shape. is this supported to happen?")
                  sys.exit()
            
               elif len( found_shapes ) == 1:
                  cur_found_shapes[ prev_filename ] = prev_combining_shape
                  cur_found_shapes[ each_file ] = found_shapes[0]
            
                  find_further_files_brknUp_shapes( found_shapes[0], each_file, cur_found_shapes )         


         if len( cur_found_shapes ) != 0: 
            consecutively_found_shapes.append( cur_found_shapes )      

      for prev_brokenUp_shape in prev_brokenUp:
         # prev_brokenUp_shape -> [ '45572', ['38784', '38784', '38784', '38784'] ]
         cur_found_shapes = {}
         
         cur_found_shapes[ prev_filename ] = prev_brokenUp_shape

         find_further_files_brknUp_shapes( prev_brokenUp_shape, prev_filename, cur_found_shapes )   
   
      
         if len( cur_found_shapes ) != 0: 
            consecutively_found_shapes.append( cur_found_shapes ) 



      prev_one_to_one = cur_files_one_to_one
      prev_combining = cur_files_combining
      prev_brokenUp = cur_files_brokenUp  

      prev_filename = each_file


across_all_files_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/data/"
consecutives_dfile = across_all_files_ddir + "consecutives.data"
with open(consecutives_dfile, 'wb') as fp:
   pickle.dump(consecutively_found_shapes, fp)
fp.close()















