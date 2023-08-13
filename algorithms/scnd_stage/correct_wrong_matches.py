
from libraries import  read_files_functions, pixel_shapes_functions, pixel_functions, image_functions, same_shapes_functions


from PIL import ImageTk, Image
import os, sys
import pickle
import copy
import math
import shutil
from operator import xor

from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files, frth_smallest_pixc, third_smallest_pixc, Lshape_size

directory = sys.argv[1]
shapes_type = "intnl_spixcShp"


if directory != "" and directory[-1] != '/':
   directory +='/'

across_all_files_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/data/"
across_all_files_dfile = across_all_files_ddir + "all_files.data"
with open (across_all_files_dfile, 'rb') as fp:
   # {'10.11': {('79935', '58671'), ('39441', '39842'), ('45331', '36516')}, '11.12': {('39842', '40243'), ('26336', '27137'), ... }, ... }
   acrs_all_files_shapes = pickle.load(fp)
fp.close()

all_matches_so_far_dfile = across_all_files_ddir + "all_matches.data"
if os.path.exists( all_matches_so_far_dfile ):
   with open (all_matches_so_far_dfile, 'rb') as fp:
      all_matches_so_far = pickle.load(fp)
   fp.close()

else:
   all_matches_so_far = acrs_all_files_shapes



if shapes_type == "normal":
   print("ERROR. shapes_type normal is not supported")
   sys.exit()

elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"
   
   shapes_dir = s_pixcShp_intnl_dir + "shapes/"


else:
   print("ERROR at " + str( os.path.basename(__file__) ) + " shapes_type " + shapes_type + " is not supported")
   sys.exit()



def size_is_too_diff( param_im1shapeid, param_im2shapeid, param_im1shapes, param_im2shapes, size_num=1, len_provided=False ):
   # check if size is too different
   
   if len_provided is False:
      im1shapes_total = len( param_im1shapes[param_im1shapeid] )
      im2shapes_total = len( param_im2shapes[param_im2shapeid] )
   else:
      im1shapes_total = param_im1shapeid
      im2shapes_total = param_im2shapeid
   
   im1_2pixels_diff = abs( im1shapes_total - im2shapes_total )
   if im1_2pixels_diff != 0:
      if im1shapes_total > im2shapes_total:
         if im1_2pixels_diff / im2shapes_total > size_num:
            return True
      else:
         if im1_2pixels_diff / im1shapes_total > size_num:
            return True

   return False     


def check_size_match( param_im_shapeids, param_im_shapes, comp1to1=False  ):

   im1shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( param_im_shapes[0][ param_im_shapeids[0] ], im_width, param_shp_type=1 )  
   im2shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( param_im_shapes[1][ param_im_shapeids[1] ] , im_width, param_shp_type=1 )  
                     
   # matching from smaller shape.
   if len( param_im_shapes[0][ param_im_shapeids[0] ] ) > len( param_im_shapes[1][ param_im_shapeids[1] ] ):
      im1im2_match = same_shapes_functions.match_shape_while_moving_it( im2shp_coord_xy, im1shp_coord_xy, match_threshold=0.3 )
   else:
      im1im2_match = same_shapes_functions.match_shape_while_moving_it( im1shp_coord_xy, im2shp_coord_xy, match_threshold=0.3 )

   if im1im2_match is False:
      return False
   
   if comp1to1 is False:
      if len( param_im_shapes[0][ param_im_shapeids[0] ] ) >= Lshape_size * 2:
         return True

   size_too_diff_result = size_is_too_diff( param_im_shapeids[0], param_im_shapeids[1], param_im_shapes[0], param_im_shapes[1], size_num=8 )
   if size_too_diff_result is True:
      return False
   elif size_too_diff_result is False:
      return True




