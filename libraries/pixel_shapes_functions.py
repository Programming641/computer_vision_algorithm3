
import re
from PIL import Image
import os, sys
from statistics import mean
import math
import pickle

from libraries import read_files_functions, image_functions, pixel_functions
from libraries.cv_globals import proj_dir, top_images_dir, top_shapes_dir, spixc_shapes, internal


# shape_ids is list containing shape ids
# [20085]
# returns all pixel shape ids and all its pixel indexes
# pixel id dictionary[ matched pixel shape id ] = [ pixel index1, pixel index2, ..... ]
def get_all_pixels_of_shapes(shape_ids, image_filename, directory_under_images=""):


    # directory is passed in parameter but does not contain /
    if directory_under_images != "" and directory_under_images[-1] != "/":
       directory_under_images +='/'

    shapes_file = open(top_shapes_dir + directory_under_images + "shapes/" + image_filename + "_shapes.txt")
    shapes_file_contents = shapes_file.read()


    original_image = Image.open(top_images_dir + str(directory_under_images) + image_filename + ".png")

    image_width, image_height = original_image.size



    # single pixel shapes
    # ( then comes [0-9]{1, len(str(image_width * image_height))} then comes , then comes 
    # space then comes [ then comes [0-9]{1,len(str(image_width * image_height))} then comes ] then comes )
    # single_pixel_pattern = '\([0-9]{1, ' + str(len(str(image_width * image_height))) + '}, \[[0-9]{1,' + str(len(str(image_width * image_height))) + '}\]\)'

    single_pixel_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}, \[[0-9]{1,' + \
                           str(len(str(image_width * image_height))) + '}\]\)'
                           
    match = re.findall(single_pixel_pattern, shapes_file_contents)


    # shapes_with_indexes[matched shape id ] = [ pixel index1, pixel index2 .... ]
    shapes_with_indexes = {}

    for matched_shape_id in shape_ids: 

        # match contains all image shapes
        for shape in match:


           shapes_id_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '},'
           match_temp = re.search(shapes_id_pattern, shape)
           shapes_id = match_temp.group().strip('(,')
           
           if str(shapes_id) != str(matched_shape_id):
              continue
              

           shapes_with_indexes[shapes_id] = [shapes_id]



    '''
    ( then comes [0-9]{1, len(str(image_width * image_height))} then comes , then comes space then comes [ then comes 
    GROUPSTART [0-9]{1,len(str(image_width * image_height))} then comes , then comes space GROUPEND then comes [0-9]{1,len(str(image_width * image_height))} 
    then comes ] then comes )

    GROUPSTART (      GROUPEND )
    '''
    multiple_pixel_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}, \[(?:[0-9]{1,' + str(len(str(image_width * image_height))) + \
                             '},\s{1})+[0-9]{1,' + str(len(str(image_width * image_height))) + '}\]\)'
    match = re.findall(multiple_pixel_pattern, shapes_file_contents)
    
    

    for matched_shape_id in shape_ids: 

        # match contains all image shapes
        for shape in match:


           shapes_id_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '},'
           match_temp = re.search(shapes_id_pattern, shape)
           shapes_id = match_temp.group().strip('(,')
           
           if str(shapes_id) != str(matched_shape_id):
              continue
              

           pixels_list_pattern = '\[.*\]'
           pixels_index_string = re.findall(pixels_list_pattern, shape)



           #pixel_index_string contains one shape
           # pixels_index_string is a list but contains only one string
           for one_string in pixels_index_string:
          
              # one_string is a one string. removing unnecessary characters leaving only the numbers
              one_string_stripped = one_string.strip('[, ]')
              one_string_stripped = one_string_stripped.replace(' ', '')
              # split each pixel index number by ,
              one_string_list = one_string_stripped.split(',')



           shapes_with_indexes[matched_shape_id] = one_string_list


    return shapes_with_indexes


# pixel is one pixel 
# pixel is pixel index number
def get_shapeid_frompix(pixel, image_filename, directory_under_images="", shapes_type="normal"):


    # directory is passed in parameter but does not contain /
    if directory_under_images != "" and directory_under_images[-1] != "/":
       directory_under_images +='/'

    if shapes_type == "normal":

       shapes_file = open(top_shapes_dir + directory_under_images + "shapes/" + image_filename + "_shapes.txt")
       shapes_file_contents = shapes_file.read()       


       original_image = Image.open(top_images_dir + str(directory_under_images) + image_filename + ".png")

       image_width, image_height = original_image.size



       # single pixel shapes
       # ( then comes [0-9]{1, len(str(image_width * image_height))} then comes , then comes 
       # space then comes [ then comes [0-9]{1,len(str(image_width * image_height))} then comes ] then comes )
       # single_pixel_pattern = '\([0-9]{1, ' + str(len(str(image_width * image_height))) + '}, \[[0-9]{1,' + str(len(str(image_width * image_height))) + '}\]\)'

       single_pixel_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}, \[[0-9]{1,' + \
                           str(len(str(image_width * image_height))) + '}\]\)'
                           
       match = re.findall(single_pixel_pattern, shapes_file_contents)


       # shapes_with_indexes[matched shape id ] = [ pixel index1, pixel index2 .... ]
       shapes_with_indexes = {}

       # match contains all image shapes
       for shape in match:


          shapes_id_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '},'
          match_temp = re.search(shapes_id_pattern, shape)
          shapes_id = match_temp.group().strip('(,')
           
          if str(shapes_id) == str(pixel):
             shapes_with_indexes[shapes_id] = [shapes_id]
          
             return shapes_with_indexes
              

       '''
       ( then comes [0-9]{1, len(str(image_width * image_height))} then comes , then comes space then comes [ then comes 
       GROUPSTART [0-9]{1,len(str(image_width * image_height))} then comes , then comes space GROUPEND then comes [0-9]{1,len(str(image_width * image_height))} 
       then comes ] then comes )

       GROUPSTART (      GROUPEND )
       '''
       multiple_pixel_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}, \[(?:[0-9]{1,' + str(len(str(image_width * image_height))) + \
                             '},\s{1})+[0-9]{1,' + str(len(str(image_width * image_height))) + '}\]\)'
       match = re.findall(multiple_pixel_pattern, shapes_file_contents)
    

       # match contains all image shapes
       for shape in match:


          shapes_id_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '},'
          match_temp = re.search(shapes_id_pattern, shape)
          shapes_id = match_temp.group().strip('(,')
       
          pixels_list_pattern = '\[.*\]'
          pixels_index_string = re.findall(pixels_list_pattern, shape)



          #pixel_index_string contains one shape
          # pixels_index_string is a list but contains only one string
          for one_string in pixels_index_string:
          
             # one_string is a one string. removing unnecessary characters leaving only the numbers
             one_string_stripped = one_string.strip('[, ]')
             one_string_stripped = one_string_stripped.replace(' ', '')
             # split each pixel index number by ,
             one_string_list = one_string_stripped.split(',')


          if pixel in one_string_list:
             shapes_with_indexes[shapes_id] = one_string_list
          
             return shapes_with_indexes

       


       return None


    elif shapes_type == "intnl_spixcShp":
       s_pixcShp_intnl_dir = top_shapes_dir + directory_under_images + "spixc_shapes/" + internal + "/"
   
       shapes_dir = s_pixcShp_intnl_dir + "shapes/"
       shapes_dfile = shapes_dir + image_filename + "shapes.data"

       with open (shapes_dfile, 'rb') as fp:
          # { '79999': ['79999', ... ], ... }
          # { 'shapeid': [ pixel indexes ], ... }
          im_shapes = pickle.load(fp)
          fp.close()  

       for shapeid in im_shapes:
          if str(pixel) in im_shapes[shapeid]:
             return shapeid


    



