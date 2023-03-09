# find staying large shapes between frames.py
# if pixel changes ocurr only a little inside the shape and not at the boundaries, then this likely implies that
# shape is still at the same location.
import tkinter
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions, same_shapes_btwn_frames, read_files_functions, image_functions, pixel_functions
from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir
import pickle
import math
import winsound
import sys, os

filename1 = "24"

directory = "videos/giraffe/min"

filename2 = "25"

filenames = [ filename1, filename2 ]

# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

staying_Lshapes_Ddir = top_shapes_dir + directory + "staying_Lshapes/data/"

if os.path.exists(staying_Lshapes_Ddir ) == False:
   os.makedirs(staying_Lshapes_Ddir )

staying_Lshapes1to2_dfile = staying_Lshapes_Ddir + filename1 + "to" + filename2 + ".data"
staying_Lshapes2to1_dfile = staying_Lshapes_Ddir + filename2 + "to" + filename1 + ".data"


pixch_dir = top_shapes_dir + directory + "pixch/data/"
pixch_file = pixch_dir + filename1 + "." + filename2 + ".data"

with open (pixch_file, 'rb') as fp:
   # ['57', '66', '107',... ]
   pixch = pickle.load(fp)
fp.close()


im1shapes_locations_path = top_shapes_dir + directory + "locations/" + filename1 + "_loc.txt"
im2shapes_locations_path = top_shapes_dir + directory + "locations/" + filename2 + "_loc.txt"

im1s_locations = read_files_functions.rd_ldict_k_v_l( filename1, directory, im1shapes_locations_path )
im2s_locations = read_files_functions.rd_ldict_k_v_l( filename2, directory, im2shapes_locations_path )

# returned value has below form
# shapes[shapes_id][pixel_index] = {}
# shapes[shapes_id][pixel_index]['x'] = x
# shapes[shapes_id][pixel_index]['y'] = y
im1shapes = read_files_functions.rd_shapes_file(filename1, directory)
im2shapes = read_files_functions.rd_shapes_file(filename2, directory)

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

im1shapes_boundaries = {}
# get boundary pixels of all shapes
for shapeid in im1shapes:
   im1shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels(im1shapes[shapeid] )
im2shapes_boundaries = {}
# get boundary pixels of all shapes
for shapeid in im2shapes:
   im2shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels(im2shapes[shapeid] )


im1_stats = image_functions.get_image_stats( filename1, directory )
# [(6267, ['69738', ... ]),... ]   [ ( pixel counts, [ list of shapes that have this pixel count ] ), ... ]
# list is ordered by descending pixel counts 
im1_stats = sorted(im1_stats.items(), reverse=True)

im2_stats = image_functions.get_image_stats( filename2, directory )
im2_stats = sorted(im2_stats.items(), reverse=True)



original_image = Image.open(top_images_dir + directory + filename1 + ".png")
image_width, image_height = original_image.size


original_im_area = image_functions.get_image_areas( filename1, directory )

im1and2_pix_im_area = {}
im1and2_im_area_pindex = 0
for y in range( 0, image_height ):
   for x in range( 0, image_width ):
      pix_image_area = pixel_functions.get_pixel_im_area( ( x,y ), original_im_area )
      
      im1and2_pix_im_area[str( im1and2_im_area_pindex )] = pix_image_area
      
      im1and2_im_area_pindex += 1
      
      

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
      # {'69738': {'x': 158, 'y': 196}, '69737': {'x': 157, 'y': 196},... }
      cur_im1shp_pixels = im1shapes[ im1shapeid ]

      # getting all current image1 shape's boundary pixels
      # {1: {'x': 190, 'y': 30}, 2: {'x': 190, 'y': 31},.... }
      cur_im1shp_bnd_pixels = im1shapes_boundaries[ im1shapeid ]


      # remove boundary pixels from image1 shape's pixels
      cur_im1shp_pindexes_wo_bnd = []
      
      for pindex, pixel_xy in cur_im1shp_pixels.items():
         if not pixel_xy in cur_im1shp_bnd_pixels.values():
            cur_im1shp_pindexes_wo_bnd.append( pindex )




      # pixels of current image1 shape that did not change
      cur_im1shp_pindexes_not_ch = []
      
      # pixels of current image1 shape that did change
      cur_im1shp_pix_at_ch = []
      
      for pindex in cur_im1shp_pindexes_wo_bnd:
         if pindex in pixch:
            cur_im1shp_pix_at_ch.append( pindex )
         else:
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
      
            for pindex, pixel_xy in cur_im2shp_pixels.items():
               if not pixel_xy in cur_im2shp_bnd_pixels.values():
                  cur_im2shp_pindexes_wo_bnd.append( pindex )




            # pixels of current image2 shape that did not change
            cur_im2shp_pindexes_not_ch = []
      
            # pixels of current image2 shape that did change
            cur_im2shp_pix_at_ch = []
      
            for pindex in cur_im2shp_pindexes_wo_bnd:
               if pindex in pixch:
                  cur_im2shp_pix_at_ch.append( pindex )
               else:
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
    
         original_shape_file = top_shapes_dir + directory + "shapes/" + str(filename1) + "_shapes/" + str(im1shapeid) + ".png"
         compare_shape_file = top_shapes_dir + directory + "shapes/" + str(filename2) + "_shapes/" + str(display_match[1]) + ".png"
   
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

with open(staying_Lshapes1to2_dfile, 'wb') as fp:
   pickle.dump(all_matches1to2, fp)
fp.close()
with open(staying_Lshapes2to1_dfile, 'wb') as fp:
   pickle.dump(all_matches2to1, fp)
fp.close()







