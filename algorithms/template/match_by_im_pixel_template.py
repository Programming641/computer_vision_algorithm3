# move whole image pixels up right left ( but not rotation ) and see if shapes match between two frames of video

from PIL import Image
import re, pickle
import math
import shutil

import os, sys
from libraries.cv_globals import top_shapes_dir, top_images_dir, frth_smallest_pixc, spixc_shapes, internal
from libraries import read_files_functions, image_functions, pixel_shapes_functions, pixel_functions



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
pixel_template_imdir = pixel_template_dir  + im1file + "." + im2file + "/"
pixel_template_ddir = pixel_template_dir + "data/"

if os.path.exists(template_dir ) == False:
   os.makedirs(template_dir )
if os.path.exists(pixel_template_dir ) == False:
   os.makedirs(pixel_template_dir )
if os.path.exists(pixel_template_ddir ) == False:
   os.makedirs(pixel_template_ddir )
# delete and create folder
if os.path.exists(pixel_template_imdir) == True:
   shutil.rmtree(pixel_template_imdir)
os.makedirs(pixel_template_imdir)


original_image = Image.open(top_images_dir + directory + im1file + ".png")
image_size = original_image.size


im1shapes_colors = {}
if shapes_type == "normal":

   # return value form is
   # shapes[shapes_id][pixel_index] = {}
   # shapes[shapes_id][pixel_index]['x'] = x
   # shapes[shapes_id][pixel_index]['y'] = y
   im1shapes = read_files_functions.rd_shapes_file(im1file, directory)
   for im1shapeid in im1shapes:
      im1shapes[im1shapeid] = list( im1shapes[im1shapeid].keys() )
   im2shapes = read_files_functions.rd_shapes_file(im2file, directory)
   for im2shapeid in im2shapes:
      im2shapes[im1shapeid] = list( im2shapes[im2shapeid].keys() )

   im1shapes_neighbors_path = top_shapes_dir + directory + "shape_nbrs/" + im1file + "_shape_nbrs.txt"
   im2shapes_neighbors_path = top_shapes_dir + directory + "shape_nbrs/" + im2file + "_shape_nbrs.txt"   

elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + spixc_shapes + "/" + internal + "/"

   shapes_dfile = s_pixcShp_intnl_dir + "shapes/" + im1file + "shapes.data"
   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()
   im2shapes_dfile = s_pixcShp_intnl_dir + "shapes/" + im2file + "shapes.data"
   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()   

   im1shapes_neighbors_path = s_pixcShp_intnl_dir + "shape_nbrs/" + im1file + "_shape_nbrs.txt"
   im2shapes_neighbors_path = s_pixcShp_intnl_dir + "shape_nbrs/" + im2file + "_shape_nbrs.txt"



im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors( im1file, directory, shapes_type )

# {"shapeid": ["nbr_shapeid", "nbr_shapeid", ...], ...  }
im1shape_nbrs = read_files_functions.rd_dict_k_v_l(im1file, directory, im1shapes_neighbors_path)
im2shape_nbrs = read_files_functions.rd_dict_k_v_l(im2file, directory, im2shapes_neighbors_path)

im1 = Image.open(top_images_dir + directory + im1file + ".png" )
im1pxls = im1.getdata()
im1width, im1height = im1.size

im2 = Image.open(top_images_dir + directory + im2file + ".png" )
im2pxls = im2.getdata()
im2width, im2height = im2.size


