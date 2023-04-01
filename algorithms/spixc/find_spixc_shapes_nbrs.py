# find small pixel count shapes neighbors
# small pixel count shapes and their neighbors are put together if small pixel count shape itself is a direct neighbor
# or its neighbors are direct neighbor of another small pixel count shape.
#
# in short, if small pixel count shapes share one or more of their direct neighbors, or itself is a direct neighbor, then 
# they are put together
from libraries import pixel_functions, image_functions, read_files_functions

from PIL import Image
import os, sys
import pickle
import copy

from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir, internal


image_filename = '13'
directory = "videos/street3/resized/min"
shapes_type = "intnl_spixcShp"


recreate_images = False

if len(sys.argv) > 1:
   image_filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]

   directory = sys.argv[1]

   print("execute script find_same_clr_shapes.py. filename " + image_filename + " directory " + directory )

if directory != "" and directory[-1] != '/':
   directory +='/'

shapes_dir = top_shapes_dir + directory + "spixc_shapes/"
s_pixc_shapes_nbrs_dir = shapes_dir + "nbrs/"
s_pixc_shapes_nbrs_data_dir = s_pixc_shapes_nbrs_dir + "data/"
s_pixc_shapes_nbrs_dfile = s_pixc_shapes_nbrs_data_dir + image_filename + ".data"

if os.path.exists(shapes_dir ) == False:
   os.makedirs(shapes_dir)
if os.path.exists(s_pixc_shapes_nbrs_dir ) == False:
   os.makedirs(s_pixc_shapes_nbrs_dir)
if os.path.exists(s_pixc_shapes_nbrs_data_dir ) == False:
   os.makedirs(s_pixc_shapes_nbrs_data_dir)


# getting small pixel count shapes
pix_counts_w_shapes = image_functions.get_image_stats( image_filename, directory, shapes_type )

small_pixc_shapes = []
for pixel_count in pix_counts_w_shapes:
   if pixel_count < 50:
      small_pixc_shapes.extend( pix_counts_w_shapes[ pixel_count ] )


if shapes_type == "normal":
   nbr_filepath = top_shapes_dir + directory + "shape_nbrs/" + image_filename + "_shape_nbrs.txt"
   
elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"
   nbr_filepath = s_pixcShp_intnl_dir + "shape_nbrs/" + image_filename + "_shape_nbrs.txt"

# {"shapeid": ["nbr_shapeid", "nbr_shapeid", ...], ...  }
shape_nbrs = read_files_functions.rd_dict_k_v_l(image_filename, directory, nbr_filepath)






# [{'shapeid':[shapeid's neighbors], 'nbr_nbrs': []}, ... ]
# [ { small pixel count shapeid: [ its neighbors ], 'nbr_nbrs': [      ] }, ... ]
# nbr_nbrs contain other small pixel count shapes that are the direct neighbors of shapeid's neighbors. if it is a direct neighbor, then all its neighbors
# will be added to the nbr_nbrs.
s_pixc_nbrs = []

