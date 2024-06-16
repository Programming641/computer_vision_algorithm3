import tkinter
from PIL import ImageTk, Image
from libraries import btwn_amng_files_functions, pixel_shapes_functions, same_shapes_functions, pixel_functions, image_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files, scnd_stg_spixc_dir, scnd_stg_ch_btwn_frames_dir
import pickle, copy
import sys, pathlib, os


directory = "videos/street3/resized/min1"
if len( sys.argv ) >= 2:
   directory = sys.argv[1]


# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

shapes_dir = top_shapes_dir + directory + "shapes/"

   
all_matches_ddir = top_shapes_dir + directory + "all_matches/data/"
all_matches_dfile = all_matches_ddir + "1.data"
with open (all_matches_dfile, 'rb') as fp:
   all_matches_so_far = pickle.load(fp)
fp.close()


# { 1.2: [ im1shapes, im2shapes ], ... }
all_files_im_shapes = {}
for each_file in all_matches_so_far: 

   cur_im1file = each_file.split(".")[0]
   cur_im2file = each_file.split(".")[1]
   
   shapes_dfile = shapes_dir + cur_im1file + "shapes.data"
   im2shapes_dfile = shapes_dir + cur_im2file + "shapes.data"

   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()

   for shapeid in im1shapes:
      im1shapes[ shapeid ] = set( im1shapes[ shapeid ] )

   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()
   
   for shapeid in im2shapes:
      im2shapes[shapeid] = set( im2shapes[ shapeid ] )
   
   all_files_im_shapes[ each_file ] = []
   all_files_im_shapes[ each_file ].append( im1shapes )
   all_files_im_shapes[ each_file ].append( im2shapes )




def fill_results( previously_matched_shapes, first=False ):
   for each_file in previously_matched_shapes:
      if first is True:
         alrdy_matched_shapes[ each_file ] = []
      
      else:

         for each_shapes in previously_matched_shapes[ each_file ]:
            # [{'7077', '6009', ... }, {'7077', '6009', ... }]
            # check if  90% or more similar shapes already exist in alrdy_matched_shapes
            cur_each_shapes_matched = False
            prev_im1shapes = set()
            prev_im2shapes = set()

            skip = False
 
            for prev_im1shape in each_shapes[0]:
               # if shape from previously_matched_shapes is not present in all_files_im_shapes, this means that separate_1tomulti_matches.py or separate_big_to_small_matches.py
               # deleted it. if so, skip this match.
               if prev_im1shape not in all_files_im_shapes[ each_file ][0].keys():
                  skip = True
                  break
                  
               prev_im1shapes |= all_files_im_shapes[ each_file ][0][ prev_im1shape ]
            for prev_im2shape in each_shapes[1]:
               if prev_im2shape not in all_files_im_shapes[ each_file ][1].keys():
                  skip = True
                  break
            
               prev_im2shapes |= all_files_im_shapes[ each_file ][1][ prev_im2shape ]

            if skip is True:
               continue
               
            for alrdy_m_each_shapes in alrdy_matched_shapes[ each_file ]:
               alrdy_m_im1shapes = set()
               alrdy_m_im2shapes = set()   
               
            
               for alrdy_m_im1shape in alrdy_m_each_shapes[0]:
                  alrdy_m_im1shapes |= all_files_im_shapes[ each_file ][0][ alrdy_m_im1shape ]
               for alrdy_m_im2shape in alrdy_m_each_shapes[1]:
                  alrdy_m_im2shapes |= all_files_im_shapes[ each_file ][1][ alrdy_m_im2shape ]
               
               '''
               size_diff = check_shape_size( prev_im1shapes, alrdy_m_im1shapes, size_threshold=0.23 )
               if size_diff is True:
                  continue
               '''
               
               common_im1pixels = prev_im1shapes.intersection( alrdy_m_im1shapes )
               
               if len( common_im1pixels ) / len( prev_im1shapes ) >= 0.8:
                  # closer to the im2shapes pixel counts is the better match
                  cur_each_shapes_matched = True
                  
                  prev_pix_count_diff = abs( len( prev_im1shapes ) - len( prev_im2shapes ) )
                  alrdy_m_pix_count_diff = abs( len( alrdy_m_im1shapes ) - len( alrdy_m_im2shapes ) )
               
                  if prev_pix_count_diff < alrdy_m_pix_count_diff:
                     # current previously_matched_shapes is the better match
                     alrdy_matched_shapes[ each_file ].remove( alrdy_m_each_shapes )
                  
                     alrdy_matched_shapes[ each_file ].append( each_shapes )
                     
                  break
               
               elif len( common_im1pixels ) / len( alrdy_m_im1shapes ) >= 0.8:
                  
                  cur_each_shapes_matched = True
                  break
            
            if cur_each_shapes_matched is False:
               # 80% similar shapes were not found
                  
               alrdy_matched_shapes[ each_file ].append( each_shapes )
            

