# computer_vision_algorithm3
finding shapes based on the appearance change. my first attempt to analyze pictures at low level


Please note that I am not using any conventional computer vision algorithm! algorithm are entirely created by me! The advantages of my algorithm are straightforward and intuitive, because for one, I am not using heavy mathmatics.

execute the following and see how it works for yourself!!!

**Caution:** image format must NOT be JPG!!! JPG does not work! Use PNG instead.

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

you can use **ffmpeg** to get frames from the video

- things in the video needs to be non-moving, only one moving is the camera.

example video

https://user-images.githubusercontent.com/56218301/140649130-48e34f72-b9c7-4533-877d-94d96134cf73.mp4

in this example, camera is the only moving and things in the video are non-moving.

# Instruction

### Instructional requirement

- you need to place read_files_functions.py under libraries directory

Once you obtain the frames from video, you need to execute finding_shapes.py and so on the same as image analysis written above.

1. execute putting_pixels_into_color_groups revision 2.py on *two consequtive* images/frames.
2. execute finding_shapes.py on both images/frames.
3. execute recreate_shapes.py
this is option but I recommend to do it because you would not know if you get the right shape from both images/frames.
4. execute find_shapes_in_diff_frames test.py. you need to provide images/frames in this file.

After executing this file, you will know which shape in one image is the which in another image.

**cautions:** turning movement is not supported.


## Note
Still needs improvements but it works acceptably for now.

## Warning
It takes quite a long time! on intel i7? computer, it took about 30-40mins. You can limit the search by doing below.

**Search for a shape in interest.**

![無題](https://user-images.githubusercontent.com/56218301/144179394-297b1930-7c0d-4367-9847-14e5bcdf8b99.png)


**put if statement like below to limit search for a shape chosen above.**

find_shapes_in_diff_frames.py

![無題](https://user-images.githubusercontent.com/56218301/144179233-fd3c1869-ad0c-4575-8550-88a5000eb1f8.png)

## Debugging

You can see where the matches are made in the shape image like below. Below image is for the matching by virtical boundary processing.

![orig 26720 compare 38838](https://user-images.githubusercontent.com/56218301/144517167-f6b7be85-f5c4-47f9-bc87-a3a62e761607.png)

![original 26720 comp 38838](https://user-images.githubusercontent.com/56218301/144517171-4afb900d-bf72-4fce-aaa7-5f7637a9c3db.png)


The code below is the debugging function inside virtical boundary processing. you can enable or disable by commenting out ***pixel_shapes_functions.highlight_matches***. 
**right now it is supported for virtical boundary processing only**

![無題](https://user-images.githubusercontent.com/56218301/144517134-8e7a139a-8041-4028-958d-de799f7dc5ec.png)


## Execution results

two frames

![hanger002_color_group](https://user-images.githubusercontent.com/56218301/140649783-0c68763d-ca29-489e-8374-ee01affe39f9.png)
![hanger003_color_group](https://user-images.githubusercontent.com/56218301/143502379-cae8e4d2-4327-4582-93f9-b1b1312207f3.png)


if you wait until the end of the processing, matched pairs will be displayed like below.


![1](https://user-images.githubusercontent.com/56218301/145308237-46d4979f-55a3-4683-8b9e-ef5414c46ce1.png)
![2](https://user-images.githubusercontent.com/56218301/145308240-05e53c6b-2c2b-4d0a-8840-d108b1a25de8.png)
![3](https://user-images.githubusercontent.com/56218301/145308246-f450a961-c98c-4dbd-a04d-1a099f3410af.png)
![4](https://user-images.githubusercontent.com/56218301/145308252-f3b50532-364e-4381-8ffe-dfce65327fb3.png)
![5](https://user-images.githubusercontent.com/56218301/145308254-d644115a-8799-4f66-bfe2-faaf2767da37.png)
![6](https://user-images.githubusercontent.com/56218301/145308800-8cd0032e-ae36-4cf8-8696-fc40e4ddf7a0.png)
![7](https://user-images.githubusercontent.com/56218301/145308262-7353629f-a800-49f9-908e-0058414f3bfe.png)
![8](https://user-images.githubusercontent.com/56218301/145308267-6a2e010a-0da8-45d8-8440-5b59e88fed84.png)
![9](https://user-images.githubusercontent.com/56218301/145308280-62bfdd08-b007-460e-a529-bd9f90da1913.png)
![10](https://user-images.githubusercontent.com/56218301/145308287-4ee70d3a-a39e-4884-9629-57fc3e2040d8.png)
![11](https://user-images.githubusercontent.com/56218301/145308291-836fffa4-9d6b-477d-a1cd-d0db0b6f9406.png)
![12](https://user-images.githubusercontent.com/56218301/145308295-ab01943b-09d0-455d-9500-eaf8ea54993a.png)
![13](https://user-images.githubusercontent.com/56218301/145308309-57ec36ed-ba69-4f15-9003-ee53c0af6eec.png)
![14](https://user-images.githubusercontent.com/56218301/145308313-63ef420d-2438-4521-baa9-af0106489066.png)
![15](https://user-images.githubusercontent.com/56218301/145308318-6b7a7f19-4f55-4945-9696-9c7a3eb9095b.png)
![16](https://user-images.githubusercontent.com/56218301/145308836-2d81a571-a339-43da-95c1-92631a8228c4.png)
![17](https://user-images.githubusercontent.com/56218301/145308841-1c4ef438-b475-405d-92d4-dfd806ced19d.png)
![18](https://user-images.githubusercontent.com/56218301/145308335-36843365-7ae6-4c19-bd45-939d19822e79.png)
![19](https://user-images.githubusercontent.com/56218301/145308342-b321fed4-db0b-4a39-be7a-28f9c22c72e2.png)
![20](https://user-images.githubusercontent.com/56218301/145308350-78dc8550-3a2e-4cff-81ce-c046fdc5cb5b.png)
![21](https://user-images.githubusercontent.com/56218301/145308354-66161399-e633-49de-bfa4-8741d2a042ae.png)
![22](https://user-images.githubusercontent.com/56218301/145308358-67dbfa60-b45b-46da-a262-bb4b16522fd5.png)
![23](https://user-images.githubusercontent.com/56218301/145308360-9b028d22-97ae-4a81-be01-6843b8c7f20a.png)

the pair 4 38533. the pair 725 49680 are displayed by bug which I think I fixed now.



This is still in progress. I'm going to improve when I get time.