def match_shape_w_moved_image( image_data, LUp_RUp_LDwn_RDwn,  mv_im_amount, DirectlyUpDown ):
   matched_shapes = []
   start_position = None
   if DirectlyUpDown is True:
      start_position = 0
   elif DirectlyUpDown is False:
      start_position = 1
   
   for move_im_LorR in range( start_position, mv_im_amount, 2 ):
      matched_shapes_LR_index = len( matched_shapes )
      matched_shapes.append( [] )   
      
      # if moved_im2pixel results in negative value, this means that this pixel is the non-image color pixel
      moved_im2pixel = 0
      if "left" in LUp_RUp_LDwn_RDwn.lower():
         # if moving the image left, this means that current pixel is the previous right pixel with moved amount.
         moved_im2pixel += move_im_LorR
         move_image_LorR = image_functions.move_image_left( image_data, move_im_LorR, image_size )
      elif "right" in LUp_RUp_LDwn_RDwn.lower():
         # if moving the image right, this means that current pixel is the previous left pixel with moved amount.
         moved_im2pixel -= move_im_LorR
         move_image_LorR = image_functions.move_image_left( image_data, move_im_LorR, image_size )

      #img = Image.new("RGB", image_size)
      #img.putdata( move_image_left )
      #img.show()
      
      for move_im_UpDown in range( 0, mv_im_amount, 2 ):
         matched_shapes_UpDwn_index = len( matched_shapes[ matched_shapes_LR_index ] )
         # { "image1shapeid": [ matched image2 pixels ], ... }
         matched_shapes[ matched_shapes_LR_index ].append( {} )
         
      
         if "up" in LUp_RUp_LDwn_RDwn.lower():
            # if moving the image top, this means that current pixel is the previous down pixel with moved amount
            moved_im2pixel += im2width
            
            move_image_LorR_up_down = image_functions.move_image_up( move_image_LorR, move_im_UpDown, image_size )
         elif "down" in LUp_RUp_LDwn_RDwn.lower():
            # if moving the image down, this means that current pixel is the previous up pixel with moved amount
            moved_im2pixel -= im2width
            move_image_LorR_up_down = image_functions.move_image_down( move_image_LorR, move_im_UpDown, image_size )

         

         for shapeid, pixels in im1shapes.items():
            if len( pixels ) < frth_smallest_pixc:
               continue
   
            im2pixels = set()
            cur_shape_m_count = 0
            for pixel in pixels:
               clrch, brit_thres, brit_ch_v = pixel_functions.compute_appearance_difference(im1shapes_colors[shapeid] ,
                                                 move_image_LorR_up_down[int(pixel)], 30 )
                  
               # color did not change and brightness is within threshold
               if not clrch and brit_thres:
                  cur_im2pixel = int(pixel) + moved_im2pixel
                  
                  im2pixel_y = math.floor( int(cur_im2pixel) / im2width)
                  im2pixel_x  = int(cur_im2pixel) % im2width
            
                  if ( im2pixel_x >= im2width or im2pixel_x < 0 ) or ( im2pixel_y >= im2height or im2pixel_y < 0 ):
                     # pixel matched non-image color. so skip it
                     continue
                  
                  # also check if cur_im2pixel does not cross left/right/top/bottom side of the image from 
                  # currrent image1 shape pixel
                  im1pixel_y = math.floor( int(pixel) / im1width)
                  im1pixel_x  = int(pixel) % im1width    

                  # check if cur_im2pixel is crossing the left side of the image from current image1 shape's pixel
                  if im2pixel_x + mv_im_amount >= im2width and im1pixel_x - mv_im_amount <= 0:
                     # im2pixel is near the right side of the image while current im1 pixel is near the left side of the image
                     continue
                  # check right side
                  elif im1pixel_x + mv_im_amount >= im1width and im2pixel_x - mv_im_amount <= 0:
                     # im1pixel is near the right side of the image while im2pixel is near the left side the image
                     continue
                  # check top side
                  elif im2pixel_y - mv_im_amount <= 0 and im1pixel_y + mv_im_amount >= im1height:
                     # image2 pixel is near the top side of the image while image1 pixel is near the bottom side of the image
                     continue
                  # check bottom side
                  elif im1pixel_y - mv_im_amount <= 0 and im2pixel_y + mv_im_amount >= im2height:
                     # image1 pixel is near the top side of the image while image2 pixel is near the bottom side of the image
                     continue
                  
                  
                  cur_shape_m_count += 1
                  im2pixels.add( cur_im2pixel )
         
            # all pixels of current shape is done. now check if current shape is a match
            if cur_shape_m_count >= len( pixels ) * 0.6:
               matched_shapes[ matched_shapes_LR_index ][ matched_shapes_UpDwn_index ][shapeid] = im2pixels


   return matched_shapes



