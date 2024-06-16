# find internal small pixel count shapes.
# if a small pixel count shape is entirely surrounded by one bigger shape, then it is the internal pixels of the one bigger shape.
from libraries import pixel_functions, image_functions, pixel_shapes_functions

from PIL import Image
import os, sys
import pickle
import math

from libraries.cv_globals import top_shapes_dir, top_images_dir, internal
from help_lib import crud_shape_locations, crud_shape_neighbors, crud_shape_boundaries
from libraries import cv_globals


image_filename = '11'
directory = "videos/street6/resized/min3"
shapes_type = "intnl_spixcShp"


if len(sys.argv) > 1:
   image_filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   directory = sys.argv[3]
   shapes_type = "intnl_spixcShp"   
   
   print("execute " + os.path.basename(__file__) + " " + directory + " " + image_filename )
   
   

if directory != "" and directory[-1] != '/':
   directory +='/'



shapes_dir = top_shapes_dir + directory + "shapes/"


original_image = Image.open(top_images_dir + directory + image_filename + ".png")
im_width, im_height = original_image.size

shapes_dfile = shapes_dir + image_filename + "shapes.data"
with open (shapes_dfile, 'rb') as fp:
   im_shapes = pickle.load(fp)
fp.close()


# getting small pixel count shapes
pix_counts_w_shapes = image_functions.get_image_stats( image_filename, directory, shapes_type="normal" )

smallest_pixc = cv_globals.get_smallest_pixc( original_image.size )
sec_smallest_pixc = cv_globals.get_sec_smallest_pixc( original_image.size )

small_pixc_shapes = []
bigger_shapes = []
for pixel_count in pix_counts_w_shapes:

   if pixel_count < sec_smallest_pixc:
      small_pixc_shapes.extend( pix_counts_w_shapes[ pixel_count ] )
   if pixel_count > smallest_pixc:
      bigger_shapes.extend( pix_counts_w_shapes[ pixel_count ] )


shapes_locations_path = shapes_dir + "locations/" + image_filename + "_loc.data"
with open (shapes_locations_path, 'rb') as fp:
   #  {'79971': ['25'], '79999': ['25'], ... }
   shapes_locations = pickle.load(fp)
fp.close()

small_pixc_shapes_im_areas = {}
for shapeid in small_pixc_shapes:
   small_pixc_shapes_im_areas[shapeid] = shapes_locations[shapeid]

bigger_shapes_im_areas = {}
for shapeid in bigger_shapes:
   bigger_shapes_im_areas[shapeid] = shapes_locations[shapeid]


s_pixc_shapes_boundaries = {}
# get boundary pixels of bigger pixel count shapes
for shapeid in small_pixc_shapes:
   cur_pixels = set()
   
   for pindex in im_shapes[shapeid]:
      xy = pixel_functions.convert_pindex_to_xy( pindex, im_width )
      cur_pixels.add( xy )
   
   s_pixc_shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels(cur_pixels)


internal_s_pixc_shapes = []
for small_pixc_shapeid in small_pixc_shapes:

   cur_s_pixc_shp_locations = small_pixc_shapes_im_areas[small_pixc_shapeid]
   
   cur_s_pixc_shape_pixels = im_shapes[ small_pixc_shapeid ]
   
   cur_s_pixc_boundaries = []
   for xy in s_pixc_shapes_boundaries[small_pixc_shapeid]:
      pixel_index = ( xy[1] * im_width )+ xy[0]
      cur_s_pixc_boundaries.append( pixel_index )
   
   
   for bigger_shapeid in bigger_shapes:
      
      # check if current small pixel count shape is located in the same image area as current bigger shape
      cur_Lshape_locations = bigger_shapes_im_areas[bigger_shapeid]
      
      check = any(im_area in cur_s_pixc_shp_locations for im_area in cur_Lshape_locations)

      if not check:
         continue
      
      
      # getting all pixels of current bigger shape
      cur_bigger_shape_pixels = im_shapes[bigger_shapeid]
      
      # check if all boundary pixels of current small pixel count shape are direct neighbor to current bigger shape
      match_counter = 0
      cur_boundaries_total = len( cur_s_pixc_boundaries )
      for small_pixc_pindex in cur_s_pixc_boundaries:
         
         # get neighbor pixels of current small pixel count pixel index
         p_neighbors = pixel_functions.get_nbr_pixels( small_pixc_pindex, original_image.size )

         # check if current pixel is neighbor to current bigger shape
         # first, convert p_neighbors to list of strings
         p_neighbors = [ pindex for pindex in p_neighbors]
         
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
         # any other bigger shape will not be neighbor with current small pixel count shape. so end it
         break
         


s_pixc_shapes_dir = top_shapes_dir + directory + "spixc_shapes/data/"
if os.path.exists(s_pixc_shapes_dir ) == False:
   os.makedirs(s_pixc_shapes_dir)

main_dfile = s_pixc_shapes_dir + image_filename + ".data"
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
   shapes_w_intnl_s_pixcShp[shapeid] = im_shapes[ shapeid ]
   
   cur_matched_s_pixc_shapeids = [ shapeids[0] for shapeids in internal_s_pixc_shapes if shapeids[1] == shapeid ]
   
   for cur_matched_spixc_shapeid in cur_matched_s_pixc_shapeids:
      # getting all pixels of internal small pixel count shape
      cur_pixels = im_shapes[ cur_matched_spixc_shapeid ]
      
      shapes_w_intnl_s_pixcShp[shapeid].extend( cur_pixels )



main_shapes_dfile = shapes_dir + image_filename + "shapes.data"
# updating main shapes data
with open(main_shapes_dfile, 'wb') as fp:
   pickle.dump(shapes_w_intnl_s_pixcShp, fp)
fp.close()

bigger_shapeids = { temp_shapeids[1] for temp_shapeids in internal_s_pixc_shapes }
spixc_shapeids = { temp_shapeids[0] for temp_shapeids in internal_s_pixc_shapes }

pixel_shapes_functions.create_shapeids_by_pindex( image_filename, directory, original_image.size )

print("delete and update shape boundaries for " + image_filename )
crud_shape_boundaries.do_delete( image_filename, directory, spixc_shapeids )
crud_shape_boundaries.do_update( image_filename, directory, bigger_shapeids )

print("delete and update shape locations for " + image_filename )
crud_shape_locations.do_delete( image_filename, directory, spixc_shapeids )
crud_shape_locations.do_update( image_filename, directory, bigger_shapeids )

print("delete and update shape neighbors for " + image_filename )
crud_shape_neighbors.do_delete( image_filename, directory, spixc_shapeids )
crud_shape_neighbors.do_update( image_filename, directory, bigger_shapeids )


























