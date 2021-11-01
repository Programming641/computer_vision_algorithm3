# computer_vision_algorithm3
finding shapes based on the appearance change. my first attempt to analyze pictures at low level


Please note that I am not using any conventional computer vision algorithm! algorithm are entirely created by me! The advantages of my algorithm are straightforward and intuitive, because for one, I am not using heavy mathmatics.

execute the following and see how it works for yourself!!!

Caution:
image format must NOT be JPG!!! JPG does not work! Use PNG instead.

Directory structure

For this to work, you need to have below directory structure
execution directory where you execute python script files. Let's call this "top directory"

top directory

|

->images

   |
   
   ->optional directory under images folder for organizing your image files

->shapes 

->libraries

you need to place "pixel_shapes_functions.py" under libraries directory


Instructions

First you need to execute "putting_pixels_into_color_groups revision 2.py"
make sure to provide filename and optional directory.


On windows:
py -3 "finding_shapes.py"

you need to change the following

image_filename

directory

directory is optional whether you have directory under image directory

provide image for image_filename

after executing the finding_shapes.py

"filename"_shapes.txt will be created under shapes folder

Then, you can execute "recreate_shapes.py" to see each one of shapes

To execute "recreate_shapes.py", you need to pass filename in the first parameter and optional image sub-directory in second parameter

python recreate_shapes.py filename (image sub-directory)

"get_boundary_pixels test.py"

First, you need to have already executed finding_shapes.py for the intented image.

you need to change filename and directory as before.

Also you will need shape id number in the below variable

pixel_ids_list = [shape id number ]

this shape id number is the one created by finding_shapes.py

Also below lines

b_filename = "20085"

b_directory = "boundary_test"

b_filename is the shape id number mentioned above

b_directory is optional but you will need to put shape id number's image for the below line

image_original = 'images/' + b_directory + b_filename + '.png'

image_original is the shape id number image that is created by "recreate_shapes.py"

below are some examples of "get_boundary_pixels test.py"

![20085](https://user-images.githubusercontent.com/56218301/139615314-d99024d5-5012-4f4c-8f78-f0e59a9e821b.png)
![20085_boundary](https://user-images.githubusercontent.com/56218301/139615338-52c6ee02-0e08-4a13-a9ae-3da5ac9d4eb9.png)
![27468](https://user-images.githubusercontent.com/56218301/139615346-e3b990c9-d424-48a4-b2f2-941b3c2cf118.png)
![27468_boundary](https://user-images.githubusercontent.com/56218301/139615354-be0a7369-2b85-4dad-8675-3fe047e41219.png)
![54720](https://user-images.githubusercontent.com/56218301/139615366-5b67a080-d7f5-4802-a1cb-04b10b4bf4b5.png)
![54720_boundary](https://user-images.githubusercontent.com/56218301/139615370-cbc099c6-9804-4a85-af05-5b38937c6917.png)



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
