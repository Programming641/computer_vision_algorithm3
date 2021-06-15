# computer_vision_algorithm3
finding shapes based on the appearance change. my first attempt to analyze pictures at low level


Please note that I am not using any conventional computer vision algorithm! algorithm are entirely created by me! The advantages of my algorithm are straightforward and intuitive, because for one, I am not using heavy mathmatics.


Instructions

image format must NOT be JPG!!! JPG does not work! Use PNG instead.

execute the following and see how it works for yourself!!!

On windows:
py -3 "finding_shapes3 dbg.py"

py -3 recreate_shapes.py

On linux:

python3 "finding_shapes3 dbg.py"

python3 recreate_shapes.py



Error handling

if you see error with alpha something something, then you need to add or delete alpha

either

   original_red, original_green, original_blue = current_pix

   compare_red, compare_green, compare_blue = compare_pixel
   
or

   original_red, original_green, original_blue, alpha = current_pix

   compare_red, compare_green, compare_blue, alpha = compare_pixel
   
this works



This is still in progress. I'm going to fix some minor bugs when I get time
