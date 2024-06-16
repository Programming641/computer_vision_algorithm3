import tkinter
from PIL import ImageTk, Image
from libraries import btwn_amng_files_functions
from libraries.cv_globals import top_shapes_dir, snd_stg_alg_shp_nbrs_dir, styLshapes, styLshapes_wo_pixch, internal, scnd_stg_all_files
import pickle
import sys, pathlib, os



shapes_type = "intnl_spixcShp"
directory = sys.argv[1]

# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'


pixch_dir = top_shapes_dir + directory + "pixch/"
pixch_sty_shapes_ddir = pixch_dir + "sty_shapes/data/"


# loop all "sty_shapes" files
data_dir = pathlib.Path(pixch_sty_shapes_ddir)

btwn_frames_files = []
for data_file in data_dir.iterdir():
   data_filename = os.path.basename(data_file)
   
   # check if the file has the following form. if so, then the target file is found
   # 10.11verified.data   11.12verified.data and so on.
   filename_split_by_period = data_filename.split(".")
   
   if len( filename_split_by_period ) != 3:
      continue
   
   fst_filename = filename_split_by_period[0]
   scnd_filename = filename_split_by_period[1].strip("verified")
   data_extension = filename_split_by_period[2]
   
   if not fst_filename.isnumeric() or not scnd_filename.isnumeric() or data_extension != "data":
      continue   
   
   btwn_frames_files.append( fst_filename + "." + scnd_filename )


# ordered_files -> ['10.11', '11.12', '12.13']
ordered_files = btwn_amng_files_functions.put_btwn_frames_files_in_order( btwn_frames_files )


# staying large shapes. current file
staying_Lshapes_Ddir = top_shapes_dir + directory + styLshapes + "/" + shapes_type + "/data/"

staying_Lshapes_wo_pixch_Ddir = top_shapes_dir + directory + styLshapes_wo_pixch + "/" + shapes_type + "/data/"

pixch_shapes_dir = top_shapes_dir + directory + "pixch/ch_shapes/pixch_shapes/"

template_dir = top_shapes_dir + directory + "template/"
image_template_dir = template_dir + "image_pixels/"
image_template_ddir = image_template_dir + "data/"


# { prev_filename_cur_filename: [ prev image1 shapeid, prev image2 shapeid, cur image1 shapeid, cur image2 shapeid ], ... }
verified_shapes = {}
prev_all_sty_shapes = None
prev_scnd_stg_algo_shapes = None
for data_file in ordered_files:
   print("current file " + data_file )
   
   
   cur_all_sty_shapes = set()
   
   sty_shapes_file = pixch_sty_shapes_ddir + data_file + "verified.data"
   with open (sty_shapes_file, 'rb') as fp:
      # [('1270', '2072'), ('2062', '2062'), ... ]
      # [ ( image1 shapeid, image2 shapeid ), ... ]
      pixch_sty_shapes = pickle.load(fp)
   fp.close()

   pixch_sty_shapes = set( pixch_sty_shapes )
   
   cur_all_sty_shapes |= pixch_sty_shapes
   

   staying_Lshapes1to2_dfile = staying_Lshapes_Ddir + data_file + ".data"
   with open (staying_Lshapes1to2_dfile, 'rb') as fp:
      # [['56099', '56105'], ... ]
      styLshapes = pickle.load(fp)
   fp.close()

   styLshapes = { (temp_shapes[0], temp_shapes[1] ) for temp_shapes in styLshapes }
   
   cur_all_sty_shapes |= styLshapes
   
   staying_Lshapes_wo_pixch_dfile = staying_Lshapes_wo_pixch_Ddir + data_file + "verified.data"
   with open (staying_Lshapes_wo_pixch_dfile, 'rb') as fp:
      # [['79999', '79936', ['67590', '67196']]]
      # [ ['image1 shapeid', 'image2 shapeid' [ matched pixels ]], ... ]
      styLshapes_wo_pixch = pickle.load(fp)
   fp.close()

   styLshapes_wo_pixch = { ( temp_shapes[0], temp_shapes[1] ) for temp_shapes in styLshapes_wo_pixch }
   
   cur_all_sty_shapes |= styLshapes_wo_pixch

   
   pixch_shapes_dfile = pixch_shapes_dir + "data/" + data_file + ".data"
   with open (pixch_shapes_dfile, 'rb') as fp:
      # [('1270', '2072'), ('2062', '2062'), ... ]
      # [ ( image1 shapeid, image2 shapeid ), ... ]
      pixch_shapes = pickle.load(fp)
   fp.close()

   cur_all_sty_shapes |= { (temp_shapes[0], temp_shapes[1] ) for temp_shapes in pixch_shapes }

   image_template_dfile = image_template_ddir + data_file + ".data"
   with open (image_template_dfile, 'rb') as fp:
      # {('59428', '59426'), ('39679', '38065'), ... }
      whole_image_tmpl = pickle.load(fp)
   fp.close()   

   cur_all_sty_shapes |= whole_image_tmpl
   

   # comparing with other current file shapes, if the type of match is one to one match, then matching the same 
   # image1 and image2 shapes will verify the match
   # for example. match from pixch_sty_shapes im1 is 100. im2 is 200. match type is one to one
   #              match from styLshapes, im1 is 100. im2 is 200. match type is one to one
   #              image1 100 and image2 200 are verified.

   # cur_all_sty_shapes
   # {(29138, 38742), (56897, 57293), ... }
   
   if prev_all_sty_shapes is None:
      prev_all_sty_shapes = cur_all_sty_shapes
      prev_filename = data_file
      
      
   else:
      verified_shapes[ prev_filename + "_" + data_file ] = []
      
      for each_prev_shapes in prev_all_sty_shapes:
         found_shapes = { temp_shapes for temp_shapes in cur_all_sty_shapes if each_prev_shapes[1] == temp_shapes[0] }
         
         if len( found_shapes ) == 0:
            
            continue            
         
         for each_found_shapes in found_shapes:
            verified_shapes[ prev_filename + "_" + data_file ].append( [ each_prev_shapes[0], each_prev_shapes[1], each_found_shapes[0], each_found_shapes[1] ] )
  
      prev_all_sty_shapes = cur_all_sty_shapes
      prev_filename = data_file


