# find internal small pixel count shapes.
# if a small pixel count shape is entirely surrounded by one bigger shape, then it is the internal pixels of the one bigger shape.
from libraries import pixel_functions, image_functions, read_files_functions, pixel_shapes_functions

from PIL import Image
import os, sys
import pickle
import math

from libraries.cv_globals import top_shapes_dir, top_images_dir, internal
from help_lib import create_shape_locations, create_shape_neighbors


image_filename = '14'

directory = "videos/street3/resized/min"

shapes_type = "intnl_spixcShp"


if len(sys.argv) > 1:
   image_filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]

   directory = sys.argv[1]

   print("execute script find_same_clr_shapes.py. filename " + image_filename + " directory " + directory )

if directory != "" and directory[-1] != '/':
   directory +='/'

s_pixc_shapes_dir = top_shapes_dir + directory + "spixc_shapes/"
main_dir = s_pixc_shapes_dir + internal + "/"
main_data_dir = main_dir + "data/"
main_dfile = main_data_dir + image_filename + ".data"

main_loc_dir = main_dir + "locations/"

main_shapes_dir = main_dir + "shapes/"
main_shapes_dfile = main_shapes_dir + image_filename + "shapes.data"

main_shape_nbrs_dir = main_dir + "shape_nbrs/"

shapes_dir = top_shapes_dir + directory + "shapes/"
shapes_intnl_s_pixcShp_dir = shapes_dir + "intnl_spixcShp/"
shapes_intnl_s_pixcShp_ddir = shapes_intnl_s_pixcShp_dir + "data/"
shapes_intnl_s_pixcShp_dfile = shapes_intnl_s_pixcShp_ddir + image_filename + "shapes.data"

if os.path.exists(s_pixc_shapes_dir ) == False:
   os.makedirs(s_pixc_shapes_dir)
if os.path.exists(main_dir ) == False:
   os.makedirs(main_dir)
if os.path.exists(main_data_dir ) == False:
   os.makedirs(main_data_dir)
if os.path.exists(shapes_intnl_s_pixcShp_ddir ) == False:
   os.makedirs(shapes_intnl_s_pixcShp_ddir)
if os.path.exists(main_loc_dir ) == False:
   os.makedirs(main_loc_dir)
if os.path.exists(main_shapes_dir ) == False:
   os.makedirs(main_shapes_dir)
if os.path.exists(main_shape_nbrs_dir ) == False:
   os.makedirs(main_shape_nbrs_dir)


original_image = Image.open(top_images_dir + directory + image_filename + ".png")
im_width, im_height = original_image.size

# returned value has below form
# shapes[shapes_id][pixel_index] = {}
# shapes[shapes_id][pixel_index]['x'] = x
# shapes[shapes_id][pixel_index]['y'] = y
im_shapes = read_files_functions.rd_shapes_file(image_filename, directory)

# getting small pixel count shapes
pix_counts_w_shapes = image_functions.get_image_stats( image_filename, directory, shapes_type="normal" )

print("preparing data...")

small_pixc_shapes = []
bigger_shapes = []
for pixel_count in pix_counts_w_shapes:

   if pixel_count < 50:
      small_pixc_shapes.extend( pix_counts_w_shapes[ pixel_count ] )
   if pixel_count > 2:
      bigger_shapes.extend( pix_counts_w_shapes[ pixel_count ] )


shapes_locations_path = top_shapes_dir + directory + "locations/" + image_filename + "_loc.txt"
shapes_locations = read_files_functions.rd_ldict_k_v_l( image_filename, directory, shapes_locations_path )



small_pixc_shapes_im_areas = {}
for shapeid in small_pixc_shapes:
   
   for s_locs in shapes_locations:
      if shapeid in s_locs.keys():
         small_pixc_shapes_im_areas[shapeid] = s_locs[ list(s_locs.keys())[0] ]
         break
bigger_shapes_im_areas = {}
for shapeid in bigger_shapes:
   
   for s_locs in shapes_locations:
      if shapeid in s_locs.keys():
         bigger_shapes_im_areas[shapeid] = s_locs[ list(s_locs.keys())[0] ]
         break


s_pixc_shapes_boundaries = {}
# get boundary pixels of bigger pixel count shapes
for shapeid in small_pixc_shapes:
   s_pixc_shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels(im_shapes[shapeid] )







