# create pixel change image under top image directory

from PIL import Image
import re, pickle

import os, sys
from libraries.cv_globals import proj_dir

if proj_dir != "" and proj_dir[-1] != "/":
   proj_dir +='/'

top_shapes_dir = proj_dir + "shapes/"
top_images_dir = proj_dir + "images/"


def do_create( im1file, im2file, directory ):

   pixch_color = ( 0, 255, 0 )
   back_ground_clr = ( 0, 0, 0 )

   # directory is specified but does not contain /
   if directory != "" and directory[-1] != ('/'):
      directory +='/'


   pixch_imdir = top_images_dir + directory + "pixch/"

   im1 = Image.open(top_images_dir + directory + im1file + ".png" )
   im1pxls = im1.getdata()
   im1width, im1height = im1.size

   im2 = Image.open(top_images_dir + directory + im2file + ".png" )
   im2pxls = im2.getdata()
   im2width, im2height = im2.size


   pxlch_im = Image.new('RGB', (im1width,im1height))

   image_data = []
   pixch_data = []


   #image_size[0] is image width
   for y in range(im1height):


     for x in range(im1width):

       #getting pixel index value.
       pixel_index =  ( y * im1width ) + x
    
       # if im1pxls[pixel_index] != im2pxls[pixel_index] and ( im1pxls[pixel_index] != (255, 255, 255) and im2pxls[pixel_index] != (255, 255, 255) ): 
       if im1pxls[pixel_index] != im2pxls[pixel_index] :
          image_data.append( pixch_color )    

          pixch_data.append( str(pixel_index) )

       else:
          # if pixel did not chage
          image_data.append( back_ground_clr )


   pxlch_im.putdata (image_data)


   temp_num = [x for x in list(im1file) if x.isdigit()]
   im1file_num = ""
   for i in range( 0, len( temp_num ) ):
      im1file_num += temp_num[i]

   im2file_num = ""
   temp_num = [x for x in list(im2file) if x.isdigit()]
   for i in range( 0, len( temp_num ) ):
      im2file_num += temp_num[i]
   
   if os.path.exists(pixch_imdir ) == False:
      os.makedirs(pixch_imdir )


   pxlch_im.save (pixch_imdir  + im1file_num + "." + im2file_num + ".png" )


if __name__ == '__main__':
   im1file = ""
   im2file = ""
   directory = ""
   
   do_create( im1file, im2file, directory )















