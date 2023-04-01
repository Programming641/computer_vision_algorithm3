from libraries import read_files_functions
from libraries import pixel_shapes_functions
from libraries import pixel_functions
import sys, os
import copy
import pickle
import winsound

from collections import OrderedDict
from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir

temp_dir = proj_dir + "/temp/"


filename = "24"

directory = "videos/giraffe/min"
shapes_dir = directory

if len(sys.argv) > 1:
   filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]

   directory = sys.argv[1]

   print("execute script find_rpt_ptn_shapes.py. filename " + filename + " directory " + directory )

if directory != "" and directory[-1] != ('/'):
   directory +='/'
if shapes_dir != "" and shapes_dir[-1] != ('/'):
   shapes_dir +='/'


if not os.path.isdir(top_shapes_dir + shapes_dir + "/rpt_ptn/"):
   os.makedirs(top_shapes_dir + shapes_dir + "/rpt_ptn/")

rpt_ptn_file = open(top_shapes_dir + shapes_dir + "/rpt_ptn/" + filename + "_rpt_ptn_shapes.txt" , "w" )



nbr_filepath = top_shapes_dir + directory + "shape_nbrs/" + filename + "_shape_nbrs.txt"

shape_nbrs = read_files_functions.rd_ldict_k_v_l(filename, directory, nbr_filepath)

# list of dictionaries. each dictionary contains list of nbr_shapeid
# [ { src_shapeid: [ nbr_shapeid, nbr_shapeid, nbr_shapeid ] }, { src_shapeid: [ nbr_shapeid, nbr_shapeid ] }, ... ]
rpt_ptn_shapes = []

prev_src_nbr = None

cur_rpt_ptn = []

all_cur_rpt_ptns = []

rpt_ptn_temp_file = temp_dir + shapes_dir.replace("/", ".") + filename + "_rpt_ptn.txt"
shape_nbrs_clrs = None
if os.path.exists(rpt_ptn_temp_file):
   with open (rpt_ptn_temp_file, 'rb') as fp:
      shape_nbrs_clrs = pickle.load(fp)
else:
   # returned form. shape_id: { r, g, b }
   # { '35719': {'r': 239, 'g': 53, 'b': 60}, '35731': {'r': 255, 'g': 255, 'b': 255},....}
   shapes_colors = pixel_shapes_functions.get_all_shapes_colors( filename, directory )

   shape_nbrs_clrs = copy.deepcopy( shape_nbrs )

   # populating shape_nbrs_clrs
   for shapeid_color in shapes_colors:
      for shape_nbr in shape_nbrs:
         for shapeid , shapeid_nbrs in shape_nbr.items():
         
            if shapeid == shapeid_color:
            
               cur_shapeid_index = shape_nbrs.index( shape_nbr )
               shape_nbrs_clrs[ cur_shapeid_index ][ "shapeid_clr" ] = shapes_colors[shapeid_color]
         
            elif shapeid_color in shapeid_nbrs:
            
               cur_s_nbr_index = shape_nbrs.index( shape_nbr )
            
               if not shape_nbrs_clrs[ cur_s_nbr_index ].get("nbr_clrs"):
                  shape_nbrs_clrs[ cur_s_nbr_index ]["nbr_clrs"] = []
            
               found_nbr_index = shapeid_nbrs.index( shapeid_color )

            
               shape_nbrs_clrs[cur_s_nbr_index]["nbr_clrs"].insert( found_nbr_index, shapes_colors[shapeid_color] )
            

   with open(rpt_ptn_temp_file, 'wb') as fp:
      pickle.dump(shape_nbrs_clrs, fp)
   fp.close()



debug = False


