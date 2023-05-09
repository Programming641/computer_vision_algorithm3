
from PIL import Image
import pickle
import math
import copy
import os, sys
from libraries.cv_globals import top_temp_dir, top_shapes_dir, top_images_dir, internal, pixch_sty_dir, scnd_stage_alg_dir, snd_stg_alg_shp_nbrs_dir
from libraries.cv_globals import frth_smallest_pixc, Lshape_size, third_smallest_pixc
from libraries import read_files_functions, pixel_shapes_functions, image_functions, pixel_functions, same_shapes_functions
import winsound


directory = "videos/street3/resized/min"
im1file = "11"
im2file = "12"
shapes_type = "intnl_spixcShp"


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'


pixch_dir = top_shapes_dir + directory + pixch_sty_dir + "/"
pixch_sty_dfile = pixch_dir + "confirmed.data"
with open (pixch_sty_dfile, 'rb') as fp:
   # [[('10.11_11.12', ('49469', '50270')), ('10.11_11.12', ('50270', '55045')), ('11.12_12.13', ('55045', '50670')), ('12.13_13.14', ('50670', '51070'))], ... ]
   # [ [ (( filenames, ( image10 shapeid, image 11 shapeid )), ( filenames , ( image11 shapeid, image12 shapeid ) ), ... ], ... ]
   pixch_stayed_shapes = pickle.load(fp)
fp.close()

scnd_stg_alg_shp_nbrs_dir = top_shapes_dir + directory + snd_stg_alg_shp_nbrs_dir + "/"
with open(scnd_stg_alg_shp_nbrs_dir + im1file + "." + im2file + "." + im1file + ".data",  'rb') as fp:
   # [[['2072', '867', '1669', '2080', '53280'], ['1236', '8439', '13231', '44819', '57316']], ... ]
   # [ [ [ image1 shapeids ], [ image2 shapeids ] ], ... ]
   shapes_neighbors_matches = pickle.load(fp)
fp.close()

shape_neighbors_delete_matches = []
for lindex, shapes_neighbors_match in enumerate(shapes_neighbors_matches):
   # shapes_neighbors_match -> [['2072', '867', '1669', '2080', '53280'], ['1236', '8439', '13231', '44819', '57316']]
   
   
   found = False
   for each_pixch_stayed_shapes in pixch_stayed_shapes:
      # each_pixch_stayed_shapes -> [('10.11_11.12', ('49469', '50270')), ('10.11_11.12', ('50270', '55045')), 
      #                                               image10   image11                    image11  image12 
      #                              ('11.12_12.13', ('55045', '50670')), ('12.13_13.14', ('50670', '51070'))]
      #                                               image12  image13                     image13  image14
      
      # check if first and second filenames are the same. 
      first_scnd_files_are_same = False
      if each_pixch_stayed_shapes[0][0] == each_pixch_stayed_shapes[1][0]:
         first_scnd_files_are_same = True
      

      for each_files_match in each_pixch_stayed_shapes:
         
         two_pairs_of_files = each_files_match[0].split("_")
         
         filename1 = two_pairs_of_files[0].split(".")[0]
         filename2 = two_pairs_of_files[0].split(".")[1]
         
         filename3 = two_pairs_of_files[1].split(".")[0]
         filename4 = two_pairs_of_files[1].split(".")[1]
         
         if ( im1file == filename1 and im2file == filename2 and first_scnd_files_are_same is True ) or ( im1file == filename3 and 
            im2file == filename4 and first_scnd_files_are_same is False ):
            # found the files pair match
            im1shapeid = each_files_match[1][0]
            im2shapeid = each_files_match[1][1]
            
            if im1shapeid in shapes_neighbors_match[0]:
               if not im2shapeid in shapes_neighbors_match[1]:
                  # image1 shapeid is found in current shapes_neighbors_match but not im2shapeid
                  shape_neighbors_delete_matches.append( lindex )
               else:
                  # image1 and image2 shapes are both found
                  # delete current lindex from shape_neighbors_delete_matches
                  list(filter((lindex).__ne__, shape_neighbors_delete_matches))
                  
                  found = True
                  break
                  
               
            else:
               if im2shapeid in shapes_neighbors_match[1]:
                  # image1 shapeid is not found but im2shapeid is found
                  shape_neighbors_delete_matches.append( lindex )
            
         
         elif im1file == filename3 and im2file == filename4 and first_scnd_files_are_same is True:
            # found the files pair match         
            im1shapeid = each_files_match[1][0]
            im2shapeid = each_files_match[1][1]
            
            
            if im1shapeid in shapes_neighbors_match[0]:
               if not im2shapeid in shapes_neighbors_match[1]:
                  # image1 shapeid is found in current shapes_neighbors_match but not im2shapeid
                  shape_neighbors_delete_matches.append( lindex )
               else:
                  # image1 and image2 shapes are both found
                  list(filter((lindex).__ne__, shape_neighbors_delete_matches))
                  
                  found = True
                  break                                 
               
            else:
               if im2shapeid in shapes_neighbors_match[1]:
                  # image1 shapeid is not found but im2shapeid is found
                  shape_neighbors_delete_matches.append( lindex )            

         
      if found is True:
         break      

deleted = 0
for delete_by_index in shape_neighbors_delete_matches:
   shapes_neighbors_matches.pop( delete_by_index - deleted )
   
   deleted += 1

      
   
with open(scnd_stg_alg_shp_nbrs_dir + im1file + "." + im2file + ".data", 'wb') as fp:
   pickle.dump(shapes_neighbors_matches, fp)
fp.close()



frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)





