def find_LRUpDwn_best_matches( matched_shapes ):

   LRUpDwn_best_matches_temp = []
   # algorithm for determining the best matched shapes
   # parameters are: pixel counts of all matched shapes that are neighbors to each other.
   # the count of matched direct neighbor shapes.
   # calculation: sum of all direct neighbor shapes + ( count of direct neighbors * 0.6 * ( pixel counts * 0.3 ) )
   for each_matched_shapes in matched_shapes:
      # 1 pixel left
      cur_left = 0
      for each_shapes in each_matched_shapes:
         # 1 pixel up
         cur_up = 0
         for im1shape in each_shapes:
            # see if current shape's neighbors are in the current left and up amount
         
            cur_im1shape_found_nbrs = [ shape for shape in each_shapes.keys() if shape in im1shape_nbrs[im1shape]  ]
         
            # get total pixel counts
            cur_pixel_counts = len( im1shapes[ im1shape ] )

            cur_im2pixels = []
            # adding current image1 shape's image2 pixels
            cur_im2pixels.extend( list( each_shapes[ im1shape ] ) )
         
            for cur_im1shape_found_nbr in cur_im1shape_found_nbrs:
               # adding current image1 shape's neighbor's image2 pixels
               cur_im2pixels.extend( list( each_shapes[ cur_im1shape_found_nbr ] ) )
               
               cur_pixel_counts += len( im1shapes[cur_im1shape_found_nbr] )
            
            if cur_pixel_counts < ( ( im1width * im1height ) / ( ( im1width + im1height ) * 1.3 ) ):
               # check if total pixels are big enough, if not, skip it
               continue
         
            cur_total = cur_pixel_counts + ( len(cur_im1shape_found_nbrs) * 0.6 * ( cur_pixel_counts * 0.3 ) )
         
            LRUpDwn_best_matches_temp.append( { im1shape: cur_total, "nbrs": cur_im1shape_found_nbrs, "im2pixels": cur_im2pixels } )
      
         cur_up += 1
   
      cur_left += 1

   # delete duplicates from LRUpDwn_best_matches_temp
   deleted = 0
   for cur_element in range ( 0, len(LRUpDwn_best_matches_temp) ):
      if LRUpDwn_best_matches_temp.count( LRUpDwn_best_matches_temp[cur_element + deleted] ) > 1:
         LRUpDwn_best_matches_temp.pop(cur_element + deleted)
         deleted -= 1

   
   already_processed_shapes = []
   LRUpDwn_best_matches = []
   for LRUpDwn_best_match in LRUpDwn_best_matches_temp:
      for shape_or_nbrs in LRUpDwn_best_match:
         if shape_or_nbrs in already_processed_shapes:
            # LRUpDwn_best_matches_temp may contain same shapeids with different score or maybe different neighbors
            continue
      
         highest_cur_shape = None
         if shape_or_nbrs != "nbrs" and shape_or_nbrs != "im2pixels":

            # get one that has highest value for the current shape
            cur_largest_value = max( [ shape[shape_or_nbrs] for shape in LRUpDwn_best_matches_temp if shape_or_nbrs in shape.keys() ] )
      
            highest_cur_shape = [ shape for shape in LRUpDwn_best_matches_temp if shape_or_nbrs in shape.keys() and shape[shape_or_nbrs] == cur_largest_value  ]
         
            # check if highest_cur_shape returns multiple same highest values
            # if so, check if the highest value shapes are exactly the same. that is, shapes with same neighbors
            if len( highest_cur_shape ) >= 1:
               # delete duplicates and put it in LRUpDwn_best_matches
               deleted = 0
               for cur_element in range ( 0, len(highest_cur_shape) ):
                  if highest_cur_shape.count( highest_cur_shape[cur_element + deleted] ) > 1:
                     highest_cur_shape.pop(cur_element + deleted)
                     deleted -= 1
               
               LRUpDwn_best_matches.append( highest_cur_shape )
             
            
            already_processed_shapes.append( shape_or_nbrs )
         if highest_cur_shape is None and shape_or_nbrs != "nbrs" and shape_or_nbrs != "im2pixels":      
            print("ERROR for every shape, highest_cur_shape has to exist")
            sys.exit()
         
         

   return LRUpDwn_best_matches


