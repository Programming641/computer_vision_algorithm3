# find internal small pixel count shapes.
# if a small pixel count shape is entirely surrounded by one large shape, then it is the internal pixels of the one large shape.
from libraries import pixel_functions, image_functions, read_files_functions, pixel_shapes_functions

from PIL import Image
import os, sys
import pickle
import math

from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir


image_filename = '24'

directory = "videos/giraffe/min"


recreate_images = False

if len(sys.argv) > 1:
   image_filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]

   directory = sys.argv[1]

   print("execute script find_same_clr_shapes.py. filename " + image_filename + " directory " + directory )

if directory != "" and directory[-1] != '/':
   directory +='/'

s_pixc_shapes_dir = top_shapes_dir + directory + "s_pixc_shapes/"
main_dir = s_pixc_shapes_dir + "internal/"
main_data_dir = main_dir + "data/"
main_dfile = main_data_dir + image_filename + ".data"

if os.path.exists(s_pixc_shapes_dir ) == False:
   os.makedirs(s_pixc_shapes_dir)
if os.path.exists(main_dir ) == False:
   os.makedirs(main_dir)
if os.path.exists(main_data_dir ) == False:
   os.makedirs(main_data_dir)

original_image = Image.open(top_images_dir + directory + image_filename + ".png")
im_width, im_height = original_image.size

# returned value has below form
# shapes[shapes_id][pixel_index] = {}
# shapes[shapes_id][pixel_index]['x'] = x
# shapes[shapes_id][pixel_index]['y'] = y
im_shapes = read_files_functions.rd_shapes_file(image_filename, directory)

# getting small pixel count shapes
pix_counts_w_shapes = image_functions.get_image_stats( image_filename, directory )

print("preparing data...")

small_pixc_shapes = []
Lshapes = []
for pixel_count in pix_counts_w_shapes:

   if pixel_count < 50:
      small_pixc_shapes.extend( pix_counts_w_shapes[ pixel_count ] )
   else:
      Lshapes.extend( pix_counts_w_shapes[ pixel_count ] )


shapes_locations_path = top_shapes_dir + directory + "locations/" + image_filename + "_loc.txt"
shapes_locations = read_files_functions.rd_ldict_k_v_l( image_filename, directory, shapes_locations_path )



small_pixc_shapes_im_areas = {}
for shapeid in small_pixc_shapes:
   
   for s_locs in shapes_locations:
      if shapeid in s_locs.keys():
         small_pixc_shapes_im_areas[shapeid] = s_locs[ list(s_locs.keys())[0] ]
         break
Lshapes_im_areas = {}
for shapeid in Lshapes:
   
   for s_locs in shapes_locations:
      if shapeid in s_locs.keys():
         Lshapes_im_areas[shapeid] = s_locs[ list(s_locs.keys())[0] ]
         break


s_pixc_shapes_boundaries = {}
# get boundary pixels of large pixel count shapes
for shapeid in small_pixc_shapes:
   s_pixc_shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels(im_shapes[shapeid] )







print("main process begins. please wait")

internal_s_pixc_shapes = []
for small_pixc_shapeid in small_pixc_shapes:

   cur_s_pixc_shp_locations = small_pixc_shapes_im_areas[small_pixc_shapeid]
   
   cur_s_pixc_boundaries = []
   for xy in s_pixc_shapes_boundaries[small_pixc_shapeid].values():
      pixel_index = ( xy['y'] * im_width )+ xy['x']
      cur_s_pixc_boundaries.append( str( pixel_index ) )
   
   
   for Lshapeid in Lshapes:
      
      # check if current small pixel count shape is located in the same image area as current large shape
      cur_Lshape_locations = Lshapes_im_areas[Lshapeid]
      
      check = any(im_area in cur_s_pixc_shp_locations for im_area in cur_Lshape_locations)

      if not check:
         continue
      
      # getting all pixels of current large shape
      cur_Lshape_pixels = list(im_shapes[Lshapeid].keys())
      
      # check if all boundary pixels of current small pixel count shape are neighbor to current large shape
      match_counter = 0
      cur_boundaries_total = len( cur_s_pixc_boundaries )
      for small_pixc_pindex in cur_s_pixc_boundaries:
         
         # get neighbor pixels of current small pixel count pixel index
         p_neighbors = pixel_functions.get_nbr_pixels( small_pixc_pindex, original_image.size )

         # check if current pixel is neighbor to current larege shape
         # first, convert p_neighbors to list of strings
         p_neighbors = [str(pindex) for pindex in p_neighbors]
         
         check =  any(pindex in cur_Lshape_pixels for pindex in p_neighbors)

         if check:
            # current pixel is neighbor to current large shape
            match_counter += 1
       
      if match_counter == cur_boundaries_total:
         # current small pixel count shape is surrounded entirely by current large shape
         internal_s_pixc_shapes.append( ( small_pixc_shapeid, Lshapeid ) )
         # if current small pixel count shape is surrounded by current large shape then, it also means that 
         # any other large shape will not be neighbor current small pixel count shape. so end it
         break
         


print( internal_s_pixc_shapes )

with open(main_dfile, 'wb') as fp:
   pickle.dump(internal_s_pixc_shapes, fp)
fp.close()







































