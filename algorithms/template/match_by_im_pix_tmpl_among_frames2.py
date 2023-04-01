import tkinter
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions
from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir
import pickle
import sys, os
import pathlib
import winsound

directory = "videos/street3/resized/min"


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

pixel_template_dir = top_shapes_dir + directory + "template/pixels/"
pixel_template_ddir = pixel_template_dir + "data/"
pixel_template_dfile = pixel_template_ddir + "among.data"


# loop all "btwn_frames" files
data_dir = pathlib.Path(pixel_template_ddir)

btwn_frames_files = []
for data_file in data_dir.iterdir():
   data_filename = os.path.basename(data_file)
   # filename without last comma ( which should be extension )
   data_filename = os.path.splitext(data_filename)[0]
   # check if file has the following form
   # number.number
   if data_filename.count(".") == 1:
      first_num_lastindex = data_filename.find(".")
      if data_filename[0: first_num_lastindex].isnumeric() and data_filename[first_num_lastindex + 1: len( data_filename )].isnumeric():
         # current file is "btwn_frames" file
         btwn_frames_files.append( data_filename )


with open (pixel_template_dfile, 'rb') as fp:
   # [ [{'1400': 628.3199999999999, 'nbrs': ['1405', '11441'], 'im2pixels': ['424', '428', '6830'] }], ... ]
   # [ [ { image1shapeid: matched count, image1 neighbors: [ image1 neighbors ], im2pixels: [ matched image2 pixels ], ... ]
   pixel_template = pickle.load(fp)
fp.close()


def find_next_match( prev_each_pixel_template, cur_match):
   # prev_each_pixel_template -> {'prevfile': '10.11', 'prev_shapeid': '2577', 'prev_nbrs': ['2985'], 'prev_im2pixels': [182,], 
   #                              'curfile': '11.12', 'cur_shapeid': '13043', 'cur_nbrs': ['5419',], 'cur_im2pixels': [4619 ]}
   next_match = [ match for match in pixel_template if match["prevfile"] == prev_each_pixel_template["curfile"] and 
                  match["prev_shapeid"] == prev_each_pixel_template["cur_shapeid"] ]

   if len(next_match) >= 1:
      
      first_cur_match = None
      for each_next_match in next_match:
         # check if this frame's shape match is already taken. if so, this is the similar shape match, so only take differences.
         if first_cur_match is not None and first_cur_match["prevfile"] == each_next_match["prevfile"] and first_cur_match["prev_shapeid"] == each_next_match["prev_shapeid"]:
            cur_match[0]["similar_shapes"].append( each_next_match["curfile"] )
            
            shapes = [ each_next_match["cur_shapeid"] ]
            shapes.extend( each_next_match["cur_nbrs"] )
            
            cur_match[0]["similar_shapes"].append( shapes )
            
            # lastly, take im2pixels differences
            # this takes awful lot of time
            #im2pixels_diff = set( each_next_match["cur_im2pixels"] ).difference( set( first_cur_match["cur_im2pixels"] ) )
            #cur_match[0]["similar_shapes"].append( im2pixels_diff )
            
         
         else:
            first_cur_match = each_next_match
            cur_match.append( each_next_match )

         # see if there is next frame pair
         if btwn_frames_files.index( each_next_match["curfile"] ) - len( btwn_frames_files ) == -1:
            # this is the last frame pair, skip it
            continue
         find_next_match( each_next_match, cur_match )




all_matches = []
progress_counter = len( pixel_template )
for each_pixel_template in pixel_template:
   print( str( progress_counter ) + " remaining" )
   progress_counter -= 1
   # each_pixel_template -> {'prevfile': '10.11', 'prev_shapeid': '2577', 'prev_nbrs': ['2985'], 'prev_im2pixels': [1789, 1790], 
   #                         'curfile': '11.12', 'cur_shapeid': '2992', 'cur_nbrs': ['5419'], 'cur_im2pixels': [1792, ... ]}
      
   # see if there is next frame pair
   if btwn_frames_files.index( each_pixel_template["curfile"] ) - len( btwn_frames_files ) == -1:
      # this is the last frame pair, skip it
      continue
   
   each_pixel_template["similar_shapes"] = []
   cur_match = [each_pixel_template]
   find_next_match( each_pixel_template, cur_match )
   
   if len(cur_match) > 1:
      all_matches.append( cur_match )