across_all_files_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/data/"


# { filename: [ ( image1 shapeid, image2 shapeid ), ... ], ...  }
all_shapes = {}
for data_file in ordered_files:
   # data_file -> 10.11
   
   all_shapes[data_file] = set()
   
   cur_im1file = data_file.split(".")[0]
   cur_im2file = data_file.split(".")[1]
   

   cur_files_dfile = across_all_files_ddir + data_file + ".data"
   with open (cur_files_dfile, 'rb') as fp:
      # {('79935', '58671'), ('38784', '45572'), ... }
      cur_files_shapes = pickle.load(fp)
   fp.close()


   for each_shapes in cur_files_shapes:
      # each_shapes -> ('25591', '21189')
   
      all_shapes[data_file].add( each_shapes )

   for each_files in verified_shapes:

      prev_cur_files = each_files.split("_")
      verified_prev_im1file = prev_cur_files[0].split(".")[0]
   
      verified_cur_im1file = prev_cur_files[1].split(".")[0] 

      found_as_prev = False
      found_as_cur = False
      if verified_prev_im1file == cur_im1file:
         found_as_prev = True
      
      elif verified_cur_im1file == cur_im2file:
         found_as_cur = True
      else:
         continue
   
      for each_shapes in verified_shapes[each_files]:
         # each_shapes -> ['13044', '13045', '13045', '13446'], ['37380', '39372', '', '']
         # prev im1shape, prev im2shape, cur_im1shape, cur_im2shape
      
         if found_as_prev is True:
            if each_shapes[0] != "" and each_shapes[1] != "":
               all_shapes[data_file].add( ( each_shapes[0], each_shapes[1] ) )
            
            elif each_shapes[0] != "" and each_shapes[1] == "":
               all_shapes[data_file].add( ( each_shapes[0], "" ) )
            
            elif each_shapes[0] == "" and each_shapes[1] != "":
               all_shapes[data_file].add( ( "", each_shapes[1] ) )
               
      
         elif found_as_cur is True:
            if each_shapes[2] != "" and each_shapes[3] != "":
               all_shapes[data_file].add( ( each_shapes[2], each_shapes[3] ) )
            
            elif each_shapes[2] != "" and each_shapes[3] == "":
               all_shapes[data_file].add( ( each_shapes[2], "" ) )
            
            elif each_shapes[2] == "" and each_shapes[3] != "":
               all_shapes[data_file].add( ( "", each_shapes[3] ) )


# all_shapes may contain empty shapes?
for each_files in all_shapes:
   empty_shapes = set()
   for each_shapes in all_shapes[each_files]:
      if each_shapes[0] == "" or each_shapes[1] == "":
         # matched shapes pair contain empty shape?
         # delete for now
         empty_shapes.add( each_shapes )

   for each_empty_shapes in empty_shapes:
      all_shapes[each_files].remove( each_empty_shapes )

with open(across_all_files_ddir + "all_files.data", 'wb') as fp:
   pickle.dump(all_shapes, fp)
fp.close()





























