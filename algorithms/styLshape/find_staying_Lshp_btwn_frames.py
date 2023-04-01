# find staying large shapes between frames.py
# if pixel changes ocurr only a little inside the shape and not at the boundaries, then this likely implies that
# shape is still at the same location.
import tkinter
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions, same_shapes_btwn_frames, read_files_functions, image_functions, pixel_functions
from libraries.cv_globals import  top_shapes_dir, top_images_dir, styLshapes, spixc_shapes, internal
import pickle
import math
import winsound
import sys, os

###########################                    user input begin                ##################################
filename1 = "12"
directory = "videos/street3/resized/min"
filename2 = "13"
filenames = [ filename1, filename2 ]
shapes_type = "intnl_spixcShp"
###########################                    user input end                  ##################################


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

original_image = Image.open(top_images_dir + directory + filename1 + ".png")
im_width, im_height = original_image.size


im1shapes_boundaries = {}
im2shapes_boundaries = {}
if shapes_type == "normal":
   staying_Lshapes_Ddir = top_shapes_dir + directory + styLshapes + "/normal/data/"
   
   im1shapes_locations_path = top_shapes_dir + directory + "locations/" + filename1 + "_loc.txt"
   im2shapes_locations_path = top_shapes_dir + directory + "locations/" + filename2 + "_loc.txt"



   # returned value has below form
   # shapes[shapes_id][pixel_index] = {}
   # shapes[shapes_id][pixel_index]['x'] = x
   # shapes[shapes_id][pixel_index]['y'] = y
   im1shapes = read_files_functions.rd_shapes_file(filename1, directory)
   im2shapes = read_files_functions.rd_shapes_file(filename2, directory)   
   
   # get boundary pixels of all shapes
   for shapeid in im1shapes:
      im1shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels(im1shapes[shapeid] )
   
   # get boundary pixels of all shapes
   for shapeid in im2shapes:
      im2shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels(im2shapes[shapeid] )
   
   
   
   
elif shapes_type == "intnl_spixcShp":
   staying_Lshapes_Ddir = top_shapes_dir + directory + styLshapes + "/intnl_spixcShp/data/"
   
   s_pixcShp_intnl_dir = top_shapes_dir + directory + spixc_shapes  + "/" + internal + "/"
   
   s_pixcShp_intnl_loc_dir = s_pixcShp_intnl_dir + "locations/"
   im1shapes_locations_path = s_pixcShp_intnl_loc_dir + filename1 + "_loc.txt"   
   im2shapes_locations_path = s_pixcShp_intnl_loc_dir + filename2 + "_loc.txt"  

   
   shapes_dir = s_pixcShp_intnl_dir + "shapes/"

   shapes_dfile = shapes_dir + filename1 + "shapes.data"
   im2shapes_dfile = shapes_dir + filename2 + "shapes.data"

   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()

   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()   

   # get boundary pixels of all shapes
   for shapeid in im1shapes:
      cur_shape_pixels = { }
      for pindex in im1shapes[shapeid]:
         cur_shape_pixels[pindex] = {}
            
         y = math.floor( int(pindex) / im_width)
         x  = int(pindex) % im_width 
      
         cur_shape_pixels[pindex]['x'] = x
         cur_shape_pixels[pindex]['y'] = y

      # {1: {'x': 190, 'y': 30}, 2: {'x': 190, 'y': 31},.... }
      # convert this form into list of pixel indexes
      cur_pixels = pixel_shapes_functions.get_boundary_pixels(cur_shape_pixels )
      
      cur_pindexes = []
      for pixel in cur_pixels.values():
         pindex = pixel['x'] + ( pixel['y'] * im_width )
         
         cur_pindexes.append( str( pindex ) )
      
      im1shapes_boundaries[shapeid] = cur_pindexes
      

   # get boundary pixels of all shapes
   for shapeid in im2shapes:
      cur_shape_pixels = { }
      for pindex in im2shapes[shapeid]:
         cur_shape_pixels[pindex] = {}
            
         y = math.floor( int(pindex) / im_width)
         x  = int(pindex) % im_width 
      
         cur_shape_pixels[pindex]['x'] = x
         cur_shape_pixels[pindex]['y'] = y

      # {1: {'x': 190, 'y': 30}, 2: {'x': 190, 'y': 31},.... }
      # convert this form into list of pixel indexes
      cur_pixels = pixel_shapes_functions.get_boundary_pixels(cur_shape_pixels )
      
      cur_pindexes = []
      for pixel in cur_pixels.values():
         pindex = pixel['x'] + ( pixel['y'] * im_width )
         
         cur_pindexes.append( str( pindex ) )
      
      im2shapes_boundaries[shapeid] = cur_pindexes


   
else:
   print("ERROR at " + str( os.path.basename(__file__) ) + " shapes_type " + shapes_type + " is not supported")
   sys.exit()


im1s_locations = read_files_functions.rd_ldict_k_v_l( filename1, directory, im1shapes_locations_path )
im2s_locations = read_files_functions.rd_ldict_k_v_l( filename2, directory, im2shapes_locations_path )