wrong_matches = {}
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
for each_files in all_matches_so_far:
   print(each_files)

   wrong_matches[each_files] = set()
   
   cur_im1file = each_files.split(".")[0]
   cur_im2file = each_files.split(".")[1]

   if ref_imagefile_op is False:
      im1 = Image.open(top_images_dir + directory + cur_im1file + ".png" )
      im_size = im1.size
      im_width, im_height = im_size
      
      im1pixels = im1.getdata()
      im2 = Image.open(top_images_dir + directory + cur_im2file + ".png" )
      im2pixels = im2.getdata()
      
      ref_imagefile_op = True


   shapes_dfile = shapes_dir + cur_im1file + "shapes.data"
   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()     


   im1shapes_by_pindex = {}
   for shapeid in im1shapes:
      cur_pixels = set()
      
      for temp_p in im1shapes[shapeid]:
         im1shapes_by_pindex[ temp_p ] = shapeid
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im1shapes[shapeid] = cur_pixels



   im2shapes_dfile = shapes_dir + cur_im2file + "shapes.data"
   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()   

   
   im2shapes_by_pindex = {}
   for shapeid in im2shapes:
      cur_pixels = set()
      
      for temp_p in im2shapes[shapeid]:
         im2shapes_by_pindex[temp_p] = shapeid
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im2shapes[shapeid] = cur_pixels

 

   im1shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + cur_im1file + "_shape_nbrs.txt"
   im2shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + cur_im2file + "_shape_nbrs.txt"

   im1shapes_neighbors = read_files_functions.rd_dict_k_v_l(cur_im1file, directory, im1shape_neighbors_file)
   im2shapes_neighbors = read_files_functions.rd_dict_k_v_l(cur_im2file, directory, im2shape_neighbors_file)

   im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im1file, directory, shapes_type=shapes_type, min_colors=True)
   im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im2file, directory, shapes_type=shapes_type, min_colors=True)

   done_im_shapes = set()

   for each_shapes in all_matches_so_far[ each_files ]:
      
      if each_shapes in done_im_shapes:
         continue
      
      cur_shapes = set()
      
      result_im_shapes = { temp_shapes for temp_shapes in all_matches_so_far[ each_files ] if temp_shapes[0] == each_shapes[0] and temp_shapes != each_shapes }

      done_im_shapes |= result_im_shapes
      cur_shapes |= result_im_shapes
      
      result_im1shapes = { temp_shape[0] for temp_shape in result_im_shapes }
      result_im2shapes = { temp_shape[1] for temp_shape in result_im_shapes }

      result_im_shapes = { temp_shapes for temp_shapes in all_matches_so_far[ each_files ] if temp_shapes[1] == each_shapes[1] and temp_shapes != each_shapes }

      done_im_shapes |= result_im_shapes
      cur_shapes |= result_im_shapes
      
      result_im1shapes |= { temp_shape[0] for temp_shape in result_im_shapes }
      result_im1shapes.add( each_shapes[0] )
      
      result_im2shapes |= { temp_shape[1] for temp_shape in result_im_shapes }
      result_im2shapes.add( each_shapes[1] )
      

      cur_im1pixels = set()
      for result_im1shape in result_im1shapes:
         cur_im1pixels |= im1shapes[ result_im1shape ]
      
      cur_im2pixels = set()
      for result_im2shape in result_im2shapes:
         cur_im2pixels |= im2shapes[ result_im2shape ]


      # { xy in string: shape color }
      all_im1shapes_pix = {}
      all_im2shapes_pix = {}
      
      # { shapeid: count of how many pixels matched, ... }
      matched_im1shapes = {}
      matched_im2shapes = {}
      
      # [ [ source xy, shape coordinate xy ], ... ]
      # [ [ (x,y), (x,y) ], ... ]
      im1shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( cur_im1pixels, im_width, param_shp_type=1, return_src_pix=True )
      for xy in im1shp_coord_xy:
         xy_str = str( xy[1][0] ) + "." + str( xy[1][1] )
         # get source pixel's color
         pindex = pixel_functions.convert_xy_to_pindex( xy[0], im_width )
         all_im1shapes_pix[ xy_str ] =  im1pixels[ pindex ]

      im2shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( cur_im2pixels, im_width, param_shp_type=1, return_src_pix=True )
      for xy in im2shp_coord_xy:
         xy_str = str( xy[1][0] ) + "." + str( xy[1][1] )
         # get source pixel's color
         pindex = pixel_functions.convert_xy_to_pindex( xy[0], im_width )
         all_im2shapes_pix[ xy_str ] =  im2pixels[ pindex ]

      im1im2_match = same_shapes_functions.match_shape_while_moving_it2( all_im1shapes_pix, all_im2shapes_pix, im_size, best_match=True )
      if im1im2_match is not None:
         # im1im2_match -> [ {(3, 4), (3, 1), ... }, { (x,y), ... } ]
         # im1im2_match -> [ image1 matched pixels, image2 matched pixels ]
         
         debug_im1pixels = set()
         for matched_im1pixel in im1im2_match[0]:
            
            # getting source pixel from im1shp_coord_xy
            matched_im1src_pixel = [ temp_xy[0] for temp_xy in im1shp_coord_xy if temp_xy[1] == matched_im1pixel ]
            
            if len( matched_im1src_pixel ) != 1:
               print("ERROR. there should be exactly one pixel match in im1shp_coord_xy")
               sys.exit()
            elif len( matched_im1src_pixel ) == 1:
               # find which shape's pixel matched_im1src_pixel is
               cur_pixel_matched = False
               for result_im1shape in result_im1shapes:
                  if matched_im1src_pixel[0] in im1shapes[ result_im1shape ]:
                     if result_im1shape not in matched_im1shapes.keys():
                        matched_im1shapes[ result_im1shape ] = 1
                     else:
                        matched_im1shapes[ result_im1shape ] += 1
                     
                     cur_pixel_matched = True
                     break
                  
               if cur_pixel_matched is False:
                  print("ERROR. every pixel has to be found")
                  sys.exit()

               debug_im1pixels.add( matched_im1src_pixel[0] )
         
         
         debug_im_file = top_shapes_dir + directory + scnd_stg_all_files + "/correct_matches/temp/debug_im1.png"
         #image_functions.cr_im_from_shapeslist2( cur_im1file, directory, result_im1shapes, save_filepath=None , shapes_rgb=(255,0,0) )
         #image_functions.cr_im_from_shapeslist2( cur_im2file, directory, result_im2shapes, save_filepath=None , shapes_rgb=(0,0,255) )
         #image_functions.cr_im_from_pixels( cur_im1file, directory, debug_im1pixels, pixels_rgb=(255,0,255) )

         debug_im2pixels = set()
         for matched_im2pixel in im1im2_match[1]:
            # # getting source pixel from im2shp_coord_xy
            matched_im2src_pixel = [ temp_xy[0] for temp_xy in im2shp_coord_xy if temp_xy[1] == matched_im2pixel ]
            
            if len( matched_im2src_pixel ) != 1:
               print("ERROR. there should be exactly one pixel match in im2shp_coord_xy")
               sys.exit()
            elif len( matched_im2src_pixel ) == 1:
               cur_pixel_matched = False
               for result_im2shape in result_im2shapes:
                  if matched_im2src_pixel[0] in im2shapes[ result_im2shape ]:
                     if result_im2shape not in matched_im2shapes.keys():
                        matched_im2shapes[ result_im2shape ] = 1
                     else:
                        matched_im2shapes[ result_im2shape ] += 1

                     cur_pixel_matched = True
                     break
               
               if cur_pixel_matched is False:
                  print("ERROR. every pixel has to be found")
                  sys.exit()
               
               debug_im2pixels.add( matched_im2src_pixel[0] )
         
         #image_functions.cr_im_from_pixels( cur_im2file, directory, debug_im2pixels, pixels_rgb=(255,0,255) )
               
         result_im1shapes = list( result_im1shapes )
         result_im2shapes = list( result_im2shapes )
         cur_shapes = list( cur_shapes )
         match_threshold = 0.22
         
         debug_shape_pair = ( ) # ( image1 shapeid, image2 shapeid )
         
         if len( result_im1shapes ) == 1 and len( result_im2shapes ) > 1:
            for result_im2shape in result_im2shapes:
               if ( result_im2shape not in matched_im2shapes.keys() ) or matched_im2shapes[ result_im2shape ] / len( im2shapes[ result_im2shape ] ) < match_threshold:
                  size_match_result = check_size_match( ( result_im2shape, result_im1shapes[0] ), [ im2shapes, im1shapes ] )
                  if size_match_result is False:
                     wrong_matches[ each_files ].add( ( result_im1shapes[0], result_im2shape ) )

                     if ( result_im1shapes[0], result_im2shape ) == debug_shape_pair:
                        print( "debug1 " + str( each_shapes ) )
                  
         elif len( result_im1shapes ) > 1 and len( result_im2shapes ) == 1:
            for result_im1shape in result_im1shapes:
               if ( result_im1shape not in matched_im1shapes.keys() ) or matched_im1shapes[ result_im1shape ] / len( im1shapes[ result_im1shape ] ) < match_threshold:
                  size_match_result = check_size_match( ( result_im1shape, result_im2shapes[0] ), [ im1shapes, im2shapes ] )
                  if size_match_result is False:
                     wrong_matches[ each_files ].add( ( result_im1shape, result_im2shapes[0] ) ) 

                     if ( result_im1shape, result_im2shapes[0] ) == debug_shape_pair:
                        print( "debug2 " + str( each_shapes ) )
         
         elif len( result_im1shapes ) == 1 and len( result_im2shapes ) == 1:
            if matched_im1shapes[ result_im1shapes[0] ] / len( im1shapes[ result_im1shapes[0] ] ) < match_threshold:
               if matched_im2shapes[ result_im2shapes[0] ] / len( im2shapes[ result_im2shapes[0] ] ) < match_threshold:
                  size_match_result = check_size_match( ( result_im1shapes[0] , result_im2shapes[0] ), [ im1shapes, im2shapes ], comp1to1=True  )
                  if size_match_result is False:
                     wrong_matches[ each_files ].add( ( result_im1shapes[0] , result_im2shapes[0] ) ) 

                     if ( result_im1shapes[0] , result_im2shapes[0] ) == debug_shape_pair:
                        print( "debug3 " + str( each_shapes ) )                  
         
         elif len( result_im1shapes ) > 1 and len( result_im2shapes ) > 1:
            for cur_im1shape in cur_shapes[0]:
               if cur_im1shape not in matched_im1shapes.keys() or matched_im1shapes[ cur_im1shape ] / len( im1shapes[ cur_im1shape ] ) < match_threshold:
                  # cur_im1shape not matched, so remove all matched pairs that have cur_im1shape
                  
                  cur_im1shape_pairs = [ temp_shapes for temp_shapes in cur_shapes if temp_shapes[0] == cur_im1shape ]

            for cur_im1shape_pair in cur_im1shape_pairs:
               for cur_im2shape in cur_im1shape_pair[1]:
                  if cur_im2shape not in matched_im2shapes.keys() or matched_im2shapes[ cur_im2shape ] / len( im2shapes[ cur_im2shape ] ) < match_threshold:
                     cur_im2shape_pairs = [ temp_shapes for temp_shapes in cur_im1shape_pairs if temp_shapes[1] == cur_im2shape ]
                  
                     for cur_im2shape_pair in cur_im2shape_pairs:
                        size_match_result = check_size_match( cur_im2shape_pair, [ im1shapes, im2shapes ], comp1to1=True  )
                        if size_match_result is False:
                           wrong_matches[ each_files ].add( cur_im2shape_pair )
      
                           if cur_im2shape_pair == debug_shape_pair:
                              print( "debug4 " + str( each_shapes ) )




