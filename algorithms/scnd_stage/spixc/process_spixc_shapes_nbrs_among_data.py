
from libraries import pixel_functions, image_functions, read_files_functions

import tkinter
from PIL import ImageTk, Image
import os, sys
import pickle
import copy
import pathlib

from libraries.cv_globals import top_shapes_dir, top_images_dir, internal


directory = "videos/street3/resized/min"
shapes_type = "intnl_spixcShp"

if directory != "" and directory[-1] != '/':
   directory +='/'

spixcShp_nbrs_dir = top_shapes_dir + directory  + "spixc_shapes/nbrs/"
spixcShp_nbrs_ddir = spixcShp_nbrs_dir + "data/"

# loop all "btwn_frames" files
data_dir = pathlib.Path(spixcShp_nbrs_ddir)

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
         

s_pixc_shapes_nbrs_dfile = spixcShp_nbrs_ddir + "among.data"
with open (s_pixc_shapes_nbrs_dfile, 'rb') as fp:
   # [[{'10': '555', '11': '29056'}], [{'10': '832', '11': '47310'}, {'11': '47310', '12': '11232'}, {'11': '47310', '12': '75'}], ... ]
   among_data = pickle.load(fp)
fp.close()


image_shapes = {}
spixc_shapes_nbrs = {}
# { btwn frames file number: btwn frames data, ... }
btwn_frames_data = {}
for btwn_frames_file in btwn_frames_files:
   with open (spixcShp_nbrs_ddir + btwn_frames_file + ".data" , 'rb') as fp:
      # [[], [['555', '29056', 0.23620627479264333, "im1"]], ... ]
      # [ [ shapes did not match more than 50% ], 
      #   [ image1 shapeid, image2 shapeid, percentage of not found pixels so the lower the better match, im1 or im2 that matched most of its pixels ], ... ]
      one_btwn_frm_data = pickle.load(fp)
   fp.close()

   btwn_frames_data[btwn_frames_file] = one_btwn_frm_data

   first_num_lastindex = btwn_frames_file.find(".")
   first_filenum = btwn_frames_file[0: first_num_lastindex] 
   second_filenum = btwn_frames_file[first_num_lastindex + 1: len( btwn_frames_file )] 

   spixc_shapes_nbrs_file = spixcShp_nbrs_ddir + first_filenum + ".data"
   with open (spixc_shapes_nbrs_file, 'rb') as fp:
      # [{'213': ['638', '641', '1066'], 'nbr_nbrs': ['215', '641', '1066', '1070', '635',... ]}, ... ]
      # [ { spixc_shapeid: [  spixc_shapeid's direct neighbors ], 'nbr_nbrs': [ spixc_shapeid's neighbor's neighbors ] }, ... ]
      im1spixc_shapes_nbrs = pickle.load(fp)
   fp.close()   

   spixc_shapes_nbrs[first_filenum] = im1spixc_shapes_nbrs

   spixc_shapes_nbrs_file = spixcShp_nbrs_ddir + second_filenum + ".data"
   with open (spixc_shapes_nbrs_file, 'rb') as fp:
      # [{'213': ['638', '641', '1066'], 'nbr_nbrs': ['215', '641', '1066', '1070', '635',... ]}, ... ]
      # [ { spixc_shapeid: [  spixc_shapeid's direct neighbors ], 'nbr_nbrs': [ spixc_shapeid's neighbor's neighbors ] }, ... ]
      im1spixc_shapes_nbrs = pickle.load(fp)
   fp.close()   

   spixc_shapes_nbrs[second_filenum] = im1spixc_shapes_nbrs


   if shapes_type == "normal":
      # we need to get every pixel of the shapes
      # return value form is
      # shapes[shapes_id][pixel_index] = {}
      # shapes[shapes_id][pixel_index]['x'] = x
      # shapes[shapes_id][pixel_index]['y'] = y
      im1shapes = read_files_functions.rd_shapes_file(first_filenum, directory)
      im2shapes = read_files_functions.rd_shapes_file(second_filenum, directory)
   
      # converting image shapes to the same format as "intnl_spixcShp"
      for im1shapeid in im1shapes:
         im1shapes[im1shapeid] = list( im1shapes[im1shapeid].keys() )
      for im2shapeid in im2shapes:
         im2shapes[im2shapeid] = list( im2shapes[im2shapeid].keys() )   
   
   
   
   elif shapes_type == "intnl_spixcShp":
      s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"
   
      shapes_dir = s_pixcShp_intnl_dir + "shapes/"
      shapes_dfile = shapes_dir + first_filenum + "shapes.data"
      im2shapes_dfile = shapes_dir + second_filenum + "shapes.data"  

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

   image_shapes[ first_filenum ] = im1shapes
   image_shapes[ second_filenum ] = im2shapes