if os.path.exists(staying_Lshapes_Ddir ) == False:
   os.makedirs(staying_Lshapes_Ddir )

staying_Lshapes1to2_dfile = staying_Lshapes_Ddir + filename1 + "." + filename2 + ".data"


pixch_dir = top_shapes_dir + directory + "pixch/data/"
pixch_file = pixch_dir + filename1 + "." + filename2 + ".data"

with open (pixch_file, 'rb') as fp:
   # ['57', '66', '107',... ]
   pixch = pickle.load(fp)
fp.close()


im1shapes_in_im_areas = {}
for shapeid in im1shapes:
   for s_locs in im1s_locations:
      if shapeid in s_locs.keys():
         im1shapes_in_im_areas[shapeid] = s_locs[ list(s_locs.keys())[0] ]
         break
im2shapes_in_im_areas = {}
for shapeid in im2shapes:
   for s_locs in im2s_locations:
      if shapeid in s_locs.keys():
         im2shapes_in_im_areas[shapeid] = s_locs[ list(s_locs.keys())[0] ]
         break


im1_stats = image_functions.get_image_stats( filename1, directory, shapes_type=shapes_type )
# [(6267, ['69738', ... ]),... ]   [ ( pixel counts, [ list of shapes that have this pixel count ] ), ... ]
# list is ordered by descending pixel counts 
im1_stats = sorted(im1_stats.items(), reverse=True)

im2_stats = image_functions.get_image_stats( filename2, directory, shapes_type=shapes_type )
im2_stats = sorted(im2_stats.items(), reverse=True)

original_image = Image.open(top_images_dir + directory + filename1 + ".png")
image_width, image_height = original_image.size

original_im_area = image_functions.get_image_areas( filename1, directory )
      
      

all_matches1to2 = []
all_matches2to1 = []

# this is used for displaying closest matched images
root = tkinter.Tk()

