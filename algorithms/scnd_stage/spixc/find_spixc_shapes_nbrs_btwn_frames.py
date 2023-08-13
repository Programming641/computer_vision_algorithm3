# it takes the results of find_spixc_shapes_nbrs.py and find the best matches between frames of video
# algorithm for finding the best match is how many pixels overlap between shapes from two frames.
from libraries import pixel_functions, image_functions, read_files_functions
import tkinter
from PIL import ImageTk, Image
import os, sys
import pickle
import copy

from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir, internal


image1file = '12'
image2file = "13"
directory = "videos/street3/resized/min"
shapes_type = "intnl_spixcShp"

# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'


s_pixc_shapes_nbrs_dir = top_shapes_dir + directory + "spixc_shapes/nbrs/"
spixc_shapes_nbrs_im1dir = s_pixc_shapes_nbrs_dir + image1file + "/"
spixc_shapes_nbrs_im2dir = s_pixc_shapes_nbrs_dir + image2file + "/"
s_pixc_shapes_nbrs_data_dir = s_pixc_shapes_nbrs_dir + "data/"
s_pixc_shapes_nbrs_file1 = s_pixc_shapes_nbrs_data_dir + image1file + ".data"
s_pixc_shapes_nbrs_file2 = s_pixc_shapes_nbrs_data_dir + image2file + ".data"
with open (s_pixc_shapes_nbrs_file1, 'rb') as fp:
   # [{'213': ['638', '641', '1066'], 'nbr_nbrs': ['215', '641', '1066', '1070', '635',... ]}, ... ]
   # [ { spixc_shapeid: [  spixc_shapeid's direct neighbors ], 'nbr_nbrs': [ spixc_shapeid's neighbor's neighbors ] }, ... ]
   im1spixc_shapes_nbrs = pickle.load(fp)
fp.close()   
with open (s_pixc_shapes_nbrs_file2, 'rb') as fp:
   # [{'213': ['638', '641', '1066'], 'nbr_nbrs': ['215', '641', '1066', '1070', '635',... ]}, ... ]
   # [ { spixc_shapeid: [  spixc_shapeid's direct neighbors ], 'nbr_nbrs': [ spixc_shapeid's neighbor's neighbors ] }, ... ]
   im2spixc_shapes_nbrs = pickle.load(fp)
fp.close()   




if shapes_type == "normal":
   # we need to get every pixel of the shapes
   # return value form is
   # shapes[shapes_id][pixel_index] = {}
   # shapes[shapes_id][pixel_index]['x'] = x
   # shapes[shapes_id][pixel_index]['y'] = y
   im1shapes = read_files_functions.rd_shapes_file(image1file, directory)
   im2shapes = read_files_functions.rd_shapes_file(image2file, directory)
   
   # converting image shapes to the same format as "intnl_spixcShp"
   for im1shapeid in im1shapes:
      im1shapes[im1shapeid] = list( im1shapes[im1shapeid].keys() )
   for im2shapeid in im2shapes:
      im2shapes[im2shapeid] = list( im2shapes[im2shapeid].keys() )   
   
   
   
elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"
   
   shapes_dir = s_pixcShp_intnl_dir + "shapes/"
   shapes_dfile = shapes_dir + image1file + "shapes.data"
   im2shapes_dfile = shapes_dir + image2file + "shapes.data"  

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


