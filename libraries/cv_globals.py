import os

debug = False

os.chdir("./")

proj_dir = os.getcwd()

if proj_dir != "" and proj_dir[-1] != "/":
   proj_dir +='/'

top_shapes_dir = proj_dir + "shapes/"
top_images_dir = proj_dir + "images/"
top_tools_dir = proj_dir + "tools/"
top_tests_dir = proj_dir + "tests/"
top_temp_dir = proj_dir + "temp/"


# folder names
top_pixch_dir = "pixch/"
pixch_sty_dir = top_pixch_dir + "sty_shapes"

# staying large shapes
styLshapes = "styLshapes"
styLshapes_w_nbrs = "styLshp_w_nbrs"
styLshapes_wo_pixch = "styLshp_wo_pixch"
shp_nbrs = "shp_nbrs"
pixch_bnd_dir = "pixch_bnd"
scnd_stage_alg_dir = "scnd_stage"
snd_stg_alg_shp_nbrs_dir = scnd_stage_alg_dir + "/shape_nbrs_matches"
only_nfnd_pixch_sty_dir = "only_nfnd_pixch_sty"
scnd_stg_all_files = scnd_stage_alg_dir + "/acrs_all_files"

scnd_stg_spixc_dir = scnd_stage_alg_dir + "/spixc"

scnd_stg_ch_btwn_frames_dir = scnd_stage_alg_dir + "/ch_btwn_frames"

spixc_shapes = "spixc_shapes"

# internal small pixel count shapes
internal = "intnl"


def get_smallest_pixc( im_size ):
   smallest_pixc = ( im_size[0] * im_size[1] ) / 20000
   return smallest_pixc

def get_sec_smallest_pixc( im_size ):
   sec_smallest_pixc = ( im_size[0] * im_size[1] ) / 11428
   return sec_smallest_pixc

def get_third_smallest_pixc( im_size ):
   third_smallest_pixc = ( im_size[0] * im_size[1] ) / 6154
   return third_smallest_pixc

def get_frth_smallest_pixc( im_size ):
   frth_smallest_pixc = ( im_size[0] * im_size[1] ) / 3809
   return frth_smallest_pixc

def get_fifth_s_pixc( im_size ):
   fifth_s_pixc = ( im_size[0] * im_size[1] ) / 2857
   return fifth_s_pixc

def get_6th_s_pixc( im_size ):
   sixth_s_pixc = ( im_size[0] * im_size[1] ) / 2424
   return sixth_s_pixc

def get_svnth_pixch( im_size ):
   svnth_s_pixc = ( im_size[0] * im_size[1] ) / 1951
   return svnth_s_pixc

def get_Lshape_size( im_size ):
   Lshape_size = ( im_size[0] * im_size[1] ) / 1600
   return Lshape_size

def get_indpnt_shape_size( im_size ):
   # independent shape size
   indpnt_shape_size = ( im_size[0] * im_size[1] ) / 1230
   return indpnt_shape_size

def get_default_color_threshold():
   return 30

def get_smallest_mv_threshold( im_size ):
   smallest_mv_threshold = ( im_size[0] * im_size[1] ) / 40000
   return smallest_mv_threshold



















