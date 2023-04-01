# find 2nd smallest pixel count group ( 1 to 12 ) shapes that share the same large shapes
from libraries import pixel_functions, image_functions, read_files_functions, pixel_shapes_functions

from PIL import Image
import os, sys
import pickle
import math

from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir


image_filename = '12'
directory = "videos/street3/resized/min"

shapes_type = "intnl_spixcShp"

if len(sys.argv) > 1:
   image_filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]

   directory = sys.argv[1]

   print("execute script find_spixcShp_Dnbr_sharing_Lshapes.py. filename " + image_filename + " directory " + directory )

if directory != "" and directory[-1] != '/':
   directory +='/'


spixcShp_w_same_Lshapes_dir = top_shapes_dir + directory + "spixc_shapes/same_Lshapes/" + shapes_type + "/"
spixcShp_w_same_Lshapes_ddir = spixcShp_w_same_Lshapes_dir + "data/"
spixcShp_w_same_Lshapes_dfile = spixcShp_w_same_Lshapes_ddir + image_filename + ".data"

if os.path.exists(spixcShp_w_same_Lshapes_dir ) == False:
   os.makedirs(spixcShp_w_same_Lshapes_dir)
if os.path.exists(spixcShp_w_same_Lshapes_ddir ) == False:
   os.makedirs(spixcShp_w_same_Lshapes_ddir)

shapes_intnl_s_pixcShp_dfile = top_shapes_dir + directory + "shapes/" + shapes_type + "/data/" + image_filename + "shapes.data"

with open (shapes_intnl_s_pixcShp_dfile, 'rb') as fp:
   # { 'shapeid': [ pixel indexes ], ... }
   im_shapes = pickle.load(fp)
fp.close()

if shapes_type == "normal":
   nbr_filepath = top_shapes_dir + directory + "shape_nbrs/" + image_filename + "_shape_nbrs.txt"
elif shapes_type == "intnl_spixcShp":
   nbr_filepath = top_shapes_dir + directory + "spixc_shapes/internal/shape_nbrs/" + image_filename + "_shape_nbrs.txt"
else:
   print("ERROR in find_spixcShp_Dnbr_sharing_Lshapes.py. shapes_type " + shapes_type + " is not supported")
   sys.exit()

   
# [ {'79999': ['67998', '67199', '67599', '79998']}, ... ]
shape_nbrs = read_files_functions.rd_dict_k_v_l(image_filename, directory, nbr_filepath)

# second smallest pixel count group value
scnd_sShp_value = 12
Lshape_size = 50

# { 'im_shapeid': [ [ list of ano_im_shapeids ], [ large shapes ] ], ... }
spixcShp_w_same_Lshapes = {}

already_processed = []

progress_counter = len( im_shapes )
for im_shapeid in im_shapes:
   print( str( progress_counter ) + " remaining" )
   progress_counter -= 1

   # process 2nd smallest pixel count group shapes only
   # or it is already processed
   if not len( im_shapes[im_shapeid] ) <= scnd_sShp_value or im_shapeid in already_processed:
      continue

   cur_shape_neighbors = shape_nbrs[ im_shapeid ]

   # check if any of current shape neighbors are internal spixc shape. if so, remove them.
   pixels = set( im_shapes[im_shapeid] )
   cur_shape_neighbors = [shapeid for shapeid in cur_shape_neighbors if shapeid not in pixels]
   
   cur_Shp_Lshape_neighbors = []
   # check if neighbors are large shapes
   for cur_shape_neighbor in cur_shape_neighbors:
      if len( im_shapes[ cur_shape_neighbor ] ) >= Lshape_size:
         cur_Shp_Lshape_neighbors.append( cur_shape_neighbor )
      
   spixcShp_w_same_Lshapes[ im_shapeid ] = [ [], set() ]
   
   for ano_im_shapeid in im_shapes:
      # skip itself or already processed
      if im_shapeid == ano_im_shapeid or ano_im_shapeid in already_processed:
         continue
      # process 2nd smallest pixel count group shapes only
      if not len( im_shapes[ano_im_shapeid] ) <= scnd_sShp_value:
         continue
      
      ano_cur_shape_neighbors =  shape_nbrs[ ano_im_shapeid ]

      # check if any of current shape neighbors are internal spixc shape. if so, remove them.
      pixels = set( im_shapes[ano_im_shapeid] )
      ano_cur_shape_neighbors = [shapeid for shapeid in ano_cur_shape_neighbors if shapeid not in pixels]
   
      ano_cur_Shp_Lshape_neighbors = []
      # check if neighbors are large shapes
      for ano_cur_shape_neighbor in ano_cur_shape_neighbors:
         if len( im_shapes[ ano_cur_shape_neighbor ] ) >= Lshape_size:
            ano_cur_Shp_Lshape_neighbors.append( ano_cur_shape_neighbor )      
      
      # all of ano_cur_Shp_Lshape_neighbors are contained in cur_Shp_Lshape_neighbors? but not vice versa.
      ano_check =  all(Lshapeid in cur_Shp_Lshape_neighbors for Lshapeid in ano_cur_Shp_Lshape_neighbors)
      
      check = all(Lshapeid in ano_cur_Shp_Lshape_neighbors for Lshapeid in cur_Shp_Lshape_neighbors)

      # also make sure that ano_cur_Shp_Lshape_neighbors contain at least one large neighbor
      # or cur_Shp_Lshape_neighbors contain at least one large neighbor
      if ( ano_check is True and len( ano_cur_Shp_Lshape_neighbors ) > 0 ) or ( check is True and len( cur_Shp_Lshape_neighbors ) > 0 ):
         spixcShp_w_same_Lshapes[ im_shapeid][0].append( ano_im_shapeid )
         
         already_processed.append( ano_im_shapeid )
         
         if len( spixcShp_w_same_Lshapes[ im_shapeid][1] ) > 0:
               
            # all current ano_im_shapeid's large shapes have to match the im_shapeid's large shapes
            ano_check2 =  all(Lshapeid in spixcShp_w_same_Lshapes[ im_shapeid][1] for Lshapeid in ano_cur_Shp_Lshape_neighbors)
            check2 = all(Lshapeid in spixcShp_w_same_Lshapes[ im_shapeid][1] for Lshapeid in cur_Shp_Lshape_neighbors)
         
            if ( check is True and check2 is True ) or ( ano_check is True and ano_check2 is True ):
               spixcShp_w_same_Lshapes[ im_shapeid][1] |=  set( ano_cur_Shp_Lshape_neighbors )
            else:
               print("ERROR. ano_im_shapeid's large shapes have to match the im_shapeid's large shapes")
               print("spixcShp_w_same_Lshapes[ im_shapeid][1] " + str( spixcShp_w_same_Lshapes[ im_shapeid][1] ) )
               print("ano_cur_Shp_Lshape_neighbors " + str( ano_cur_Shp_Lshape_neighbors ) )
               print("cur_Shp_Lshape_neighbors " + str(cur_Shp_Lshape_neighbors) )
               sys.exit()
         
         else:
            spixcShp_w_same_Lshapes[ im_shapeid][1] |=  set( cur_Shp_Lshape_neighbors )



   if len( spixcShp_w_same_Lshapes[im_shapeid][0] ) == 0:
      # no match found
      spixcShp_w_same_Lshapes.pop( im_shapeid )
   
   already_processed.append( im_shapeid )



with open(spixcShp_w_same_Lshapes_dfile, 'wb') as fp:
   pickle.dump(spixcShp_w_same_Lshapes, fp)
fp.close()





























