# find staying large shapes between frames.py
# if pixel changes ocurr only a little inside the shape and not at the boundaries, then this likely implies that
# shape is still at the same location.
# take out the pixel changes from the shape. then match based on the non-changed pixels.
import tkinter
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions, same_shapes_btwn_frames, read_files_functions, image_functions, pixel_functions
from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir, styLshapes_wo_pixch, spixc_shapes, internal
import pickle
import math
import winsound
import sys, os

filename1 = "14"
directory = "videos/street3/resized/min"
filename2 = "15"
filenames = [ filename1, filename2 ]
shapes_type = "intnl_spixcShp"



# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'


if shapes_type == "normal":
   print("shapes_type normal is not supported")
   sys.exit()


elif shapes_type == "intnl_spixcShp":
   staying_Lshapes_Ddir = top_shapes_dir + directory + styLshapes_wo_pixch + "/" + shapes_type + "/data/"
   
   s_pixcShp_intnl_dir = top_shapes_dir + directory + spixc_shapes + "/" + internal + "/"

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

else:
   print("ERROR at " + str( os.path.basename(__file__) ) + " shapes_type " + shapes_type + " is not supported")
   sys.exit()


if os.path.exists(staying_Lshapes_Ddir ) == False:
   os.makedirs(staying_Lshapes_Ddir )

staying_Lshapes_wo_pixch_dfile = staying_Lshapes_Ddir + filename1 + "." + filename2 + ".data"


pixch_dir = top_shapes_dir + directory + "pixch/data/"
pixch_file = pixch_dir + filename1 + "." + filename2 + ".data"

with open (pixch_file, 'rb') as fp:
   # ['57', '66', '107',... ]
   pixch = pickle.load(fp)
fp.close()


im1_stats = image_functions.get_image_stats( filename1, directory, shapes_type=shapes_type )
# [(6267, ['69738', ... ]),... ]   [ ( pixel counts, [ list of shapes that have this pixel count ] ), ... ]
# list is ordered by descending pixel counts 
im1_stats = sorted(im1_stats.items(), reverse=True)

print("preparing data....")

# getting image1 shapes pixels without pixel changes
im1shapes_wo_pixch = {}
for im1shapeid in im1shapes:
   # getting all current image1 shape's pixels
   # {'69738': {'x': 158, 'y': 196}, '69737': {'x': 157, 'y': 196},... }
   cur_im1shp_pixels = im1shapes[ im1shapeid ]

   if len( cur_im1shp_pixels ) < 50:
      continue

   # remove changed pixels
   cur_im1shp_pindexes_wo_pixch = []
      
   for pindex in cur_im1shp_pixels:
      if not pindex in pixch:
         cur_im1shp_pindexes_wo_pixch.append( pindex )
   
   im1shapes_wo_pixch[im1shapeid] = cur_im1shp_pindexes_wo_pixch

# getting image2 shapes pixels without pixel changes
im2shapes_wo_pixch = {}
for im2shapeid in im2shapes:
   # getting all current image2 shape's pixels
   # {'69738': {'x': 158, 'y': 196}, '69737': {'x': 157, 'y': 196},... }
   cur_im2shp_pixels = im2shapes[ im2shapeid ]

   if len( cur_im2shp_pixels ) < 50:
      continue

   # remove changed pixels
   cur_im2shp_pindexes_wo_pixch = []
      
   for pindex in cur_im2shp_pixels:
      if not pindex in pixch:
         cur_im2shp_pindexes_wo_pixch.append( pindex )
   
   im2shapes_wo_pixch[im2shapeid] = cur_im2shp_pindexes_wo_pixch


# this is used for displaying closest matched images
root = tkinter.Tk()