# get all shapeids for the given parameter pixel index numbers
# input parameter "pixels" is list containing pixel index numbers
def get_shapeids_frompixels( pixels, imfile, imdir ):

    if shapes_type == "normal":
       # directory is passed in parameter but does not contain /
       if imdir != "" and imdir[-1] != ('/'):
          imdir +='/'

       shapes_file = open(top_shapes_dir + imdir + "shapes/" + imfile + "_shapes.txt")
       shapes_file_contents = shapes_file.read()


       img = Image.open(top_images_dir + str(imdir) + imfile + ".png")

       image_width, image_height = img.size



       # single pixel shapes
       # ( then comes [0-9]{1, len(str(image_width * image_height))} then comes , then comes 
       # space then comes [ then comes [0-9]{1,len(str(image_width * image_height))} then comes ] then comes )
       # single_pixel_pattern = '\([0-9]{1, ' + str(len(str(image_width * image_height))) + '}, \[[0-9]{1,' + str(len(str(image_width * image_height))) + '}\]\)'

       single_pixel_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}, \[[0-9]{1,' + \
                           str(len(str(image_width * image_height))) + '}\]\)'
                           
       match = re.findall(single_pixel_pattern, shapes_file_contents)


       # shapes_with_indexes[matched shape id ] = [ pixel index1, pixel index2 .... ]
       shapepix = {}

       # match contains all image shapes
       for shape in match:


          shapes_id_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '},'
          match_temp = re.search(shapes_id_pattern, shape)
          shapeid = match_temp.group().strip('(,')
           
          if shapeid in pixels:
             shapepix[shapeid] = [ shapeid ]




       '''
       ( then comes [0-9]{1, len(str(image_width * image_height))} then comes , then comes space then comes [ then comes 
       GROUPSTART [0-9]{1,len(str(image_width * image_height))} then comes , then comes space GROUPEND then comes [0-9]{1,len(str(image_width * image_height))} 
       then comes ] then comes )

       GROUPSTART (      GROUPEND )
       '''
       multiple_pixel_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}, \[(?:[0-9]{1,' + str(len(str(image_width * image_height))) + \
                             '},\s{1})+[0-9]{1,' + str(len(str(image_width * image_height))) + '}\]\)'
       match = re.findall(multiple_pixel_pattern, shapes_file_contents)


       # match contains all image shapes
       for shape in match:

          # getting shapeid
          shapes_id_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '},'
          match_temp = re.search(shapes_id_pattern, shape)
          # removing "(,"
          shapeid = match_temp.group().strip('(,')
       
          # get list of all pixels of a shape
          # start_pixel_list
          start_pix_l = shape.find("[")
          end_pix_l = shape.find("]")
       
          allpix = shape[ start_pix_l : end_pix_l + 1]
          allpix = allpix.strip('][').split(', ')
       
       
       
          # check if image pixel is containd in input pixels
          for pix in allpix:
             if pix in pixels:
                shapepix[shapeid] = allpix



       return shapepix