def group_by_same_color( cur_match_results, subgroup=None, matched_grp=None, unmatched=None, matched_grp_index=None ):
   final_matched_groups = []

   if subgroup == None:
      # first, get first subgroup
      cur_first_subgrp_src_nbr_sid = list(cur_match_results.keys())[0]
      cur_first_subgrp = cur_match_results[cur_first_subgrp_src_nbr_sid]
      
      cur_matched_grp = []
      
      cur_unmatched_grp = []
      
      cur_matched_grp.append( [ cur_first_subgrp_src_nbr_sid ] )
      cur_matched_grp_index = cur_matched_grp.index( [ cur_first_subgrp_src_nbr_sid ] )
            
      matched_src_nbrs = []
      for src_nbr_sid_in_first_subgrp, matched in cur_first_subgrp.items():
         if matched:
            matched_src_nbrs.append( src_nbr_sid_in_first_subgrp )
         else:
            cur_unmatched_grp.append( src_nbr_sid_in_first_subgrp )
                  
   
      final_matched_groups = group_by_same_color( cur_match_results, subgroup=matched_src_nbrs, matched_grp=cur_matched_grp, matched_grp_index=cur_matched_grp_index,
                           unmatched=cur_unmatched_grp )
      return final_matched_groups
   else:
      first = True
      cur_subgroup = []
      for shapeid in subgroup:
         if first:
            first_shapeid = shapeid
            
            matched_grp[matched_grp_index].append( first_shapeid )
            
            first = False
            continue
         
         if cur_match_results[first_shapeid][shapeid]:
            cur_subgroup.append( shapeid )
         else:
            unmatched.append( shapeid )
         
      if len(cur_subgroup) >= 2:     
         final_matched_groups = group_by_same_color( cur_match_results, subgroup=cur_subgroup, matched_grp=matched_grp, matched_grp_index=matched_grp_index, unmatched=unmatched )
         
         return final_matched_groups
      
      elif len( cur_subgroup ) == 1:
         matched_grp[matched_grp_index].append( cur_subgroup[0] )

         
      if unmatched and len(unmatched) >= 2:
         cur_unmatched = []
         matched_grp.append( [ matched_grp[0][0] ] )
         cur_matched_grp_index = matched_grp.index( [ matched_grp[0][0] ] )            
            
         final_matched_groups = group_by_same_color( cur_match_results, subgroup=unmatched, matched_grp=matched_grp, matched_grp_index=cur_matched_grp_index, unmatched=cur_unmatched )
            
         return final_matched_groups
         
      elif unmatched and len(unmatched) == 1:
         matched_grp.append( [ unmatched[0] ] )

      
      return matched_grp
      
            


