# find_stayedLshape_nbrs_among_frames makes match if pixels match more than 60 something percent. this takes only highest match.
import tkinter
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions, same_shapes_btwn_frames, read_files_functions, image_functions, pixel_functions, btwn_frames_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir, styLshapes_w_nbrs, internal
import pickle
import winsound
import sys, os
import pathlib

###########################                    user input begin                ##################################
directory = "videos/street3/resized/min"
shapes_type = "intnl_spixcShp"
###########################                    user input end                  ##################################


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

styLshapes_w_neighbors_Ddir = top_shapes_dir + directory + styLshapes_w_nbrs + "/" + shapes_type + "/data/"

 

# loop all "btwn_frames" files
data_dir = pathlib.Path(styLshapes_w_neighbors_Ddir)

btwn_frames_files = []
for data_file in data_dir.iterdir():
   data_filename = os.path.basename(data_file)
   # filename without last comma ( which should be extension )
   data_filename = os.path.splitext(data_filename)[0]
   # check if file has the following form
   # number.number
   if data_filename.count(".") == 1:
      first_num_lastindex = data_filename.find(".")
      if data_filename[0: first_num_lastindex].isnumeric() and data_filename[first_num_lastindex + 1: len( data_filename )].isnumeric():
         # current file is "btwn_frames" file
         btwn_frames_files.append( data_filename )
  

# now that I have all the "btwn_frames" files, I need to put them in order.
# the order is that the small number file comes first.
# example. 10.11 -> 11.12 -> 12.13 ...
# if there are multiple same numbers before the comma, then the smallest second number after the comma should come first
# example. 10.11 -> 10.12 -> 10.13 ...
ordered_btwn_frames_files = btwn_frames_functions.put_btwn_frames_files_in_order( btwn_frames_files )

print("now begins the main processing...")

