
import os, sys
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions, pixel_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir, internal
import pickle
import math


# im_fnames -> 25.26
def do_create( im_fnames , directory, main_filename ):

   # directory is specified but does not contain /
   if directory != "" and directory[-1] != '/':
      directory +='/'

   pixch_ddir = top_shapes_dir + directory + "pixch/data/"
   pixch_dfile = pixch_ddir  + im_fnames + ".data"
   with open (pixch_dfile, 'rb') as fp:
      pixch = pickle.load(fp)
   fp.close()

   shapes_dfile = top_shapes_dir + directory + "shapes/" + main_filename + "shapes.data"
   with open (shapes_dfile, 'rb') as fp:
      # { "shapeid": [ pixel indexes ], ... }
      image_shapes = pickle.load(fp)
   fp.close()

   # { shapeid: % of pixch, ... }
   pixch_shapes = {}
   most_pixch_shapes = []

   for shapeid in image_shapes:
      pixch_pixels = [ pixel for pixel in image_shapes[shapeid] if pixel in pixch ]
   
      if len( pixch_pixels ) >= len( image_shapes[shapeid] ) * 0.8:
         # 80% or more pixels have changed
         most_pixch_shapes.append( shapeid )

      pixch_shapes[ shapeid ] = pixch_pixels

   pixch_shapes_file = pixch_ddir + im_fnames + "." + main_filename + "pixch_shapes.data"
   with open(pixch_shapes_file, 'wb') as fp:
      pickle.dump(pixch_shapes, fp)
   fp.close()

   pixch_shapes_file = pixch_ddir + im_fnames + "." + main_filename + "most_ch.data"
   with open(pixch_shapes_file, 'wb') as fp:
      pickle.dump(most_pixch_shapes, fp)
   fp.close()



def do_delete( im_fnames , directory, main_filename, target_shapeids ):

   # directory is specified but does not contain /
   if directory != "" and directory[-1] != '/':
      directory +='/'

   pixch_ddir = top_shapes_dir + directory + "pixch/data/"
   pixch_shapes_file = pixch_ddir + im_fnames + "." + main_filename + "pixch_shapes.data"
   with open (pixch_shapes_file, 'rb') as fp:
      pixch_shapes = pickle.load(fp)
   fp.close()

   most_pixch_shapes_file = pixch_ddir + im_fnames + "." + main_filename + "most_ch.data"
   with open (most_pixch_shapes_file, 'rb') as fp:
      most_pixch_shapes = pickle.load(fp)
   fp.close()

   for target_shapeid in target_shapeids:
      if target_shapeid in pixch_shapes:
         pixch_shapes.pop(target_shapeid)
         
      if target_shapeid in most_pixch_shapes:
         most_pixch_shapes.remove( target_shapeid )
      

   with open(pixch_shapes_file, 'wb') as fp:
      pickle.dump(pixch_shapes, fp)
   fp.close()

   
   with open(most_pixch_shapes_file, 'wb') as fp:
      pickle.dump(most_pixch_shapes, fp)
   fp.close()   







def do_update( im_fnames , directory, main_filename, target_shapeids ):

   # directory is specified but does not contain /
   if directory != "" and directory[-1] != '/':
      directory +='/'

   pixch_ddir = top_shapes_dir + directory + "pixch/data/"
   pixch_dfile = pixch_ddir  + im_fnames + ".data"
   with open (pixch_dfile, 'rb') as fp:
      pixch = pickle.load(fp)
   fp.close()
   
   pixch_shapes_file = pixch_ddir + im_fnames + "." + main_filename + "pixch_shapes.data"
   with open (pixch_shapes_file, 'rb') as fp:
      pixch_shapes1 = pickle.load(fp)
   fp.close()

   most_ch_shapes_dfile = pixch_ddir + im_fnames + "." + main_filename + "most_ch.data"
   with open (most_ch_shapes_dfile, 'rb') as fp:
      most_ch_shapes = pickle.load(fp)
   fp.close()



   shapes_dfile = top_shapes_dir + directory + "shapes/" + main_filename + "shapes.data"
   with open (shapes_dfile, 'rb') as fp:
      # { "shapeid": [ pixel indexes ], ... }
      image_shapes = pickle.load(fp)
   fp.close() 

   for shapeid in target_shapeids:
      pixch_pixels = [ pixel for pixel in image_shapes[shapeid] if pixel in pixch ]
   
      if len( pixch_pixels ) >= len( image_shapes[shapeid] ) * 0.8:
         # 80% or more pixels have changed
         if shapeid not in most_ch_shapes:
            most_ch_shapes.append( shapeid )

      pixch_shapes1[ shapeid ] = pixch_pixels

   pixch_shapes_file = pixch_ddir + im_fnames + "." + main_filename + "pixch_shapes.data"
   with open(pixch_shapes_file, 'wb') as fp:
      pickle.dump(pixch_shapes1, fp)
   fp.close()

   pixch_shapes_file = pixch_ddir + im_fnames + "." + main_filename + "most_ch.data"
   with open(pixch_shapes_file, 'wb') as fp:
      pickle.dump(most_ch_shapes, fp)
   fp.close()      





