#  parameter in and out is a dictionary with following form.
#    pixels = { (x,y), (x,y), ... }
#    or list of tuple xy.
#  keys are not pixel index number. they are just incremental values starting from 1
def get_boundary_pixels(pixels):
   pixel_boundaries = []

   # first, we are going to get boundaries horizontally

   smallest_y = min(int(d[1]) for d in pixels)
   largest_y = max(int(d[1]) for d in pixels)

   # for loop for going from smallest y value to the largest y value
   # this means going from very top pixel to very bottom pixel
   #  for y in range(start, stop) stop value is excluded
   for y in range(smallest_y, largest_y + 1):

      # pixel_ids_with_current_y_values contains all xy coordinate pairs that have the current running y value.
      pixel_ids_with_current_y_values = [k for k in pixels  if (int( k[1] )) == y]
      
      first = True
      
      
      # we first obtain all x values for the current running y value
      x_values_list_in_current_y = []
      
      
      '''
      -------------------        boundary finding algorithm            ---------------------------
      
      With current running y value, boundary is where there is no consecutive x values. This means there is no more 
      neighbor x values on the right or left side.  The " boundary left side " has missing x values on the " left " ( no more smaller x values )
      The " boundary right side " has missing x values on the " right " ( missing neighbor larger x values )
      finally, the smallest and largest x values are the farthest of all pixels in the current running y value.
      '''
      
      # key is the coordinate pair id.  
      for key in pixel_ids_with_current_y_values:
      
         # putting all x values for all xy coordinates that have current running y vaule
         x_values_list_in_current_y.append(key[0])

      
      # we need to sort x values so that we can work with neighbor x values
      x_values_list_in_current_y.sort()
      
      # this is for getting the largest x value in current running y. largest x value is the last one in current running y because
      # x values are sorted from smallest to largest
      x_counter_in_current_running_y = 1
      
      x_numbers_in_current_running_y = len(x_values_list_in_current_y)

      for x_value in x_values_list_in_current_y:

         # boundary is also on smallest y and largest y because very top and very bottom will be the boundaries
         # this is for the very top
         if y == smallest_y:
            pixel_boundaries.append( (x_value, y ) )              

    
         # boundary is also on smallest y and largest y because very top and very bottom will be the boundaries
         # this is for the bottom
         if y == largest_y:
            pixel_boundaries.append( (x_value, y) )          
         
         # checking to see if x value is the last one in current running y
         if x_counter_in_current_running_y == x_numbers_in_current_running_y:
            
            pixel_boundaries.append( (x_value,y) )     


         # smallest x value and largest x value in the current running y value are the farthest boundary pixels
         # x values are sorted, so smallest x value in current running y is the first x value
         if first != False:
         
            pixel_boundaries.append( (x_value,y) )
            
            first = False
            
         else:
         
             # if two consecutive pixels are right next to each other, the difference of them should produce 1
             if abs( x_value - previous_x_value ) > 1:
                # boundary is found

                if x_value - previous_x_value < 0:
                   # result is negative, this means current x value is smaller ( it is on the left relative to previous )
                   # then, current x value is the boundary pixel " on the left side "

                   pixel_boundaries.append( (x_value,y) )
                

                else:

                   # result is positive, this means current x value is larger than previous ( it is on the right relative 
                   # to previous ). Then, current x value is the boundary pixel " on the right side " relative to previous

                   pixel_boundaries.append( (x_value,y) )
                
                
                   # because current x value is not consecutive from previous x value, previous x value is also the boundary
                   pixel_boundaries.append( ( previous_x_value, y ) )
                
         previous_x_value = x_value               

         x_counter_in_current_running_y += 1


   # -----------------------------          now this is for getting boundaries vertically        ----------------------------------------

   smallest_x = min(int(d[0]) for d in pixels)
   largest_x = max(int(d[0]) for d in pixels)


   # for loop for going from smallest x value to largest x value
   # here, we will look at each one of the columns of pixels from smallest x value to the largest x_counter_in_current_running_y
   # for example, we will look at all pixels that lie in ( 0, all y values ), ( 1, all y values ) ..... 
   #  for x in range(start, stop) stop value is excluded
   for x in range(smallest_x, largest_x + 1):

      # pixel_ids_with_current_x_values contains all xy coordinate pairs that have the current running x value.
      pixel_ids_with_current_x_values = [k for k in pixels  if int(k[0]) == x]
      
      first = True
      y_counter_in_current_running_x = 1
      
      # we first obtain all y values for the current running x value
      y_values_list_in_current_x = []
      
      
      '''
      -------------------        boundary finding algorithm            ---------------------------
      
      With current running x value, boundary is where there is no consecutive y values. This means there is no more 
      neighbor y values on the top or bottom.  The " boundary top side " has missing y values on the " top " ( no more smaller y values )
      The " boundary bottom side " has missing y values on the " bottom " ( missing neighbor larger y values) 
      '''
      
      # key is the coordinate pair id.  
      for key in pixel_ids_with_current_x_values:
      
         # putting all y values for all xy coordinates that have current running x vaule
         y_values_list_in_current_x.append(key[1])

      
      # we need to sort x values so that we can work with neighbor x values
      y_values_list_in_current_x.sort()
        

      for y_value in y_values_list_in_current_x:
 
         # check if current y value is the last one in the current running x
         if y_counter_in_current_running_x == len(y_values_list_in_current_x):
         
            pixel_boundaries.append( ( x, y_value ) )
         
         # for the current running x value (all pixels vertically ), first y is the very top pixel which should be boundary
         if first == True:
         
            pixel_boundaries.append( (x, y_value ) )
 
            previous_y_value = y_value
            first = False
         else:          

            # if two consecutive pixels are right next to each other, the difference of them should produce 1
            if abs( y_value - previous_y_value ) > 1:
               # boundary is found
                
               pixel_boundaries.append( (x, y_value ) )

               # because current y value is not consecutive from previous y value, previous y value is also the boundary
               pixel_boundaries.append( (x, previous_y_value ) )
   
                
         previous_y_value = y_value    

         y_counter_in_current_running_x += 1


   # duplicate xy coordinates created if pixels are found both virtically and horizontally. so remove them
   temp = []
   for pixel in pixel_boundaries:
      if pixel not in temp:
         temp.append( pixel )
      
   pixel_boundaries = temp
   pixel_boundaries = [ pixel for pixel in sorted(pixel_boundaries, key=lambda item: (item[1], item[0]) ) ]

   return pixel_boundaries






