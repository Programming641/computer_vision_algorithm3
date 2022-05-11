import re
import math
from PIL import Image
from libraries import read_files_functions, pixel_shapes_functions, pixel_functions
import os, sys
import pickle
import winsound

from libraries.cv_globals import proj_dir

shapes_dir = proj_dir + "/shapes/"
images_dir = proj_dir + "/images/"
temp_dir = proj_dir + "/temp/"


filename = "1clrgrp"

directory = "videos/cat"

# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'


original_image = Image.open(images_dir + directory + filename + ".png")

image_width, image_height = original_image.size

rpt_ptn_dir = shapes_dir + directory + "rpt_ptn/"

filepath = rpt_ptn_dir + filename + "_rpt_ptn_shapes.txt"

combi_rpt_ptn_txtfile = open(rpt_ptn_dir + filename + "_combi_rpt_ptn_shapes.txt" , "w" )
combi_rpt_ptn_datafile = rpt_ptn_dir + filename + "_combi_rpt_ptn_shapes.data"

# getting repeating pattern shapes
orig_rpt_ptn_shapes = read_files_functions.rd_ldict_k_v_l(filename, directory, filepath)


# we need to get every pixel of the shapes along with their colors
# return value form is
# {0: [{0: (102, 153, 153)}, {1: (102, 153, 153)}, {181: (102, 153, 153)} .... ], ..... }
# list includes shapeid's pixel as well
im_shapes_colors = pixel_shapes_functions.get_all_shapes_colors(filename, directory)


# this will store repeating pattern's shapeids along with their colors
# [ { rpt_ptn_shapeid: [ { shapeid: { color }, shapeid2: { color }, .... }, { shapeid3: { color }, shapeid4: { color } } }, { rpt_ptn_shapeid: .... } ]
rpt_ptn_shapes_wk = []

combi_rpt_ptn_shapes = []

combi_rpt_ptn_temp_file = temp_dir + directory.replace("/", ".") + filename + "_combi_rpt_ptn1.data"

rpt_ptn_shapes_w_clrs = []

debug = False


def classify_shape_colors( diff_colors, same_colors ):
   second_cur_diff_colors = {}
   first_diff_shapeid = first_diff_color = None
   
   # same_colors_counter points at the next list that not exist at this point.
   same_colors_counter = len(same_colors)
   for cur_diff_shapeid in diff_colors:
      # compare with first one with all others in the diff_colors
      if not first_diff_shapeid:
         first_diff_shapeid = cur_diff_shapeid
         first_diff_color = diff_colors[first_diff_shapeid]
         
         # if no shapes have same color as the first_diff_shapeid, then first_diff_shapeid will be only one in the list.
         same_colors.append( { first_diff_shapeid: first_diff_color } )
         
            
      else:
         clr_ch, brit_thres, brit_v = pixel_functions.compute_appearance_difference( first_diff_color, diff_colors[cur_diff_shapeid], 30 )
            
         if not clr_ch and brit_thres:
            
            
            # all current shapes will be put in the same color dictionary with first_diff_shapeid. so same_colors_counter will not change
            same_colors[same_colors_counter][cur_diff_shapeid] = diff_colors[cur_diff_shapeid]


         else:
                  
            # check if cur_diff_shapeid is not already in the same_colors
            cur_diff_found = False
            for cur_color in same_colors:
               if cur_diff_shapeid in cur_color:
                  cur_diff_found = True
                  
            if not cur_diff_found:
               second_cur_diff_colors[cur_diff_shapeid] = diff_colors[cur_diff_shapeid]



   if len(second_cur_diff_colors) >= 2:
      same_color_result = classify_shape_colors( second_cur_diff_colors, same_colors )
      

      
      return same_color_result
      
   elif len(second_cur_diff_colors) == 1:
      # last shape remains. this shape does not have same color with any of the shapes in its repeating pattern shape
      last_shapeid = list( second_cur_diff_colors.keys() )[0]
      
      same_colors.append( { last_shapeid: second_cur_diff_colors[last_shapeid] } )
      
      return same_colors

   else:

      return same_colors











