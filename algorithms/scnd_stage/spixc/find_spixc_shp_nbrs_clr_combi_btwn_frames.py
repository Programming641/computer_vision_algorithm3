# find small pixel count shapes neighbors color combinations between frames.
from libraries import pixel_shapes_functions, read_files_functions, pixel_functions

from PIL import Image
import os, sys
import pickle
import copy

from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir


im1fname = "24"
im2fname = "25"

directory = "videos/giraffe/min"


recreate_images = False

if len(sys.argv) > 1:
   image_filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]

   directory = sys.argv[1]

   print("execute script find_same_clr_shapes.py. filename " + image_filename + " directory " + directory )

if directory != "" and directory[-1] != '/':
   directory +='/'

shapes_dir = top_shapes_dir + directory + "s_pixc_shapes/"
s_pixc_shapes_nbrs_dir = shapes_dir + "nbrs/"
s_pixc_shapes_nbrs_data_dir = s_pixc_shapes_nbrs_dir + "data/"
s_pixc_shapes_nbrs_dfile1 = s_pixc_shapes_nbrs_data_dir + im1fname + ".data"
s_pixc_shapes_nbrs_dfile2 = s_pixc_shapes_nbrs_data_dir + im2fname + ".data"


with open (s_pixc_shapes_nbrs_dfile1, 'rb') as fp:
   # [{'213': ['638', '641', '1066'], 'nbr_nbrs': ['215', '641', '1066', '1070', '635',... ]}, ... ]
   s_pixc_shape_nbrs4im1 = pickle.load(fp)
fp.close()

with open (s_pixc_shapes_nbrs_dfile2, 'rb') as fp:
   # [{'213': ['638', '641', '1066'], 'nbr_nbrs': ['215', '641', '1066', '1070', '635',... ]}, ... ]
   s_pixc_shape_nbrs4im2 = pickle.load(fp)
fp.close()

# shapes_colors[shape_id] = { 'r': r, 'g': g, 'b': b }
im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im1fname, directory)
im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im2fname, directory)


# getting shape image locations
im1shape_locations_path = top_shapes_dir + directory + "locations/" + im1fname + "_loc.txt"
im2shape_locations_path = top_shapes_dir + directory + "locations/" + im2fname + "_loc.txt"

im1s_locations = read_files_functions.rd_ldict_k_v_l( im1fname, directory, im1shape_locations_path )
im2s_locations = read_files_functions.rd_ldict_k_v_l( im2fname, directory, im2shape_locations_path )

im1shape_locations_list = []
for cur_s_pixc_shape in s_pixc_shape_nbrs4im1:
   cur_shapeids_list = []
   for shapeids in cur_s_pixc_shape.values():
      cur_shapeids_list.extend( shapeids )
      

   # removing duplicates
   cur_shapeids_list = list(dict.fromkeys(cur_shapeids_list))   
   
   im1shape_locations = set()
   for shapeid in cur_shapeids_list:
   
      for s_locs in im1s_locations:
         if shapeid in s_locs.keys():
            for s_loc in s_locs[ list(s_locs.keys())[0] ]:
               im1shape_locations.add( s_loc ) 


   im1shape_locations_list.append( im1shape_locations )


im2shape_locations_list = []
for cur_s_pixc_shape in s_pixc_shape_nbrs4im2:
   cur_shapeids_list = []
   for shapeids in cur_s_pixc_shape.values():
      cur_shapeids_list.extend( shapeids )
      

   # removing duplicates
   cur_shapeids_list = list(dict.fromkeys(cur_shapeids_list))   
      
   im2shape_locations = set()
   for shapeid in cur_shapeids_list:   
   
      for s_locs in im2s_locations:
         if shapeid in s_locs.keys():
            for s_loc in s_locs[ list(s_locs.keys())[0] ]:
               im2shape_locations.add( s_loc ) 
            

   im2shape_locations_list.append( im2shape_locations )