# pixels are the pixels returned by get_boundary_pixels
#
# pixels ->  # [(158, 84), (159, 84), ... ]
#
# returns the following form
# [ [ ( x,y ), ( top_percentage, right_percentage, bottom_percentage, left_percentage ) ], ... ]
# percentage says how far away from each direction. 0 is 0 distance away from that direction. 1.0 is farthest from that direction.
def get_bnd_pix_w_directions(pixels):

   boundaries_w_directions = []

   top = min( [ xy[1] for xy in pixels ] )
   right = max( [ xy[0] for xy in pixels ] )
   bottom = max( [ xy[1] for xy in pixels] )
   left = min( [ xy[0] for xy in pixels ] )  

   from_top_to_botom = bottom - top
   from_left_to_right = right - left

   for boundary_pixel in pixels:

   
      cur_distance_from_top = boundary_pixel[1] - top
      cur_distance_from_right = right - boundary_pixel[0] 
      cur_distance_from_bottom =  bottom - boundary_pixel[1]
      cur_distance_from_left = boundary_pixel[0] - left
      
      if cur_distance_from_top != 0:
         cur_top_percent = cur_distance_from_top / from_top_to_botom
      else:
         cur_top_percent = 0
      
      if cur_distance_from_right != 0:
         cur_right_percent = cur_distance_from_right / from_left_to_right
      else:
         cur_right_percent = 0
      
      if cur_distance_from_bottom != 0:
         cur_bottom_percent = cur_distance_from_bottom / from_top_to_botom
      else:
         cur_bottom_percent = 0
      
      if cur_distance_from_left != 0:
         cur_left_percent = cur_distance_from_left / from_left_to_right
      else:
         cur_left_percent = 0
   
      lindex = len( boundaries_w_directions )
      boundaries_w_directions.append( [] )
   
      boundaries_w_directions[lindex].append( boundary_pixel )
   
      boundaries_w_directions[lindex].append( ( cur_top_percent, cur_right_percent, cur_bottom_percent, cur_left_percent ) )


   return boundaries_w_directions


# boundary1 is the one returned from boundary pixels
# [(158, 84), (159, 84), ... ]
# pixels1 and pixels2 are also the same form as above
#
# return set of xy
def get_attached_pixels( boundary1, pixels1, pixels2, image_size ):

   all_attached_pixels = set()
   for each_boundary1 in boundary1:
      # nbr_pixels -> [(102, 122), (103, 122), ...]
      nbr_pixels = pixel_functions.get_nbr_pixels(each_boundary1, image_size, input_xy=True)

      # removing pixels that are inside pixels1
      nbr_pixels_rm = set( nbr_pixels ).difference( set( pixels1 ) )
      
      attached_pixels = nbr_pixels_rm.intersection( set( pixels2 ) )

      all_attached_pixels |= attached_pixels

   return all_attached_pixels





# this function first takes where im1pixels attached at target_shape_bnd. likewise, it takes where im2pixels
# is attached at target2_shape_bnd. Then, it sees if the attachment of im1pixels is near the attachment of im2pixels
# 
#
# target_shape_bnd, target2_shape_bnd, im1pixels, and im2pixels are the ones returned from boundary pixels
# [(158, 84), (159, 84), ... ]
#
#
def check_shape_attached_near( target_shape_bnd, im1pixels, target2_shape_bnd, im2pixels, image_size ):
   # [[(158, 84), (0.0, 0.47368421052631576, 1.0, 0.5263157894736842)], ... ]
   # [ [ ( x,y ), ( top percentage, right percentage, bottom percentage, left percentage ) ], ... ]
   shape_bnd_w_dirct = get_bnd_pix_w_directions(target_shape_bnd)
   
   shape_bnd_w_direct2 = get_bnd_pix_w_directions(target2_shape_bnd)

   im_attached_pixels = [[], []]
   for im_index, im_pixels in enumerate( [im1pixels, im2pixels] ):
      cur_attached_pixels = set()

      for pixel in im_pixels:
         nbr_pixels = pixel_functions.get_nbr_pixels(pixel, image_size, input_xy=True)
         
         if im_index == 0:
            attached_pixels = set(nbr_pixels).intersection( set(target_shape_bnd) )
         else:
            attached_pixels = set(nbr_pixels).intersection( set(target2_shape_bnd) )
      
         if len( attached_pixels ) >= 1:
            cur_attached_pixels |= attached_pixels
   

      for pixel in cur_attached_pixels:
         if im_index == 0:
            attached_pixel = [ temp_pixel for temp_pixel in shape_bnd_w_dirct if temp_pixel[0] == pixel ][0]
         else:
            attached_pixel = [ temp_pixel for temp_pixel in shape_bnd_w_direct2 if temp_pixel[0] == pixel ][0]
   
         im_attached_pixels[im_index].append( attached_pixel )


   attached_near = _check_shape_attached_near( im_attached_pixels[0], im_attached_pixels[1] )
      
   return attached_near




# im1bnd_w_directions -> [ [(153, 87), (0.13043478260869565, 0.7368421052631579, 0.8695652173913043, 0.2631578947368421)], ... ]
#                        [ [ ( x,y ),  ( top percentage, right percentage, bottom percentage, left percentage ) ], ... ]
def _check_shape_attached_near( im1bnd_w_directions, im2bnd_w_directions ):
   # 25% or more pixels have to be near to be judged as match
   
   attch_percent_threshold = 0.25
   match_count_threshold = 0.25

   match_counter = 0
   already_matched_im2pix = []
   for im1pixel_w_direct in im1bnd_w_directions:
      im1top = im1pixel_w_direct[1][0]
      im1right = im1pixel_w_direct[1][1]

      for im2pixel_w_direct in im2bnd_w_directions:
         if im2pixel_w_direct in already_matched_im2pix:
            continue
            
         im2top = im2pixel_w_direct[1][0]
         im2right = im2pixel_w_direct[1][1]
   
         top_diff = abs( im1top - im2top )
         right_diff = abs( im1right - im2right )
         
         if top_diff + right_diff < attch_percent_threshold:
            already_matched_im2pix.append( im2pixel_w_direct )
            match_counter += 1
            break
      
   if match_counter != 0 and match_counter / len( im1bnd_w_directions ) >= match_count_threshold:
      return True

   
   return False