for each_files in wrong_matches:

   if each_files in all_matches_so_far.keys():
      print("all_matches_so_far number of shapes in image " + each_files + " before " + str( len( all_matches_so_far[ each_files ] ) ) )
      for each_shapes in wrong_matches[ each_files ]:
         
         if each_shapes in all_matches_so_far[ each_files ]:
            all_matches_so_far[ each_files ].remove( each_shapes )

      print("all_matches_so_far number of shapes in image " + each_files + " after " + str( len( all_matches_so_far[ each_files ] ) ) )
      print()


correct_matches_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/correct_matches/data/"
if os.path.exists(correct_matches_ddir ) == False:
   os.makedirs(correct_matches_ddir )

correct_matches_dfile = correct_matches_ddir + "1.data"
if os.path.exists(correct_matches_dfile):
   with open (across_all_files_dfile, 'rb') as fp:
      # {'10.11': [('79935', '58671'), ('39441', '39842'), ('45331', '36516') ], '11.12': [('39842', '40243'), ('26336', '27137'), ... ], ... }
      prev_wrong_matches = pickle.load(fp)
   fp.close()
   
   for each_files in prev_wrong_matches:
      if each_files in wrong_matches.keys():
         for each_shapes in prev_wrong_matches[ each_files ]:
            if each_shapes not in wrong_matches[ each_files ]:
               wrong_matches[ each_files ].add( each_shapes )
      
      else:
         wrong_matches[ each_files ] = prev_wrong_matches[ each_files ]


with open(correct_matches_dfile, 'wb') as fp:
   pickle.dump(wrong_matches, fp)
fp.close()


with open(all_matches_so_far_dfile, 'wb') as fp:
   pickle.dump(all_matches_so_far, fp)
fp.close()
















