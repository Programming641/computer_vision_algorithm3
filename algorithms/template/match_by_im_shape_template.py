# move whole image pixels up right left ( but not rotation ) and see if shapes match between two frames of video
# this script check if image1 shape's pixel has the same color as moved image's pixel.
# if so, this takes the image2 shape that is on the same pixel as image1 shape's pixel but not on the matched image2 pixel.
from PIL import Image
import re, pickle
import math
import shutil

import os, sys
from libraries.cv_globals import top_shapes_dir, top_images_dir, internal
from libraries.cv_globals import third_smallest_pixc, frth_smallest_pixc
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
shape_template_dir = template_dir + "shapes/"
shape_template_imdir = shape_template_dir + im1file + "." + im2file + "/"
shape_template_ddir = shape_template_dir + "data/"

if os.path.exists(template_dir ) == False:
   os.makedirs(template_dir )
if os.path.exists(shape_template_dir ) == False:
   os.makedirs(shape_template_dir )
if os.path.exists(shape_template_ddir ) == False:
   os.makedirs(shape_template_ddir )
# delete and create folder
if os.path.exists(shape_template_imdir) == True:
   shutil.rmtree(shape_template_imdir)
os.makedirs(shape_template_imdir)


original_image = Image.open(top_images_dir + directory + im1file + ".png")
image_size = original_image.size


im1shapes_colors = {}
if shapes_type == "normal":

   # return value form is
   # shapes[shapes_id][pixel_index] = {}
   # shapes[shapes_id][pixel_index]['x'] = x
   # shapes[shapes_id][pixel_index]['y'] = y
   im1shapes = read_files_functions.rd_shapes_file(im1file, directory)
   im2shapes = read_files_functions.rd_shapes_file(im2file, directory)

   im1shapes_neighbors_path = top_shapes_dir + directory + "shape_nbrs/" + im1file + "_shape_nbrs.txt"
   im2shapes_neighbors_path = top_shapes_dir + directory + "shape_nbrs/" + im2file + "_shape_nbrs.txt"   

elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"

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


# it takes so much time to see what shape contains the specific pixel, we prepare pixel and shapeid pair.
# { pixel: shapeid, pixel: shapeid, ... }
im2shape_by_pixel = {}
for im2shapeid, pixels in im2shapes.items():
   for pixel in pixels:
      im2shape_by_pixel[pixel] = im2shapeid
   



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
      
      
      if "left" in LUp_RUp_LDwn_RDwn.lower():
         move_image_LorR = image_functions.move_image_left( image_data, move_im_LorR, image_size )
      elif "right" in LUp_RUp_LDwn_RDwn.lower():
         move_image_LorR = image_functions.move_image_left( image_data, move_im_LorR, image_size )

      #img = Image.new("RGB", image_size)
      #img.putdata( move_image_left )
      #img.show()
      
      for move_im_UpDown in range( 0, mv_im_amount, 2 ):
         matched_shapes_UpDwn_index = len( matched_shapes[ matched_shapes_LR_index ] )
         # for corrent left or right, up or down image data, match is taken for every image1 shape.
         # { image1shapeid: [ matched image2 shapes ], ... }
         matched_shapes[ matched_shapes_LR_index ].append( {} )
         
      
         if "up" in LUp_RUp_LDwn_RDwn.lower():
            move_image_LorR_up_down = image_functions.move_image_up( move_image_LorR, move_im_UpDown, image_size )
         elif "down" in LUp_RUp_LDwn_RDwn.lower():
            move_image_LorR_up_down = image_functions.move_image_down( move_image_LorR, move_im_UpDown, image_size )

         
         for shapeid, pixels in im1shapes.items():
            if len( pixels ) < frth_smallest_pixc:
               continue
            
            matched_shapes[ matched_shapes_LR_index ][ matched_shapes_UpDwn_index ][shapeid] = set()
            
            found_im2shapes = {}
            for pixel in pixels:
               clrch, brit_thres, brit_ch_v = pixel_functions.compute_appearance_difference(im1shapes_colors[shapeid] ,
                                                 move_image_LorR_up_down[int(pixel)], 30 )
               
               # color did not change and brightness is within threshold
               if not clrch and brit_thres:
                  # current image1shape's pixel color matches with the image2 pixel.
                  # get image2 shape that has this pixel
                  
                  # check if image2 shape that has current image1shape's pixel is already added in found_im2shapes
                  if im2shape_by_pixel[pixel] not in found_im2shapes.keys():
                     found_im2shapes[ im2shape_by_pixel[pixel] ] = 1
                  else:
                     found_im2shapes[ im2shape_by_pixel[pixel] ] += 1
            
            # judging how current image1 shape matches image2 shape
            # match if either one of below conditions are met
            # 1. 60% or more pixels of current image1 shape or image2 shape matches if they are non-smallest pixel count shapes
            # 2. if image2 ( image1 skips smallest pixel count shapes ) is third smallest pixel count shape then 80% of pixels have to match. 
            
            # { im2shapeid: count of image1 pixel found in this image2 shape, ... }           
            for found_im2shapeid in found_im2shapes:
             
               if found_im2shapes[found_im2shapeid] >= len( pixels ) * 0.6:
                  # satisfies 60% or more pixels of image1 shape
                  matched_shapes[ matched_shapes_LR_index ][ matched_shapes_UpDwn_index ][shapeid].add( found_im2shapeid )
                  
               elif found_im2shapes[found_im2shapeid] >= len( im2shapes[ found_im2shapeid ] ) * 0.6 and len( im2shapes[ found_im2shapeid ] ) >= frth_smallest_pixc:
                  # satisfies 60% or more pixels of non-smallest pixc image2 shape
                  matched_shapes[ matched_shapes_LR_index ][ matched_shapes_UpDwn_index ][shapeid].add( found_im2shapeid )
                  
               elif found_im2shapes[found_im2shapeid] >= len( im2shapes[found_im2shapeid] ) * 0.8 and found_im2shapes[found_im2shapeid] >= third_smallest_pixc:
                  # satisfies condition2
                  matched_shapes[ matched_shapes_LR_index ][ matched_shapes_UpDwn_index ][shapeid].add( found_im2shapeid )
               
            if len( matched_shapes[ matched_shapes_LR_index ][ matched_shapes_UpDwn_index ][shapeid] ) == 0:
               matched_shapes[ matched_shapes_LR_index ][ matched_shapes_UpDwn_index ].pop( shapeid )


   

   return  matched_shapes