def compare_btwn_LRUD_matches( LRUD_matches1, LRUD_matches2 ):
   LRUD_best_matches = []
   for LRUD_match in LRUD_matches1:
      # content example of LRUD_match -> [{'2380': 21.24, 'nbrs': ['2379'], 'im2pixels': ['8432', '2824', '6832']}, ... ]
   
      # if one of the shapes in LRUD_match had same value as the LRUD_matches2, then all its contents are 
      # already put into LRUD_best_matches, so skip all other shapes in the current LRUD_match
      skip_cur_shapes_list = False
   
      for each_LRUD_shape in LRUD_match:
         # each_LRUD_shape is one shape -> {'2380': 21.24, 'nbrs': ['2379'], 'im2pixels': ['8432', '2824', '6832']}
         if skip_cur_shapes_list is True:
            continue
         for shapeid_or_nbrs in each_LRUD_shape:
            # search for current shape in the LRUD_matches2

            if shapeid_or_nbrs != "nbrs" and shapeid_or_nbrs != "im2pixels":
               # if current shape is found, then there should be only one exist in LRUD_shape
               for LRUD_shape in LRUD_matches2:
               
                  cur_LRUD2_shape = [ shape for shape in LRUD_shape if shapeid_or_nbrs in shape.keys() ]
                
                  # check if found shape has the same or higher value. 
                  if len( cur_LRUD2_shape ) >= 1:
                     if cur_LRUD2_shape[0][shapeid_or_nbrs] > each_LRUD_shape[shapeid_or_nbrs]:


                        LRUD_best_matches.append( cur_LRUD2_shape )
                     elif cur_LRUD2_shape[0][shapeid_or_nbrs] == each_LRUD_shape[shapeid_or_nbrs]:
                        for cur_LRUD_shape in LRUD_match:
                           if cur_LRUD_shape not in cur_LRUD2_shape:

                              cur_LRUD2_shape.append( cur_LRUD_shape )
                     
                        skip_cur_shapes_list = True
                        LRUD_best_matches.append( cur_LRUD2_shape )
                  
                     elif cur_LRUD2_shape[0][shapeid_or_nbrs] < each_LRUD_shape[shapeid_or_nbrs]:
                        LRUD_best_matches.append( LRUD_match )
                        skip_cur_shapes_list = True
               

      # LRUD_best_matches may contain same multiple shapes when LRUD_match has multiple same shape entries.

   return LRUD_best_matches



print("preparation complete. now main processing begins")

LeftUp_matched_shapes = match_shape_w_moved_image( im2pxls, "leftUp", 20, True )
RightUp_matched_shapes = match_shape_w_moved_image( im2pxls, "rightup", 20, False )
LeftDown_matched_shapes = match_shape_w_moved_image( im2pxls, "leftdown", 20, True )
RightDown_matched_shapes = match_shape_w_moved_image( im2pxls, "rightdown", 20, False )

print("leftUp, RightUp, LeftDown, RightDown match finding now complete. now go onto find best matches from them")

# [ [{'71298': 77.88, 'nbrs': ['64895'], 'im2pixels': ['8432', '2824', '6832']}, ... ], ... ]
# if there are multiple shapes in the list, they all have same highest values.
LeftUp_best_matches = find_LRUpDwn_best_matches( LeftUp_matched_shapes )
RightUp_best_matches = find_LRUpDwn_best_matches( RightUp_matched_shapes )
LeftDown_best_matches = find_LRUpDwn_best_matches( LeftDown_matched_shapes )
RightDown_best_matches = find_LRUpDwn_best_matches( RightDown_matched_shapes )

print("best matches found for LeftUp, RightUp, LeftDown, and RightDown. now find best shape matches of all of them")

LUp_RUp_best_matches = compare_btwn_LRUD_matches( LeftUp_best_matches, RightUp_best_matches )
LDwn_RDwn_best_matches = compare_btwn_LRUD_matches( LeftDown_best_matches, RightDown_best_matches )

#finally! get the final result
# [ [{'1400': 628.3199999999999, 'nbrs': ['1405', '11441'], 'im2pixels': ['424', '428', '6830'] }], ... ]
# [ [ { image1shapeid: matched count, image1 neighbors: [ image1 neighbors ], im2pixels: [ matched image2 pixels ] }, ... ]
pre_LRUD_best_matches = compare_btwn_LRUD_matches( LUp_RUp_best_matches, LDwn_RDwn_best_matches )