# { files : [ [ { im1shapes }, { im2shapes } ], ... ], ... }
alrdy_matched_shapes = {}

spixc_dir = top_shapes_dir + directory + scnd_stg_spixc_dir
spixc_shapes_dfile = spixc_dir + "/data/" + "1.data"
with open (spixc_shapes_dfile, 'rb') as fp:
   # { '10.11': [ [ [ im1shapes ], [ im2shapes ] ], ...  ], ... }
   spixc_shapes = pickle.load(fp)
fp.close()

fill_results( spixc_shapes, first=True )

ch_btwn_frames_ddir = top_shapes_dir + directory + scnd_stg_ch_btwn_frames_dir + "/data/"
ch_btwn_frames4_dfile = ch_btwn_frames_ddir + "4.data"
with open (ch_btwn_frames4_dfile, 'rb') as fp:
   # { '10.11': [ [ [ im1shapes ], [ im2shapes ] ], ...  ], ... }
   pixch_on_notfnd_shapes = pickle.load(fp)
fp.close()

fill_results( pixch_on_notfnd_shapes )

image_template_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/image_template/data/"
multi_shapes_by_img_tmpl_dfile = image_template_ddir + "verified_multi1.data"  
with open (multi_shapes_by_img_tmpl_dfile, 'rb') as fp:
   # {'1.2': [[{'68452', '52800'}, ['56042', '68454']]], '2.3': [[['37593', '33271'], {'33811', '32189', ... }], ... ], ... }
   multi_shapes_by_img_tmpl = pickle.load(fp)
fp.close()

fill_results( multi_shapes_by_img_tmpl )


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


def find_match_from_next_file( next_file, image2shape, cur_file=None, already_done=None ):
   
   if type( image2shape ) is int:
      found_shapes = [ temp_shapes for temp_shapes in all_matches_so_far[next_file] if temp_shapes[0] == image2shape ]

      return found_shapes
   
   elif type( image2shape ) is list or type( image2shape ) is set:
      image2shapes_pixels = set()
      for each_image2shape in image2shape:
         image2shapes_pixels |= all_files_im_shapes[cur_file][1][ each_image2shape ] 
      
      for next_file_each_shapes in alrdy_matched_shapes[ next_file ]:
         if ( next_file_each_shapes, next_file ) in already_done:
            continue
         already_done.append( ( next_file_each_shapes, next_file ) )

         next_file_im1shapes_pixels = set()
         for next_file_im1shape in next_file_each_shapes[0]:
            next_file_im1shapes_pixels |= all_files_im_shapes[ next_file ][0][ next_file_im1shape ]
         
         common_pixels = image2shapes_pixels.intersection( next_file_im1shapes_pixels )
         if len( common_pixels ) / len( image2shapes_pixels ) >= 0.55:
            return next_file_each_shapes

      return None          




