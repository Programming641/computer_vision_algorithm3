# find small pixel count shapes neigbor to large shapes boundries
# image shapes used are from shapes which incorporate internal small pixel count shapes.
# 
from libraries import pixel_functions, image_functions, read_files_functions, pixel_shapes_functions

from PIL import Image
import os, sys
import pickle
import math

from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir


image_filename = '10'

directory = "videos/street3/resized/min"


recreate_images = False

if len(sys.argv) > 1:
   image_filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]

   directory = sys.argv[1]

   print("execute script find_same_clr_shapes.py. filename " + image_filename + " directory " + directory )

if directory != "" and directory[-1] != '/':
   directory +='/'

s_pixc_shapes_dir = top_shapes_dir + directory + "s_pixc_shapes/"
main_dir = s_pixc_shapes_dir + "nbr2Lshp_bnd/"
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
pix_counts_w_shapes = image_functions.get_image_stats( image_filename, directory, shapes_type="intnl_spixcShp" )

print("preparing data...")

small_pixc_shapes = []
Lshapes = []
for pixel_count in pix_counts_w_shapes:

   if pixel_count < 50:
      small_pixc_shapes.extend( pix_counts_w_shapes[ pixel_count ] )
   else:
      Lshapes.extend( pix_counts_w_shapes[ pixel_count ] )
   

Lshapes_boundaries = {}
# get boundary pixels of large pixel count shapes
for Lshapeid in Lshapes:
   Lshapes_boundaries[Lshapeid] = pixel_shapes_functions.get_boundary_pixels(im_shapes[Lshapeid] )


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


print("main process begins. please wait")

small_pixc_nbr2Lshp_bnd = {}
for small_pixc_shapeid in small_pixc_shapes:
   
   small_pixc_nbr2Lshp_bnd[small_pixc_shapeid] = []
   
   cur_s_pixc_shp_locations = small_pixc_shapes_im_areas[small_pixc_shapeid]
   
   for Lshapeid in Lshapes:
      
      # check if current small pixel count shape is located in the same image area as current large shape
      cur_Lshape_locations = Lshapes_im_areas[Lshapeid]
      
      check = any(im_area in cur_s_pixc_shp_locations for im_area in cur_Lshape_locations)

      if not check:
         continue
      
      for small_pixc_pindex in im_shapes[small_pixc_shapeid]:
         
         # get neighbor pixels of current small pixel count pixel index
         p_neighbors = pixel_functions.get_nbr_pixels( small_pixc_pindex, original_image.size )

         # current small pixel count shape's pixel index is neighbor to large shape's boundary
         found = False
         for p_neighbor in p_neighbors:
         
            y = math.floor( int(p_neighbor) / im_width)
            x  = int(p_neighbor) % im_width

            xy = { 'x': x, 'y': y }            
            
            for Lshape_bnd_pixel in Lshapes_boundaries[Lshapeid].values():
               if Lshape_bnd_pixel == xy:
                  small_pixc_nbr2Lshp_bnd[small_pixc_shapeid].append( small_pixc_pindex )
                  
                  found = True
                  break
            
            if found:
               break
   
   if len( small_pixc_nbr2Lshp_bnd[small_pixc_shapeid] ) == 0:
      small_pixc_nbr2Lshp_bnd.pop(small_pixc_shapeid)


print( small_pixc_nbr2Lshp_bnd )

with open(main_dfile, 'wb') as fp:
   pickle.dump(small_pixc_nbr2Lshp_bnd, fp)
fp.close()







