def find_LRUpDwn_best_matches( matched_shapes ):

   LRUpDwn_best_matches_temp = []
   # algorithm for determining the best matched shapes
   # parameters are: pixel counts of all matched shapes that are neighbors to each other.
   # the count of matched direct neighbor shapes.
   # calculation: sum of all direct neighbor shapes + ( count of direct neighbors * 0.6 * ( pixel counts * 0.3 ) )
   for each_matched_shapes in matched_shapes:
      # 1 pixel left or left
      cur_left = 0
      for each_shapes in each_matched_shapes:
         # 1 pixel up or down
         cur_up = 0
         
         # if image1 shape is taken as the neighbor in the current image1 shape, then should I skip it? but neighbor itselt has
         # its own neighbors.

         for im1shape in each_shapes:
            # each_shapes has all image1 shapes of current left/right and up/down
            # {'425': {'44819'}, ... }
            # { image1 shapeid: { image2 shapeids }, ... }

            
            # see if current im1shape's neighbors are in the current left/right and up/down
            cur_im1shape_found_nbrs = [ shape for shape in each_shapes.keys() if shape in im1shape_nbrs[im1shape]  ]
         
            # get total pixel counts
            cur_pixel_counts = len( im1shapes[ im1shape ] )
            
            non_small_found_nbrs = 0
            small_found_nbrs = 0
            
            cur_im2shapes = []
            # adding current image1 shape's image2ids
            cur_im2shapes.extend( list( each_shapes[ im1shape ] ) )
            
            
            # third smallest pixel count shapes should have less weight than bigger shapes for direct neighbor parameter
            for cur_im1shape_found_nbr in cur_im1shape_found_nbrs:
               cur_im2shapes.extend( list( each_shapes[ cur_im1shape_found_nbr ] ) )
               
               if len( im1shapes[cur_im1shape_found_nbr] ) >= third_smallest_pixc:
                  non_small_found_nbrs += len( im1shapes[cur_im1shape_found_nbr] )
               elif len( im1shapes[cur_im1shape_found_nbr] ) < third_smallest_pixc:
                  small_found_nbrs += len( im1shapes[cur_im1shape_found_nbr] )
               
               cur_pixel_counts += len( im1shapes[cur_im1shape_found_nbr] )
         
            cur_total = cur_pixel_counts + ( non_small_found_nbrs * 0.6 * ( cur_pixel_counts * 0.3 ) ) + ( small_found_nbrs * 0.3 * ( cur_pixel_counts * 0.3 ) )
         
            LRUpDwn_best_matches_temp.append( { im1shape: cur_total, "nbrs": cur_im1shape_found_nbrs, "im2_shapes": cur_im2shapes } )
            
      
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
         if shape_or_nbrs != "nbrs" and shape_or_nbrs != "im2_shapes":

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
      
         if highest_cur_shape is None and shape_or_nbrs != "nbrs" and shape_or_nbrs != "im2_shapes":
            print("ERROR for every shape, highest_cur_shape has to exist")
            sys.exit()
         
         

   return LRUpDwn_best_matches


