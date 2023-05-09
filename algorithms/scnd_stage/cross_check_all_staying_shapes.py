import tkinter
from PIL import ImageTk, Image
from libraries import read_files_functions
from libraries.cv_globals import top_shapes_dir, pixch_sty_dir, styLshapes, styLshapes_wo_pixch, internal
import pickle
import sys



target_im_file = "14"
target_im_file2 = "15"
shapes_type = "intnl_spixcShp"
directory = "videos/street3/resized/min"
no_prev_files = False


# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

prev_file = str( int(target_im_file) - 1 )
next_file = str( int(target_im_file) + 1 )


# pixch staying shapes. current file
sty_shapes_dir = top_shapes_dir + directory + pixch_sty_dir + "/"
sty_shapes_file = sty_shapes_dir + "data/" + target_im_file + "." + next_file + "verified.data"
with open (sty_shapes_file, 'rb') as fp:
   # {('21046', '18645'), ... }
   # { ( image1 shapeid, image2 shapeid ), ... }
   cur_file_pixch_sty_shapes = pickle.load(fp)
fp.close()



# staying large shapes. current file
staying_Lshapes_Ddir = top_shapes_dir + directory + styLshapes + "/" + shapes_type + "/data/"
staying_Lshapes1to2_dfile = staying_Lshapes_Ddir + target_im_file + "." + next_file + ".data"
with open (staying_Lshapes1to2_dfile, 'rb') as fp:
   # [['56099', '56105'], ... ]
   cur_file_styLshapes = pickle.load(fp)
fp.close()



staying_Lshapes_wo_pixch_Ddir = top_shapes_dir + directory + styLshapes_wo_pixch + "/" + shapes_type + "/data/"
staying_Lshapes_wo_pixch_dfile = staying_Lshapes_wo_pixch_Ddir + target_im_file + "." + next_file + ".data"
with open (staying_Lshapes_wo_pixch_dfile, 'rb') as fp:
   # [['79999', '79936', ['67590', '67196']]]
   # [ ['image1 shapeid', 'image2 shapeid' [ matched pixels ]], ... ]
   cur_file_styLshapes_wo_pixch = pickle.load(fp)
fp.close()

if no_prev_files is False:

   # pixch staying shapes. previous file
   sty_shapes_file = sty_shapes_dir + "data/" + prev_file + "." + target_im_file + "verified.data"
   with open (sty_shapes_file, 'rb') as fp:
      # [('1270', '2072'), ('2062', '2062'), ... ]
      # [ ( image1 shapeid, image2 shapeid ), ... ]
      prev_file_pixch_sty_shapes = pickle.load(fp)
   fp.close()

   # staying large shapes. previous file
   staying_Lshapes1to2_dfile = staying_Lshapes_Ddir + prev_file + "." + target_im_file + ".data"
   with open (staying_Lshapes1to2_dfile, 'rb') as fp:
      # [['56099', '56105'], ... ]
      prev_file_styLshapes = pickle.load(fp)
   fp.close()

   staying_Lshapes_wo_pixch_dfile = staying_Lshapes_wo_pixch_Ddir + prev_file + "." + target_im_file + ".data"
   with open (staying_Lshapes_wo_pixch_dfile, 'rb') as fp:
      # [['79999', '79936', ['67590', '67196']]]
      # [ ['image1 shapeid', 'image2 shapeid' [ matched pixels ]], ... ]
      prev_file_styLshapes_wo_pixch = pickle.load(fp)
   fp.close()


if shapes_type == "normal":
   print("shapes_type normal is not supported in " + os.path.basename(__file__) )
   sys.exit()
   

elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"
   im_shape_neighbors_filepath = s_pixcShp_intnl_dir + "shape_nbrs/" + target_im_file + "_shape_nbrs.txt"
   im2shape_neighbors_filepath = s_pixcShp_intnl_dir + "shape_nbrs/" + target_im_file2 + "_shape_nbrs.txt"


#  { '79999': ['79950', '69559', ... ], ... }
im_shapes_neighbors = read_files_functions.rd_dict_k_v_l(target_im_file, directory, im_shape_neighbors_filepath)
im2shapes_neighbors = read_files_functions.rd_dict_k_v_l(target_im_file2, directory, im2shape_neighbors_filepath)