def same_im1or2entries(image1or2):
   all_im_entries = []
   finished_im1or2 = []
   for each_among_data in among_data:
      # each_among_data ->   [{'10': '832', '11': '47310'}, {'11': '47310', '12': '11232'}, {'11': '47310', '12': '75'}]
      for one_among_data in each_among_data:
         # one_among_data -> {'10': '832', '11': '47310'}
      
         im1file = min( one_among_data.keys() )
         im2file = max( one_among_data.keys() )
         
         if image1or2 == "im1":
            target_imfile = im1file
         elif image1or2 == "im2":
            target_imfile = im2file

         if ( target_imfile, one_among_data[str(target_imfile)] ) in finished_im1or2:
               continue
        
      
         cur_btwn_frame_found = False
         same_im_entries = []
         ano_finished_im_entries = []
         # see if current one_among_data image2 entry is present as image2 in other one_among_data
         for ano_each_among_data in among_data:
            for ano_one_among_data in ano_each_among_data:
               ano_im1file = min( ano_one_among_data.keys() )
               ano_im2file = max( ano_one_among_data.keys() )
               
               if image1or2 == "im1":
                  ano_target_imfile = ano_im1file
               elif image1or2 == "im2":
                  ano_target_imfile = ano_im2file
               
               if one_among_data != ano_one_among_data and one_among_data[ str( target_imfile ) ] == ano_one_among_data[ str(ano_target_imfile) ] and \
                  target_imfile == ano_target_imfile:

                  for each_btwn_frames_data in btwn_frames_data[str(im1file) + "." + str(im2file)]:
                     if cur_btwn_frame_found is False:
                        cur_btwn_frame = [ values for values in each_btwn_frames_data if values[0] == one_among_data[str(im1file)] and values[1] == one_among_data[str(im2file)] ]
                        
                        if len( cur_btwn_frame ) == 1:
                           temp = []
                           temp.extend( cur_btwn_frame[0] )
                           temp.append( str(im1file) + "." + str(im2file) )
                           same_im_entries.append( temp )
                           cur_btwn_frame_found = True
                                         
                     ano_cur_btwn_frame = [ values for values in each_btwn_frames_data if values[0] == ano_one_among_data[str(im1file)] and values[1] == ano_one_among_data[str(im2file)] ]

                     if len( ano_cur_btwn_frame ) == 1 and ano_cur_btwn_frame[0] not in ano_finished_im_entries:
                        temp = []
                        temp.extend( ano_cur_btwn_frame[0] )
                        temp.append( str(ano_im1file) + "." + str(ano_im2file) )
                        same_im_entries.append( temp )
                        ano_finished_im_entries.append( ano_cur_btwn_frame[0] )
      
      
         if len( same_im_entries ) >= 1:
            all_im_entries.append( same_im_entries )
      
         finished_im1or2.append( ( target_imfile, one_among_data[str(target_imfile)] ) )

   return all_im_entries


def all_same_im_matches( same_im_entries, im1or2 ):
   all_im_matches = [ ]
   for each_im_entries in same_im_entries:
      # each_im2entries -> [['47310', '11232', 0.15415268456375839, 'im1', '11.12'], ['47310', '75', 0.3544605239054772, 'im2', '11.12']]
   
      cur_im_matches = [ values for values in each_im_entries if values[3] == im1or2 ]
   
      if len(cur_im_matches) < 2:
         # there has to be at least 2 inside cur_im2matches
         continue

      common_pixels = set()
      first = True
      btwn_filename = None
      target_filename = None
      matching_im_shapeid = None
      for cur_im_match in cur_im_matches:
         # cur_im_match ->  ['54085', '11232', 0.20191804707933741, 'im1', '11.12']
   
         if first is True:
            btwn_filename = cur_im_match[4]
            first_num_lastindex = cur_im_match[4].find(".")
            
            if im1or2 == "im1":
               # getting im2shapid here, and for common_pixels are from matching image1 shapes
               matching_im_shapeid = cur_im_match[1]
               # image1 filename
               target_filename = cur_im_match[4][0: first_num_lastindex] 
               # getting pixels for current image1 shape
               # spixc_shapes_nbrs[ filename ] -> [{'213': ['638', '641', '1066'], 'nbr_nbrs': ['215', '641', '1066', '1070', '635',... ]}, ... ]
               #                                  [ { spixc_shapeid: [  spixc_shapeid's direct neighbors ], 'nbr_nbrs': [ spixc_shapeid's neighbor's neighbors ] }, ... ]
               cur_spixc_shapes_nbrs = [ values for values in spixc_shapes_nbrs[ target_filename ] if cur_im_match[0] in values.keys() ]
            elif im1or2 == "im2":
               matching_im_shapeid = cur_im_match[0]
               # image2 filename
               target_filename = cur_im_match[4][first_num_lastindex + 1: len( cur_im_match[4] )]
            
               cur_spixc_shapes_nbrs = [ values for values in spixc_shapes_nbrs[ target_filename ] if cur_im_match[1] in values.keys() ]
         
            if len( cur_spixc_shapes_nbrs ) == 1:
               shapeid = None
               for key in cur_spixc_shapes_nbrs[0]:
               
                  if key != "nbr_nbrs":
                     shapeid = key
                     cur_shape_pixels = image_shapes[ target_filename ][ shapeid ]
                  
                     common_pixels |= set( cur_shape_pixels )
                  elif key == "nbr_nbrs":
                     for nbr_shape in cur_spixc_shapes_nbrs[0][key]:
                        cur_shape_pixels = image_shapes[ target_filename ][ nbr_shape ]
                        common_pixels |= set( cur_shape_pixels )
                  
            else:
               print("ERROR. cur_spixc_shapes_nbrs has to be found and there has to be exactly one")
               sys.exit()

            
            first = False

         else:
            cur_pixels = set()
            # getting pixels for current image1 shape
            # spixc_shapes_nbrs[ filename ] -> [{'213': ['638', '641', '1066'], 'nbr_nbrs': ['215', '641', '1066', '1070', '635',... ]}, ... ]
            #                                  [ { spixc_shapeid: [  spixc_shapeid's direct neighbors ], 'nbr_nbrs': [ spixc_shapeid's neighbor's neighbors ] }, ... ]
            cur_spixc_shapes_nbrs = [ values for values in spixc_shapes_nbrs[ target_filename ] if cur_im_match[0] in values.keys() ]
         
            if len( cur_spixc_shapes_nbrs ) == 1:
               shapeid = None
               for key in cur_spixc_shapes_nbrs[0]:
               
                  if key != "nbr_nbrs":
                     shapeid = key
                     cur_shape_pixels = image_shapes[ target_filename ][ shapeid ]
                  
                     cur_pixels |= set( cur_shape_pixels )
                  elif key == "nbr_nbrs":
                     for nbr_shape in cur_spixc_shapes_nbrs[0][key]:
                        cur_shape_pixels = image_shapes[ target_filename ][ nbr_shape ]
                        cur_pixels |= set( cur_shape_pixels )
                  
            else:
               print("ERROR. cur_spixc_shapes_nbrs has to be found and there has to be exactly one")
               sys.exit()
            
            common_pixels = common_pixels.intersection( set( cur_pixels ) )
   
   
      all_im_matches.append( [ matching_im_shapeid, btwn_filename, common_pixels ] )
      
      
   return all_im_matches