print("main process begins. please wait")

internal_s_pixc_shapes = []
for small_pixc_shapeid in small_pixc_shapes:

   cur_s_pixc_shp_locations = small_pixc_shapes_im_areas[small_pixc_shapeid]
   
   cur_s_pixc_shape_pixels = list( im_shapes[ small_pixc_shapeid ].keys() )
   
   cur_s_pixc_boundaries = []
   for xy in s_pixc_shapes_boundaries[small_pixc_shapeid].values():
      pixel_index = ( xy['y'] * im_width )+ xy['x']
      cur_s_pixc_boundaries.append( str( pixel_index ) )
   
   
   for bigger_shapeid in bigger_shapes:
      
      # check if current small pixel count shape is located in the same image area as current bigger shape
      cur_Lshape_locations = bigger_shapes_im_areas[bigger_shapeid]
      
      check = any(im_area in cur_s_pixc_shp_locations for im_area in cur_Lshape_locations)

      if not check:
         continue
      
      # getting all pixels of current bigger shape
      cur_bigger_shape_pixels = list(im_shapes[bigger_shapeid].keys())
      
      # check if all boundary pixels of current small pixel count shape are direct neighbor to current bigger shape
      match_counter = 0
      cur_boundaries_total = len( cur_s_pixc_boundaries )
      for small_pixc_pindex in cur_s_pixc_boundaries:
         
         # get neighbor pixels of current small pixel count pixel index
         p_neighbors = pixel_functions.get_nbr_pixels( small_pixc_pindex, original_image.size )

         # check if current pixel is neighbor to current bigger shape
         # first, convert p_neighbors to list of strings
         p_neighbors = [str(pindex) for pindex in p_neighbors]
         
         # make sure that all neighbors are not pixels of current small pixel count shape
         p_neighbors = [ pindex for pindex in p_neighbors if pindex not in cur_s_pixc_shape_pixels ]
         
         check =  all(pindex in cur_bigger_shape_pixels for pindex in p_neighbors)

         if check:
            # current pixel is neighbor to current bigger shape
            match_counter += 1
       
      if match_counter == cur_boundaries_total:
         # current small pixel count shape is surrounded entirely by current bigger shape
         internal_s_pixc_shapes.append( ( small_pixc_shapeid, bigger_shapeid ) )
         # if current small pixel count shape is surrounded by current bigger shape then, it also means that 
         # any other bigger shape will not be neighbor current small pixel count shape. so end it
         break
         

with open(main_dfile, 'wb') as fp:
   pickle.dump(internal_s_pixc_shapes, fp)
fp.close()


shapes_w_intnl_s_pixcShp = {}
for shapeid in im_shapes:
   # check if current shapeid is a internal small pixel count shape. if so, skip this because it will be incorporated into its bigger shape
   is_it_intnl_spixc_shape = any( True for shapeids in internal_s_pixc_shapes if shapeids[0] == shapeid )

   if is_it_intnl_spixc_shape:
      continue

   # for non internal spixc shapes, first, get its own pixels
   shapes_w_intnl_s_pixcShp[shapeid] = list( im_shapes[ shapeid ].keys() )
   
   cur_matched_s_pixc_shapes = [ shapeids[0] for shapeids in internal_s_pixc_shapes if shapeids[1] == shapeid ]
   
   for cur_matched_spixc_shapeid in cur_matched_s_pixc_shapes:
      # getting all pixels of internal small pixel count shapes
      cur_pixels = list ( im_shapes[ cur_matched_spixc_shapeid ].keys() )
      
      shapes_w_intnl_s_pixcShp[shapeid].extend( cur_pixels )


with open(shapes_intnl_s_pixcShp_dfile, 'wb') as fp:
   pickle.dump(shapes_w_intnl_s_pixcShp, fp)
fp.close()

with open(main_shapes_dfile, 'wb') as fp:
   pickle.dump(shapes_w_intnl_s_pixcShp, fp)
fp.close()


print("finished main processing. now create shape locations")
create_shape_locations.do_create( image_filename, directory, shapes_type=shapes_type )
print("finished creating shape locations. now create shape neighbors")
create_shape_neighbors.do_create( image_filename, directory, shapes_type=shapes_type )


























