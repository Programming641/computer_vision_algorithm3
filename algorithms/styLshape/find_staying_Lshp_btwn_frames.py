# find staying large shapes between frames.py
# if pixel changes ocurr only a little inside the shape and not at the boundaries, then this likely implies that
# shape is still at the same location.
import tkinter
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions, image_functions, pixel_functions, cv_globals
from libraries.cv_globals import  top_shapes_dir, top_images_dir, styLshapes, spixc_shapes
import pickle
import math
import winsound
import sys, os

###########################                    user input begin                ##################################
filename1 = "2"
directory = "videos/horse1/resized/min"
filename2 = "3"
shapes_type = "intnl_spixcShp"
display_or_not = True
###########################                    user input end                  ##################################

if len(sys.argv) > 1:
   filename1 = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   filename2 = sys.argv[1][0: len( sys.argv[1] ) - 4 ]
   directory = sys.argv[3]
   
   shapes_type = "intnl_spixcShp"
   
   display_or_not = False

   print("execute script algorithms/styLshapes/find_staying_Lshp_btwn_frames.py file1 " + filename1 + " file2 " + filename2 + " directory " + directory )



# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

original_image = Image.open(top_images_dir + directory + filename1 + ".png")
im_width, im_height = original_image.size

Lshape_size = cv_globals.get_Lshape_size( original_image.size )

im1shapes_boundaries = {}
im2shapes_boundaries = {}
if shapes_type == "normal":
   print("shapes_type normal is not supported")
   sys.exit()
   
   
elif shapes_type == "intnl_spixcShp":

   shapes_dir = top_shapes_dir + directory + "shapes/"
   
   loc_dir = shapes_dir + "locations/"
   im1shapes_locations_path = loc_dir + filename1 + "_loc.data"   
   im2shapes_locations_path = loc_dir + filename2 + "_loc.data"  

   
   

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


   boundary_dir = shapes_dir + "boundary/"
   boundary_dfile = boundary_dir + filename1 + ".data"
   with open (boundary_dfile, 'rb') as fp:
      im1shapes_boundaries = pickle.load(fp)
   fp.close()

   # get boundary pixels of all shapes
   for shapeid in im1shapes:
      # convert xy into pixel indexes
      cur_pixel_indexes = set()
      for xy in im1shapes_boundaries[shapeid]:
         pindex = pixel_functions.convert_xy_to_pindex( xy, im_width )
         cur_pixel_indexes.add( pindex )
      
      im1shapes_boundaries[shapeid] = cur_pixel_indexes


   boundary_dfile2 = boundary_dir + filename2 + ".data"
   with open (boundary_dfile2, 'rb') as fp:
      im2shapes_boundaries = pickle.load(fp)
   fp.close()



   # get boundary pixels of all shapes
   for shapeid in im2shapes:
      
      # convert xy into pixel indexes
      cur_pixel_indexes = set()
      for xy in im2shapes_boundaries[shapeid]:
         pindex = pixel_functions.convert_xy_to_pindex( xy, im_width )
         cur_pixel_indexes.add( pindex )
      
      im2shapes_boundaries[shapeid] = cur_pixel_indexes


   
else:
   print("ERROR at " + os.path.basename(__file__) + " shapes_type " + shapes_type + " is not supported")
   sys.exit(1)


with open (im1shapes_locations_path, 'rb') as fp:
   # { '79968': ['25'], '79999': ['25'], ... }
   im1s_locations = pickle.load(fp)
fp.close()

with open (im2shapes_locations_path, 'rb') as fp:
   # { '79968': ['25'], '79999': ['25'], ... }
   im2s_locations = pickle.load(fp)
fp.close()


pixch_dir = top_shapes_dir + directory + "pixch/data/"
pixch_file = pixch_dir + filename1 + "." + filename2 + ".data"
with open (pixch_file, 'rb') as fp:
   #  {'378', '20048', ...}
   pixch = pickle.load(fp)
fp.close()


im1_stats = image_functions.get_image_stats( filename1, directory, shapes_type=shapes_type )
# [(6267, ['69738', ... ]),... ]   [ ( pixel counts, [ list of shapes that have this pixel count ] ), ... ]
# list is ordered by descending pixel counts 
im1_stats = sorted(im1_stats.items(), reverse=True)

im2_stats = image_functions.get_image_stats( filename2, directory, shapes_type=shapes_type )
im2_stats = sorted(im2_stats.items(), reverse=True)
      
      
all_matches1to2 = []
all_matches2to1 = []