matches = []
progress_counter = len( s_pixc_shape_nbrs4im1 )
for cur_im1_index, s_nbrs4im1 in enumerate(s_pixc_shape_nbrs4im1):
   print( str( progress_counter ) + " remaining" )
   progress_counter -= 1
   
   cur_im1_shapeid = None
   # put together all shapes in one list
   s_nbrs_list4im1 = []
   
   for s_nbr in s_nbrs4im1:
      # get shapeid first
      if s_nbr != "nbr_nbrs":
         s_nbrs_list4im1.append( s_nbr )
         cur_im1_shapeid = s_nbr
      
      # get both shapeid key's list and "nbr_nbrs" key's list
      s_nbrs_list4im1.extend( s_nbrs4im1[s_nbr] )
   
   # last, removing duplicates
   s_nbrs_list4im1 = list(dict.fromkeys(s_nbrs_list4im1))


   # getting colors for current image1 shapes
   cur_im1_colors = []
   duplicate_colors = []
   for cur_im1shapeid in s_nbrs_list4im1:
      if im1shapes_colors[cur_im1shapeid] in duplicate_colors:
         continue
      
      cur_im1_colors.append( im1shapes_colors[cur_im1shapeid] )
      
      duplicate_colors.append( im1shapes_colors[cur_im1shapeid] )
   


   # getting image locations for current image1 shapes
   cur_im1_locations = im1shape_locations_list[cur_im1_index]



   for cur_im2_index, s_nbrs4im2 in enumerate(s_pixc_shape_nbrs4im2):
      cur_im2_shapeid = None

      # put together all shapes in one list
      s_nbrs_list4im2 = []
      for s_nbr in s_nbrs4im2:
         # get shapeid first
         if s_nbr != "nbr_nbrs":
            s_nbrs_list4im2.append( s_nbr )
            cur_im2_shapeid = s_nbr
      
         # get both shapeid key's list and "nbr_nbrs" key's list
         s_nbrs_list4im2.extend( s_nbrs4im2[s_nbr] )
   
      # last, removing duplicates
      s_nbrs_list4im2 = list(dict.fromkeys(s_nbrs_list4im2))
   

      cur_im2_colors = []
      duplicate_colors = []
      for cur_im2shapeid in s_nbrs_list4im2:
         if im2shapes_colors[cur_im2shapeid] in duplicate_colors:
            continue
      
         cur_im2_colors.append( im2shapes_colors[cur_im2shapeid] )
      
         duplicate_colors.append( im2shapes_colors[cur_im2shapeid] )


      # checking if current image1 shapes colors match with current image2 shapes colors
      # first, check if numbers of colors match
      # actually, if I check numbers of colors then, shapes with many pixels should have more weight than shapes with little pixels
      # so I'm going to comment out this for now
      
      cur_im1_clr_num = len( cur_im1_colors )
      cur_im2_clr_num = len( cur_im2_colors )
      
      
      bigger_clr_num = None
      smaller_clr_num = None
      if cur_im1_clr_num >= cur_im2_clr_num:
         bigger_clr_num = cur_im1_clr_num
         smaller_clr_num = cur_im2_clr_num
      else:
         bigger_clr_num = cur_im2_clr_num
         smaller_clr_num = cur_im1_clr_num
      
      '''
      color_num_average = ( cur_im1_clr_num + cur_im2_clr_num ) / 2
      clr_num_percent = color_num_average / bigger_clr_num
      if clr_num_percent < 0.9:
         # color number mismatch between current image1 shape and image2 shape
         continue
      
      '''
      
      # color number check has passed. now check if actual colors match
      # color match is determined by using smaller color number
      color_match_count = 0
      
      if smaller_clr_num == cur_im1_clr_num:
         for cur_im1_color in cur_im1_colors:
            for cur_im2_color in cur_im2_colors:
               clrch, brit_thres, brit_ch_v = pixel_functions.compute_appearance_difference(cur_im1_color , cur_im2_color, 30 )
                  
               # color did not change and brightness is within threshold
               if not clrch and brit_thres:
                  color_match_count += 1
                  
                  # if current shape color match, then count this as match and go to next color.
                  break
      
      else:
         for cur_im2_color in cur_im2_colors:
            for cur_im1_color in cur_im1_colors:
               clrch, brit_thres, brit_ch_v = pixel_functions.compute_appearance_difference(cur_im1_color , cur_im2_color, 30 )
                  
               # color did not change and brightness is within threshold
               if not clrch and brit_thres:
                  color_match_count += 1      
      
                  # if current shape color match, then count this as match and go to next color.
                  break     
      
      
      color_match_average = ( smaller_clr_num + color_match_count ) / 2
      colr_match_percent = color_match_average / smaller_clr_num
      
      if colr_match_percent < 0.9:
         # color mismatch between current image1 shape and image2 shape 
         continue



      # getting image locations for current image1 shapes
      cur_im2_locations = im2shape_locations_list[ cur_im2_index ]
   

      im1shape_im_loc_num = len( cur_im1_locations )
      im2shape_im_loc_num = len( cur_im2_locations )
      
      im1_2_im_loc_match = len( cur_im2_locations.intersection( cur_im1_locations ) )
      
      smaller_loc_num = None
      bigger_loc_num = None
      if im1shape_im_loc_num > im2shape_im_loc_num:
         bigger_loc_num = im1shape_im_loc_num
         smaller_loc_num = im2shape_im_loc_num
      else:
         bigger_loc_num = im2shape_im_loc_num
         smaller_loc_num = im1shape_im_loc_num         

      im_loc_average = ( smaller_loc_num + im1_2_im_loc_match ) / 2
      im1_2_im_loc_m_percent = im_loc_average / smaller_loc_num

      if im1_2_im_loc_m_percent >= 0.9:
         matches.append( (cur_im1_shapeid, cur_im2_shapeid) )




print( matches )






































