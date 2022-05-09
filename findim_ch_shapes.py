

from PIL import Image
import re
import os, sys
from libraries import pixel_shapes_functions, read_files_functions, pixel_functions

from libraries.cv_globals import proj_dir

shapes_dir = proj_dir + "/shapes/"
images_dir = proj_dir + "/images/"


directory = "videos/cutveg"
im1file = "1clrgrp"
im2file = "2clrgrp"

# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'




im1 = Image.open("images/" + directory + im1file + ".png" )
im1pxls = im1.getdata()
im1width, im1height = im1.size

im2 = Image.open("images/" + directory + im2file + ".png" )
im2pxls = im2.getdata()
im2width, im2height = im2.size


# returned value has below form
# { { { } } }
# shapes[shapes_id][pixel_index] = {}
# shapes[shapes_id][pixel_index]['x'] = x
# shapes[shapes_id][pixel_index]['y'] = y
# these will be used for location data. pixel indexes are locations.
im1shape_pindexes = read_files_functions.rd_shapes_file(im1file, directory)

im2shape_pindexes = read_files_functions.rd_shapes_file(im2file, directory)

# dictionary key is shapeid, dictionary data is shape rgb
im1shape_clrs = pixel_shapes_functions.get_all_shapes_colors(im1file, directory)

im2shape_clrs = pixel_shapes_functions.get_all_shapes_colors(im2file, directory)

im1nbr_filepath = shapes_dir + directory + "shape_nbrs/" + im1file + "_shape_nbrs.txt"

# list contains dictionary. dictionary key is shapeid. dictionary data is list of neighbor shapeids.
im1shape_nbrs = read_files_functions.rd_ldict_k_v_l(im1file, directory, im1nbr_filepath)

im2nbr_filepath = shapes_dir + directory + "shape_nbrs/" + im2file + "_shape_nbrs.txt"

im2shape_nbrs = read_files_functions.rd_ldict_k_v_l(im2file, directory, im2nbr_filepath)


im1shape_locations_path = shapes_dir + directory + "locations/" + im1file + "_loc.txt"
im2shape_locations_path = shapes_dir + directory + "locations/" + im2file + "_loc.txt"

im1shape_in_im_areas = read_files_functions.rd_ldict_k_v_l( im1file, directory, im1shape_locations_path )
im2shape_in_im_areas = read_files_functions.rd_ldict_k_v_l( im2file, directory, im2shape_locations_path )

im1shapes_in_im_areas = {}
for shapeid in im1shape_pindexes:
   
   for s_locs in im1shape_in_im_areas:
      if shapeid in s_locs.keys():
         im1shapes_in_im_areas[shapeid] = s_locs[ list(s_locs.keys())[0] ]
         break


im2shapes_in_im_areas = {}
for shapeid in im2shape_pindexes:
   
   for s_locs in im2shape_in_im_areas:
      if shapeid in s_locs.keys():
         im2shapes_in_im_areas[shapeid] = s_locs[ list(s_locs.keys())[0] ]
         break



# this will contain shape locations, colors, and their neighbors colors. 
# { shapeid: [ [ pixel indexes ], shape_color_rgb, [ neighbor1_rgb, neighbor2_rgb, ... ] ] , shapeid: [ [ ... ], ... [ ... ] ] }
im1_shapes = {}
im2_shapes = {}
im_shapes = [ im1_shapes, im2_shapes ]


im_orig_shapes = [ im1shape_pindexes, im2shape_pindexes ]

im_orig_shapes_clrs = [ im1shape_clrs, im2shape_clrs ]

im_orig_shapes_nbrs = [ im1shape_nbrs, im2shape_nbrs ]


for im_shape_counter in range( 0, 2 ):

   for shapeid in im_orig_shapes[ im_shape_counter ]:
      
      # current image shape initialization
      im_shapes[im_shape_counter][shapeid] = []
 
      shape_pixels = list( im_orig_shapes[ im_shape_counter ][ shapeid ].keys() )
      
      if not shape_pixels:
         print("ERROR. shapeid " + shapeid + " pixels were not found")
         sys.exit()
   
      im_shapes[im_shape_counter][shapeid].append( shape_pixels )

      shape_rgb = im_orig_shapes_clrs[ im_shape_counter ][shapeid]
      
      if not shape_rgb:
         print("ERROR. shapeid " + shapeid + " rgb was not found")
         sys.exit()
   
      im_shapes[im_shape_counter][shapeid].append( shape_rgb )

      # there is only one key "shapeid" in each dictionary inside im1shape_nbrs
      shape_nbrs = [ shape_nbrs[shapeid] for shape_nbrs in im_orig_shapes_nbrs[ im_shape_counter ]  if shapeid in shape_nbrs.keys() ][0]
      
      if not shape_nbrs:
         print("ERROR shapeid " + shapeid + " neighbors were not found")
         sys.exit()
      
      
      temp = []
      for shape_nbr in shape_nbrs:
         nbr_rgb = im_orig_shapes_clrs[ im_shape_counter ][shape_nbr]

         temp.append( nbr_rgb )
      
   
      
      im_shapes[im_shape_counter][shapeid].append( temp )
      
   