# [ [ 10.11&11.12_p11.12&12.13 ... , 455, 336 ], ... ]
# [ [ previous image1file number.previous image2 file number&current image1file number.current image2file number, previous shapeid, current shapeid ], ... ]
shapes_among_frames = []
first_frame = True
prev_styLshapes_w_neighbors = None
prev_im2shapes = None
for ordered_btwn_frames_file in ordered_btwn_frames_files:
   print("current files " + ordered_btwn_frames_file )
   
   first_num_lastindex = ordered_btwn_frames_file.find(".")
   first_filenum = ordered_btwn_frames_file[0: first_num_lastindex] 
   second_filenum = ordered_btwn_frames_file[first_num_lastindex + 1: len( ordered_btwn_frames_file )] 

   if shapes_type == "normal":
      # returned value has below form
      # shapes[shapes_id][pixel_index] = {}
      # shapes[shapes_id][pixel_index]['x'] = x
      # shapes[shapes_id][pixel_index]['y'] = y
      im1shapes = read_files_functions.rd_shapes_file(first_filenum, directory)
      im2shapes = read_files_functions.rd_shapes_file(second_filenum, directory)   
   
      for im1shapeid in im1shapes:
         im1shapes[im1shapeid] = list( im1shapes[im1shapeid].keys() )
      for im2shapeid in im2shapes:
         im2shapes[im2shapeid] = list( im2shapes[im2shapeid].keys() )
   
   elif shapes_type == "intnl_spixcShp":
      s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"
      shapes_dir = s_pixcShp_intnl_dir + "shapes/"

      shapes_dfile = shapes_dir + first_filenum + "shapes.data"
      im2shapes_dfile = shapes_dir + second_filenum + "shapes.data"

      with open (shapes_dfile, 'rb') as fp:
         # { '79999': ['79999', ... ], ... }
         # { 'shapeid': [ pixel indexes ], ... }
         im1shapes = pickle.load(fp)
      fp.close()

      with open (im2shapes_dfile, 'rb') as fp:
         # { '79999': ['79999', ... ], ... }
         # { 'shapeid': [ pixel indexes ], ... }
         im2shapes = pickle.load(fp)
      fp.close()  




   
   with open (styLshapes_w_neighbors_Ddir + ordered_btwn_frames_file + ".data", 'rb') as fp:
      # {'2072.1': [['2072', '2874'], ['53280', '57316']], ... }
      # { image1 shapeid: [ list of all neighbors put together ], ... }
      styLshapes_w_neighbors = pickle.load(fp)
   fp.close()
   
   if prev_styLshapes_w_neighbors is None:
      prev_im2shapes = im2shapes
      prev_first_filenum = first_filenum
      prev_sec_filenum = second_filenum
      prev_styLshapes_w_neighbors = styLshapes_w_neighbors
   
   else:
      # check if there is a match between prev_styLshapes_w_neighbors's image2 shapes and current styLshapes_w_neighbors's image2
      for prev_shapeid in prev_styLshapes_w_neighbors:
         # prev_shapeid -> 2072.1
         # prev_styLshapes_w_neighbors[prev_shapeid] -> [['2072', '2874'], ['53280', '57316']]
         
         prev_cur_im2shapes = []
         for prev_shapes in prev_styLshapes_w_neighbors[prev_shapeid]:
            prev_cur_im2shapes.append( prev_shapes[1] )
         
         # get previous shapes image indexes
         prev_cur_im2pixels = set()
         for prev_cur_im2shape in prev_cur_im2shapes:
            prev_cur_im2pixels |= set( prev_im2shapes[prev_cur_im2shape] )
         
         # highest matched shapeid, match count
         prev_im2match = []
         cur_im2match = []
         # check all current shapeids with previous shapeids
         for cur_shapeid in styLshapes_w_neighbors:
            cur_im2shapes = []
            for cur_shapes in styLshapes_w_neighbors[cur_shapeid]:
               cur_im2shapes.append( cur_shapes[1] )
            
            # get current image2 shapes image indexes
            cur_im2pixels = set()
            for cur_im2shape in cur_im2shapes:
               cur_im2pixels |= set( im2shapes[ cur_im2shape ] )
            
            # now that I have both prev_cur_im2pixels and cur_im2pixels, check if they are the match
            found_pixels = prev_cur_im2pixels.intersection( cur_im2pixels )
            
            # find one that matches the most
            if len( found_pixels ) >= len( prev_cur_im2pixels ) * 0.65:
               # passed minimum match check. check if it is highest match
               if len( prev_im2match ) == 0:
                  prev_im2match.append( cur_shapeid )
                  prev_im2match.append( len( found_pixels ) / len( prev_cur_im2pixels ) )
                  
               elif prev_im2match[1] < len( found_pixels ) / len( prev_cur_im2pixels ):
                  # bigger match is found, so clear prev_im2match
                  prev_im2match = []
                  prev_im2match.append( cur_shapeid )
                  prev_im2match.append( len( found_pixels ) / len( prev_cur_im2pixels ) )
                  
               elif prev_im2match[1] == len( found_pixels ) / len( prev_cur_im2pixels ):
                  # same match count. so just add current match
                  prev_im2match_index = len( prev_im2match )
                  prev_im2match.append( cur_shapeid )
                  
            
            
            if len( found_pixels ) >= len( cur_im2pixels ) * 0.65:
               # passed minimum match check. check if it is highest match
               if len( cur_im2match ) == 0:
                  cur_im2match.append( cur_shapeid )
                  cur_im2match.append( len( found_pixels ) / len( prev_cur_im2pixels ) )
                  
               elif cur_im2match[1] < len( found_pixels ) / len( prev_cur_im2pixels ):
                  # bigger match is found, so clear cur_im2match
                  cur_im2match = []
                  cur_im2match.append( cur_shapeid )
                  cur_im2match.append( len( found_pixels ) / len( prev_cur_im2pixels ) )
                  
               elif cur_im2match[1] == len( found_pixels ) / len( prev_cur_im2pixels ):
                  # same match count. so just add current match
                  cur_im2match.append( cur_shapeid )             
               
               
         if len( prev_im2match ) >= 1 or len( cur_im2match ) >= 1:
            # match is found
            # check if previous shapeid is present in shapes_among_frames
            found_in_shp_amng_frm = False
            for lindex, each_shapes_among_frames in enumerate( shapes_among_frames ):
               # each_shapes_among_frames -> ['10.11&11.12', '2072.1', '4497.1']
               if prev_shapeid == each_shapes_among_frames[1]:
                  # previous shapeid is found, so add it to this list
                  found_in_shp_amng_frm = True
                  
                  # if there is exact same one, then skip it
                  skip = False
                  file_nums = each_shapes_among_frames[0].split("_")
                  for fileindex, each_filenums in enumerate(file_nums):
                     cur_file_shape_num = fileindex + fileindex + 1
                     if each_filenums == prev_first_filenum + "." + prev_sec_filenum + "&" + first_filenum + "." + second_filenum :
                        if each_shapes_among_frames[ cur_file_shape_num ] == prev_shapeid and each_shapes_among_frames[ cur_file_shape_num + 1 ] == cur_shapeid:
                           # image file pair and shape pair are exact same one found. skip it
                           skip = True
                           break                  
                  
                  
                  
                  if skip is False:
                     for each_prev_im2match in prev_im2match:
                        if isinstance( each_prev_im2match, str ):
                           # if it is a string, it is shapeid, if it is not, it is a match count
                           frames_name = each_shapes_among_frames[0] + "_" + prev_first_filenum + "." + prev_sec_filenum + "&" + first_filenum + "." + second_filenum
                           shapes_among_frames[lindex][0] = frames_name
                           shapes_among_frames[lindex].append( prev_shapeid )
                           shapes_among_frames[lindex].append( each_prev_im2match )

                     for each_cur_im2match in cur_im2match:
                        if isinstance( each_cur_im2match, str ):
                           # if it is a string, it is shapeid, if it is not, it is a match count
                           frames_name = each_shapes_among_frames[0] + "_" + prev_first_filenum + "." + prev_sec_filenum + "&" + first_filenum + "." + second_filenum
                           shapes_among_frames[lindex][0] = frames_name
                           shapes_among_frames[lindex].append( prev_shapeid )
                           shapes_among_frames[lindex].append( each_cur_im2match )                     
            
            if found_in_shp_amng_frm is False:
               for each_prev_im2match in prev_im2match:
                  if isinstance( each_prev_im2match, str ):
                     # if it is a string, it is shapeid, if it is not, it is a match count           
                     # cur_match ->  [ 10.11&11.12, 455.1, 336.2 ]
                     cur_match = []
                     cur_match.append( prev_first_filenum + "." + prev_sec_filenum + "&" + first_filenum + "." + second_filenum )
                     cur_match.append( prev_shapeid )
                     cur_match.append( each_prev_im2match )
               
                     shapes_among_frames.append( cur_match )

               for each_cur_im2match in cur_im2match:
                  if isinstance( each_cur_im2match, str ):
                     # if it is a string, it is shapeid, if it is not, it is a match count           
                     # cur_match ->  [ 10.11&11.12, 455.1, 336.2 ]
                     cur_match = []
                     cur_match.append( prev_first_filenum + "." + prev_sec_filenum + "&" + first_filenum + "." + second_filenum )
                     cur_match.append( prev_shapeid )
                     cur_match.append( each_cur_im2match )
               
                     shapes_among_frames.append( cur_match )

        
         
      prev_im2shapes = im2shapes
      prev_first_filenum = first_filenum
      prev_sec_filenum = second_filenum
      prev_styLshapes_w_neighbors = styLshapes_w_neighbors      
               