def put_into_rpt_ptn_shapes( matched_groups, all_cur_rpt_ptns, rpt_ptn_shapes ):
   # put all same color src_nbrs in the same repeating pattern shape.
   
   def compareList(l1,l2):
      l1.sort()
      l2.sort()
      if(l1==l2) and l1 and l2:
         return "Equal"
      else:
         return "Non equal"
   
   

   
   # check if src_nbrs in the matched_groups are contained in the exactly the same all_cur_rpt_ptns. if so, skip them and put only one
   # into all_same_clr_src_nbrs
   matched_groups_in_all_cur_rpt_ptns = []
   for one_src_nbrs in matched_groups:
      cur_matched_group = []
      already_added_indexes = []
      for same_clr_shapeid in  one_src_nbrs:
         for all_cur_rpt_ptn in all_cur_rpt_ptns:
            if same_clr_shapeid in all_cur_rpt_ptn:
               if all_cur_rpt_ptns.index( all_cur_rpt_ptn ) not in already_added_indexes:
                  cur_matched_group.append( all_cur_rpt_ptns.index( all_cur_rpt_ptn ) )
                  already_added_indexes.append( all_cur_rpt_ptns.index( all_cur_rpt_ptn ) )

      matched_groups_in_all_cur_rpt_ptns.append( cur_matched_group )
   
   
   cur_matched_group_index = 0
   ano_cur_matched_group_index = 0
   src_nbr_pairs_in_same_cur_rpt_ptns = []
   for matched_group in matched_groups_in_all_cur_rpt_ptns:
      cur_matched_group = []
      first = True
      for ano_matched_group in matched_groups_in_all_cur_rpt_ptns:
         if cur_matched_group_index == ano_cur_matched_group_index:
            # itself
            continue
            
         for contained_indexes in src_nbr_pairs_in_same_cur_rpt_ptns:
            if cur_matched_group_index in contained_indexes and ano_cur_matched_group_index in contained_indexes:
               continue
         
         contained_in_same_cur_rpt_pnts = compareList( matched_group, ano_matched_group )
         
         if contained_in_same_cur_rpt_pnts == "Equal":
            if first:
               cur_matched_group.append( cur_matched_group_index )
               cur_matched_group.append( ano_cur_matched_group_index )
               first = False
            else:
               cur_matched_group.append( ano_cur_matched_group_index )
            
         
         
         ano_cur_matched_group_index += 1
      
      cur_matched_group_index += 1
      
      if cur_matched_group:
         src_nbr_pairs_in_same_cur_rpt_ptns.append( cur_matched_group )


   # delete all_cur_rpt_ptn after looping all matched_groups
   same_clr_rpt_ptn_items = []
   
   all_same_clr_src_nbrs = []   
   
   for one_src_nbrs in matched_groups:
      # first, check if current matched_group is contained in exactly the same all_cur_rpt_ptns as another matched_group
      skip = False
      for src_nbr_pair_indexes in src_nbr_pairs_in_same_cur_rpt_ptns:
         if matched_groups.index( one_src_nbrs ) in src_nbr_pair_indexes and len(src_nbr_pair_indexes) >= 2:
            src_nbr_pair_indexes.remove( matched_groups.index( one_src_nbrs ) )
            
            skip = True
            break
   
      if skip:
         continue
   
   
      # one_src_nbrs contains shapeids with same color
      cur_same_clr_src_nbrs = []
      added_all_cur_rpt_ptn = []

      src_nbr_not_in_rpt_ptn = []
      
      # take results from looping both shapes in the one_src_nbrs
      first = True
      
      for same_clr_shapeid in  one_src_nbrs:
         
         
         src_nbr_found = False
         # then, look for repeating pattern that contains same_clr_shapeid
         for all_cur_rpt_ptn in all_cur_rpt_ptns:
            if same_clr_shapeid in all_cur_rpt_ptn:

                        
               src_nbr_found = True
               
               if all_cur_rpt_ptns.index(all_cur_rpt_ptn) not in added_all_cur_rpt_ptn:
                  cur_same_clr_src_nbrs += all_cur_rpt_ptn
                  
                  added_all_cur_rpt_ptn.append( all_cur_rpt_ptns.index(all_cur_rpt_ptn) )
               
               # if same color src_nbr is found in all_cur_rpt_ptn, then this all_cur_rpt_ptn will be deleted from all_cur_rpt_ptns
               if all_cur_rpt_ptn not in same_clr_rpt_ptn_items:
                  same_clr_rpt_ptn_items.append( all_cur_rpt_ptn )
        
         if not src_nbr_found:
            src_nbr_not_in_rpt_ptn.append( same_clr_shapeid )
            
         if first:
            first = False
            continue
            
            
      # current same color src_nbr ended
      if cur_same_clr_src_nbrs:
      
         # each all_cur_rpt_ptn may contain same shapes, so delete them
         res = []
         for i in cur_same_clr_src_nbrs:
            if i not in res:
               res.append(i) 
      
         cur_same_clr_src_nbrs = res

         if src_nbr_not_in_rpt_ptn:
            cur_same_clr_src_nbrs += src_nbr_not_in_rpt_ptn
                                        
         
         all_same_clr_src_nbrs.append( { cur_same_clr_src_nbrs[0]: cur_same_clr_src_nbrs } )
            
      elif src_nbr_not_in_rpt_ptn:
                  
                     
         # same color src_nbrs did not have any nested neighbors. then just put same color src_nbrs into rpt_ptn_shapes
         temp = [ src_shapeid ]
         temp += src_nbr_not_in_rpt_ptn
                  
         all_same_clr_src_nbrs.append( { src_shapeid: temp } )


   # check if same_clr_src_nbrs contain exactly the same all_cur_rpt_ptn
   # this happens if src_nbrs are in the same all_cur_rpt_ptn  
   res = []
   for i in all_same_clr_src_nbrs:
      if debug:
         print("adding")
         print(str(i))
         print("to rpt_ptn_shapes")
      
      rpt_ptn_shapes.append( i )


   for same_clr_rpt_ptn_item in same_clr_rpt_ptn_items:

      all_cur_rpt_ptns.remove( same_clr_rpt_ptn_item )      
         
         





