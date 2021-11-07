# computer_vision_algorithm3
finding shapes based on the appearance change. my first attempt to analyze pictures at low level


Please note that I am not using any conventional computer vision algorithm! algorithm are entirely created by me! The advantages of my algorithm are straightforward and intuitive, because for one, I am not using heavy mathmatics.

execute the following and see how it works for yourself!!!

*Caution:*
image format must NOT be JPG!!! JPG does not work! Use PNG instead.

# Directory structure

For this to work, you need to have below directory structure.

execution directory is where you execute python script files. Let's call this "top directory"
~~~
top directory
|
->images
       |
       ->optional directory under images folder for organizing your image files
       
->shapes 

->libraries
~~~
you need to place "pixel_shapes_functions.py" under libraries directory


## Instructions

First you need to execute "putting_pixels_into_color_groups revision 2.py"

you need to change the following

image_filename

directory

directory is optional whether you have directory under image directory

provide image for image_filename

Then you need to execute

py -3 "finding_shapes.py"

make sure to provide filename and optional directory.


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

original image and image transformed by "putting_pixels_into_color_groups revision 2.py"

![hanger001](https://user-images.githubusercontent.com/56218301/139683609-18d83a72-58f8-4523-9a86-84675c091327.png)
![hanger001_color_group](https://user-images.githubusercontent.com/56218301/139676481-55cbdf86-1da0-4f2a-a9c1-2ae5e604414a.png)

shapes created by "recreate_shapes.py" and boundary found by "get_boundary_pixels test.py"

![20085](https://user-images.githubusercontent.com/56218301/139615314-d99024d5-5012-4f4c-8f78-f0e59a9e821b.png)
![20085_boundary](https://user-images.githubusercontent.com/56218301/139615338-52c6ee02-0e08-4a13-a9ae-3da5ac9d4eb9.png)
![27468](https://user-images.githubusercontent.com/56218301/139615346-e3b990c9-d424-48a4-b2f2-941b3c2cf118.png)
![27468_boundary](https://user-images.githubusercontent.com/56218301/139615354-be0a7369-2b85-4dad-8675-3fe047e41219.png)
![54720](https://user-images.githubusercontent.com/56218301/139615366-5b67a080-d7f5-4802-a1cb-04b10b4bf4b5.png)
![54720_boundary](https://user-images.githubusercontent.com/56218301/139615370-cbc099c6-9804-4a85-af05-5b38937c6917.png)



## Error handling

if you see error with alpha something something, then you need to add or delete alpha

either

   original_red, original_green, original_blue = current_pix

   compare_red, compare_green, compare_blue = compare_pixel
   
or

   original_red, original_green, original_blue, alpha = current_pix

   compare_red, compare_green, compare_blue, alpha = compare_pixel
   
this works


# Video Analysis

## Requirement

- You need frames from video
At least two consecutive frames are needed.

you can use ffmpeg to get frames from the video

- things in the video needs to be non-moving, only one is moving is the camera.
example video

https://user-images.githubusercontent.com/56218301/140649130-48e34f72-b9c7-4533-877d-94d96134cf73.mp4

in this example, camera is the only moving and things in the video are non-moving.

# Instruction

### Instruction requirement

- you need to place read_files_functions.py under libraries directory

Once you obtain the frames from video, you need to execute finding_shapes.py and so on the same as image analysis written above.

1. execute putting_pixels_into_color_groups revision 2.py on *two consequtive* images/frames.
2. execute finding_shapes.py on both images/frames.
3. (optionally) execute recreate_shapes.py
this is option but I recommend to do it because you would not know if you get the right shape from both images/frames.
4. execute find_shapes_in_diff_frames test.py
you need to provide images/frames in this file.

After executin this file, you will know which shape in one image is the which in another image.

## Note
I only implemented the very simple algorithm for start. It looks for consecutive matches but it works really good for this algorithm. Details of algorithm are in the commands in the code. I am planning to add more algorithms to find shapes in the video.

## Sample

two frames
![hanger001_color_group](https://user-images.githubusercontent.com/56218301/140649774-7cef131e-44b2-448c-9045-7a3deb07918d.png)

![hanger002_color_group](https://user-images.githubusercontent.com/56218301/140649783-0c68763d-ca29-489e-8374-ee01affe39f9.png)

found shapes

![9633](https://user-images.githubusercontent.com/56218301/140649862-0ddfba16-7ff2-461b-96c0-569cd6ef45d7.png)
![9097](https://user-images.githubusercontent.com/56218301/140649873-9f9eb855-8514-41c9-bbbd-ff588e13c4fe.png)

![12657](https://user-images.githubusercontent.com/56218301/140649910-d04888c0-613b-4098-ab4b-587b6dc525ed.png)
![13916](https://user-images.githubusercontent.com/56218301/140649923-1d03cf5e-4cec-4710-a64c-7ab2e6d23029.png)

![19536](https://user-images.githubusercontent.com/56218301/140650139-1bc8fc49-65fd-4e7c-8846-cf202bd784f0.png)
![19536](https://user-images.githubusercontent.com/56218301/140650143-5bdcf775-fd53-4b82-ac6f-50198585ecea.png)

![20085](https://user-images.githubusercontent.com/56218301/140650212-9f3f22d3-f576-403f-8f1e-37abb1705c05.png)
![19725](https://user-images.githubusercontent.com/56218301/140650224-fcceea17-69ff-430a-b1d3-0ff48797a9b1.png)



This is still in progress. I'm going to improve when I get time.