'''        
shapes_among_frames analysis
one data example....  ['10.11&11.12_10.11&11.12_11.12&12.13_11.12&12.13_11.12&12.13, '35536.1', '30214.1', '35536.1', '32600.1', '35536.1', '35536.1', '35536.1', '37380.1', '35536.1', '39000.1']

10.11&11.12
'35536.1', '30214.1'
image11 shapes that belong to '35536.1' matched with image12 shapes that belong to '30214.1'
Also image11 shapeid '35536.1' is matched with image10 '35536.1'.
Likewise, image12 shapeid '30214.1' is matced with image11 '30214.1'

image11 '35536.1' matchd with image12 '30214.1'
image11 '35536.1' matched with image10 '35536.1'
image12 '30214.1' matched with image11 '30214.1'

image11 '35536.1' may match image11 '30214.1'
image12 '30214.1' may match image10 '35536.1'


11.12&12.13
'35536.1', '35536.1'
image12 shapes that belong to '35536.1' matched with image13 shapes that belong to '35536.1'
Also image12 shapeid '35536.1' is matched with image11 shapeid '35536.1'
Likewise, image13 shapeid '35536.1' is matched with image12 shapeid '35536.1'

image12 '35536.1' matched with image13 '35536.1'
image12 '35536.1' matched with image11 '35536.1'
image13 '35536.1' matched with image12 '35536.1'

image13 '35536.1' may match with image11 '35536.1'

'''



styLshapes_w_neighbors_dfile = styLshapes_w_neighbors_Ddir + "among2.data"
with open(styLshapes_w_neighbors_dfile, 'wb') as fp:
   pickle.dump(shapes_among_frames, fp)
fp.close()




















