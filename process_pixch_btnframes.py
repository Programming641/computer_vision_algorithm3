# reference note: "find same colored object between two adjacent video frames"
# folder name: find_1clrobj_btwn_frames

# shape and object are the same thing.

from PIL import Image
import re
from libraries import pixel_shapes_functions, read_files_functions
import math
import os, sys


def fill_im1objs_wpix( im1objs, same_chpix, sameorch ):

   # for storing same pixel data for the image1 objects into im1objs_allpix
   for each_im1same in same_chpix:
      cur_im1obj = list(each_im1same.values())[0][0]
      cur_im2obj = list(each_im1same.values())[0][1]
      cur_pixindex = list( each_im1same.keys())[0]


      cur_im1obj_present = False

      # checking if current image1 object is already in im1objs
      for im1obj_allpix in im1objs:
         if cur_im1obj in im1obj_allpix:
            # current im1obj_allpix is the cur_im1obj, so get it
            cur_im1obj_present = True
            
            # current im1obj_allpix is cur_im1obj but not sure if it contains current sameorch. add it if it doesn't
            if not sameorch in im1obj_allpix[ cur_im1obj ]:
               im1obj_allpix[ cur_im1obj ][sameorch] = [ { cur_im2obj: [ cur_pixindex ] } ]
               
               break
         
            # check if staythesame image2 index number is already added
            # get staythesame list index number for the cur_im2obj
            stayim2_lindex = next((index for (index, d) in enumerate( im1obj_allpix[ cur_im1obj][sameorch] ) if cur_im2obj in d ), None)
            if stayim2_lindex != None:

         
               im1obj_allpix[ cur_im1obj ][sameorch][ stayim2_lindex ][ cur_im2obj ].append( cur_pixindex )
         
            else:
               im1obj_allpix[ cur_im1obj ][ sameorch ].append( { cur_im2obj: [ cur_pixindex ] } )
         
         
   

      if len( im1objs ) == 0 or not cur_im1obj_present:
         im1objs.append( { cur_im1obj : { sameorch : [ { cur_im2obj: [ cur_pixindex ] } ] } } )

               
   return im1objs


def fill_im2objs_wpix( im2objs, same_chpix, sameorch ):

   # for storing same pixel data for the image1 objects into im1objs_allpix
   for each_im1same in same_chpix:
      cur_im1obj = list(each_im1same.values())[0][0]
      cur_im2obj = list(each_im1same.values())[0][1]
      cur_pixindex = list( each_im1same.keys())[0]



      cur_im1obj_present = False

      # checking if current image1 object is already in im2objs
      for im2obj_allpix in im2objs:
         if cur_im2obj in im2obj_allpix:
            # current im2obj_allpix is the cur_im2obj, so get it
            cur_im1obj_present = True
            
            # current im2obj_allpix is cur_im2obj but not sure if it contains current sameorch. add it if it doesn't
            if not sameorch in im2obj_allpix[ cur_im2obj ]:
               im2obj_allpix[ cur_im2obj ][sameorch] = [ { cur_im1obj: [ cur_pixindex ] } ]
               
               break
         
            # check if staythesame image2 index number is already added
            # get staythesame list index number for the cur_im1obj
            stayim1_lindex = next((index for (index, d) in enumerate( im2obj_allpix[ cur_im2obj][sameorch] ) if cur_im1obj in d ), None)
            if stayim1_lindex != None:
         
               im2obj_allpix[ cur_im2obj ][sameorch][ stayim1_lindex ][ cur_im1obj ].append( cur_pixindex )
         
            else:
               im2obj_allpix[ cur_im2obj ][ sameorch ].append( { cur_im1obj: [ cur_pixindex ] } )
         
         
   

      if len( im2objs ) == 0 or not cur_im1obj_present:
         im2objs.append( { cur_im2obj : { sameorch : [ { cur_im1obj: [ cur_pixindex ] } ] } } )

               
   return im2objs


















directory = "videos/hanger"

im1file = "1_clrgrp"
im2file = "2_clrgrp"

# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

shapes_dir = "shapes/" + directory


im1objs_filename = shapes_dir + im1file[0:1] + "." + im2file[0:1] + im1file[1: len( im1file ) ] + "_diff1objs.txt"
im2objs_filename = shapes_dir + im1file[0:1] + "." + im2file[0:1] + im1file[1: len( im1file ) ] + "_diff2objs.txt"

im1 = Image.open("images/" + directory + im1file + ".png" )
im1pxls = im1.getdata()
im1width, im1height = im1.size

im2 = Image.open("images/" + directory + im2file + ".png" )
im2pxls = im2.getdata()
im2width, im2height = im2.size

# returned value has below form
# { { { } } }
# shapes[shapes_id][pixel_index] = {}
# shapes[shapes_id][pixel_index]['x'] = x
# shapes[shapes_id][pixel_index]['y'] = y
im1shape_pindexes = read_files_functions.read_shapes_file(im1file, directory)
im2shape_pindexes = read_files_functions.read_shapes_file(im2file, directory)


# for storing all image1 and image2 pixels at pixel change locations
im1pixch = []
im2pixch = []

# for storing all image1 and image2 objects at pixel change locations
# { shapeid : [ pixelindex1, pixelindex2, pixelindex3.... ] , shapeid2 : [ pixelindex15, pixelindex20,.... ] }
im1objs_atch = {}
im2objs_atch = {}

# image1 and image2 objects at pixel change location
# pixel1 changed. get image1 object and image2 object at pixel1 location
# [ { location of pixel changed : [ image1 object index, image2 object index ] }, ..... ]
im1im2objs_atch = []

