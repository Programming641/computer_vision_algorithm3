# move whole image pixels up right left ( but not rotation ) and see if shapes match between two frames of video

from PIL import Image
import pickle
import math
import shutil
import pathlib

import os, sys
from libraries.cv_globals import top_shapes_dir, top_images_dir, frth_smallest_pixc, spixc_shapes, internal
from libraries import read_files_functions, image_functions, pixel_shapes_functions, pixel_functions, btwn_frames_functions



directory = "videos/street3/resized/min"
im1file = "12"
im2file = "13"
shapes_type = "intnl_spixcShp"


if len(sys.argv) > 1:
   im1file = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   im2file = sys.argv[1][0: len( sys.argv[1] ) - 4 ]

   directory = sys.argv[3]

   print("execute script findim_pixch.py. file1 " + im1file + " file2 " + im2file + " directory " + directory )

# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

template_dir = top_shapes_dir + directory + "template/"
pixel_template_dir = template_dir + "pixels/"
pixel_template_ddir = pixel_template_dir + "data/"


# loop all "btwn_frames" files
data_dir = pathlib.Path(pixel_template_ddir)

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




all_matches = []

first_frame = True
prev_pixel_template = None
prev_im1shapeid = None
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

   
   with open (pixel_template_ddir + ordered_btwn_frames_file + ".data", 'rb') as fp:
      # [ [{'1400': 628.3199999999999, 'nbrs': ['1405', '11441'], 'im2pixels': ['424', '428', '6830'] }], ... ]
      # [ [ { image1shapeid: matched count, image1 neighbors: [ image1 neighbors ], im2pixels: [ matched image2 pixels ], ... ]
      pixel_template = pickle.load(fp)
   fp.close()
   

   if prev_pixel_template is None:
      prev_im1shapes = im1shapes
      prev_first_filenum = first_filenum
      prev_sec_filenum = second_filenum
      prev_pixel_template = pixel_template
   
   else:
      progress_counter = len( prev_pixel_template )
      # check if there is a match between prev_styLshapes_w_neighbors's image2 shapes and current styLshapes_w_neighbors's image2
      for each_prev_pixel_template in prev_pixel_template:
         print( str( progress_counter ) + " remaining")
         progress_counter -= 1
         
         #  each_prev_pixel_template ->  {'im1shapeid': '2577', 'match_count': 173.46, 'im1nbrs': ['2985'], 'im2pixels': [ 1789, 1790], 
         #                                'similar_im1shapes': [['2577', '2985'], {1783, 1791}, ['2577', '2985'], { 2173}]}
         # similar_im1shapes -> [ [ similar image1 shapes ], { image2 pixels that only exist in this one and not the im1shapeid's im2pixels }, ... ]

         prev_pix_tmpl_im1shapeid = each_prev_pixel_template["im1shapeid"]
       
         prev_pix_tmpl_im1shapes = [ prev_pix_tmpl_im1shapeid ]
         prev_pix_tmpl_im1shapes.extend( each_prev_pixel_template["im1nbrs"] )

         prev_pix_tmpl_im1pixels = set()
         for prev_pix_tmpl_im1shape in prev_pix_tmpl_im1shapes:
            prev_pix_tmpl_im1pixels |= set( prev_im1shapes[ prev_pix_tmpl_im1shape ] )

         for each_cur_pixel_template in pixel_template:
               cur_pix_tmpl_im1shapeid = each_cur_pixel_template["im1shapeid"]

               cur_pix_tmpl_im1shapes = [ cur_pix_tmpl_im1shapeid ]
               cur_pix_tmpl_im1shapes.extend( each_cur_pixel_template["im1nbrs"] )                  
                  
               # now that I have both prev_pix_tmpl_im1shapes and cur_pix_tmpl_im1shapes, see if they match
               cur_pix_tmpl_im1pixels = set()
               for cur_pix_tmpl_im1shape in cur_pix_tmpl_im1shapes:
                  cur_pix_tmpl_im1pixels |= set( im1shapes[ cur_pix_tmpl_im1shape ] )
                  
               found_pixels = prev_pix_tmpl_im1pixels.intersection( cur_pix_tmpl_im1pixels )
                  
               if len( found_pixels ) >= len( prev_pix_tmpl_im1pixels ) * 0.65 or len( found_pixels ) >= len( cur_pix_tmpl_im1pixels ) * 0.65:
                  #  match is found
                  cur_match = {"prevfile": prev_first_filenum + "." + prev_sec_filenum, "prev_shapeid": prev_pix_tmpl_im1shapeid, 
                               "prev_nbrs": each_prev_pixel_template["im1nbrs"], "prev_im2pixels": each_prev_pixel_template["im2pixels"],
                               "curfile": first_filenum + "." + second_filenum, "cur_shapeid": cur_pix_tmpl_im1shapeid, "cur_nbrs": each_cur_pixel_template["im1nbrs"],
                               "cur_im2pixels": each_cur_pixel_template["im2pixels"] }


                  all_matches.append( cur_match )


      prev_im1shapes = im1shapes
      prev_first_filenum = first_filenum
      prev_sec_filenum = second_filenum
      prev_pixel_template = pixel_template   



pixel_template_dfile = pixel_template_ddir + "among.data"
with open(pixel_template_dfile, 'wb') as fp:
   pickle.dump(all_matches, fp)
fp.close()