progress_counter = len( im1_stats )
for im1pcount_shapes in im1_stats:
   if im1pcount_shapes[0] < 50:
      continue

   print( str( progress_counter ) + " remaining" )
   progress_counter -= 1

   # looping list of shapes for each pixel counts
   for im1shapeid in im1pcount_shapes[1]:


      cur_match1to2 = [im1shapeid]
      cur_match2to1 = [im1shapeid]

      # getting all current image1 shape's pixels
      # {'69738': {'x': 158, 'y': 196}, '69737': {'x': 157, 'y': 196},... } for normal shape type
      # [ pixel indexes ] for intnl_spixcShp shape type
      cur_im1shp_pixels = im1shapes[ im1shapeid ]

      # getting all current image1 shape's boundary pixels
      # {1: {'x': 190, 'y': 30}, 2: {'x': 190, 'y': 31},.... } for normal shape type
      # [ pixel indexes ] for intnl_spixcShp shape type
      cur_im1shp_bnd_pixels = im1shapes_boundaries[ im1shapeid ]


      # remove boundary pixels from image1 shape's pixels
      cur_im1shp_pindexes_wo_bnd = []
      
      if shapes_type == "normal":
         for pindex, pixel_xy in cur_im1shp_pixels.items():
            if not pixel_xy in cur_im1shp_bnd_pixels.values():
               cur_im1shp_pindexes_wo_bnd.append( pindex )
      elif shapes_type == "intnl_spixcShp":
         for pindex in cur_im1shp_pixels:
            if not pindex in cur_im1shp_bnd_pixels:
               cur_im1shp_pindexes_wo_bnd.append( pindex )


      # pixels of current image1 shape that did not change
      cur_im1shp_pindexes_not_ch = []
      
      for pindex in cur_im1shp_pindexes_wo_bnd:
         if not pindex in pixch:
            cur_im1shp_pindexes_not_ch.append( pindex )
            
      
      # check if more than 50% of pixels did not change. this ensures that shape is still at the same location because
      # lots of shape pixel changes implies that it moved to another location or it changed its shape more than just a little
      if len( cur_im1shp_pindexes_not_ch ) < len( cur_im1shp_pindexes_wo_bnd ) * 0.5:
         continue
         
      
      cur_im1shp_locations = im1shapes_in_im_areas[im1shapeid]


      for im2pcount_shapes in im2_stats:
      
         if im2pcount_shapes[0] < 50:
            continue

         # looping list of shapes for each pixel counts
         for im2shapeid in im2pcount_shapes[1]:
         
            # check if current im1shapeid and im2shapeid are located at the same place
            cur_im2shp_locations = im2shapes_in_im_areas[im2shapeid]
            check = any(im_area in cur_im1shp_locations for im_area in cur_im2shp_locations)

            if not check:
               continue            

            # getting all current image2 shape's pixels
            # {'69738': {'x': 158, 'y': 196}, '69737': {'x': 157, 'y': 196},... }
            cur_im2shp_pixels = im2shapes[ im2shapeid ]

            # getting all current image2 shape's boundary pixels
            # {1: {'x': 190, 'y': 30}, 2: {'x': 190, 'y': 31},.... }
            cur_im2shp_bnd_pixels = im2shapes_boundaries[ im2shapeid ]


            # remove boundary pixels from image1 shape's pixels
            cur_im2shp_pindexes_wo_bnd = []
      
            if shapes_type == "normal":
               for pindex, pixel_xy in cur_im2shp_pixels.items():
                  if not pixel_xy in cur_im2shp_bnd_pixels.values():
                     cur_im2shp_pindexes_wo_bnd.append( pindex )
            elif shapes_type == "intnl_spixcShp":
               for pindex in cur_im2shp_pixels:
                  if not pindex in cur_im2shp_bnd_pixels:
                     cur_im2shp_pindexes_wo_bnd.append( pindex )




            # pixels of current image2 shape that did not change
            cur_im2shp_pindexes_not_ch = []
      
            for pindex in cur_im2shp_pindexes_wo_bnd:
               if not pindex in pixch:
                  cur_im2shp_pindexes_not_ch.append( pindex )

      
      
            # check if more than 50% of pixels did not change. this ensures that shape is still at the same location because
            # lots of shape pixel changes implies that it moved to another location or it changed its shape more than just a little
            if len( cur_im2shp_pindexes_not_ch ) < len( cur_im2shp_pindexes_wo_bnd ) * 0.5:
               continue

            not_ch_p_match_count1to2 = 0
            not_ch_p_match_count2to1 = 0
            
            # image1 shape's not changed pixel in image2 shape's not changed pixels?
            for cur_im1not_ch_pix in cur_im1shp_pindexes_not_ch:
               if cur_im1not_ch_pix in cur_im2shp_pindexes_not_ch:
                  not_ch_p_match_count1to2 += 1
            # reverse of above. image2 shape's not changed pixel is in image1 shape's not changed pixels?
            for cur_im2not_ch_pix in cur_im2shp_pindexes_not_ch:
               if cur_im2not_ch_pix in cur_im1shp_pindexes_not_ch:
                  not_ch_p_match_count2to1 += 1

            # comparison operator is greater than and not greater than equal to. this is because there is a chance that
            # not changed pixel count might be 0. if so, even if no pixel matching can become matched.
            if not_ch_p_match_count1to2 > len( cur_im1shp_pindexes_not_ch ) * 0.8:
               # most of image1 shape's not changed pixels are matched with image2 shape's not changed pixels
               cur_match1to2.append( im2shapeid )
            if not_ch_p_match_count2to1 > len( cur_im2shp_pindexes_not_ch ) * 0.8:
               # most of image2 shape's not changed pixels are matched with image1 shape's not changed pixels
               cur_match2to1.append( im2shapeid )



      display_match = []
      # displaying closest match images/
      if len(cur_match1to2) == 2:
         all_matches1to2.append( cur_match1to2 )
         display_match.extend( cur_match1to2 )
      if len(cur_match2to1) == 2:
         all_matches2to1.append( cur_match2to1 )
         if len(display_match) == 0:
            display_match.extend( cur_match2to1 )
      
      if len( display_match ) == 2:      
         # match found for this image1 shape
         window = tkinter.Toplevel(root)
         window.title( display_match[0] + " " + display_match[1] )
         
         
         if shapes_type == "normal":
            original_shape_file = top_shapes_dir + directory + "shapes/" + str(filename1) + "_shapes/" + str(im1shapeid) + ".png"
            compare_shape_file = top_shapes_dir + directory + "shapes/" + str(filename2) + "_shapes/" + str(display_match[1]) + ".png"
         elif shapes_type == "intnl_spixcShp":
            original_shape_file = top_shapes_dir + directory + "shapes/intnl_spixcShp/" + str(filename1) + "/" + str(im1shapeid) + ".png"
            compare_shape_file = top_shapes_dir + directory + "shapes/intnl_spixcShp/" + str(filename2) + "/"  + str(display_match[1]) + ".png"         
         
   
         img = ImageTk.PhotoImage(Image.open(original_shape_file))
         img2 = ImageTk.PhotoImage(Image.open(compare_shape_file))
  
         label1 = tkinter.Label(window, image = img, bg="white")
         label1.image = img
         label1.pack()
   
         label2 = tkinter.Label(window, image = img2, bg="white" )
         label2.image = img2
         label2.pack()
      
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)      

root.mainloop()

unique_sty_im1_2_shapes = [value for value in all_matches1to2 if value not in all_matches2to1]
unique_sty_im2_1_shapes = [value for value in all_matches2to1 if value not in all_matches1to2]
common_sty_im1_2_shapes = [value for value in all_matches2to1 if value in all_matches1to2]

# [['12641', '13043'], ['44346', '44748'], ... ]
all_sty_im1_2_shapes = unique_sty_im1_2_shapes + unique_sty_im2_1_shapes + common_sty_im1_2_shapes


with open(staying_Lshapes1to2_dfile, 'wb') as fp:
   pickle.dump(all_sty_im1_2_shapes, fp)
fp.close()

