def process_neighbor ( cur_already_processed, shape_id_w_clr ,  nbr_shapeid_w_clr , src_nbr_rgb, called_from_src ):

   global prev_src_nbr, cur_rpt_ptn
   
   
   shape_id = shape_id_w_clr[0]
   shape_id_rbg = shape_id_w_clr[1]
   
   if called_from_src:
      nbr_shapeid = nbr_shapeid_w_clr
   else:
      nbr_shapeid = nbr_shapeid_w_clr[0]
      cur_neighbor_rgb = nbr_shapeid_w_clr[1]
   
   '''
   if debug and called_from_src:
      print("src_shapeid " + shape_id + " src_nbr_shapeid " + nbr_shapeid )
      print()
   elif debug and not called_from_src and prev_src_nbr != shape_id:
      print("nested neighbor " + shape_id + " deeply nested neighbor " + nbr_shapeid )
      print()
   elif debug and not called_from_src and prev_src_nbr == shape_id:
      print("src_nbr " + shape_id + " nested neighbor " + nbr_shapeid )
   '''

   if ( nbr_shapeid in cur_already_processed and not called_from_src ):
      return
      
   cur_already_processed.append(nbr_shapeid)

      
   if called_from_src:
      if prev_src_nbr and prev_src_nbr != nbr_shapeid:
         # another src_neighbor called it.

         # check if at least one nested neighbor had same color and added to cur_rpt_ptn
         if len(cur_rpt_ptn) > 2:
            
            
            all_cur_rpt_ptns.append( cur_rpt_ptn )  
           

         
         # initializing cur_rpt_ptn  
         cur_rpt_ptn = []
         
         cur_already_processed = []
         
         cur_already_processed.append( shape_id )
         cur_already_processed.append( nbr_shapeid )
         
         cur_rpt_ptn.append( shape_id )
            
         # adding src_neighbor
         cur_rpt_ptn.append(nbr_shapeid)
         
         prev_src_nbr = nbr_shapeid
         
      else:
         # first src_neighbor with current src_shapeid
         # adding src_neighbor to cur_rpt_ptn
         cur_rpt_ptn.append(nbr_shapeid)

         
         prev_src_nbr = nbr_shapeid
      

      
   if not called_from_src:
      # called with nested neighbor. Either called by src_neighbor with nested neighbor or called by nested neighbor with deeply nested neighbor        
         
      neighbor_same_color = False

      clrch, brit_thres, brit_ch_v = pixel_functions.compute_appearance_difference(shape_id_rbg, cur_neighbor_rgb, 30)
      if not clrch and brit_thres:
         neighbor_same_color = True
         

      else:
         debug_cur_rpt_ptn_rgbs_counter = 1
         # neighbor's neighbor or deeply nested neighbor. check if neighbor's neighbor has color same as any of the cur_rpt_ptn color        

         clrch, brit_thres, brit_ch_v = pixel_functions.compute_appearance_difference(src_nbr_rgb, cur_neighbor_rgb, 30)

         if not clrch and brit_thres:
               
            neighbor_same_color = True


                     
      if neighbor_same_color:
         # appearance did not change more than threshold value
                     
         cur_rpt_ptn.append(nbr_shapeid)
         

   

   # find nested neighbors only if its from src_neighbor or same color was found
   if called_from_src or neighbor_same_color:
      # find nbr_shapeid's neighbors
      
      # first, get nbr_shapeid's neighbors
      nbr_shapeid_nbrs_found = False
      nested_nbrs_counter = 0
      
      for shape_nbr in shape_nbrs_clrs:
         for shapeid, shapeid_nbrs in shape_nbr.items():
            if shapeid == nbr_shapeid:
               if shapeid == "nbr_clrs" or shapeid == "shapeid_clr":
                  continue
               
               
               for nested_nbr in shapeid_nbrs:
                  if nested_nbr in cur_already_processed:
                     nested_nbrs_counter += 1
                     continue
                     
                  nested_nbr_rgb = shape_nbr["nbr_clrs"][nested_nbrs_counter]

                  
                  process_neighbor(cur_already_processed, ( nbr_shapeid, shape_id_rbg ) , ( nested_nbr, nested_nbr_rgb ), src_nbr_rgb, False )

                  nested_nbrs_counter += 1

               
               nbr_shapeid_nbrs_found = True
               break
               
         if nbr_shapeid_nbrs_found:
            break

      
      
   #---------------------------------------------          End of process_neighbor           --------------------------------------------------
      

