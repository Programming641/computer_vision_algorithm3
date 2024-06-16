import tkinter
from PIL import ImageTk, Image
from libraries import btwn_amng_files_functions, pixel_shapes_functions, same_shapes_functions, pixel_functions, image_functions, cv_globals
from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files, scnd_stg_spixc_dir, scnd_stg_ch_btwn_frames_dir
import pickle, copy
import sys, pathlib, os


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
   
consecutives_ddir = top_shapes_dir + directory + "all_matches/consecutives/data/"
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

if "min" in directory:
   min_colors = True
else:
   min_colors = False

smallest_pixc = cv_globals.get_smallest_pixc( im_size )



def get_cur_neighbor_matches( adjacent_fnums, each_files, correspond_fnum ):

   adj_im1fnum = adjacent_fnums.split(".")[0]
   adj_im2fnum = adjacent_fnums.split(".")[1]

   if len(consecutive[adjacent_fnums]) != 2 or ( type( consecutive[adjacent_fnums][0] ) is not set and type( consecutive[adjacent_fnums][1] ) is not set ):
      adj_im1shapeids = { temp_shapes[0] for temp_shapes in consecutive[adjacent_fnums] }
      adj_im2shapeids = { temp_shapes[1] for temp_shapes in consecutive[adjacent_fnums] }    
   else:
      adj_im1shapeids = consecutive[adjacent_fnums][0]
      adj_im2shapeids = consecutive[adjacent_fnums][1]
      

   adj_im_shapes_neighbors = [ all_im_shapes_neighbors[int(adj_im1fnum) - lowest_filenum] , all_im_shapes_neighbors[int(adj_im2fnum) - lowest_filenum] ]


   # [ {(53308, 53296), ...}, {(54920, 56125), ...} ]
   # [ { image1 shapeids neighbors matches }, { image2 shapeids neighbors matches } ]
   adj_neighbor_matches = pixel_shapes_functions.get_nbr_matches( ( adj_im1shapeids, adj_im2shapeids ), adj_im_shapes_neighbors, all_matches[adjacent_fnums] )

   adj_comm_neighbors_matches = adj_neighbor_matches[0].intersection( adj_neighbor_matches[1] )
   adj_comm_im_neighbors_ids = { temp_shapeids[correspond_fnum] for temp_shapeids in adj_comm_neighbors_matches }

   adjacent_cur_fnum = abs( correspond_fnum - 1 )

   cur_neighbor_matches = { temp_shapes for temp_shapes in all_matches[each_files] if temp_shapes[adjacent_cur_fnum] in adj_comm_im_neighbors_ids }
         
   cur_im1neighbors = { temp_shapes[0] for temp_shapes in cur_neighbor_matches }
   cur_im2neighbors = { temp_shapes[1] for temp_shapes in cur_neighbor_matches }

   return [ cur_im1neighbors, cur_im2neighbors ]


def get_matched_shapeids_from_m_pixels( matched_pixels, im_shapeids_by_pindex, im_shapes ):

   matched_shapeids = {}
   for pixel in matched_pixels:
      
      for shapeid in im_shapeids_by_pindex[pixel]:
         if shapeid not in matched_shapeids.keys():
            matched_shapeids[shapeid] = 1
         else:
            matched_shapeids[shapeid] += 1

   actual_matched_shapeids = set()
   
   for shapeid in matched_shapeids:
      if len( im_shapes[shapeid] ) < smallest_pixc:
         continue
      if matched_shapeids[shapeid] / len( im_shapes[shapeid] ) >= 0.4:
         actual_matched_shapeids.add(shapeid)

   return actual_matched_shapeids