# first, get color of shapes in repeating pattern.
if os.path.exists(combi_rpt_ptn_temp_file):
   with open (combi_rpt_ptn_temp_file, 'rb') as fp:
      rpt_ptn_shapes_w_clrs = pickle.load(fp)
else:
   for rpt_ptn_shape in orig_rpt_ptn_shapes:
      
      cur_rpt_ptn_shape = {}
      for rpt_ptn_shapeid, rpt_ptn_shapeids in rpt_ptn_shape.items():
         cur_rpt_ptn_shape[rpt_ptn_shapeid] = {}
         
         cur_shapes_counter = len( rpt_ptn_shapeids )
         for im_shapeid, im_s_color in im_shapes_colors.items():
         
            if im_shapeid in rpt_ptn_shapeids:      
               cur_rpt_ptn_shape[rpt_ptn_shapeid][im_shapeid] = im_s_color
      
               cur_shapes_counter -= 1
               
               if cur_shapes_counter == 0:
                  break
      
      
         # at the end of current repeating pattern shape
         rpt_ptn_shapes_w_clrs.append( cur_rpt_ptn_shape )
 

   with open(combi_rpt_ptn_temp_file, 'wb') as fp:
      pickle.dump(rpt_ptn_shapes_w_clrs, fp)
   fp.close() 


for rpt_ptn_shape in rpt_ptn_shapes_w_clrs:
   
   for rpt_ptn_shapeid, rpt_ptn_shapeids_w_color in rpt_ptn_shape.items():
      cur_rpt_ptn = { rpt_ptn_shapeid: [] }
      


      for shapeid, color in rpt_ptn_shapeids_w_color.items():

               
         cur_colors = [ { shapeid: color } ]
         cur_diff_colors = {}
         for ano_shapeid, ano_color in rpt_ptn_shapeids_w_color.items():
            if shapeid == ano_shapeid:
               # itself
               continue
               
            clr_ch, brit_thres, brit_v = pixel_functions.compute_appearance_difference( color,ano_color, 30 )
               
            if not clr_ch and brit_thres:
               cur_colors[0][ano_shapeid] =  ano_color
                  
            else:
               cur_diff_colors[ano_shapeid] = ano_color
         
         # first shape comparing with every other shape to get same color shapes and different color shapes.         
         break
      

      
      # at this point, all shapes are included in either cur_diff_colors or cur_colors
      same_colors = classify_shape_colors( cur_diff_colors, cur_colors )
      
      
      cur_rpt_ptn[rpt_ptn_shapeid] += same_colors
      

      rpt_ptn_shapes_wk.append( cur_rpt_ptn )




debug_counter = 2


debug_shapeids = [ "28029", "4831" ]