def remove_duplicate_shapes(param_result_shapes):
   
   pairs_with_same_shape = set()
   done_indexes = set()
   for consec_index, consecutive in enumerate(param_result_shapes):

      for each_files in consecutive:

         for ano_consec_index, ano_consecutive in enumerate(param_result_shapes):
            if consec_index == ano_consec_index or ano_consec_index in done_indexes:
               continue
            for each_shapes in consecutive[each_files]:
               
               if each_files in ano_consecutive.keys():

                  # { ( "111", "222" ), ( "111", "334" ), ( "155", "222" ), ... }
                  common_shapes = { temp_shapes for temp_shapes in ano_consecutive[each_files] if ( temp_shapes[0] == each_shapes[0] or temp_shapes[1] == each_shapes[1] ) \
                                       and temp_shapes != each_shapes }
                     
                  if len(common_shapes) >= 1:
                     for each_common_shapes in common_shapes:
                     
                        pairs_with_same_shape.add( ( consec_index, ano_consec_index, each_files, each_common_shapes ) )

      done_indexes.add(consec_index)

   for each_data in pairs_with_same_shape:
      cur_index = each_data[0]
      ano_index = each_data[1]
      ano_files = each_data[2]
      ano_shapes = each_data[3]
   
      if ano_files in param_result_shapes[ano_index].keys() and ano_shapes in param_result_shapes[ano_index][ano_files]:
         param_result_shapes[ ano_index ][ ano_files ].remove( ano_shapes )
      
      if ano_shapes not in param_result_shapes[ cur_index ][ ano_files ]:
         param_result_shapes[ cur_index ][ ano_files ].append( ano_shapes )
      

   for index, each_data in enumerate(param_result_shapes):
      each_data_cp = copy.deepcopy(each_data)
      for each_files in each_data_cp:
         if len( each_data[each_files] ) == 0:
            each_data.pop( each_files )
         
   # remove empty consecutives
   result_shapes_processed = [ temp_consec for temp_consec in param_result_shapes if len( temp_consec ) >= 1 ]   



   # [ [ delete index number, file number, shapes ], ... ]
   # [ [ 1, 25.26, ( '111', '222' ) ], ... ]
   delete_duplicate_shapes = set()
   done_indexes = set()
   for consec_index, consecutive in enumerate(result_shapes_processed):

      for each_files in consecutive:

         for ano_consec_index, ano_consecutive in enumerate(result_shapes_processed):
            if consec_index == ano_consec_index or ano_consec_index in done_indexes:
               continue

            if each_files in ano_consecutive.keys():

               for each_shapes in consecutive[each_files]:

                  if each_shapes in ano_consecutive[each_files]:
                     delete_duplicate_shapes.add( ( ano_consec_index, each_files, each_shapes ) )
   
      done_indexes.add( consec_index )


   for del_data in delete_duplicate_shapes:
      del_index = del_data[0]
      del_files = del_data[1]
      del_shapes = del_data[2]

      result_shapes_processed[ del_index ][ del_files ].remove( del_shapes )

   # remove empty files
   for consec_index, consecutive in enumerate(result_shapes_processed):
      consecutive_cp = copy.deepcopy( consecutive )
      for each_files in consecutive_cp:

         if len( consecutive[ each_files ] ) == 0:
            consecutive.pop( each_files )

   # remove empty consecutive
   result_shapes_processed = [ temp_consec for temp_consec in result_shapes_processed if len( temp_consec ) >= 1 ]     

   return result_shapes_processed



result_shapes = []
result_shapes2 = []
already_done = []