def show_images( im_matches, im1or2 ):
   # im_matches -> [ "im1", ['13528', '12.13', {'36278',}], ... ]
   root = tkinter.Tk()
   labels = []

   for all_im_match in im_matches:
      # all_im_match -> ['13528', '12.13', {'36278',}]

      first_num_lastindex = all_im_match[1].find(".")
      first_filenum = all_im_match[1][0: first_num_lastindex] 
      second_filenum = all_im_match[1][first_num_lastindex + 1: len( all_im_match[1] )]
   
      window = tkinter.Toplevel(root)
      window_titile = all_im_match[1] + "_" + im1or2 + "." + all_im_match[0]

      im1 = Image.open(top_images_dir + directory + first_filenum + ".png")
      im_width, im_height = im1.size

      for pixel in all_im_match[2]:
         xy = pixel_functions.convert_pindex_to_xy( pixel, im_width )
   
         im1.putpixel( xy , (255, 0, 0) )

      if im1or2 == "im1":
         im2 = spixcShp_nbrs_dir + first_filenum + "/" + all_im_match[0] + ".png"
      elif im1or2 == "im2":
         im2 = spixcShp_nbrs_dir + second_filenum + "/" + all_im_match[0] + ".png"
   
      img1 = ImageTk.PhotoImage(im1)
      label_index = len( labels )
      labels.append( tkinter.Label(window, image = img1, bg="white") )
      labels[label_index].img = img1
      labels[label_index].pack()

      img2 = ImageTk.PhotoImage(Image.open(im2))
   
      label_index = len( labels )
      labels.append( tkinter.Label(window, image = img2, bg="white") )
      labels[label_index].img = img2
      labels[label_index].pack()   

      window.title( window_titile  )


   root.mainloop()



all_im1entries = same_im1or2entries("im1")
all_im2entries = same_im1or2entries("im2")

# image2 shapes that are matching the same image1 shape
# image2 shapes pixels will be obtained for the same one image1 shape
all_same_im2matches = all_same_im_matches( all_im1entries, "im2")
# image1 shapes that are matching the same image2 shape
# image1 shapes pixels will be obtained for the same one image2 shape
all_same_im1matches = all_same_im_matches( all_im2entries, "im1")

# image1 pixc_shapes_nbrs shapeid whereas for image2 pixc_shapes_nbrs, pixels are obtained and combined
show_images( all_same_im2matches, "im1" )
# image2 pixc_shapes_nbrs shapeid whereas for image1 pixc_shapes_nbrs, pixels are obtained and combined
show_images( all_same_im1matches, "im2" )

results = { "im1shpid_im2_pixels": all_same_im2matches }
results["im2shpid_im1_pixels"] = all_same_im1matches 




with open(spixcShp_nbrs_ddir + "among2.data", 'wb') as fp:
   pickle.dump(results, fp)
fp.close()






