progress_counter = len( small_pixc_shapes )
for s_pixc_shape in small_pixc_shapes:
   if progress_counter % 100 == 0:
      print( str( progress_counter ) + " remaining" )
   progress_counter -= 1
   
   cur_s_pixc_shape_nbrs = shape_nbrs[ str( s_pixc_shape ) ]
   
   
   # check if s_pixc_shape or any of its neighbors is already in the s_pixc_nbrs. if so, s_pixc_shape and its neighbors will be combined
   # with them.
   s_pixc_sid_containg_sid_lindex = None
   cur_shapeid_found = False
   s_pixc_shape_containing_shapeid = None
   first_s_pixc_shapeid_containg_shapeid = True
   delete_already_added = []
   
   

   for s_pixc_sid_containg_sid_lindex, s_pixc_nbr in enumerate(copy.deepcopy(s_pixc_nbrs)):
      # check if s_pixc_shape is a direct neighbor of any of the shapes in s_pixc_nbrs
      cur_shapeid_exists = { key: values for key, values in  s_pixc_nbr.items() if str( s_pixc_shape ) in values and key != "nbr_nbrs" }      
      
   
      if len( cur_shapeid_exists ) > 1:
         print("ERROR. here, there should only be one dictionary")
         sys.exit()
   
      if len(cur_shapeid_exists) == 1:
         cur_shapeid_found = True
      
         # s_pixc_shape's direct neighbor's shape id.
         cur_sid_containg_sid = [ sid for sid in cur_shapeid_exists.keys() ][0]
      
         if first_s_pixc_shapeid_containg_shapeid:
            s_pixc_nbrs[s_pixc_sid_containg_sid_lindex] [ "nbr_nbrs" ].append( str( s_pixc_shape ) )
            s_pixc_nbrs[s_pixc_sid_containg_sid_lindex] [ "nbr_nbrs" ].extend ( cur_s_pixc_shape_nbrs )
      
            first_s_pixc_shapeid_containg_shapeid = False
            
            s_pixc_shape_containing_shapeid = s_pixc_sid_containg_sid_lindex
      
         else:
            # combining other current small pixel count shapeid containg shapes
            s_pixc_nbrs[s_pixc_shape_containing_shapeid][ "nbr_nbrs" ].append( str( cur_sid_containg_sid ) )
            s_pixc_nbrs[s_pixc_shape_containing_shapeid][ "nbr_nbrs" ].extend( s_pixc_nbrs[s_pixc_sid_containg_sid_lindex][cur_sid_containg_sid] )
            s_pixc_nbrs[s_pixc_shape_containing_shapeid][ "nbr_nbrs" ].extend( s_pixc_nbrs[s_pixc_sid_containg_sid_lindex]["nbr_nbrs"] )
            
            delete_already_added.append( s_pixc_sid_containg_sid_lindex )
            

   
   if cur_shapeid_found:
      deleted_index = 0
      for i in delete_already_added:
         i -= deleted_index
         s_pixc_nbrs.pop( i )
      
         deleted_index += 1
      
      continue
   
   
   # check all current neighbors too. if any of them is already in the existing list
   cur_shape_n_nbrs_present = False
   cur_nbr_containg_sid_lindex = None
   first_sid_containg_s_pixc_sid_nbrs = True
   nbr_containg_shapeid = None
   
   already_added_sid_lindex = []
   delete_sids = []


   for cur_s_pixc_shape_nbr in cur_s_pixc_shape_nbrs:

      for cur_nbr_containg_sid_lindex, s_pixc_nbr in enumerate(copy.deepcopy(s_pixc_nbrs)):
         if cur_nbr_containg_sid_lindex in already_added_sid_lindex:
            continue
         cur_nbr_exists = { key: values for key, values in  s_pixc_nbr.items() if str( cur_s_pixc_shape_nbr ) in values and key != "nbr_nbrs" }
            
   
         if len( cur_nbr_exists ) > 1: 
            print("ERROR. there should only be one dictionary")
            sys.exit()
   
         if len( cur_nbr_exists ) == 1:

            cur_shape_n_nbrs_present = True
               
            cur_nbr_exists = s_pixc_nbrs[ cur_nbr_containg_sid_lindex ]
               
            
            # adding current neighbor alreadying containing shapeid

            cur_nbr_containg_sid = [ sid for sid in cur_nbr_exists.keys() if sid != "nbr_nbrs" ][0]
                  
            if first_sid_containg_s_pixc_sid_nbrs:
               s_pixc_nbrs[cur_nbr_containg_sid_lindex] [ "nbr_nbrs" ].append( str( s_pixc_shape ) )
               s_pixc_nbrs[cur_nbr_containg_sid_lindex] [ "nbr_nbrs" ].extend ( cur_s_pixc_shape_nbrs )
      
               first_sid_containg_s_pixc_sid_nbrs = False
            
               nbr_containg_shapeid = cur_nbr_containg_sid_lindex
               already_added_sid_lindex.append( cur_nbr_containg_sid_lindex )
            else:
               # combining other current small pixel count shapeid containg shapes
               s_pixc_nbrs[nbr_containg_shapeid][ "nbr_nbrs" ].append( str( cur_nbr_containg_sid ) )
               s_pixc_nbrs[nbr_containg_shapeid][ "nbr_nbrs" ].extend( s_pixc_nbrs[cur_nbr_containg_sid_lindex][cur_nbr_containg_sid] )
               s_pixc_nbrs[nbr_containg_shapeid][ "nbr_nbrs" ].extend( s_pixc_nbrs[cur_nbr_containg_sid_lindex]["nbr_nbrs"] )
            
               delete_sids.append( cur_nbr_containg_sid_lindex )
                                     
         

               
   if cur_shape_n_nbrs_present:
      deleted_index = 0
      for delete_sid in delete_sids:
         delete_sid -= deleted_index
         s_pixc_nbrs.pop( delete_sid )
         
         deleted_index += 1
         
      continue
   
   s_pixc_nbrs.append( { str( s_pixc_shape ): cur_s_pixc_shape_nbrs, "nbr_nbrs": [] } )



# removing duplicates from nbr_nbrs list
for s_pixc_nbr in s_pixc_nbrs:
   s_pixc_nbr["nbr_nbrs"] =  list(dict.fromkeys(s_pixc_nbr["nbr_nbrs"]))



with open(s_pixc_shapes_nbrs_dfile, 'wb') as fp:
   pickle.dump(s_pixc_nbrs, fp)
fp.close()







































