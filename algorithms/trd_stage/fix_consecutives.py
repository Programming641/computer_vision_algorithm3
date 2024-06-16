import tkinter
from PIL import ImageTk, Image
from libraries import btwn_amng_files_functions, pixel_shapes_functions, same_shapes_functions, pixel_functions, image_functions, cv_globals
from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files, scnd_stg_spixc_dir, scnd_stg_ch_btwn_frames_dir
import pickle, copy
import sys, pathlib, os



shapes_type = "intnl_spixcShp"
directory = "videos/street3/resized/min1"


if len( sys.argv ) >= 2:
   directory = sys.argv[1]


# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

shapes_dir = top_shapes_dir + directory + "shapes/"

all_matches_ddir = top_shapes_dir + directory + "all_matches/data/"
all_matches_dfile = all_matches_ddir + "1.data"
with open (all_matches_dfile, 'rb') as fp:
   all_matches = pickle.load(fp)
fp.close()
   
consecutives_ddir = top_shapes_dir + directory + "all_matches/consecutives2/data/"
consecutives1_dfile = consecutives_ddir + "1to1.data"
with open (consecutives1_dfile, 'rb') as fp:
   # [{'25.26': [(55310, 53315), (55310, 55702), (55310, 56108)], '26.27': [(53315, 56105), (55702, 56105), (56108, 56105)], ... }, ... ]
   consecutives = pickle.load(fp)
fp.close()

# both integers.
lowest_filenum, highest_filenum = btwn_amng_files_functions.get_low_highest_filenums( directory )
all_image_nums = { str(temp_im_num) for temp_im_num in range(lowest_filenum, highest_filenum + 1 ) }

im1 = Image.open(top_images_dir + directory + str(lowest_filenum) + ".png" )
im_size = im1.size
im1.close()

# ['25.26', '26.27', '27.28', '28.29', '29.30']
all_btwn_files_nums = btwn_amng_files_functions.get_btwn_files_nums( lowest_filenum, highest_filenum )

all_im_shapes_neighbors = btwn_amng_files_functions.get_all_im_target_data( directory, "neighbors" )



def get_each_files_in_order( param_consecutive ):

   all_each_files = []
   for each_files in all_btwn_files_nums:
      if each_files in param_consecutive.keys():
         all_each_files.append(each_files)
   
   return all_each_files


def get_each_files_shapeids( param_consecutive, each_files ):
   
   if len( param_consecutive[each_files] ) == 2 and type( param_consecutive[each_files][0] ) is set and type( param_consecutive[each_files][1] ) is set:
      # current each_files has this data format -> [{4096}, {4096, 4089}]
      cur_im1shapeids = param_consecutive[each_files][0]
      cur_im2shapeids = param_consecutive[each_files][1]
         
   else:
      cur_im1shapeids = { temp_shapes[0] for temp_shapes in param_consecutive[each_files] }
      cur_im2shapeids = { temp_shapes[1] for temp_shapes in param_consecutive[each_files] }

   return [ cur_im1shapeids, cur_im2shapeids ]



for consec_index, consecutive in enumerate(consecutives):
   # {'25.26': [(2077, 4097)], '26.27': [(4097, 4096)], '27.28': [{4096}, {4096, 4089}], ... }

   each_files_in_order = get_each_files_in_order( consecutive )
   
   for each_files in each_files_in_order:
      
      cur_im1file =  each_files.split(".")[0] 
      cur_im2file = each_files.split(".")[1]
      
      # fix1: matched shapes are missing in the next each_files. see documentation algorithms/all_matches/fix.docx
      
      # [ { im1shapeids }, { im2shapeids } ]
      cur_im_shapeids = get_each_files_shapeids( consecutive, each_files )
      
      existing_matches = { temp_shapes for temp_shapes in all_matches[each_files] if temp_shapes[0] in cur_im_shapeids[0] or temp_shapes[1] in cur_im_shapeids[1] }
      cur_im_shapeids[0] |= { temp_shapes[0] for temp_shapes in existing_matches }
      cur_im_shapeids[1] |= { temp_shapes[1] for temp_shapes in existing_matches }

      next_each_files = cur_im2file + "." + str( int(cur_im2file) + 1 )
      if next_each_files in each_files_in_order:
         next_existing_matches = [ temp_shapes for temp_shapes in all_matches[next_each_files] if temp_shapes[0] in cur_im_shapeids[1] ]

         if len( consecutive[next_each_files] ) == 2 and type( consecutive[next_each_files][0] ) is set and type( consecutive[next_each_files][1] ) is set:
            # next_each_files has this data format -> [{4096}, {4096, 4089}]
            for im1or2 in range(2):
               for each_match in next_existing_matches:
                  consecutive[next_each_files][0].add( each_match[0] )
                  consecutive[next_each_files][1].add( each_match[1] )
         else:

            consecutive[next_each_files].extend( next_existing_matches )
            # removing duplicates
            consecutive[next_each_files] = list( set(consecutive[next_each_files]) )


consecutives2_dfile = consecutives_ddir + "1to1.2.data"
with open(consecutives2_dfile, 'wb') as fp:
   # [ {'28.29': [(79998, 79998)], '29.30': [(79998, 79998)], '27.28': [{79962, 75948, 77965, 79998}, {79998}]}, ... ]
   # [ { each_files: inner list, ... }, ... ]
   # inner list contains either tuple of image1 shapeid and image2 shapeid or 2 sets of image1 shapeids and image2 shapeids. below shows with format.
   # [ ( image1 shapeid, image2 shapeid ), ( another image1 shapeid, another image2 shapeid ) ], [ { image1 shapeids }, { image2 shapeids } ].
   pickle.dump(consecutives, fp)
fp.close()