already_added_rpt_ptn = []
progress_counter = len( rpt_ptn_shapes_wk )
for rpt_ptn_shapes in rpt_ptn_shapes_wk:
   print(str( progress_counter ) + " remaining" )
   
   all_shapeids = set()
   matched_ano_rpt_ptn_shapeids = set()
   combined_rpt_ptn = []
   cur_rpt_ptn_shapeid = None
   for ano_rpt_ptn_shapes in rpt_ptn_shapes_wk:
      if rpt_ptn_shapes == ano_rpt_ptn_shapes or rpt_ptn_shapes in already_added_rpt_ptn:
         # itself
         continue
         
      
      for rpt_ptn_shapeid, rpt_ptn_colors in rpt_ptn_shapes.items():
         cur_rpt_ptn_shapeid = rpt_ptn_shapeid
         '''
         if rpt_ptn_shapeid == "4831" and "4831" in debug_shapeids and debug:
            print("4831 rpt_ptn_colors")
            print(str( rpt_ptn_colors ) )
            
            debug_shapeids.remove( "4831" )
            
            debug_counter -= 1
         
         if rpt_ptn_shapeid == "28029" and "28029" in debug_shapeids and debug:
            print("28029 rpt_ptn_colors")
            print( str( rpt_ptn_colors ) )
            
            debug_shapeids.remove( "28029" )
            
            debug_counter -= 1
            
         if rpt_ptn_shapeid != "4831" and rpt_ptn_shapeid != "28029" and debug:
            continue

         if debug_counter == 0 and debug:
            sys.exit()
         '''

         required_match_count = len( rpt_ptn_colors ) 
         
         cur_rpt_ptn_match = False
         for rpt_ptn_color in rpt_ptn_colors:
            # get first color as representive of all shapes that have this same color. 
            # rpt_ptn_colors is a list that contains all colors
            representive_shapeid = list(rpt_ptn_color.keys())[0]
            representive_color = rpt_ptn_color[representive_shapeid]
            
            
            cur_rpt_ptn_color_matched = False
            for ano_rpt_ptn_shapeid, ano_rpt_ptn_colors in ano_rpt_ptn_shapes.items():

               for ano_rpt_ptn_color in ano_rpt_ptn_colors:
                  ano_representive_shapeid = list(ano_rpt_ptn_color.keys())[0]
                  ano_representive_color = ano_rpt_ptn_color[ano_representive_shapeid]

   
                  clr_ch, brit_thres, brit_v = pixel_functions.compute_appearance_difference( representive_color, ano_representive_color, 30 )
                 
                  if not clr_ch and brit_thres:
                     required_match_count -= 1
                     cur_rpt_ptn_color_matched = True
                     
   
                     if required_match_count == 0:
                        cur_rpt_ptn_match = True
                        
                     
                        break
               
               
               
               if cur_rpt_ptn_match or cur_rpt_ptn_color_matched:
                  break
                  
            if cur_rpt_ptn_match:
               break

                  
         if cur_rpt_ptn_match:
            # combine rpt_ptn_shapes and ano_rpt_ptn_shapes

            
            already_added_rpt_ptn.append( ano_rpt_ptn_shapes )

            ano_rpt_ptn_shapeid = None
            cur_rpt_ptn_shapeids = set()
            ano_all_rpt_ptn_shapeids = set()

            for shapeids_w_clr in rpt_ptn_colors:

               cur_rpt_ptn_shapeids = set( shapeids_w_clr.keys() )
               
               
               
            for ano_rpt_ptn_shapeid, ano_shapeid_w_clrs_list in ano_rpt_ptn_shapes.items():
               ano_rpt_ptn_shapeid = ano_rpt_ptn_shapeid
               for ano_shapeid_w_clrs in ano_shapeid_w_clrs_list:
                  ano_all_rpt_ptn_shapeids =  set( ano_shapeid_w_clrs.keys() )
                  
               break

            temp = cur_rpt_ptn_shapeids | ano_all_rpt_ptn_shapeids
            temp.add( ano_rpt_ptn_shapeid )
            all_shapeids.update( temp )
            
            matched_ano_rpt_ptn_shapeids.add( ano_rpt_ptn_shapeid )

   if cur_rpt_ptn_shapeid and matched_ano_rpt_ptn_shapeids:
      all_shapeids.add( cur_rpt_ptn_shapeid )
      combined_rpt_ptn.append( all_shapeids )  
      combined_rpt_ptn.append( { "shapeid1": cur_rpt_ptn_shapeid , "shapeid2": matched_ano_rpt_ptn_shapeids } )
   
      combi_rpt_ptn_shapes.append( combined_rpt_ptn )


   progress_counter -= 1

    
combi_rpt_ptn_txtfile.write(str( combi_rpt_ptn_shapes ) )
combi_rpt_ptn_txtfile.close()

with open(combi_rpt_ptn_datafile, 'wb') as fp:
   pickle.dump(combi_rpt_ptn_shapes, fp)
fp.close() 


frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)     



