all_shapes = len( shape_nbrs_clrs )
debug_counter = all_shapes + 1
for shape_nbr in shape_nbrs_clrs:
   for src_shapeid, src_nbrs in shape_nbr.items():
      if src_shapeid == "nbr_clrs" or src_shapeid == "shapeid_clr":
         continue
      
      print("src_shapeid " + src_shapeid + " " + str( all_shapes ) + " remaining" )
         
      if debug_counter < 0:
         break
      

      src_shapeid_rgb =  shape_nbr["shapeid_clr"]
      
      # this is for checking if current src_nbr finishes and next one started
      prev_src_nbr = None
      
      # if the src_nbr finished and next src_nbr started. previous src_nbr repeating pattern will be added to 
      # all_cur_rpt_ptn
      all_cur_rpt_ptns = []

      # current repeating pattern. this contains all repeating patterns for current src_shape. repeating pattern will be created for each src_nbr
      # if src_nbr have same color, they will be combined at the end of the current src_shape processing.
      cur_rpt_ptn = [  src_shapeid  ]
 
   
      # already processed shape for current running src_shapeid.
      # nested neibor will be added after comparing its color with any of the cur_rpt_ptn color
      cur_already_processed = []
      cur_already_processed.append(src_shapeid)

      src_nbr_same_clr = []
      # checking if src_nbrs have same color 
      for src_nbr in range( len(src_nbrs) ):
         
         cur_src_nbr_already_putin = False
         if src_nbr_same_clr:
            for already_putin_src_nbrs in src_nbr_same_clr:
               if src_nbrs[src_nbr] in already_putin_src_nbrs:
                  cur_src_nbr_already_putin = True
                  break
            
            if cur_src_nbr_already_putin:
               continue
      
         src_nbr_rgb = shape_nbr["nbr_clrs"][src_nbr]
         
         temp_src_nbr = []
         
         for ano_src_nbr in range( len(src_nbrs) ):
            if src_nbr == ano_src_nbr:
               continue
            
            ano_nbr_rgb = shape_nbr["nbr_clrs"][ano_src_nbr]
            
            clrch, brit_thres, brit_ch_v = pixel_functions.compute_appearance_difference(src_nbr_rgb, ano_nbr_rgb, 30)
            
            if not clrch and brit_thres:
               # src_nbr and ano_src_nbr have same color
                  temp_src_nbr.append( src_nbrs[src_nbr] )
                  temp_src_nbr.append( src_nbrs[ano_src_nbr] )
         
         if temp_src_nbr:
            src_nbr_same_clr.append( temp_src_nbr )
      


      # this is for getting src_nbr color from shape_nbr
      src_nbr_counter = 0
      for src_nbr in src_nbrs:
         src_nbr_rgb = shape_nbr["nbr_clrs"][src_nbr_counter]      
         
         src_nbr_counter += 1
        
         # initialize for current src_nbr

         # check if src_nbr and src_shapeid are already in the same rpt_ptn_shape
         skip = False
         if rpt_ptn_shapes:
            for rpt_ptn_shape in rpt_ptn_shapes:
               for src_id , rpt_ptn_neighbors in rpt_ptn_shape.items():
                  if ( src_nbr == src_id or src_nbr in rpt_ptn_neighbors ) and ( src_shapeid == src_id or src_shapeid in rpt_ptn_neighbors ):
                     skip = True
                     break
               if skip:
                  break
            if skip:
               continue

         cur_already_processed.append( src_nbr )
         process_neighbor(cur_already_processed, ( src_shapeid, src_shapeid_rgb ) , src_nbr , src_nbr_rgb ,  True )

         



      # at the end of src_neighbors. put cur_rpt_ptn into rpt_ptn_shapes
      # first put cur_rpt_ptn into all_cur_rpt_ptns
      # check if repeating pattern shape contains at least one nested neighbor
      if len( cur_rpt_ptn ) > 2:
         all_cur_rpt_ptns.append( cur_rpt_ptn )
     
      
      # check if current src_nbrs have same color
      if src_nbr_same_clr:
         
         # if one src_nbr has same color with multiple other src_nbrs. if so, put them together.
         grouped_by_same_clr_src_nbrs = {}
         
         already_done = []
         
         for same_clr_src_nbr_pair in src_nbr_same_clr:
            for same_clr_src_nbr_shapeid in same_clr_src_nbr_pair:
               
               first = True
               for ano_same_clr_src_nbr_pair in src_nbr_same_clr:
                  if same_clr_src_nbr_pair == ano_same_clr_src_nbr_pair:
                     # itself
                     continue
                  
                  if same_clr_src_nbr_shapeid in ano_same_clr_src_nbr_pair and same_clr_src_nbr_shapeid not in already_done:
                     
                     
                     # get another shapeid in the ano_same_clr_src_nbr_pair
                     cur_ano_same_clr_src_nbr1 = None
                     if same_clr_src_nbr_shapeid == ano_same_clr_src_nbr_pair[0]:
                        cur_ano_same_clr_src_nbr1 = ano_same_clr_src_nbr_pair[1]
                     else:
                        cur_ano_same_clr_src_nbr1 = ano_same_clr_src_nbr_pair[0]

                     # get another shapeid in the same_clr_src_nbr_pair only one time.
                     
                     if first:
                        cur_ano_same_clr_src_nbr2 = None
                        if same_clr_src_nbr_shapeid == same_clr_src_nbr_pair[0]:
                           cur_ano_same_clr_src_nbr2 = same_clr_src_nbr_pair[1]
                        else:
                           cur_ano_same_clr_src_nbr2 = same_clr_src_nbr_pair[0]
                        
                        grouped_by_same_clr_src_nbrs[same_clr_src_nbr_shapeid] = []
                        grouped_by_same_clr_src_nbrs[same_clr_src_nbr_shapeid].append( cur_ano_same_clr_src_nbr2 )
                           
                        first = False
                     
                     
                     grouped_by_same_clr_src_nbrs[same_clr_src_nbr_shapeid].append( cur_ano_same_clr_src_nbr1 )
                     
               
               # the end of current shapeid going through all other same color neighbor pairs
               already_done.append( same_clr_src_nbr_shapeid )
               
         
         # now we have grouped_by_same_clr_src_nbrs. the data inside it is like below
         # {'10': ['5', '1', '12', '13'], '5': ['10', '1'], '1': ['2', '3', '4', '5', '10']}
         # { group_src_nbr_shapeid: src_nbrs_in_group, group_src_nbr_shapeid: src_nbrs_in_group, .... }
         # 
         # list contains all groups of same color source neighbors. dictionary key in each group is a source neighbor.
         # this source neighbor has same color with all source neighbors in the list.
         
         # now we need to know if source neighbors in the list have same colors with each other. only source neighbors 
         # that have same colors are put together
         
         # 
         # cur_match_results contains match results for "current" all group_src_nbr_shapeids
         # so if we have grouped_by_same_clr_src_nbrs of the following
         # {'10': ['5', '1', '12', '13'], '5': ['10', '1'], '1': ['2', '3', '4', '5', '10']}
         # then the cur_match_results becomes like the following. the following is the 10 "group_src_nbr_shapeid" example.
         #
         # naming: ['5', '1', '12', '13'] is the subgroup of group_src_nbr_shapeid 10
         #
         # { 5: { 1: True, 12: False, 13: True }, 1: { 5: True, 12: False, 13: True }, 12: { 5: False, 1: False, 13: False }, 
         #       13: { 5: True, 1: True, 12: False } }
         
         
         for group_src_nbr_shapeid, src_nbrs_in_group in grouped_by_same_clr_src_nbrs.items():
            cur_unmatched = []
            cur_match_results = {}
            
            for cur_src_nbr_shapeid in src_nbrs_in_group:
               cur_match_results[cur_src_nbr_shapeid] = {}
               
               for ano_cur_src_nbr_shapeid in src_nbrs_in_group:
                  if cur_src_nbr_shapeid == ano_cur_src_nbr_shapeid:
                     continue
                     
                  # now that we have both cur_src_nbr_shapeid and  cur_src_nbr_shapeid, we need to get their colors to compare.
                  # their colors are in the src_nbrs
                  
                  cur_src_nbr_clr_index = src_nbrs.index( cur_src_nbr_shapeid )
                  
                  cur_ano_src_nbr_clr_index = src_nbrs.index( ano_cur_src_nbr_shapeid )
            
                  cur_src_nbr_clr = shape_nbr["nbr_clrs"][cur_src_nbr_clr_index]
                  cur_ano_src_nbr_clr = shape_nbr["nbr_clrs"][cur_ano_src_nbr_clr_index]
            
                  
                  clrch, brit_thres, brit_ch_v = pixel_functions.compute_appearance_difference(cur_src_nbr_clr, cur_ano_src_nbr_clr, 30)
            
                  if not clrch and brit_thres:
                     cur_match_results[cur_src_nbr_shapeid][ano_cur_src_nbr_shapeid] = True
                  else:
                     cur_match_results[cur_src_nbr_shapeid][ano_cur_src_nbr_shapeid] = False


            # finished current group_src_nbr_shapeid 
            
            matched_groups = group_by_same_color( cur_match_results )
            
            for matched_group in matched_groups:
               matched_group.append( group_src_nbr_shapeid )
         
         
            put_into_rpt_ptn_shapes( matched_groups, all_cur_rpt_ptns, rpt_ptn_shapes )


         if not grouped_by_same_clr_src_nbrs:
            put_into_rpt_ptn_shapes( src_nbr_same_clr, all_cur_rpt_ptns, rpt_ptn_shapes )



      for all_cur_rpt_ptn in all_cur_rpt_ptns:

         rpt_ptn_shapes.append( { all_cur_rpt_ptn[0]: all_cur_rpt_ptn } )
         
      
      all_shapes -= 1
      
      debug_counter -= 1
      
      
      if debug:
         sys.exit()
         
   if debug_counter < 0:
      break


            
rpt_ptn_file.write(str( rpt_ptn_shapes ) )
rpt_ptn_file.close()

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)