# orig_pixels, comp_pixels parameter form is....
#    [(28, 0), ...] or set of xy
#
# returns False or None if any pixel of orig_pixels is not neighbor with any pixel of comp_pixels
# returns matched orig and comp index numbers
# returns { orig1: orig index, comp1: comp index, orig2: orig index, comp2: comp index..... }

def find_direct_neighbors(orig_pixels, comp_pixels):

   original_smallest_y = min(int( xy[1] ) for xy in orig_pixels)
   original_largest_y = max(int( xy[1] ) for xy in orig_pixels)
   original_smallest_x = min(int( xy[0] ) for xy in orig_pixels)
   original_largest_x = max(int( xy[0] ) for xy in orig_pixels)   
   
   
   
   # original shape's neighbor will be somewhere between original_smallest_y - 1 and original_largest_y + 1
   orig_neighbor_top = original_smallest_y - 1
   orig_neighbor_bottom = original_largest_y + 1
   orig_neighbor_left = original_smallest_x - 1
   orig_neighbor_right = original_largest_x + 1
   
   comp_smallest_y = min(int(xy[1]) for xy in comp_pixels)
   comp_largest_y = max(int( xy[1] ) for xy in comp_pixels)
   comp_smallest_x = min(int( xy[0] ) for xy in comp_pixels)
   comp_largest_x = max(int( xy[0] ) for xy in comp_pixels) 
   
   maybe_neighbors_y = False
   maybe_neighbors_x = False

   # when compare shape is above original shape, compare shape's bottom has to be at the same place or below original top.
   if comp_smallest_y <= orig_neighbor_top and comp_largest_y >= orig_neighbor_top:
      maybe_neighbors_y = True
   
   # when compare shape is below original shape then compare shape's top has to be at the same place or above original shape's 
   # bottom
   elif comp_smallest_y > orig_neighbor_top and comp_smallest_y <= orig_neighbor_bottom:
      maybe_neighbors_y = True
      
   # when comapre shape is at the same place or further left than original shape, compare shape's right has to be at the same 
   # place or further right than original shape's left 
   if comp_smallest_x <= orig_neighbor_left and comp_largest_x >= orig_neighbor_left:
      maybe_neighbors_x = True
      
   # when compare shape is at the same place or further right than original shape, compare shape's left has to be at the same 
   # place or further left than the original shape's right
   elif comp_smallest_x > orig_neighbor_left and comp_smallest_x <= orig_neighbor_right:
      maybe_neighbors_x = True
   
   if (not maybe_neighbors_y) or (not maybe_neighbors_x):
      return False

   # all found direct neighbors
   found_neighbors = set()
   found_neighbor_flag = False
   
   for orig_pixel in orig_pixels:
      for comp_pixel in comp_pixels:
  
         # looking for top direct neighbor
         # if current pixel is ( current x, y )  then direct top neighbor is ( top x, y - 1)
         if comp_pixel[0] == orig_pixel[0] and comp_pixel[1] == orig_pixel[1] - 1:
            found_neighbors.add( orig_pixel )
            found_neighbors.add( comp_pixel )
            found_neighbor_flag = True
         
         # looking for top right direct neighbor
         # if current pixel is  ( current x, y ) then direct top right neighbor is ( top right x + 1, y - 1 )
         if comp_pixel[0] == orig_pixel[0] + 1 and comp_pixel[1] == orig_pixel[1] - 1:
            found_neighbors.add( orig_pixel )
            found_neighbors.add( comp_pixel )
            found_neighbor_flag = True
         
         # looking for direct right neighbor
         # if current pixel is ( current x, y )  then direct right neighbor is ( right x + 1, y )
         if comp_pixel[0] == orig_pixel[0] + 1 and comp_pixel[1] == orig_pixel[1]:
            found_neighbors.add( orig_pixel )
            found_neighbors.add( comp_pixel )
            found_neighbor_flag = True
         
         # looking for direct bottom right neighbor
         # if current pixel is  ( current x, y )  then direct bottom right neighbor is ( bottom right x + 1, y + 1 )
         if comp_pixel[0] == orig_pixel[0] + 1 and comp_pixel[1] == orig_pixel[1] + 1:
            found_neighbors.add( orig_pixel )
            found_neighbors.add( comp_pixel )
            found_neighbor_flag = True
         
         # looking for direct bottom neighbor
         # if current pixel is ( current x, y )  then direct bottom neighbor is ( bottom x, y + 1 )
         if comp_pixel[0] == orig_pixel[0] and comp_pixel[1] == orig_pixel[1] + 1:
            found_neighbors.add( orig_pixel )
            found_neighbors.add( comp_pixel )
            found_neighbor_flag = True
         
         # looking for direct bottom left neighbor
         # if current pixel is ( current x, y )  then direct bottom left neighbor is ( bottom x - 1, y + 1 )
         if comp_pixel[0] == orig_pixel[0] - 1 and comp_pixel[1] == orig_pixel[1] + 1:
            found_neighbors.add( orig_pixel )
            found_neighbors.add( comp_pixel )
            found_neighbor_flag = True
         
         # looking for direct left neighbor
         # if current pixel is ( current x, y )  then direct left neighbor is ( bottom x - 1, y )
         if comp_pixel[0] == orig_pixel[0] - 1 and comp_pixel[1] == orig_pixel[1]:
            found_neighbors.add( orig_pixel )
            found_neighbors.add( comp_pixel )
            found_neighbor_flag = True
         
         # looking for direct top left neighbor
         # if current pixel is ( current x, y )  then direct top left neighbor is ( bottom x - 1, y - 1 )
         if comp_pixel[0] == orig_pixel[0] - 1 and comp_pixel[1] == orig_pixel[1] - 1:
            found_neighbors.add( orig_pixel )
            found_neighbors.add( comp_pixel )
            found_neighbor_flag = True
         
   if found_neighbor_flag: 
      return found_neighbors
   else:
      return