im1objs = []
im2objs = []

# image1 objects with their changed pixels
# if pixel1 changed in image1 object1 then this will be included in it
# [ { shape_id1: [ changed pixel1 in shape id1, changed pixel2 in shape id1... ] }, .... ]
im1objs_wch = []
im2objs_wch = []



# [  {'57598': ['54720', '42120']}, {'57599': ['54720', '42120']} ]
# [ { staythesame pixel index number : [ image1 object index number , image2 object index number ] } ]
im1im2samepix = []


# im1objs_allpix = [ { image1 object index number : { staythesame: [ { image2index number : [ pixel index ] } ] },
#                                                   { ch : [ { image2 index number : [ pixel index ] } ] } } ]
# see note: "storing image object's pixels between video frames."
im1objs_allpix = []

im2objs_allpix = []


print("processing started. please wait")

for y in range(im1height):

  for x in range(im1width):

    #getting pixel index value.
    pixel_index =  ( y * im1width ) + x
    
    pixel_index = str( pixel_index )
    
    # check pixel change
    if im1pxls[ int(pixel_index)] != im2pxls[ int(pixel_index) ] :
       
       im1pixch.append( {pixel_index: im1pxls[ int(pixel_index) ] } )
       im2pixch.append( { pixel_index: im2pxls[ int(pixel_index) ] } )
       
       im1im2objs_atch.append( { pixel_index : [] } )
       
       
    else:
       im1im2samepix.append( { pixel_index : [] } )


for samepixel in im1im2samepix:
   samep = list( samepixel.keys() )[0]
   for im1shapeid, im1shapeid_pindexes in im1shape_pindexes.items():
      if samep in list( im1shapeid_pindexes.keys() ):
         samepixel[ samep ].append( im1shapeid )
         
   for im2shapeid, im2shapeid_pindexes in im2shape_pindexes.items():
      if samep in list( im2shapeid_pindexes.keys() ):
         samepixel[ samep ].append( im2shapeid )
         

print("finished im1im2samepix")

# this is for filling im1objs_atch with all objects at pixel change locations
for each_im1pixch in im1pixch:
   changed_pix = list(each_im1pixch.keys())[0]
   for im1shapeid, im1shapeid_pindexes in im1shape_pindexes.items():
      if changed_pix in list( im1shapeid_pindexes.keys() ):
         # changed_pix is included in im1shapeid_pindexes. 
         im1objs_atch[ im1shapeid ] = { }
         
         im1objs.append( im1shapeid )

         for im1obj_wch in im1objs_wch:
            if im1obj_wch.get(im1shapeid):
               im1obj_wch[im1shapeid].append( changed_pix )
               break
            elif not any(im1shapeid in d for d in im1objs_wch):
               im1objs_wch.append( { im1shapeid: [ changed_pix ] } )
               break       
               
         if len(im1objs_wch) == 0:
            im1objs_wch.append( { im1shapeid: [ changed_pix ] } )
         

         for each_im1im2objs_atch in im1im2objs_atch:
            if list( each_im1im2objs_atch.keys() )[0] == changed_pix:
               each_im1im2objs_atch[ changed_pix ].append( im1shapeid )
         
         
         for im1shapeid_pindex, xy in im1shapeid_pindexes.items():
            
            im1objs_atch[ im1shapeid ][ im1shapeid_pindex ] = xy
            

print("finished im1objs_atch")

# this is for filling im2objs_atch with all objects at pixel change locations
for each_im2pixch in im2pixch:
   changed_pix = list(each_im2pixch.keys())[0]
   for im2shapeid, im2shapeid_pindexes in im2shape_pindexes.items():
      if changed_pix in list( im2shapeid_pindexes.keys() ):
         # each_im2pixch pixel is included in im2shapeid_pindexes. 
         im2objs_atch[ im2shapeid ] = { }
         
         im2objs.append( im2shapeid )
         
         for im2obj_wch in im2objs_wch:
            if im2obj_wch.get(im2shapeid):
               im2obj_wch[im2shapeid].append( changed_pix )
            elif not any(im2shapeid in d for d in im2objs_wch):
               im2objs_wch.append( { im2shapeid: [ changed_pix ] } )
               break       
         
         if len(im2objs_wch) == 0:
            im2objs_wch.append( { im2shapeid: [ changed_pix ] } )        
         
         for each_im1im2objs_atch in im1im2objs_atch:
            if list( each_im1im2objs_atch.keys() )[0] == changed_pix:
               each_im1im2objs_atch[ changed_pix ].append( im2shapeid )
        
         
         for im2shapeid_pindex, xy in im2shapeid_pindexes.items():
            
            im2objs_atch[ im2shapeid ][ im2shapeid_pindex ] = xy


print("proceeding to get im1objs_allpix")

im1objs_allpix = fill_im1objs_wpix( im1objs_allpix, im1im2samepix,  "staythesame" )
im1objs_allpix = fill_im1objs_wpix( im1objs_allpix, im1im2objs_atch, "change" )

print("proceeding to get im2objs_allpix")

im2objs_allpix = fill_im2objs_wpix( im2objs_allpix, im1im2samepix,  "staythesame" )
im2objs_allpix = fill_im2objs_wpix( im2objs_allpix, im1im2objs_atch, "change" )


im1objs_file = open( im1objs_filename, mode="w" )
im1objs_file.write(str(im1objs_allpix))

im2objs_file = open( im2objs_filename, mode="w" )
im2objs_file.write(str(im2objs_allpix))
