def find_conflicting_matches( param_file_matches, param_ano_file_matches, param_filename, param_ano_filename, param_cur_results ):
      
   if param_file_matches[0] == param_ano_file_matches[0] and param_file_matches[1] != param_ano_file_matches[1]:
      # image1 shape is the same but with different image2 shape
      param_cur_results.append( [ ( param_file_matches[0], param_file_matches[1] ), param_filename, param_ano_filename ] )
      param_cur_results.append( [ ( param_ano_file_matches[0], param_ano_file_matches[1] ), param_filename, param_ano_filename ] )

      already_added_cnfct.append( [ ( param_file_matches[0], param_file_matches[1] ), param_filename, param_ano_filename ] )
      already_added_cnfct.append( [ ( param_ano_file_matches[0], param_ano_file_matches[1] ), param_filename, param_ano_filename ] )

               
   elif param_file_matches[1] == param_ano_file_matches[1] and param_file_matches[0] != param_ano_file_matches[0]:
      # image2 shape is the same but with different image1 shape    

      param_cur_results.append( [ ( param_file_matches[0], param_file_matches[1] ), param_filename, param_ano_filename ] )
      param_cur_results.append( [ ( param_ano_file_matches[0], param_ano_file_matches[1] ), param_filename, param_ano_filename ] )

      already_added_cnfct.append( [ ( param_file_matches[0], param_file_matches[1] ), param_filename, param_ano_filename ] )
      already_added_cnfct.append( [ ( param_ano_file_matches[0], param_ano_file_matches[1] ), param_filename, param_ano_filename ] )



all_files_matches = [ cur_file_pixch_sty_shapes, cur_file_styLshapes, cur_file_styLshapes_wo_pixch ]

verified_matches = []
conflicting_matches = []
already_added_cnfct = []
for lindex, each_file in enumerate(all_files_matches):
   for each_file_matches in each_file:
      

      cur_filename = None
      if lindex == 0:
         cur_filename = "cur_pixch_sty"
      elif lindex == 1:
         cur_filename = "cur_styLshapes"
      elif lindex == 2:
         cur_filename = "cur_styLs_wo_pixch"
         
      cur_already_done = [ temp for temp in already_added_cnfct if ( cur_filename == temp[1] or cur_filename == temp[2] ) and \
                           ( temp[0] == each_file_matches ) ]
      
      if len( cur_already_done ) >= 1:
         continue
      

      cur_cnfct_matches = []
   
      for ano_lindex, ano_file in enumerate(all_files_matches):
         for ano_file_matches in ano_file:
            if each_file == ano_file and each_file_matches == ano_file_matches:
               # as far as I checked, there were no duplicates in each file matches so, this is itself
               continue            
               
            if ano_lindex == 0:
               ano_cur_filename = "cur_pixch_sty"
            elif ano_lindex == 1:
               ano_cur_filename = "cur_styLshapes"
            elif ano_lindex == 2:
               ano_cur_filename = "cur_styLs_wo_pixch"

            ano_already_done = [ temp for temp in already_added_cnfct if ( ano_cur_filename == temp[1] or ano_cur_filename == temp[2] ) and \
                           ( temp[0] == ano_file_matches ) ]
      
            if len( ano_already_done ) >= 1:
               continue   

            if each_file == ano_file:
               # because there are appearantly no duplicates in each file, same file comparison is done
               # only to find conflicting matches
               find_conflicting_matches( each_file_matches, ano_file_matches, cur_filename, ano_cur_filename, cur_cnfct_matches)
               
            
            
            else:
               # comparison with different file
               # cross file matches and conflicing matches will be searched here.
               find_conflicting_matches( each_file_matches, ano_file_matches, cur_filename, ano_cur_filename, cur_cnfct_matches )
               
               if each_file_matches[0] == ano_file_matches[0] and each_file_matches[1] == ano_file_matches[1]:
                  verified_matches.append( [ ( each_file_matches[0], each_file_matches[1] ), cur_filename, ano_cur_filename ]  )
               
      
      if len( cur_cnfct_matches ) >= 1:
         conflicting_matches.append( cur_cnfct_matches )    
            

# this is used for displaying images
root = tkinter.Tk()

for each_matches in conflicting_matches:
   # each_matches -> [[('27539', '28740'), 'cur_pixch_sty', 'cur_styLs_wo_pixch'], [('7538', '28740'), 'cur_pixch_sty', 'cur_styLs_wo_pixch']]
   
   window = tkinter.Toplevel(root)
   window.geometry("1600x800")
   window_title = ""
   row_counter = 0
   column_couner = 0
   for each_im1im2 in each_matches:
      
      window_title += each_im1im2[1] + "." + each_im1im2[0][0] + each_im1im2[2] + "." + each_im1im2[0][1] + "_"
      
      original_shape_file = top_shapes_dir + directory + "shapes/" + shapes_type + "/" + target_im_file + "/" + each_im1im2[0][0] + ".png"
      compare_shape_file = top_shapes_dir + directory + "shapes/" + shapes_type + "/" + target_im_file2 + "/" + each_im1im2[0][1] + ".png"
   
      img = ImageTk.PhotoImage(Image.open(original_shape_file))
      img2 = ImageTk.PhotoImage(Image.open(compare_shape_file))
  
      label1 = tkinter.Label(window, image = img, bg="white")
      label1.image = img
      label1.grid( row=row_counter, column=column_couner )
      column_couner += 1
      
      if column_couner == 4:
         column_couner = 0
         row_counter += 1
   
      label2 = tkinter.Label(window, image = img2, bg="white" )
      label2.image = img2
      label2.grid( row=row_counter, column=column_couner )
      
      column_couner += 1
      if column_couner == 4:
         column_couner = 0
         row_counter += 1

   
   window.title( window_title )



root.mainloop()



