# min_colors has only about 30 colors. so every shape has only one color or a few color variations. 
# so for min_colors, get most abundant colors in the shape
def get_all_shapes_colors(filename, directory, shapes_type=None, min_colors=False):

   # directory is specified but does not contain /
   if directory != "" and directory[-1] != ('/'):
      directory +='/'

   image_file = top_images_dir + directory + filename + '.png'

   read_image = Image.open(image_file)
   image_width, image_height = read_image.size
   image_pixels = read_image.getdata()

   shapes_colors = {}

   if shapes_type == "normal":
      whole_image_shapes = read_files_functions.rd_shapes_file(filename, directory)

      for shape_id , pixel_xy_values in whole_image_shapes.items():
         shapes_colors[shape_id] = tuple()
    
         # for storing RGB values for each shape. Initializing for each shape
         Reds = []
         Greens = []
         Blues = []
    
         pixels_color_counter = 0
         for pixel_id in pixel_xy_values:

            image_index = pixel_xy_values[pixel_id]['y'] * image_width + pixel_xy_values[pixel_id]['x']

            r, g, b = image_pixels[ image_index ]

            Reds.append(r)
            Greens.append(g)
            Blues.append(b)

            # maximum sample counts of each shape is 100
            if pixels_color_counter > 100:
                break
            pixels_color_counter += 1
         
         if min_colors is False:
         
            r = round(mean(Reds))
            g = round(mean(Greens))
            b = round(mean(Blues))
         else:
            r = max(set(Reds), key = Reds.count)
            g = max(set(Greens), key = Greens.count)
            b = max(set(Blues), key = Blues.count)
       
         shapes_colors[shape_id] = ( r, g, b )

      return shapes_colors


   elif shapes_type == "intnl_spixcShp":
      s_pixcShp_intnl_dir = top_shapes_dir + directory + spixc_shapes + "/" + internal + "/"

      shapes_dfile = s_pixcShp_intnl_dir + "shapes/" + filename + "shapes.data"
      with open (shapes_dfile, 'rb') as fp:
         # { '79999': ['79999', ... ], ... }
         # { 'shapeid': [ pixel indexes ], ... }
         im_shapes = pickle.load(fp)
      fp.close()

      for shape_id , pixels in im_shapes.items():
         shapes_colors[shape_id] = tuple()
    
         # for storing RGB values for each shape. Initializing for each shape
         Reds = []
         Greens = []
         Blues = []
    
         pixels_color_counter = 0
         for pixel in pixels:

            r, g, b = image_pixels[ int(pixel) ]

            Reds.append(r)
            Greens.append(g)
            Blues.append(b)

            # maximum sample counts of each shape is 100
            if pixels_color_counter > 100:
                break
            pixels_color_counter += 1
          
         if min_colors is False:
         
            r = round(mean(Reds))
            g = round(mean(Greens))
            b = round(mean(Blues))
         else:
            r = max(set(Reds), key = Reds.count)
            g = max(set(Greens), key = Greens.count)
            b = max(set(Blues), key = Blues.count)
       
         shapes_colors[shape_id] = ( r,  g,  b )

      return shapes_colors



   else:
      print("ERROR at pixel_shapes_functions:get_all_shapes_colors not supported shapes_type " + shapes_type )
      sys.exit()



# get shapes positions in shape coordinate and not image coordinate
#
# shapes -> {shapeid: [ shape pixels ], shapeid: [ shape pixels ], ... }
# shape pixels are indexes
# above is param_shp_type is 0
# below is param_shp_type is 1
# shapes -> {'5537': [(337, 13), ... }
#           { shapeid: [ (x,y), ... ], ...  }
# 
# shapes_colors is the one returned by get_all_shapes_colors
# 
# returns { shapeid: [ (r,g,b),(x,y),(x,y),... ], shapeid: [ (r,g,b),(x,y), ... ], ... }
# x,y and r,g,b are all integers
def get_shapes_pos_in_shp_coord( shapes, im_width, shapes_colors, param_shp_type=None ):
   shp_coord_shapes = {}
   all_pixel_xy = []
   
   if param_shp_type == 0:
   
      all_pixels = []
      for shapeid in shapes:
         all_pixels.extend( shapes[shapeid] )

      # convert all pixels from indexes to xy
      for pindex in all_pixels:
         xy = pixel_functions.convert_pindex_to_xy( pindex, im_width )
      
         all_pixel_xy.append( xy )
   
   elif param_shp_type == 1:
      for shapeid in shapes:
         all_pixel_xy.extend( shapes[shapeid] )   
      
      
   smallest_x = min( [ xy[0] for xy in all_pixel_xy ] )
   smallest_y = min( [ xy[1] for xy in all_pixel_xy ] )


   shp_coord_x_es = [ xy[0] - smallest_x for xy in all_pixel_xy ]
   shp_coord_y_s = [ xy[1] - smallest_y for xy in all_pixel_xy ]
   
   pixel_index_iterator = 0
   for shapeid in shapes:
      cur_pix_len = len( shapes[shapeid] )
      shp_coord_shapes[shapeid] = []
      shape_iterator = 0
      for pixel in all_pixel_xy:
         if cur_pix_len == 0:
            break
         
         if shape_iterator == 0:
            shp_coord_shapes[shapeid].append( shapes_colors[shapeid] )
         
         shp_coord_shapes[shapeid].append( ( shp_coord_x_es[pixel_index_iterator], shp_coord_y_s[pixel_index_iterator] ) )
         
         shape_iterator += 1
         cur_pix_len -= 1
         pixel_index_iterator += 1
         
   
   smallest_xy = ( smallest_x, smallest_y )
   
   return shp_coord_shapes, smallest_xy



