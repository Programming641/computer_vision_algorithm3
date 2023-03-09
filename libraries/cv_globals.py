import os

debug = False

os.chdir("C:/Users/Taichi/Documents/computer_vision")

proj_dir = os.getcwd()

if proj_dir != "" and proj_dir[-1] != "/":
   proj_dir +='/'

top_shapes_dir = proj_dir + "shapes/"
top_images_dir = proj_dir + "images/"
top_tools_dir = proj_dir + "tools/"