matches = []
progress_counter = len( im1shapes_wo_pixch )
for im1shapeid in im1shapes_wo_pixch:
      print(str( progress_counter ) + " remaining" )
      progress_counter -= 1

      # getting all current image1 shape's pixels
      # {'69738': {'x': 158, 'y': 196}, '69737': {'x': 157, 'y': 196},... }
      cur_im1shp_pixels = im1shapes[ im1shapeid ]
      
      # remove changed pixels
      cur_im1shp_pindexes_wo_pixch = im1shapes_wo_pixch[im1shapeid]

      # there has to be more than 30% of nonchanged pixels
      if len( cur_im1shp_pindexes_wo_pixch ) < len( cur_im1shp_pixels ) * 0.3:
         continue

      # there may be multiple image2 shapes matching current image1 shape
      # this happens when current image1 is broken up into pieces.
      # if so, then, matching pieces should be deducted as well in addion to pixel changes.
      cur_matched_shapes = []
      
      
      run_count = 0
      end = False
      prev_matched_pixels = 0

      # image2 shapes needs to be run as long as there remains image1 shape pixels to be matched.
      while end is False:
         run_count += 1
         
         for im2shapeid in im2shapes_wo_pixch:
         
            if run_count >= 2 and len( cur_matched_shapes ) == 0:
               # this is second run but did not find any matching shape, so end it
               end = True
               break

            # remove changed pixels
            cur_im2shp_pindexes_wo_pixch = im2shapes_wo_pixch[im2shapeid]
         
            if len( cur_im2shp_pindexes_wo_pixch ) < len( im2shapes[im2shapeid] ) * 0.3:
               continue

            cur_matched_pixels = []
            for cur_im1shp_pindex_wo_pixch in cur_im1shp_pindexes_wo_pixch:
               if cur_im1shp_pindex_wo_pixch in cur_im2shp_pindexes_wo_pixch:
                  # matched pixel
                  cur_matched_pixels.append( cur_im1shp_pindex_wo_pixch )

            smaller_pixel_counts = 0
            
            if run_count >= 2 and len( cur_matched_shapes ) >= 1:
               # second time run or more than second
               second_run_im1shp_pixels = len( cur_im1shp_pindexes_wo_pixch ) - prev_matched_pixels
               
               if second_run_im1shp_pixels > len( cur_im2shp_pindexes_wo_pixch ):
                  smaller_pixel_counts = len( cur_im2shp_pindexes_wo_pixch )
               else:
                  # current image1 shape is the smaller pixel count shape. so make sure that enough pixels remain to match with 
                  # image2 shape
                  if second_run_im1shp_pixels < len( im1shapes[im1shapeid] ) * 0.3:
                     end = True
                     break
                  smaller_pixel_counts = second_run_im1shp_pixels
            
               if len(cur_matched_pixels) >= smaller_pixel_counts * 0.8:
                  
                  # make sure it is not the same match from the first run
                  if not [ im1shapeid, im2shapeid, cur_matched_pixels ] in  matches:
                     matches.append( [ im1shapeid, im2shapeid, cur_matched_pixels ] )
                     cur_matched_shapes.append( [im1shapeid, im2shapeid] )

               prev_matched_pixels += len( cur_matched_pixels )   
                  
            elif run_count == 1:
               # first time run
               if len( cur_im1shp_pindexes_wo_pixch ) > len( cur_im2shp_pindexes_wo_pixch ):
                  smaller_pixel_counts = len( cur_im2shp_pindexes_wo_pixch )
               else:
                  smaller_pixel_counts = len( cur_im1shp_pindexes_wo_pixch )
            
               if len(cur_matched_pixels) >= smaller_pixel_counts * 0.8:
                  cur_matched_shapes.append( [im1shapeid, im2shapeid] )
                  prev_matched_pixels += len( cur_matched_pixels )
                  matches.append( [ im1shapeid, im2shapeid, cur_matched_pixels ] )
                  
               first = False

            else:
               print("ERROR at " + str( os.path.basename(__file__) ) + " line " + sys._getframe().f_lineno )
               sys.exit()
            
      # displaying closest match images/

      if len( cur_matched_shapes ) >= 1:
         for match_index, match in enumerate( cur_matched_shapes ):     
            # match found for this image1 shape
            window = tkinter.Toplevel(root)
            window.title( cur_matched_shapes[match_index][0] + " " + cur_matched_shapes[match_index][1] )
    

            original_shape_file = top_shapes_dir + directory + "shapes/intnl_spixcShp/" + filename1 + "/" + im1shapeid + ".png"
            compare_shape_file = top_shapes_dir + directory + "shapes/intnl_spixcShp/" + filename2 + "/" + cur_matched_shapes[match_index][1] + ".png"            
   
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

with open(staying_Lshapes_wo_pixch_dfile, 'wb') as fp:
   pickle.dump(matches, fp)
fp.close()