def compare_btwn_LRUD_matches( LRUD_matches1, LRUD_matches2 ):
   LRUD_best_matches = []
   for LRUD_match in LRUD_matches1:
      # content example of LRUD_match -> [ {'425': 14190.5, 'nbrs': ['7639', '17240'], 'im2_shapes': ['8432', '2824', '6832']},
      #                                    {'425': 14190.5, 'nbrs': ['7639', '17240'], 'im2_shapes': ['424', '428', '6830']}, ... ]
   
      # if one of the shapes in LRUD_match had same value as the LRUD_matches2, then all its contents are 
      # already put into LRUD_best_matches, so skip all other shapes in the current LRUD_match
      skip_cur_shapes_list = False
   
      for each_LRUD_shape in LRUD_match:
         # each_LRUD_shape is one shape -> {'425': 14190.5, 'nbrs': ['7639', '17240'], 'im2_shapes': ['424', '428', '6830']}
         if skip_cur_shapes_list is True:
            continue
         for shapeid_or_nbrs in each_LRUD_shape:
            # search for current shape in the LRUD_matches2

            if shapeid_or_nbrs != "nbrs" and shapeid_or_nbrs != "im2_shapes":
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

# [ [{'71298': 77.88, 'nbrs': ['64895']}, {'71298': 77.88, 'nbrs': ['66666']}, ... ], ... ]
# if there are multiple shapes in the list, they all have same highest values.
LeftUp_best_matches = find_LRUpDwn_best_matches( LeftUp_matched_shapes )


RightUp_best_matches = find_LRUpDwn_best_matches( RightUp_matched_shapes )
LeftDown_best_matches = find_LRUpDwn_best_matches( LeftDown_matched_shapes )
RightDown_best_matches = find_LRUpDwn_best_matches( RightDown_matched_shapes )

print("best matches found for LeftUp, RightUp, LeftDown, and RightDown. now find best shape matches of all of them")

LUp_RUp_best_matches = compare_btwn_LRUD_matches( LeftUp_best_matches, RightUp_best_matches )
LDwn_RDwn_best_matches = compare_btwn_LRUD_matches( LeftDown_best_matches, RightDown_best_matches )

#finally! get the final result
LRUD_best_matches = compare_btwn_LRUD_matches( LUp_RUp_best_matches, LDwn_RDwn_best_matches )

print("all best matches are obtained. now creating images")


with open(shape_template_ddir  + im1file + "." + im2file + ".data", 'wb') as fp:
   pickle.dump(LRUD_best_matches, fp)
fp.close()
   
progress_counter = len( LRUD_best_matches )
for each_LRUD_shapes in LRUD_best_matches:
   print( str( progress_counter ) + " remaining")
   progress_counter -= 1
   
   # example each_LRUD_shapes -> [{'1400': 628.3199999999999, 'nbrs': ['1405', '11441'], 'im2_shapes': ['424', '428', '6830'] }]
   
   for each_shapes in each_LRUD_shapes:   
      # example each_shapes -> {'1400': 628.3199999999999, 'nbrs': ['1405', '11441'], 'im2_shapes': ['424', '428', '6830'] }
      cur_shapeid = None
      for shapeid_or_nbrs in each_shapes:
         
         if shapeid_or_nbrs != "nbrs" and shapeid_or_nbrs != "im2_shapes":
            cur_im1shapes_list = []
            cur_shapeid = shapeid_or_nbrs
            cur_im1shapes_list.append( cur_shapeid )
            cur_im1shapes_list.extend( each_shapes["nbrs"] )
       
            save_filepath = shape_template_imdir + "im1." + shapeid_or_nbrs + ".png"
                  
            # creating image for each shapeid inside each_LRUD_shapes or should I combine all shapes inside each_LRUD_shapes?     
            image_functions.cr_im_from_shapeslist2( im1file, directory, cur_im1shapes_list, save_filepath=save_filepath )
   

         if shapeid_or_nbrs == "im2_shapes" and cur_shapeid is not None:
            save_filepath = shape_template_imdir + "im1." + cur_shapeid + "im2shapes.png"
               
            # creating image for each shapeid inside each_LRUD_shapes or should I combine all shapes inside each_LRUD_shapes?     
            image_functions.cr_im_from_shapeslist2( im2file, directory, each_shapes["im2_shapes"], save_filepath=save_filepath )            
            




