# get shape positions in shape coordinate and not image coordinate
#
# shape_pixels -> [ shape pixels ]
# shape_pixels are indexes
# above is param_shp_type is 0
# below is param_shp_type is 1
# shape_pixels -> [(337, 13), ... ]
#          [ (x,y), ... ]
# 
# returns [ ( x,y ), (x,y), ... ]
# x,y and r,g,b are all integers
def get_shape_pos_in_shp_coord( shape_pixels, im_width, param_shp_type=None ):
   shp_coord_shapes = {}
   all_pixel_xy = []
   
   if param_shp_type == 0:

      # convert all pixels from indexes to xy
      for pindex in shape_pixels:
         xy = pixel_functions.convert_pindex_to_xy( pindex, im_width )
      
         all_pixel_xy.append( xy )
   
   elif param_shp_type == 1:
      all_pixel_xy = shape_pixels
      
      
   smallest_x = min( [ xy[0] for xy in all_pixel_xy ] )
   smallest_y = min( [ xy[1] for xy in all_pixel_xy ] )


   shp_coord_xy = [ ( xy[0] - smallest_x, xy[1] - smallest_y )  for xy in all_pixel_xy ]

   return shp_coord_xy




# input parameter
# shape_boundary is the shape boundary pixels returned by get_boundary_pixels
# {1: {'x': 190, 'y': 30}, 2: {'x': 190, 'y': 31},.... }
# above shape_boundary is used when param_shp_type is 0
#
# below shape_boundary is used when param_shp_type is 1
# [ (x,y), (x,y) ... ] or { (x,y), (x,y) ... }
# 
# vicinity_value is how many pixels for shape to be expanded.
# vicinity_value is integer

# return value. vicinity_pixels
# return form is set of tuples
# {(231, 63), (244, 82), ... }
# { ( x, y ), ( x, y ), ... }
def get_shape_vicinity_pixels( shape_boundary, vicinity_value, image_size, param_shp_type ):
   vicinity_pixels = set() 
   
   if param_shp_type == 0:
      for boundary_pixel in shape_boundary.values():
         vicinity_pixels |= set( pixel_functions.get_vicinity_pixels( boundary_pixel, vicinity_value, image_size) )
   
   elif param_shp_type == 1:
      for boundary_pixel in shape_boundary:
         vicinity_pixels |= set( pixel_functions.get_vicinity_pixels( boundary_pixel, vicinity_value, image_size) )


   return vicinity_pixels


   


# shape_coordinates can be either of the two forms
# {27273: {'x': 93, 'y': 151}, 27453: {'x': 93, 'y': 152}, 27452: {'x': 92, 'y': 152}, 27632: {'x': 92, 'y': 153}}
#  { ( x, y ), ( x, y ), ... }
# returns
# { "shapeid number": [ image_area number, image_area number ... ] }
def localize_shape( shape_coordinates , image_areas , shapeid ):

   if type( shape_coordinates ) is dict:
      shape_locations = shape_coordinates.values()
   elif type( shape_coordinates ) is set or type( shape_coordinates ) is list:
      shape_locations = shape_coordinates

   shape_in_image_areas = []
   
   location_threshold = 3  
   
   location_labels = [ { 'top_middle': {'y_threshold': ( - location_threshold ), 'x_threshold': ( location_threshold, - location_threshold ) }, \
                      'right': { 'y_threshold': ( location_threshold, - location_threshold ), 'x_threshold': ( location_threshold ) }, \
                      'bottom_middle': { 'y_threshold': ( location_threshold ), 'x_threshold': ( location_threshold, - location_threshold ) }, \
                      'left': { 'y_threshold': ( location_threshold, - location_threshold ), 'x_threshold': ( - location_threshold ) } } ]

   
   for shape_location in shape_locations:
      # image_areas -> {integer area number: ( left, right, top, bottom )
      for area_num, image_loc in image_areas.items():
            area_num = str(area_num)
            cur_area_present = False
            if shape_in_image_areas:
               for shape_in_image_area in shape_in_image_areas:
                  if shape_in_image_area['image_area'] == area_num:
                     cur_area_present = True
                     
                     break
            
            if cur_area_present:
               continue
               
            image_shape_loc_match = False
            
            for location_label in location_labels:
               if image_shape_loc_match:
                  break
               for loc_label, thresholds in location_label.items():
                  if image_shape_loc_match:
                     break               

                  if type(shape_location) is dict:
                     if shape_location['x'] >= image_loc[0] and shape_location['x'] <= image_loc[1]:
                        if shape_location['y'] >= image_loc[2] and shape_location['y'] <= image_loc[3]:
                           image_shape_loc_match = True
                     
                           temp = {}
                           temp['shapeid'] = shapeid
                           temp['image_area'] = area_num
                        
                           shape_in_image_areas.append( temp )
                    
                           break
               
                     # if there is only one threshold, it becomes int value only. if there is two, it would be tuple
                     if type(thresholds['x_threshold']) != int:
                        for x_threshold in thresholds['x_threshold']:                
               
                           if not image_shape_loc_match:
                              # check with the threshold
                              if shape_location['x'] + x_threshold >= image_loc[0] and shape_location['x'] + x_threshold <= image_loc[1]:
                                 if shape_location['y'] >= image_loc[2] and shape_location['y'] <= image_loc[3]:
                                    image_shape_loc_match = True
                     
                                    temp = {}
                                    temp['shapeid'] = shapeid
                                    temp['image_area'] = area_num
                     
                                    shape_in_image_areas.append( temp )
                        
                                    break

                     if type( thresholds['y_threshold'] ) != int :
                        for y_threshold in thresholds['y_threshold']:
   
                           if not image_shape_loc_match:
                              # check with the threshold
                              if shape_location['x']  >= image_loc[0] and shape_location['x'] <= image_loc[1]:
                                 if shape_location['y'] + y_threshold >= image_loc[2] and shape_location['y'] + y_threshold <= image_loc[3]:
                                    image_shape_loc_match = True
                    
                                    temp = {}
                                    temp['shapeid'] = shapeid
                                    temp['image_area'] = area_num
                     
                                    shape_in_image_areas.append( temp )
                        
                                    break   


                  if type(shape_location) is tuple:
                     if shape_location[0] >= image_loc[0] and shape_location[0] <= image_loc[1]:
                        if shape_location[1] >= image_loc[2] and shape_location[1] <= image_loc[3]:
                           image_shape_loc_match = True
                     
                           temp = {}
                           temp['shapeid'] = shapeid
                           temp['image_area'] = area_num
                        
                           shape_in_image_areas.append( temp )
                    
                           break
               
                     # if there is only one threshold, it becomes int value only. if there is two, it would be tuple
                     if type(thresholds['x_threshold']) != int:
                        for x_threshold in thresholds['x_threshold']:                
               
                           if not image_shape_loc_match:
                              # check with the threshold
                              if shape_location[0] + x_threshold >= image_loc[0] and shape_location[0] + x_threshold <= image_loc[1]:
                                 if shape_location[1] >= image_loc[2] and shape_location[1] <= image_loc[3]:
                                    image_shape_loc_match = True
                     
                                    temp = {}
                                    temp['shapeid'] = shapeid
                                    temp['image_area'] = area_num
                     
                                    shape_in_image_areas.append( temp )
                        
                                    break

                     if type( thresholds['y_threshold'] ) != int :
                        for y_threshold in thresholds['y_threshold']:
   
                           if not image_shape_loc_match:
                              # check with the threshold
                              if shape_location[0]  >= image_loc[0] and shape_location[0] <= image_loc[1]:
                                 if shape_location[1] + y_threshold >= image_loc[2] and shape_location[1] + y_threshold <= image_loc[3]:
                                    image_shape_loc_match = True
                    
                                    temp = {}
                                    temp['shapeid'] = shapeid
                                    temp['image_area'] = area_num
                     
                                    shape_in_image_areas.append( temp )
                        
                                    break   

   
   # currently shape_in_image_areas have following form
   # [{'shapeid': '30184', 'image_area': 5}, {'shapeid': '30184', 'image_area': 10}]
   # this should be in following form
   # { "shapeid number": [ image_area number, image_area number ... ] }
   shape_im_areas = {}
   im_a_shapeid = None
   for shape_in_image_area in shape_in_image_areas:
      for sid_or_im_a in shape_in_image_area:
         if len(shape_im_areas) == 0 and sid_or_im_a == "shapeid":
            im_a_shapeid = shape_in_image_area[sid_or_im_a]
            shape_im_areas[ im_a_shapeid ] = []
            
            
         
         elif sid_or_im_a == "image_area":
            shape_im_areas[im_a_shapeid].append( shape_in_image_area[sid_or_im_a] )
   
   return shape_im_areas




   