prev_file_shapes = None
prev_filename = None
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
for each_file in all_matches_so_far:
   print( each_file )
   
   cur_im1file = each_file.split(".")[0]
   cur_im2file = each_file.split(".")[1]

   if ref_imagefile_op is False:
      im1 = Image.open(top_images_dir + directory + cur_im1file + ".png" )
      im_size = im1.size
      im_width, im_height = im_size
      im1.close()
      
      ref_imagefile_op = True

  
   if prev_file_shapes is None:
      prev_file_shapes = all_matches_so_far[each_file]
      prev_filename = each_file
      
      prev_file_shapes2 = alrdy_matched_shapes[ each_file ]

   
   else:
      
      rest_of_files = get_rest_of_files( each_file )
   
      for each_shapes in all_matches_so_far[each_file]:
         skip = False
         for temp_shapes in result_shapes:
            # { files : { im1 shapes }, { im2shapes }, ... }
            if each_file in temp_shapes.keys() and each_shapes in temp_shapes[ each_file ]:
               skip = True
               break
         
         if skip is True:
            continue  
         
         found_shapes = [ temp_shapes for temp_shapes in prev_file_shapes if temp_shapes[1] == each_shapes[0] ]
         if len( found_shapes ) >= 1:
            # one to one match or combining type of match.
            
            cur_matches = {prev_filename: found_shapes}
            cur_matches[ each_file ] = [each_shapes]
            
            next_image2shape = each_shapes[1]
            
            # find current match's further consecutives.
            for next_file in rest_of_files:
               
               further_found_shapes = find_match_from_next_file( next_file, next_image2shape )
               if len(further_found_shapes) == 0:
                  break
               elif len( further_found_shapes ) >= 1:
                  
                  cur_matches[ next_file ] = further_found_shapes
                  next_image2shape = further_found_shapes[0][1]

         
            result_shapes.append( cur_matches )

      
      
      for each_shapes in alrdy_matched_shapes[ each_file ]:
         # [ { im1shapes }, { im2shapes } ]
         if ( each_shapes, each_file ) in already_done:
            continue         
         already_done.append( ( each_shapes, each_file ) )

         cur_im1shapes_pixels = set()
         for cur_im1shape in each_shapes[0]:
            cur_im1shapes_pixels |= all_files_im_shapes[ each_file ][0][ cur_im1shape ]
         
         for prev_each_shapes in prev_file_shapes2:
            if ( prev_each_shapes, prev_filename ) in already_done:
               continue

            prev_im2shapes_pixels = set()
            for prev_im2shape in prev_each_shapes[1]:
               prev_im2shapes_pixels |= all_files_im_shapes[ prev_filename ][1][ prev_im2shape ]
            
            common_pixels = cur_im1shapes_pixels.intersection( prev_im2shapes_pixels )
            if len( common_pixels ) / len( cur_im1shapes_pixels ) >= 0.55:
               # if prev_each_shapes[1] is a big shape that breaks up into smaller shapes then, there will be multiple of it as a result
               # in result_shapes2.
             
               cur_matches = { prev_filename: prev_each_shapes }

            else:
               cur_matches = {}
            
            cur_matches[ each_file ] = each_shapes
          
            cur_image2shapes = each_shapes[1] 
            cur_file = each_file        
               

            # find current match's further matches
            for next_file in rest_of_files:
               # if each_file is 2.3 then next_file is 3.4
                  
               further_found_shapes = find_match_from_next_file( next_file, cur_image2shapes, cur_file, already_done )
               if further_found_shapes is None:
                  break
               else:
                  cur_matches[ next_file ] = further_found_shapes
                  cur_image2shapes = further_found_shapes[1]
                  cur_file = next_file
                     
               
            result_shapes2.append( cur_matches )


      prev_file_shapes = all_matches_so_far[each_file]
      prev_filename = each_file
      
      prev_file_shapes2 = alrdy_matched_shapes[ each_file ]



result_shapes = remove_duplicate_shapes(result_shapes)


consecutives_ddir = top_shapes_dir + directory + "all_matches/consecutives/data/"
if os.path.exists(consecutives_ddir ) == False:
   os.makedirs(consecutives_ddir )

consecutives1_dfile = consecutives_ddir + "1to1.data"
with open(consecutives1_dfile, 'wb') as fp:
   pickle.dump(result_shapes, fp)
fp.close()

consecutives_multi_dfile = consecutives_ddir + "multi_shp_matches.data"
with open(consecutives_multi_dfile, 'wb') as fp:
   pickle.dump(result_shapes2, fp)
fp.close()

















