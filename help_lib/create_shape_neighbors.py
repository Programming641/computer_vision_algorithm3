from libraries import read_files_functions
from libraries import pixel_shapes_functions
from libraries import pixel_functions

import os, sys
from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir, internal
import winsound
import pickle
import math
from PIL import ImageTk, Image


def find_all_shape_neighbors( shapes, shapes_in_im_areas, shapes_boundaries ):
      all_shape_neighbors = {}

      all_shapes = len(shapes)
      for src_shapeid in shapes:

         if all_shapes % 100 == 0:
            print("src_shapeid " + src_shapeid + " " +  str(all_shapes) + " remaining" )

   
         all_shape_neighbors[src_shapeid] = []
   

         # comparing every one of shape of the image with every other shapes of the image
         for candidate_shapeid in shapes:
      
            if src_shapeid == candidate_shapeid :
               # itself or already processed as src_shapeid
               continue
      
            same_im_area = False
            for src_s_loc in shapes_in_im_areas[src_shapeid]:
               if src_s_loc in shapes_in_im_areas[candidate_shapeid]:
                  same_im_area = True
      
            if not same_im_area:
               continue
      
            # returned value example. {'src': {'x': 33, 'y': 33}, 1: {'x': 33, 'y': 34}, 2: {'x': 34, 'y': 34}}
            matched_neighbor_coords = pixel_shapes_functions.find_direct_neighbors( shapes_boundaries[src_shapeid] , shapes_boundaries[candidate_shapeid] )

            if matched_neighbor_coords:

               all_shape_neighbors[src_shapeid].append(candidate_shapeid)


         if len( all_shape_neighbors[src_shapeid] ) == 0:
            print("ERROR. current shape " + src_shapeid + " could not find neighbors")
            sys.exit()
      
         all_shapes -= 1
      
      return all_shape_neighbors








# shapes_type
# normal is the one created by find_shapes
# intnl_spixcShp are shapes that incorporate internal small pixel count shapes
def do_create( im_file, directory, shapes_type=None ):


   # directory is specified but does not contain /
   if directory != "" and directory[-1] != ('/'):
      directory +='/'

   original_image = Image.open(top_images_dir + directory + im_file + ".png")
   im_width, im_height = original_image.size


   if shapes_type == "normal":

      shape_locations_path = top_shapes_dir + directory + "locations/" + im_file + "_loc.data"
      shape_neighbors_path = top_shapes_dir + directory + 'shape_nbrs/'

      if not os.path.isdir(shape_neighbors_path):
         os.makedirs(shape_neighbors_path)


      with open (shape_locations_path, 'rb') as fp:
         #  {'79971': ['25'], '79999': ['25'], ... }
         shapes_in_im_areas = pickle.load(fp)
      fp.close()

      shape_neighbor_file = open(shape_neighbors_path + im_file + "_shape_nbrs.txt" , "w" )

      # returned value has below form
      # shapes[shapes_id][pixel_index] = {}
      # shapes[shapes_id][pixel_index]['x'] = x
      # shapes[shapes_id][pixel_index]['y'] = y
      shapes = read_files_functions.rd_shapes_file(im_file, directory)


      shapes_boundaries = {}
      # get boundary pixels of all shapes
      for shapeid in shapes:
         cur_shape_pixels = set()
         for pindex in pindexes:
            
            y = math.floor( int(pindex) / im_width)
            x  = int(pindex) % im_width 
      
            cur_shape_pixels.add( (x,y) )

         shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels(cur_shape_pixels )

      
      all_shape_neighbors = find_all_shape_neighbors( shapes, shapes_in_im_areas, shapes_boundaries )
            
            
      shape_neighbor_file.write(str( all_shape_neighbors ) )
      shape_neighbor_file.close()


   elif shapes_type == "intnl_spixcShp":
      s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"
      s_pixcShp_intnl_loc_dir = s_pixcShp_intnl_dir + "locations/"
      shape_locations_path = s_pixcShp_intnl_loc_dir + im_file + "_loc.data"
      shape_neighbors_path = s_pixcShp_intnl_dir + 'shape_nbrs/'

      shapes_dir = s_pixcShp_intnl_dir + "shapes/"
      shapes_dfile = shapes_dir + im_file + "shapes.data"

      if not os.path.isdir(shape_neighbors_path):
         os.makedirs(shape_neighbors_path)


      with open (shapes_dfile, 'rb') as fp:
         # { '79999': ['79999', ... ], ... }
         # { 'shapeid': [ pixel indexes ], ... }
         shapes = pickle.load(fp)
      fp.close()


      with open (shape_locations_path, 'rb') as fp:
         #  {'79971': ['25'], '79999': ['25'], ... }
         s_locations = pickle.load(fp)
      fp.close()

      shape_neighbor_file = open(shape_neighbors_path + im_file + "_shape_nbrs.txt" , "w" )

      all_shape_neighbors = []


      shapes_boundaries = {}
      # get boundary pixels of all shapes
      for shapeid, pindexes in shapes.items():
         cur_shape_pixels = set()
         for pindex in pindexes:
            
            y = math.floor( int(pindex) / im_width)
            x  = int(pindex) % im_width 
      
            cur_shape_pixels.add( (x,y) )

         shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels(cur_shape_pixels )

      all_shape_neighbors = find_all_shape_neighbors( shapes, s_locations, shapes_boundaries )
            
            
      shape_neighbor_file.write(str( all_shape_neighbors ) )
      shape_neighbor_file.close()

   
   else:
      print("ERROR at help_lib/create_shape_neighbors.py shapes_type " + shapes_type + " is not implemented " )
      sys.exit()







   frequency = 2500  # Set Frequency To 2500 Hertz
   duration = 1000  # Set Duration To 1000 ms == 1 second
   winsound.Beep(frequency, duration)




if __name__ == '__main__':
   im1file = "13"
   directory = "videos/street3/resized/min"
   
   do_create( im1file, directory, "intnl_spixcShp" )
