if display_or_not is True:
   # this is used for displaying closest matched images
   root = tkinter.Tk()

progress_counter = len( im1_stats )
max_progress_num = len( im1_stats )
cur_progress_num = len( im1_stats )
prev_progress_num = len( im1_stats )
remaining_chars = ""
for im1pcount_shapes in im1_stats:
   if im1pcount_shapes[0] < Lshape_size:
      continue

   remaining_chars = btwn_amng_files_functions.show_progress( max_progress_num, cur_progress_num, prev_progress_num, remaining_chars=remaining_chars, in_step=10 )
   prev_progress_num = cur_progress_num
   cur_progress_num -= 1

   # looping list of shapes for each pixel counts
   for im1shapeid in im1pcount_shapes[1]:


      cur_match1to2 = [im1shapeid]
      cur_match2to1 = [im1shapeid]

      # getting all current image1 shape's pixels
      # [ '63299', '63298', ... ]
      cur_im1shp_pixels = im1shapes[ im1shapeid ]

      # getting all current image1 shape's boundary pixels
      # { '75888', '55477', ... }
      cur_im1shp_bnd_pixels = im1shapes_boundaries[ im1shapeid ]
      
      # getting non-boundary pixels
      cur_im1shp_pindexes_wo_bnd = set( cur_im1shp_pixels ).difference( cur_im1shp_bnd_pixels )

      # image1 non-boundary pixels that did not change
      cur_im1shp_pindexes_not_ch = cur_im1shp_pindexes_wo_bnd.difference( pixch )
            
      
      # check if more than 50% of pixels did not change. this ensures that shape is still at the same location because
      # lots of shape pixel changes implies that it moved to another location or it changed its shape more than just a little
      if len( cur_im1shp_pindexes_not_ch ) < len( cur_im1shp_pindexes_wo_bnd ) * 0.5:
         continue
         
      # ['25', '24', '23', '22', '21', '20', '15', '19', '18', '17']
      cur_im1shp_locations = im1s_locations[im1shapeid]


      for im2pcount_shapes in im2_stats:
      
         if im2pcount_shapes[0] < Lshape_size:
            continue

         # looping list of shapes for each pixel counts
         for im2shapeid in im2pcount_shapes[1]:
         
            # check if current im1shapeid and im2shapeid are located at the same place
            cur_im2shp_locations = im2s_locations[im2shapeid]
            same_locations = set( cur_im1shp_locations ).intersection( set( cur_im2shp_locations ) )

            if len( same_locations ) < 1:
               continue            

            # getting all current image2 shape's pixels
            # [ '63299', '63298', ... ]
            cur_im2shp_pixels = im2shapes[ im2shapeid ]

            # getting all current image2 shape's boundary pixels
            # {'66205', '49151', ... }
            cur_im2shp_bnd_pixels = im2shapes_boundaries[ im2shapeid ]


            # remove boundary pixels from image1 shape's pixels
            cur_im2shp_pindexes_wo_bnd = set( cur_im2shp_pixels ).difference( cur_im2shp_bnd_pixels )


            # pixels of current image2 shape that did not change
            cur_im2shp_pindexes_not_ch = cur_im2shp_pindexes_wo_bnd.difference( pixch )

      
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
      
      if len( display_match ) == 2 and display_or_not is True:      
         # match found for this image1 shape
         window = tkinter.Toplevel(root)
         window.title( display_match[0] + " " + display_match[1] )

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


if display_or_not is True:
   root.mainloop()

unique_sty_im1_2_shapes = [value for value in all_matches1to2 if value not in all_matches2to1]
unique_sty_im2_1_shapes = [value for value in all_matches2to1 if value not in all_matches1to2]
common_sty_im1_2_shapes = [value for value in all_matches2to1 if value in all_matches1to2]

# [['12641', '13043'], ['44346', '44748'], ... ]
all_sty_im1_2_shapes = unique_sty_im1_2_shapes + unique_sty_im2_1_shapes + common_sty_im1_2_shapes

staying_Lshapes_Ddir = top_shapes_dir + directory + styLshapes + "/intnl_spixcShp/data/"
if os.path.exists(staying_Lshapes_Ddir ) == False:
   os.makedirs(staying_Lshapes_Ddir )

staying_Lshapes1to2_dfile = staying_Lshapes_Ddir + filename1 + "." + filename2 + ".data"
with open(staying_Lshapes1to2_dfile, 'wb') as fp:
   pickle.dump(all_sty_im1_2_shapes, fp)
fp.close()

