skip = 0
remaining = len(consecutives)
for consecutive in consecutives:
   # {'25.26': [(55310, 53315), (55310, 55702), (55310, 56108)], '26.27': [(53315, 56105), (55702, 56105), (56108, 56105)], ... }
   
   if skip >= 1:
      skip -= 1
      continue

   print("\r" + str(remaining) + " remaining", end="")
   remaining -= 1

   missing_btwn_files_nums = set(all_btwn_files_nums).difference( set( consecutive.keys() ) )
   remaining_files = btwn_amng_files_functions.put_btwn_frames_files_in_order( missing_btwn_files_nums )
   
   done_files = set()
   
   test_imfile = top_shapes_dir + directory + "temp/test.png"
   while len( remaining_files ) >= 1:
   
      each_files = remaining_files[0]
      
      # check which adjacent each_files are present in consecutive
      
      cur_im1file =  each_files.split(".")[0] 
      cur_im2file = each_files.split(".")[1]
      
      prev_fnums = str( int(cur_im1file) - 1 ) + "." + cur_im1file
      next_fnums = cur_im2file + "." + str( int(cur_im2file) + 1 )


      shapes_dfile = shapes_dir + cur_im1file + "shapes.data"
      with open (shapes_dfile, 'rb') as fp:
         # { 79999: [79999, ... ], ... }
         # { shapeid: [ pixel indexes ], ... }
         im1shapes = pickle.load(fp)
      fp.close()

      shapes_im2dfile = shapes_dir + cur_im2file + "shapes.data"
      with open (shapes_im2dfile, 'rb') as fp:
         im2shapes = pickle.load(fp)
      fp.close()   

      im1shape_neighbors_file = shapes_dir + "shape_nbrs/" + cur_im1file + "_shape_nbrs.data"
      im2shape_neighbors_file = shapes_dir + "shape_nbrs/" + cur_im2file + "_shape_nbrs.data"
      with open (im1shape_neighbors_file, 'rb') as fp:
         im1shapes_neighbors = pickle.load(fp)
      fp.close()   

      with open (im2shape_neighbors_file, 'rb') as fp:
         im2shapes_neighbors = pickle.load(fp)
      fp.close()   

      im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im1file, directory, min_colors=min_colors)
      im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im2file, directory, min_colors=min_colors)

      im1shapeids_by_pindex_dfile = shapes_dir + "shapeids_by_pindex/" + cur_im1file + ".data"
      with open (im1shapeids_by_pindex_dfile, 'rb') as fp:
         im1shapeids_by_pindex = pickle.load(fp)
      fp.close()           
      
      im2shapeids_by_pindex_dfile = shapes_dir + "shapeids_by_pindex/" + cur_im2file + ".data"
      with open (im2shapeids_by_pindex_dfile, 'rb') as fp:
         im2shapeids_by_pindex = pickle.load(fp)
      fp.close()    

      im2 = Image.open(top_images_dir + directory + cur_im2file + ".png" )
      im2_data = im2.getdata()

      im1 = Image.open(top_images_dir + directory + cur_im1file + ".png" )
      im1_data = im1.getdata()

      found = False
      matched_shapeids = set()
      
      if prev_fnums in consecutive.keys():
         # previous each_files is present in consecutive. find current matching image2 shape with previous image2 shape.
         if len(consecutive[prev_fnums]) != 2 or ( type( consecutive[prev_fnums][0] ) is not set and type( consecutive[prev_fnums][1] ) is not set ):
            # consecutive[prev_fnums] -> [ ( 111, 222 ), ... ]
            prev_im2shapeids = { temp_shapes[1] for temp_shapes in consecutive[prev_fnums] }
         else:
            # consecutive[prev_fnums] -> [ { image1 shapeids }, { image2 shapeids } ]
            prev_im2shapeids = consecutive[prev_fnums][1]

         # [ { cur image1 shapeids }, { cur image2 shapeids } ]
         cur_neighbor_matches = get_cur_neighbor_matches( prev_fnums, each_files, 1 )
         
         im_shapes_colors = [ im1shapes_colors, im2shapes_colors ]
         im_shapeids_by_pindex = [ im1shapeids_by_pindex, im2shapeids_by_pindex ]

         #image_functions.cr_im_from_shapeslist2( cur_im1file, directory, cur_neighbor_matches[0], shapes_rgbs=[(255,255,0)], save_filepath=test_imfile )
         #image_functions.cr_im_from_shapeslist2( cur_im1file, directory, prev_im2shapeids, shapes_rgbs=[(255,0,0)], input_im=test_imfile )
         #image_functions.cr_im_from_shapeslist2( cur_im2file, directory, cur_neighbor_matches[1], shapes_rgbs=[(0,255,255)] )
         
         im1pixels = {}
         target_im1pixels = {}
         for cur_im1index, cur_im1shapeids in enumerate( [ cur_neighbor_matches[0], prev_im2shapeids ] ):
            if cur_im1index == 1:
               fill_target_im1pixels = "target_im1pixels[pindex] = im1shapes_colors[cur_im1shapeid]"
            else:
               fill_target_im1pixels = ""
               
            for cur_im1shapeid in cur_im1shapeids:
               for pindex in im1shapes[cur_im1shapeid]:
                  im1pixels[pindex] = im1shapes_colors[cur_im1shapeid]
                  exec( fill_target_im1pixels )

         im2pixels = {}
         for cur_im2shapeid in cur_neighbor_matches[1]:
            for pindex in im2shapes[cur_im2shapeid]:
               im2pixels[pindex] = im2shapes_colors[cur_im2shapeid]

         if len(im2pixels) >= 1:
            # find mathing shape from cur_im2file.
            matched_pixels = same_shapes_functions.match_t_shape_w_nbrs_while_moving_it( im1pixels, im2pixels, target_im1pixels, None, im_size, min_colors, 
                             None, im_data=im2_data, return_pixels=True, best_match=True, im_data_shapeids_by_pindex=im2shapeids_by_pindex, im_data_shapes=im2shapes )

            if len(matched_pixels) >= 1:
               matched_shapeids = get_matched_shapeids_from_m_pixels( matched_pixels, im2shapeids_by_pindex, im2shapes )
            
               #image_functions.cr_im_from_pixels( cur_im2file, directory, matched_pixels, pixels_rgb=(50,50,255) )
               found = True

         else:
            matched_shapeids = same_shapes_functions.match_by_mov_shape_against_im( im_shapes_colors, im_shapeids_by_pindex, im1pixels, target_im1pixels,
                               im_size, min_colors, im2shapes, return_shapeids=True )
            
            if len(matched_shapeids) >= 1:
               #image_functions.cr_im_from_shapeslist2( cur_im2file, directory, matched_shapeids, shapes_rgbs=[(50,50,255)] )
               found = True

         if len(matched_shapeids) >= 1:
            consecutive[each_files] = [ prev_im2shapeids, matched_shapeids ]


      if next_fnums in consecutive.keys() and found is False: 
         # next each_files is present in consecutive. so the next each_files image1 becomes the current image2 shape and I need to find
         # matching matching image1 shape in current each_files
         
         if len(consecutive[next_fnums]) != 2 or ( type( consecutive[next_fnums][0] ) is not set and type( consecutive[next_fnums][1] ) is not set ):
            # consecutive is [(111,222), ...]
            next_im1shapeids = { temp_shapes[0] for temp_shapes in consecutive[next_fnums] }
         else:
            # consecutive is [ { 111,222 }, { 222, 223 } ]
            next_im1shapeids = consecutive[next_fnums][0]
      
         # [ { cur image1 shapeids }, { cur image2 shapeids } ]
         cur_neighbor_matches = get_cur_neighbor_matches( next_fnums, each_files, 0 )
         
         #image_functions.cr_im_from_shapeslist2( cur_im1file, directory, cur_neighbor_matches[0], shapes_rgbs=[(255,255,0)], save_filepath=test_imfile )
         #image_functions.cr_im_from_shapeslist2( cur_im2file, directory, cur_neighbor_matches[1], shapes_rgbs=[(0,255,255)], save_filepath=test_imfile )
         #image_functions.cr_im_from_shapeslist2( cur_im2file, directory, next_im1shapeids, shapes_rgbs=[(0,0,255)], input_im=test_imfile )

         im_shapes_colors = [ im2shapes_colors, im1shapes_colors ]
         im_shapeids_by_pindex = [ im2shapeids_by_pindex, im1shapeids_by_pindex ]


         im2pixels = {}
         target_im2pixels = {}
         for cur_im2index, cur_im2shapeids in enumerate( [ cur_neighbor_matches[1], next_im1shapeids ] ):
            if cur_im2index == 1:
               fill_target_im2pixels = "target_im2pixels[pindex] = im2shapes_colors[cur_im2shapeid]"
            else:
               fill_target_im2pixels = ""
               
            for cur_im2shapeid in cur_im2shapeids:
               for pindex in im2shapes[cur_im2shapeid]:
                  im2pixels[pindex] = im2shapes_colors[cur_im2shapeid]
                  exec( fill_target_im2pixels )

         im1pixels = {}
         for cur_im1shapeid in cur_neighbor_matches[0]:
            for pindex in im1shapes[cur_im1shapeid]:
               im1pixels[pindex] = im1shapes_colors[cur_im1shapeid]


         if len(im1pixels) >= 1:
            # find mathing shape from cur_im1file.
            matched_pixels = same_shapes_functions.match_t_shape_w_nbrs_while_moving_it( im2pixels, im1pixels, target_im2pixels, None, im_size, min_colors, 
                             None, im_data=im1_data, return_pixels=True, best_match=True, im_data_shapeids_by_pindex=im1shapeids_by_pindex, im_data_shapes=im1shapes )

            if len(matched_pixels) >= 1:
               matched_shapeids = get_matched_shapeids_from_m_pixels( matched_pixels, im1shapeids_by_pindex, im1shapes )
            
               #image_functions.cr_im_from_pixels( cur_im1file, directory, matched_pixels, pixels_rgb=(50,50,255) )

         else:
            matched_shapeids = same_shapes_functions.match_by_mov_shape_against_im( im_shapes_colors, im_shapeids_by_pindex, im2pixels, target_im2pixels,
                               im_size, min_colors, im1shapes, return_shapeids=True )
            
            if len(matched_shapeids) >= 1:
               pass
               #image_functions.cr_im_from_shapeslist2( cur_im1file, directory, matched_shapeids, shapes_rgbs=[(50,50,255)] )

         if len(matched_shapeids) >= 1:
            consecutive[each_files] = [ matched_shapeids, next_im1shapeids ]
      

      done_files.add(each_files)

      remaining_files = missing_btwn_files_nums.difference( done_files )
      remaining_files = btwn_amng_files_functions.put_btwn_frames_files_in_order( remaining_files )


consecutives2_ddir = top_shapes_dir + directory + "all_matches/consecutives2/data/"
if os.path.exists(consecutives2_ddir ) == False:
   os.makedirs(consecutives2_ddir )

consecutives2_dfile = consecutives2_ddir + "1to1.data"
with open(consecutives2_dfile, 'wb') as fp:
   # [ {'28.29': [(79998, 79998)], '29.30': [(79998, 79998)], '27.28': [{79962, 75948, 77965, 79998}, {79998}]}, ... ]
   # [ { each_files: inner list, ... }, ... ]
   # inner list contains either tuple of image1 shapeid and image2 shapeid or 2 sets of image1 shapeids and image2 shapeids. below shows with format.
   # [ ( image1 shapeid, image2 shapeid ), ( another image1 shapeid, another image2 shapeid ) ], [ { image1 shapeids }, { image2 shapeids } ].
   pickle.dump(consecutives, fp)
fp.close()