# still needs refining.
# LRUD_best_matches will definitely contain lots of shapes that are more than 90% of pixels similar.
# take only one of them and only take differences for all other shapes.
# [ { im1shapeid: im1shapeid, match_count: matched count, image1 neighbors: [ image1 neighbors ], im2pixels: [ matched image2 pixels ],
#        "similar_im1shape": [ [ im1shapes ], [im2pixels that only exist in current similar one], ... ] }, ... ]
LRUD_best_matches = []
for preLRUD_best_match in pre_LRUD_best_matches:
   # preLRUD_best_match -> [{'2577': 173.46, 'nbrs': ['2985'], 'im2pixels': [ 1788, 1789]}, {'2577': 173.46, 'nbrs': ['2985'], 'im2pixels': [ 1784, 1785]}]
   
   first_LRUD = {}
   first_LRUD_im2pixels = set()
   for each_preLRUD_best_match in preLRUD_best_match:
      cur_im1shapeid = None
      for key in each_preLRUD_best_match:
         if key != "nbrs" or shapeid != "im2pixels":
            cur_im1shapeid = key
            break
            
      
      if len(first_LRUD) == 0:
         first_LRUD["im1shapeid"] = cur_im1shapeid
         first_LRUD["match_count"] = each_preLRUD_best_match[ cur_im1shapeid ]
         first_LRUD["im1nbrs"] = each_preLRUD_best_match[ "nbrs" ]
         first_LRUD["im2pixels"] = each_preLRUD_best_match["im2pixels"]
         first_LRUD["similar_im1shapes"] = []

         first_LRUD_im2pixels |= set( first_LRUD["im2pixels"] )
         
      else:
         # because shapes inside the preLRUD_best_match have same match count, they are all similar shapes
         cur_im2pixels = set( each_preLRUD_best_match["im2pixels"] )
         
         cur_im1shapes = [ cur_im1shapeid ]
         cur_im1shapes.extend( each_preLRUD_best_match["nbrs"] )
         cur_im2pix_diff = cur_im2pixels.difference( first_LRUD_im2pixels )
         
         first_LRUD["similar_im1shapes"].append( cur_im1shapes )
         first_LRUD["similar_im1shapes"].append( cur_im2pix_diff )
   
   LRUD_best_matches.append( first_LRUD )   
   
print("all best matches are obtained. now creating images")


with open(pixel_template_ddir  + im1file + "." + im2file + ".data", 'wb') as fp:
   pickle.dump(LRUD_best_matches, fp)
fp.close()
   

progress_counter = len( LRUD_best_matches )
for each_LRUD_shapes in LRUD_best_matches:
   print( str( progress_counter ) + " remaining")
   progress_counter -= 1
   
   # example each_LRUD_shapes -> {'im1shapeid': '2577', 'match_count': 173.46, 'im1nbrs': ['2985'], 'im2pixels': [2577, ... ], 
   #                              'similar_im1shapes': [['2577', '2985'], {2177, ...}, ... ] } 

   cur_im1shapes_list = []
   cur_im1shapes_list.append( each_LRUD_shapes["im1shapeid"] )
   cur_im1shapes_list.extend( each_LRUD_shapes["im1nbrs"] )
       
   save_filepath = pixel_template_imdir + "im1." + each_LRUD_shapes["im1shapeid"] + ".png"
                  
   # creating image for each shapeid inside each_LRUD_shapes or should I combine all shapes inside each_LRUD_shapes?     
   image_functions.cr_im_from_shapeslist2( im1file, directory, cur_im1shapes_list, save_filepath=save_filepath )

   save_filepath = pixel_template_imdir + "im1." + each_LRUD_shapes["im1shapeid"] + "im2pixels.png" 
   im2 = Image.open(top_images_dir + directory + im2file + ".png" )  
   
   for pixel_index in each_LRUD_shapes["im2pixels"]:
      y = math.floor( int(pixel_index) / im2width)
      x  = int(pixel_index) % im2width

      im2.putpixel( (x , y) , (255, 0, 0 ) )

   im2.save( save_filepath )
















