from libraries import btwn_amng_files_functions
from libraries import pixel_shapes_functions
from libraries import pixel_functions

import os, sys
from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir, internal
import pickle
import math
from PIL import ImageTk, Image


def find_all_shape_neighbors( shapes_nbr_pixels, shapes_in_im_areas, shapes_boundaries ):
      all_shape_neighbors = {}

      max_progress_num = len(shapes_nbr_pixels)
      cur_progress_num = len(shapes_nbr_pixels)
      prev_progress_num = len(shapes_nbr_pixels)
      remaining_chars = ""
      for src_shapeid in shapes_nbr_pixels:          
         remaining_chars = btwn_amng_files_functions.show_progress( max_progress_num, cur_progress_num, prev_progress_num, remaining_chars=remaining_chars, in_step=100 )
         prev_progress_num = cur_progress_num
         cur_progress_num -= 1
   
         all_shape_neighbors[src_shapeid] = []
   

         # comparing every one of shape of the image with every other shapes of the image
         for candidate_shapeid in shapes_nbr_pixels:
      
            if src_shapeid == candidate_shapeid :
               # itself or already processed as src_shapeid
               continue
      
            same_im_area = False
            for src_s_loc in shapes_in_im_areas[src_shapeid]:
               if src_s_loc in shapes_in_im_areas[candidate_shapeid]:
                  same_im_area = True
      
            if not same_im_area:
               continue
      
            overlapped_pixels = shapes_nbr_pixels[src_shapeid].intersection( shapes_boundaries[candidate_shapeid] )
            if len(overlapped_pixels) >= 1:

               all_shape_neighbors[src_shapeid].append(candidate_shapeid)


         if len( all_shape_neighbors[src_shapeid] ) == 0:
            print("ERROR. current shape " + str(src_shapeid) + " could not find neighbors")
            sys.exit(1)


      return all_shape_neighbors



def get_shapes_locations( im_file, directory ):

   shapes_dir = top_shapes_dir + directory + "shapes/"

   shape_locations_path = shapes_dir + "locations/" + im_file + "_loc.data"

   with open (shape_locations_path, 'rb') as fp:
      #  {'79971': ['25'], '79999': ['25'], ... }
      shapes_in_im_areas = pickle.load(fp)
   fp.close()

   return shapes_in_im_areas



def get_shapes_boundaries( im_file, directory ):
   shapes_dir = top_shapes_dir + directory + "shapes/"
   shapes_boundary_path = shapes_dir + "boundary/" + im_file + ".data"
   with open (shapes_boundary_path, 'rb') as fp:
      shapes_boundaries = pickle.load(fp)
   fp.close()

   return shapes_boundaries


def get_shapes( im_file, directory, im_width, pixels_xy=False ):
   shapes_dir = top_shapes_dir + directory + "shapes/"
   shapes_dfile = shapes_dir + im_file + "shapes.data"
   with open (shapes_dfile, 'rb') as fp:
      shapes = pickle.load(fp)
   fp.close()

   if pixels_xy is True:
      for shapeid in shapes:
         pixels_xy = set()
         for pixel in shapes[shapeid]:
            xy = pixel_functions.convert_pindex_to_xy( pixel, im_width )
            
            pixels_xy.add( xy )
         
         shapes[shapeid] = pixels_xy

   return shapes



def do_create( im_file, directory, return_nbrs=False ):


   # directory is specified but does not contain /
   if directory != "" and directory[-1] != ('/'):
      directory +='/'

   original_image = Image.open(top_images_dir + directory + im_file + ".png")
   im_width, im_height = original_image.size

   shapes_dir = top_shapes_dir + directory + "shapes/"
   shape_neighbors_path = shapes_dir + 'shape_nbrs/'
   if not os.path.isdir(shape_neighbors_path):
      os.makedirs(shape_neighbors_path)

   shapes_in_im_areas = get_shapes_locations( im_file, directory )
   shapes_boundaries = get_shapes_boundaries( im_file, directory )
   shapes = get_shapes( im_file, directory, im_width, pixels_xy=True )

   #shape_neighbor_file = open(shape_neighbors_path + im_file + "_shape_nbrs.txt" , "w" )
   shape_neighbor_file = shape_neighbors_path + im_file + "_shape_nbrs.data"
      
   shapes_nbr_pixels = {}
   # get boundary pixels of all shapes
   for shapeid in shapes:
       
      nbr_pixels = set()
      for pixel in shapes_boundaries[shapeid]:
         nbr_pixels |= set( pixel_functions.get_nbr_pixels(pixel, original_image.size, input_xy=True) )
         
      shapes_nbr_pixels[shapeid] = nbr_pixels

      
   all_shape_neighbors = find_all_shape_neighbors( shapes_nbr_pixels, shapes_in_im_areas, shapes_boundaries )
   
   if return_nbrs is False:
      with open(shape_neighbor_file, 'wb') as fp:
         pickle.dump(all_shape_neighbors, fp)
      fp.close()            

   else:
      return all_shape_neighbors