all_matches = []
for im1spixc_shape in im1spixc_shapes_nbrs:
   # im1spixc_shape ->  {'213': ['638', '641', '1066'], 'nbr_nbrs': ['215', '641', '1066', '1070', '635',... ]}
   
   # get all shapes pixels of im1spixc_shape
   cur_im1pixels = set()
   cur_im1shapeid = None
   for im1shapeid in im1spixc_shape:
      if im1shapeid != "nbr_nbrs":
         cur_im1shapeid = im1shapeid
         cur_im1pixels |= set( im1shapes[ im1shapeid ] )
         for im1shape_Dneighbor in im1spixc_shape[ im1shapeid ]:
            cur_im1pixels |= set( im1shapes[ im1shape_Dneighbor ] )
      elif im1shapeid == "nbr_nbrs":
         for im1shape_nbr_nbr in im1spixc_shape["nbr_nbrs"]:
            cur_im1pixels |= set( im1shapes[ im1shape_nbr_nbr ] )
   
   # [ [ image2 shapeid, im1counts, im2counts ], ... ]
   cur_im1_results = []
      
   # all current image1 shape's pixels are obtained, now loop each one of image2 shapes to see which one matches the most
   for im2spixc_shape in im2spixc_shapes_nbrs:
      # get current image2 index number for cur_im1_results
      cur_im2index = len( cur_im1_results )
      cur_im1_results.append( [] )
   
      # get all shapes pixels of im2spixc_shape
      cur_im2pixels = set()
      for im2shapeid in im2spixc_shape:
         if im2shapeid != "nbr_nbrs":
            cur_im1_results[cur_im2index].append( im2shapeid )
            
            cur_im2pixels |= set(  im2shapes[ im2shapeid ] )
            for im2shape_Dneighbor in im2spixc_shape[ im2shapeid ]:
               cur_im2pixels |= set( im2shapes[ im2shape_Dneighbor ] )
         elif im2shapeid == "nbr_nbrs":
            for im2shape_nbr_nbr in im2spixc_shape["nbr_nbrs"]:
               cur_im2pixels |= set( im2shapes[ im2shape_nbr_nbr ] )      
      
   
      im1found_pixels = cur_im1pixels.intersection( cur_im2pixels )
      im2found_pixels = cur_im2pixels.intersection( cur_im1pixels )      
      
      im1not_found_percent = (len( cur_im1pixels ) - len( im1found_pixels ) ) / len( cur_im1pixels )
      im2not_found_percent = ( len( cur_im2pixels ) - len( im2found_pixels ) )/ len( cur_im2pixels )

      cur_im1_results[cur_im2index].append( im1not_found_percent )
      cur_im1_results[cur_im2index].append( im2not_found_percent )

   # current image1 is done. now determine which image2 shape image1 shape matches the most
   # whichever shape has the number closest to the 0 is the most match.
   im1closest = im2closest = None
   # match is the list because there may be multiple highest score
   im1most_match = []
   im2most_match = []
   for cur_im1_result in cur_im1_results:
      if im1closest is None and im1not_found_percent <= 0.5:
         # first and at least 50% pixels are found
         im1closest = cur_im1_result[1]

         im1most_match.append( [ cur_im1shapeid, cur_im1_result[0], im1closest, "im1" ] )

      elif im1not_found_percent <= 0.5:
         # second time or more
         # first, determine im1closest
         if cur_im1_result[1] > 0 and cur_im1_result[1] < im1closest:
            # current im1 score is closer match than im1closest
            # delete contents of current im1most_match
            im1most_match = []
            im1most_match.append( [ cur_im1shapeid, cur_im1_result[0], im1closest, "im1" ] )
            im1closest = cur_im1_result[1]
         
         elif cur_im1_result[1] == 0 and im1closest == 0:
            # both im1closest and current im1 score have the perfect match, so don't delete the im1most_match
            # add current one to the im1most_match
            im1most_match.append( [ cur_im1shapeid, cur_im1_result[0], im1closest, "im1" ] )
         
         elif cur_im1_result[1] == im1closest:
            # both current image1 score and im1closest are not 0 but they both have the same value.
            # so don't delete the contents of im1most_match, just add the current one
            im1most_match.append( [ cur_im1shapeid, cur_im1_result[0], im1closest, "im1" ] )
         
         elif cur_im1_result[1] < 0 and cur_im1_result[1] > im1closest:
            # current im1 score is the negative value but closer to 0 than the im1closest. so delete the im1most_match
            # and add current one to it
            im1most_match = []
            im1most_match.append( [ cur_im1shapeid, cur_im1_result[0], im1closest, "im1" ] )
            im1closest = cur_im1_result[1]
         
      if im2closest is None and im2not_found_percent <= 0.5:
         im2closest = cur_im1_result[2]
         im2most_match.append( [ cur_im1shapeid, cur_im1_result[0], im2closest, "im2" ] )
      elif im2not_found_percent <= 0.5:
         if cur_im1_result[2] > 0 and cur_im1_result[2] < im2closest:
            im2most_match = []
            im2most_match.append( [ cur_im1shapeid, cur_im1_result[0], im2closest, "im2" ] )
            im2closest = cur_im1_result[2]
         
         elif cur_im1_result[2] == 0 and im2closest == 0:
            im2most_match.append( [ cur_im1shapeid, cur_im1_result[0], im2closest, "im2" ] )
         
         elif cur_im1_result[2] == im2closest:
            im2most_match.append( [ cur_im1shapeid, cur_im1_result[0], im2closest, "im2" ] )
         
         elif cur_im1_result[2] < 0 and cur_im1_result[2] > im2closest:
            im2most_match = []
            im2most_match.append( [ cur_im1shapeid, cur_im1_result[0], im2closest, "im2" ] )
            im2closest = cur_im1_result[2]           
      
      
   all_matches.append( im1most_match )
   all_matches.append( im2most_match )





# this is used for displaying closest matched images
root = tkinter.Tk()
for match in all_matches:
   for each_match in match:
   
      window = tkinter.Toplevel(root)
      window.title( each_match[0] + " " + each_match[1] )

      original_shape_file = spixc_shapes_nbrs_im1dir + each_match[0] + ".png"
      compare_shape_file = spixc_shapes_nbrs_im2dir + each_match[1] + ".png"
   
      img = ImageTk.PhotoImage(Image.open(original_shape_file))
      img2 = ImageTk.PhotoImage(Image.open(compare_shape_file))
  
      label1 = tkinter.Label(window, image = img, bg="white")
      label1.image = img
      label1.pack()
   
      label2 = tkinter.Label(window, image = img2, bg="white" )
      label2.image = img2
      label2.pack()


root.mainloop()


with open(s_pixc_shapes_nbrs_data_dir + image1file + "." + image2file + ".data", 'wb') as fp:
   pickle.dump(all_matches, fp)
fp.close()































