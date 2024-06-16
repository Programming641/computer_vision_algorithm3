
from libraries import  read_files_functions, pixel_shapes_functions, pixel_functions, image_functions, btwn_amng_files_functions


from PIL import ImageTk, Image
import os, sys
import pickle
import copy
import math
import shutil

from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files

directory = sys.argv[1]

if directory != "" and directory[-1] != '/':
   directory +='/'

across_all_files_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/data/"

all_matches_so_far_dfile = across_all_files_ddir + "all_matches.data"
with open (all_matches_so_far_dfile, 'rb') as fp:
   all_matches_so_far = pickle.load(fp)
fp.close()

# moving all matches data to all_matches directory

all_matches_ddir = top_shapes_dir + directory + "all_matches" + "/data/"
if os.path.exists(all_matches_ddir ) == False:
   os.makedirs(all_matches_ddir )

all_matches_dfile = all_matches_ddir + "1.data"
with open(all_matches_dfile, 'wb') as fp:
   pickle.dump(all_matches_so_far, fp)
fp.close()