def do_delete( im_file, directory, target_shapeids ):
   
   # directory is specified but does not contain /
   if directory != "" and directory[-1] != ('/'):
      directory +='/'

   shapes_dir = top_shapes_dir + directory + "shapes/"

   shape_neighbors_path = shapes_dir + 'shape_nbrs/'

   shape_neighbor_file = shape_neighbors_path + im_file + "_shape_nbrs.data"
   with open (shape_neighbor_file, 'rb') as fp:
      shapes_neighbors = pickle.load(fp)
   fp.close()

   for target_shapeid in target_shapeids:
      shapes_neighbors.pop( target_shapeid )

   # need to delete target shapeids from all neighbors list as well
   for target_shapeid in target_shapeids:
      shapeids_have_tshp_as_nbr = { temp_shapeid for temp_shapeid in shapes_neighbors if target_shapeid in shapes_neighbors[temp_shapeid] }
      
      for shapeid_has_tshp_as_nbr in shapeids_have_tshp_as_nbr:
         shapes_neighbors[shapeid_has_tshp_as_nbr].remove( target_shapeid )
        
   with open(shape_neighbor_file, 'wb') as fp:
      pickle.dump(shapes_neighbors, fp)
   fp.close()      
   

def do_update( im_file, directory, target_shapeids, candidate=False ):

   # directory is specified but does not contain /
   if directory != "" and directory[-1] != ('/'):
      directory +='/'

   original_image = Image.open(top_images_dir + directory + im_file + ".png")
   im_width, im_height = original_image.size

   shapes_boundaries = get_shapes_boundaries( im_file, directory )
   shapes = get_shapes( im_file, directory, im_width )
   
   shapes_dir = top_shapes_dir + directory + "shapes/"   
   
   shapeids_by_pindex_dfile = shapes_dir + "shapeids_by_pindex/" + im_file + ".data"
   with open (shapeids_by_pindex_dfile, 'rb') as fp:
      shapeids_by_pindex = pickle.load(fp)
   fp.close()        

   shape_neighbors_path = shapes_dir + 'shape_nbrs/'
   
   shape_neighbor_file = shape_neighbors_path + im_file + "_shape_nbrs.data"
   with open (shape_neighbor_file, 'rb') as fp:
      existing_shapes_neighbors = pickle.load(fp)
   fp.close()
   
   def _do_update( all_shape_neighbors, param_target_shapeids, update_candidate=False ):
   
      candidate_shapeids_for_update = set()
      for target_shapeid in param_target_shapeids:
         all_shape_neighbors[target_shapeid] = []
      
         nbr_pixels_wk = set()
         for pixel in shapes_boundaries[target_shapeid]:
            nbr_pixels_wk |= set( pixel_functions.get_nbr_pixels(pixel, original_image.size, input_xy=True) )
      
         for pixel in nbr_pixels_wk:
            pindex = pixel_functions.convert_xy_to_pindex( pixel, im_width )
         
            # get all shapeids that have nbr_pixels. they will be neighbors with target_shapeid
            candidate_shapeids = shapeids_by_pindex[pindex]
            
            if update_candidate is False:
               candidate_shapeids_for_update |= candidate_shapeids
         
            for candidate_shapeid in candidate_shapeids:
               if candidate_shapeid not in all_shape_neighbors[target_shapeid] and candidate_shapeid != target_shapeid:
                  all_shape_neighbors[target_shapeid].append( candidate_shapeid )

         # all shapes have to have neighbors
         assert len(all_shape_neighbors[target_shapeid]) >= 1

      if update_candidate is False:
         return candidate_shapeids_for_update

   
   
   all_shape_neighbors = {}

   # when new shape is inserted into the image, not just new shape need to have neighbors but surrounding shapes that are neighbors 
   # to this new shape need to include this new shape as well in their neighbors list. but can not just add this new shape to existing_shapes_neighbors[candidate_shapeid]
   # because shapeids_by_pindex may already be updated. 
   candidate_shapeids_for_update = _do_update( all_shape_neighbors, target_shapeids )
   _do_update( all_shape_neighbors, candidate_shapeids_for_update, update_candidate=True )




   for shapeid in all_shape_neighbors:
      existing_shapes_neighbors[shapeid] = all_shape_neighbors[shapeid]

   with open(shape_neighbor_file, 'wb') as fp:
      pickle.dump(existing_shapes_neighbors, fp)
   fp.close()            









if __name__ == '__main__':

   if len( sys.argv ) >= 2:
      image_filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
      directory = sys.argv[1]
      
      do_create( image_filename, directory )
   else:


      im1file = "11"
      directory = "videos/street6/resized/min3"
   
      do_create( im1file, directory )
