# image1 shape finds same shape in image2.
# image1 and 2 pixel counts are needed when multiple image2 shapes matched with location, rgb, and neighbor.
# { image1shapeid: { image2shapeid: image2shapeid , image1pixel count: image1pixel count, image2pixel count: image2pixel count }, 
#   image1shapeid: { image2shapeid: image2shapeid , image1pixel count: image1pixel count, image2pixel count: image2pixel count } }
im_same_shapes = {}

debug = False
progress_counter = len( im_shapes[1] )
for im2_shapeid, im2shape_list in im_shapes[1].items():
   im_same_shapes[im2_shapeid] = {}
   
   print(str(progress_counter) + " remaining")

   for im1_shapeid, im1shape_list in im_shapes[0].items():

      same_im_area = False
      for src_s_loc in im2shapes_in_im_areas[im2_shapeid]:
         if src_s_loc in im1shapes_in_im_areas[im1_shapeid]:
            same_im_area = True
      
      if not same_im_area:
         continue

   
      im1shape_indexes = im1shape_list[0]
      im1shape_rgb = im1shape_list[1]
      im1shape_nbrs_rgbs = im1shape_list[2]
      

      im2shape_indexes = im2shape_list[0]
      im2shape_rgb = im2shape_list[1]
      im2shape_nbrs_rgbs = im2shape_list[2]

      # check image1 image2 location match
      location_match = False
      for im1shape_index in im1shape_indexes:
         if im1shape_index in im2shape_indexes:
            location_match = True

      if not location_match:
         continue
      
      
      clrch, brit_thres, brit_ch_v = pixel_functions.compute_appearance_difference(im1shape_rgb , im2shape_rgb, 30 )
      
      
      if clrch or ( not brit_thres ) :
         # color changed or brightness not within threshold.
         continue


      neighbor_rgb_match = False
      for im1shape_nbr_rgb in im1shape_nbrs_rgbs:
         if im1shape_nbr_rgb in im2shape_nbrs_rgbs:
            neighbor_rgb_match = True
            
      if not neighbor_rgb_match:
         continue
      
      # pixel count has to match more than 80%
      needed_pcounts = len( im1shape_indexes ) * 0.2
      needed_pcounts_plus = needed_pcounts + len( im1shape_indexes )
      needed_pcounts_minus = len( im1shape_indexes ) - needed_pcounts
      
      if not ( len( im2shape_indexes ) < needed_pcounts_plus and len( im2shape_indexes ) > needed_pcounts_minus ):
         continue
      
      if debug:
         print("im1_shapeid " + im1_shapeid + " im2_shapeid " + im2_shapeid + " matched" )
         print()
      
      # check if current image1 shape matched with another image2 shape.
      if im_same_shapes[im2_shapeid]:
      
         im2pixel_counts = len( im2shape_indexes )
         found_im1pixel_counts = im_same_shapes[im2_shapeid]["im1pixel_counts"]
         
         cur_im1pixel_counts = len( im1shape_indexes )
         
         # check which image2 pixel counts is closest to image1pixel counts
         cur_im1pcount_diff = abs( im2pixel_counts - cur_im1pixel_counts )
         found_im1pcount_diff = abs( im2pixel_counts - found_im1pixel_counts )
         
         if cur_im1pcount_diff < found_im1pcount_diff:
            im_same_shapes[im2_shapeid]["im1shapeid"] = im1_shapeid
            im_same_shapes[im2_shapeid]["im1pixel_counts"] = len( im1shape_indexes )
            im_same_shapes[im2_shapeid]["im2pixel_counts"] = len( im2shape_indexes )            
               
         
      
      else:
         im_same_shapes[im2_shapeid]["im1shapeid"] = im1_shapeid
         im_same_shapes[im2_shapeid]["im1pixel_counts"] = len( im1shape_indexes )
         im_same_shapes[im2_shapeid]["im2pixel_counts"] = len( im2shape_indexes )

   if debug:
      # current image1 and image2 debug check ended
      print("im2_shapeid " + im2_shapeid)
      print(str( im_same_shapes[im2_shapeid] ) )
      print()
      sys.exit()

   progress_counter -= 1



all_im2same_shapes = []

for im2shapeid in im_same_shapes:
   # if "not" for changed shapes.  for stayed shapes, if without not.
   if not im_same_shapes[im2shapeid]:
      all_im2same_shapes.append( im2shapeid )


pixel_shapes_functions.cr_im_from_shapeslist( im2file, directory, all_im2same_shapes, "changed_shapes", background_rgb=(255,255,255) )






