import os

debug = False

os.chdir("C:/Users/Taichi/Documents/computer_vision")

proj_dir = os.getcwd()

if proj_dir != "" and proj_dir[-1] != "/":
   proj_dir +='/'

top_shapes_dir = proj_dir + "shapes/"
top_images_dir = proj_dir + "images/"
top_tools_dir = proj_dir + "tools/"
top_tests_dir = proj_dir + "tests/"
top_temp_dir = proj_dir + "temp/"

Lshape_size = 50
smallest_pixc = 4
sec_smallest_pixc = 7
third_smallest_pixc = 13
frth_smallest_pixc = 21


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
scnd_stg_all_files = "scnd_stage/acrs_all_files"

spixc_shapes = "spixc_shapes"

# internal small pixel count shapes
internal = "intnl"




