pixel_template_dfile = pixel_template_ddir + "among2.data"
with open(pixel_template_dfile, 'wb') as fp:
   pickle.dump(all_matches, fp)
fp.close()


refined_matches = []
for each_pix_tmpl in all_matches:
   '''
   each_pix_tmpl -> [{'prevfile': '10.11', 'prev_shapeid': '2577', 'prev_nbrs': ['2985'], 'prev_im2pixels': [182,], 
                  'curfile': '11.12', 'cur_shapeid': '13043', 'cur_nbrs': ['5419', '5429',], 'cur_im2pixels': [4619,], 
                  'similar_shapes': ['12.13', ['13848', '25045'], '12.13', ['25045',]]}, 
                  
                  {'prevfile': '11.12', 'prev_shapeid': '13043', 'prev_nbrs': ['5419', ], 'prev_im2pixels': [4619,], 
                  'curfile': '12.13', 'cur_shapeid': '13044', 'cur_nbrs': ['12244', ], 'cur_im2pixels': [ 10230]}]
   
   still, there are many shapes that are more than 90% similar. 
   '''

   ref_match_index = None
   for index, refined_match in enumerate( refined_matches ):
      found = [ True for  value in refined_match if value["prev_shapeid"] == each_pix_tmpl[0]["prev_shapeid"] and value["prevfile"] == each_pix_tmpl[0]["prevfile"] ]
   
      if len(found) == 1:
         ref_match_index = index
         break
   
   if ref_match_index is not None:
      # each_pix_tmpl found in refined_matches
      # first frame shape in each_pix_tmpl and refined_matches is the same one. so take differences from second one
      for index, frame_shape in enumerate( each_pix_tmpl ):
         if not index == 0:
            refined_matches[ref_match_index][0]["similar_shapes"].append( frame_shape["curfile"] )
            
            shapes = [ frame_shape["cur_shapeid"] ]
            shapes.extend( frame_shape["cur_nbrs"] )
            
            refined_matches[ref_match_index][0]["similar_shapes"].append( shapes )         
            
               
      



   elif ref_match_index is None:
      refined_matches.append( each_pix_tmpl )
      
      

with open(pixel_template_dfile, 'wb') as fp:
   pickle.dump(refined_matches, fp)
fp.close()   
   
# this is used for displaying closest matched images
root = tkinter.Tk()

for refined_match in refined_matches:
   '''
   # refined_match -> 
   [{'prevfile': '10.11', 'prev_shapeid': '2577', 'prev_nbrs': ['2985'], 'prev_im2pixels': [ 1790], 
     'curfile': '11.12', 'cur_shapeid': '13043', 'cur_nbrs': ['5419',], 'cur_im2pixels': [4619,], 
     'similar_shapes': ['12.13', ['13848', '25045'], '12.13', ['25045', '5436',]]}, 

    {'prevfile': '11.12', 'prev_shapeid': '13043', 'prev_nbrs': [ '30214'], 'prev_im2pixels': [4619,], 
     'curfile': '12.13', 'cur_shapeid': '13044', 'cur_nbrs': ['12244'], 'cur_im2pixels': [10230]}]
   
   '''
   window = tkinter.Toplevel(root)
   first = True
   shapeid = None
   for index, each_refined_match in enumerate( refined_match ):
      if shapeid is None:
         shapeid = each_refined_match["prevfile"] + "." + each_refined_match["prev_shapeid"]
      
      if index < len( refined_match ) - 1:
         # not the last frame
         shapefile = pixel_template_dir + each_refined_match["prevfile"] + "/im1." + each_refined_match["prev_shapeid"] + ".png"
      else:
         # last frame
         shapefile = pixel_template_dir + each_refined_match["prevfile"] + "/im1." + each_refined_match["prev_shapeid"] + ".png"
         img = ImageTk.PhotoImage(Image.open(shapefile))
  
         label1 = tkinter.Label(window, image = img, bg="white")
         label1.image = img
         label1.pack()
         shapefile = pixel_template_dir + each_refined_match["curfile"] + "/im1." + each_refined_match["cur_shapeid"] + ".png"
         
      img = ImageTk.PhotoImage(Image.open(shapefile))
  
      label1 = tkinter.Label(window, image = img, bg="white")
      label1.image = img
      label1.pack()
   
   
   
   
   window.title( shapeid )      
   
   
   
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)      

root.mainloop()


   
   
   
   
   
   










































