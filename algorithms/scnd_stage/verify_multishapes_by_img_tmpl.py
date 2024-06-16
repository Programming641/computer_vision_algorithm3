import tkinter
from PIL import ImageTk, Image
from libraries import btwn_amng_files_functions, pixel_shapes_functions, same_shapes_functions, pixel_functions, image_functions
from libraries import shapes_results_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files
import pickle
import sys, pathlib, os


directory = "videos/street3/resized/min1"

if len( sys.argv ) >= 2:
   directory = sys.argv[1]



# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

   
across_all_files_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/data/"
across_all_files_dfile = across_all_files_ddir + "all_files.data"
with open (across_all_files_dfile, 'rb') as fp:
   # {'10.11': {('79935', '58671'), ('39441', '39842'), ('45331', '36516')}, '11.12': {('39842', '40243'), ('26336', '27137'), ... }, ... }
   acrs_all_files_shapes = pickle.load(fp)
fp.close()


all_matches_so_far_dfile = across_all_files_ddir + "all_matches.data"
if os.path.exists( all_matches_so_far_dfile ):
   with open (all_matches_so_far_dfile, 'rb') as fp:
      # {'25.26': {('48744', '79999'), ('52180', '50181'), ... }, ... }
      all_matches_so_far = pickle.load(fp)
   fp.close()

else:
   all_matches_so_far = acrs_all_files_shapes


image_template_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/image_template/data/"
image_template_shapes_dfile = image_template_ddir + "multi1.data"  
with open (image_template_shapes_dfile, 'rb') as fp:
   image_template_shapes = pickle.load(fp)
fp.close()

shapes_dir = top_shapes_dir + directory  + "shapes/"


result_shapes = {}

prev_file_shapes = None
prev_filename = None
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
for each_file in image_template_shapes:
   print( each_file )
   
   cur_im1file = each_file.split(".")[0]
   cur_im2file = each_file.split(".")[1]
   
   result_shapes[each_file] = []

   if ref_imagefile_op is False:
      im1 = Image.open(top_images_dir + directory + cur_im1file + ".png" )

      im_size = im1.size
      im_width, im_height = im_size
      
      ref_imagefile_op = True

   shapes_dfile = shapes_dir + cur_im1file + "shapes.data"
   im2shapes_dfile = shapes_dir + cur_im2file + "shapes.data"

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

   im1shape_neighbors_file = shapes_dir + "shape_nbrs/" + cur_im1file + "_shape_nbrs.data"
   im2shape_neighbors_file = shapes_dir + "shape_nbrs/" + cur_im2file + "_shape_nbrs.data"

   with open (im1shape_neighbors_file, 'rb') as fp:
      im1shapes_neighbors = pickle.load(fp)
   fp.close()

   with open (im2shape_neighbors_file, 'rb') as fp:
      im2shapes_neighbors = pickle.load(fp)
   fp.close()

   all_m_so_f_by_im1shp = {}
   all_m_so_f_by_im2shp = {}
   all_matches_so_far_l = list( all_matches_so_far[each_file] )
   for index, each_shapes in enumerate( all_matches_so_far_l ):
      all_m_so_f_by_im1shp[ each_shapes[0] ] = index
      all_m_so_f_by_im2shp[ each_shapes[1] ] = index


   for each_shapes in image_template_shapes[ each_file ]:
      # each_shapes -> [['5179', '13980'], {'7576', '1176', '3176'}]
      
      total_counts = 0
      matched_counts = 0
      for matched_im1shape in each_shapes[0]:
         
         for im1nbr in im1shapes_neighbors[ matched_im1shape ]:
            
            matched_nbr_im2shapes = [ temp_shapes[1] for temp_shapes in all_matches_so_far[ each_file ] if temp_shapes[0] == im1nbr ]
            
            if len( matched_nbr_im2shapes ) >= 1:

               cur_matched = False
               total_counts += 1
               for matched_im2shape in each_shapes[1]:
                  
                  for im2nbr in im2shapes_neighbors[ matched_im2shape ]:
                     
                     if im2nbr in matched_nbr_im2shapes:
                        cur_matched = True
                        matched_counts += 1
                        break
                  if cur_matched is True:
                     break         


      if matched_counts >= 1 and matched_counts / total_counts >= 0.6:
      
         # check if each_shapes are in conflict with all_matches_so_far. 
         # one of the image1 shape from each_shapes is also in all_matches_so_far
         # this image1 shape's matched image2 shape from all_matches_so_far is not in each_shapes
         # this image2 shape is large part of the whole image2 shapes. then each_shapes is judged to be not a match.
         # 
         # example.
         # each_shapes -> [['5179', '13980'], {'7576', '1176', '3176'}]
         # matched image pair from all_matches_so_far ( '13980', '55' )
         # matched image2 shape '55' is not in each_shapes. and is a large part of the whole image2 shapes of each_shapes
         # so it is not a match
         
         all_im1shapes_len = 0
         conflict_im1shapes_len = 0
         for im1shapeid in each_shapes[0]:
            all_im1shapes_len += len( im1shapes[im1shapeid] )
            
            if im1shapeid in all_m_so_f_by_im1shp.keys():
               index = all_m_so_f_by_im1shp[im1shapeid]
               cur_pair = all_matches_so_far_l[index]
               
               if cur_pair[1] not in each_shapes[1]:
                  conflict_im1shapes_len += len( im1shapes[im1shapeid] )
            
         if conflict_im1shapes_len > 0 and all_im1shapes_len * 0.5 < conflict_im1shapes_len:
            continue


         all_im2shapes_len = 0
         conflict_im2shapes_len = 0
         for im2shapeid in each_shapes[1]:
            all_im2shapes_len += len( im2shapes[im2shapeid] )
            
            if im2shapeid in all_m_so_f_by_im2shp.keys():
               index = all_m_so_f_by_im2shp[im2shapeid]
               cur_pair = all_matches_so_far_l[index]
               
               if cur_pair[0] not in each_shapes[0]:
                  conflict_im2shapes_len += len( im2shapes[im2shapeid] )
            
         if conflict_im2shapes_len > 0 and all_im2shapes_len * 0.5 < conflict_im2shapes_len:
            continue        
      
         if each_shapes not in result_shapes[ each_file ]:
            result_shapes[each_file].append( each_shapes )
      






verified_shapes_dfile = image_template_ddir + "verified_multi1.data"  
with open(verified_shapes_dfile, 'wb') as fp:
   pickle.dump(result_shapes, fp)
fp.close()


