# orig_coords and comp_coords have the following form
# {'179': {'x': 179, 'y': 0}} single pixel
# multiple pixels
# {27273: {'x': 93, 'y': 151}, 27453: {'x': 93, 'y': 152}, 27452: {'x': 92, 'y': 152}, 27632: {'x': 92, 'y': 153}}
# shape_ids are original and compare shapeid
# shape_ids is as follows
# shape_ids = [ int('550' ), int ('179') ]
# returns locations list if they are close, if not, returns empty list
def are_shapes_near(orig_file, comp_file, directory, orig_coords, comp_coords, shape_ids ):


   # needed for creating image areas
   original_image = Image.open(top_images_dir + directory + orig_file + ".png")
   image_width, image_height = original_image.size

   compare_image = Image.open(top_images_dir + directory + comp_file + ".png")
   compare_image_width, compare_image_height = compare_image.size

   # make sure original image size(width, height) is exactly the same as compare image size(width, height)
   if not (image_width == compare_image_width and image_height == compare_image_height):
      return False

   image_areas = image_functions.get_image_areas( im_file, directory )

      
   orig_locations = localize_shape( orig_coords , image_areas , shape_ids[0] )

   orig_image_areas = []
      
   for orig_location in orig_locations:
      orig_image_areas.append( orig_location['image_area'] )

   comp_locations = localize_shape( comp_coords , image_areas , shape_ids[1] )
   
   matched_areas = []
   for comp_location in comp_locations.values():
      for orig_image_area in orig_image_areas.values():
            
         for comp_loc in comp_location:
            if comp_loc in orig_image_area:
               matched_areas.append( comp_loc )
                
         
   if matched_areas:
      temp = {}
      temp['orig_shapeid'] = shape_ids[0]
      temp['comp_shapeid'] = shape_ids[1]
      temp["m_areas"] = []

      for matched_area in matched_areas:
         temp["m_areas"].append(matched_area)

      return temp
   else:
      return None





# shape_coords have the either of the following forms
# {'179': {'x': 179, 'y': 0}} single pixel
# multiple pixels
# {27273: {'x': 93, 'y': 151}, 27453: {'x': 93, 'y': 152}, 27452: {'x': 92, 'y': 152}, 27632: {'x': 92, 'y': 153}}
# shape_coords keys can be string or int. does not matter because shape_coords values are used only and keys are not used.
#
# { (93,151), (93,152), (92,152) }
# { (x,y), (x,y), (x,y) } or list of (x,y)
#
# shapeid is int.
def get_shape_im_locations( im_file, directory, shape_coords, shapeid ):
   image_areas = image_functions.get_image_areas( im_file, directory )

   shape_locations = localize_shape( shape_coords , image_areas , shapeid )

   return shape_locations










































































