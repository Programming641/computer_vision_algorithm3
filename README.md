# computer_vision_algorithm3
finding shapes based on the appearance change. my first attempt to analyze pictures at low level

## Operating environment
Windows 10

Python 3

## Note

Please note that I am not using any conventional computer vision algorithm! algorithm are entirely created by me! The advantages of my algorithm are straightforward and intuitive, because for one, I am not using heavy mathmatics.

execute the following and see how it works for yourself!!!

**Caution:** image format must NOT be JPG!!! JPG does not work! Use PNG instead.

## Directory structure

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


### Instructions

- First you need to execute put_pixels_into_clr_grps.py

~~~
py put_pixels_into_clr_grps.py
~~~

You need to provide image filename as needed.

Then you need to execute

- py -3 "finding_shapes.py"

make sure to provide filename and optional directory.


after executing the finding_shapes.py

"filename"_shapes.txt will be created under shapes folder

- Then, you can execute "recreate_shapes.py" to see each one of shapes

To get boundaries of shape, 

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

original image and image transformed by put_pixels_into_clr_grps

![hanger001](https://user-images.githubusercontent.com/56218301/139683609-18d83a72-58f8-4523-9a86-84675c091327.png)
![hanger001_color_group](https://user-images.githubusercontent.com/56218301/139676481-55cbdf86-1da0-4f2a-a9c1-2ae5e604414a.png)

shapes created by "recreate_shapes.py" and boundary found by "get_boundary_pixels test.py"

![20085](https://user-images.githubusercontent.com/56218301/139615314-d99024d5-5012-4f4c-8f78-f0e59a9e821b.png)
![20085_boundary](https://user-images.githubusercontent.com/56218301/139615338-52c6ee02-0e08-4a13-a9ae-3da5ac9d4eb9.png)
![27468](https://user-images.githubusercontent.com/56218301/139615346-e3b990c9-d424-48a4-b2f2-941b3c2cf118.png)
![27468_boundary](https://user-images.githubusercontent.com/56218301/139615354-be0a7369-2b85-4dad-8675-3fe047e41219.png)
![54720](https://user-images.githubusercontent.com/56218301/139615366-5b67a080-d7f5-4802-a1cb-04b10b4bf4b5.png)
![54720_boundary](https://user-images.githubusercontent.com/56218301/139615370-cbc099c6-9804-4a85-af05-5b38937c6917.png)

## Repeating pattern shapes

### Instructions

- execute put_pixels_into_clr_grps.py
- excute finding_shapes.py
- execute create_shape_neighbors.py
- find_rpt_ptn_shapes.py

You need to provide image filename as needed. Please see above.

### Execution Results examples

Original Image

![20](https://user-images.githubusercontent.com/56218301/145937057-2122ff1a-ca4f-4121-9d9a-b5ae633c9d7c.png)

![19](https://user-images.githubusercontent.com/56218301/145936941-9a6cde30-385a-4768-be22-c2844c2d0604.png)

![1](https://user-images.githubusercontent.com/56218301/145936603-d87c5d0d-517e-448d-89ff-b3b22f1c3849.png)
![2](https://user-images.githubusercontent.com/56218301/145936605-ebc618c8-858b-4a77-8a47-765162ea6f86.png)
![3](https://user-images.githubusercontent.com/56218301/145936609-7292502c-1656-4974-a029-7c446167ae8b.png)
![4](https://user-images.githubusercontent.com/56218301/145936612-81862262-276a-43a5-9de8-6c64b5cd6dd7.png)
![5](https://user-images.githubusercontent.com/56218301/145936617-8fb52f4b-98f5-4361-92ec-c0dd52b0688c.png)
![6](https://user-images.githubusercontent.com/56218301/145936625-238e16eb-798d-47a7-9799-b6fe58eba6c5.png)
![7](https://user-images.githubusercontent.com/56218301/145936630-481b242c-0a2a-4a48-8cd6-81bcb83dcd83.png)
![8](https://user-images.githubusercontent.com/56218301/145936633-eea1d90e-a9e8-443f-87fb-6935f9a5ce83.png)
![9](https://user-images.githubusercontent.com/56218301/145936636-b31578c8-ec82-4cb5-bbd4-9022a6da2c8c.png)
![10](https://user-images.githubusercontent.com/56218301/145936643-cb55d3a0-92ac-46bb-bebc-bd0ff2c42cf3.png)
![11](https://user-images.githubusercontent.com/56218301/145936650-83ede96b-87dd-415f-8f2a-290dcbc0f420.png)
![12](https://user-images.githubusercontent.com/56218301/145936659-8a1419be-8dcb-4cb1-b7f0-b0cdf6976c85.png)
![13](https://user-images.githubusercontent.com/56218301/145936661-8cb4e370-0ea1-41ce-b942-e285c1b1879f.png)
![14](https://user-images.githubusercontent.com/56218301/145936731-287bc03a-9fc7-4298-8955-9d2b6e8de8e0.png)
![15](https://user-images.githubusercontent.com/56218301/145936674-cf2497a9-0ccc-4c1f-a4bc-24ddd9becc66.png)
![16](https://user-images.githubusercontent.com/56218301/145936677-31d9f8b6-8a37-4be0-8af8-71f7ecbbb7b0.png)
![17](https://user-images.githubusercontent.com/56218301/145936680-7ab11f28-f9db-4b18-ab0a-700e27130d89.png)
![18](https://user-images.githubusercontent.com/56218301/145936689-e10500bd-75ac-4c76-a29d-8405beeaa4aa.png)

#### another example
![dog](https://user-images.githubusercontent.com/56218301/146460923-3a92db6e-a0c4-4a37-9637-6d9e8f10ce13.png)
![dog_clr_grp](https://user-images.githubusercontent.com/56218301/146460935-5a73c5dc-e4ad-4dba-8fcd-fda84206c40e.png)
![9777](https://user-images.githubusercontent.com/56218301/146460970-13b3473c-6c22-465c-9b94-e8c439e8c93c.png)
![31794](https://user-images.githubusercontent.com/56218301/146460988-8813e7b6-b353-4d3c-9c81-0700f2250cc9.png)
![42176](https://user-images.githubusercontent.com/56218301/146460994-5329e685-670e-4f3c-92cd-73368f371c77.png)
![42366](https://user-images.githubusercontent.com/56218301/146460996-24d933c7-4232-4d7c-9d43-89c2459d5d52.png)
![46862](https://user-images.githubusercontent.com/56218301/146461007-e326afa7-d9f5-4e2a-934c-3f3ce7f3f9e8.png)
![51938](https://user-images.githubusercontent.com/56218301/146461016-6bede500-6a40-49fc-9779-58f4b44ee18f.png)
![59761](https://user-images.githubusercontent.com/56218301/146461026-d8fb686c-5317-4f1d-a91c-94913dbac784.png)
![59974](https://user-images.githubusercontent.com/56218301/146461036-7b2d3075-ded5-4110-88b0-0d2b4b64e808.png)
![72959](https://user-images.githubusercontent.com/56218301/146461047-d05cd440-0bff-41db-84e9-d5d00ea4ee4c.png)
![86080](https://user-images.githubusercontent.com/56218301/146461064-2110e9a1-d097-492b-8459-f2a7d8a31c94.png)
![90514](https://user-images.githubusercontent.com/56218301/146461085-f4914fed-b09e-45bb-bfc0-503f663d465c.png)
![96921](https://user-images.githubusercontent.com/56218301/146461091-9a65f5f5-feef-4b3e-80c4-ece72cb4d832.png)
![96951](https://user-images.githubusercontent.com/56218301/146461100-1521def3-cc44-42ca-90b7-c7fdf30af9d2.png)
![97230](https://user-images.githubusercontent.com/56218301/146461109-ec8812e5-ea6d-463e-a30c-7cd5466e2736.png)
![99927](https://user-images.githubusercontent.com/56218301/146461118-fb644fbd-81bf-4950-8bca-8f8ac5f7715e.png)
![103690](https://user-images.githubusercontent.com/56218301/146461127-d94c4083-cb7c-4a50-92f8-2cfe491342e9.png)
![115319](https://user-images.githubusercontent.com/56218301/146461138-34a0147b-adfe-4caa-8a74-af0a70abc067.png)
![119071](https://user-images.githubusercontent.com/56218301/146461145-cb8b7c95-1ebd-46a6-b551-f00a7251a0e9.png)
![119649](https://user-images.githubusercontent.com/56218301/146461158-ad39c932-d664-4685-bfc6-91b04fa5fd60.png)
![128651](https://user-images.githubusercontent.com/56218301/146461183-6a96a8f9-87da-49d9-a45d-46ace7685029.png)
![142359](https://user-images.githubusercontent.com/56218301/146461192-0c0a3bf5-ab93-46f3-8870-b5f53b0c5f61.png)
![143929](https://user-images.githubusercontent.com/56218301/146461198-5630c39f-e939-48c0-8fe0-d317f23bc9db.png)



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


## Note
Still needs improvements but it works acceptably for now.

## Limitting search to reduce wait time dramatically
It takes quite a long time! on intel i7? computer, it took about 30-40mins. You can limit the search by doing below.

**Search for a shape in interest.**

![無題](https://user-images.githubusercontent.com/56218301/144179394-297b1930-7c0d-4367-9847-14e5bcdf8b99.png)


**put if statement like below to limit search for a shape chosen above.**

find_shapes_in_diff_frames.py

![無題](https://user-images.githubusercontent.com/56218301/145309985-9bc2a74b-7203-4ad3-9446-93198aeac163.png)



## Debugging

You can see where the matches are made in the shape image like below. Below image is for the matching by virtical boundary processing.

To enable debugging, change the debug flag to true

![無題](https://user-images.githubusercontent.com/56218301/145309175-fa9ec43f-2639-4027-aafd-2704f593a3fd.png)

![無題](https://user-images.githubusercontent.com/56218301/145309302-64928a71-5753-44d3-9502-9b64f273fc93.png)

You can see where the matches are made are highlighted

It shows the function and original shape id and compare shape id numbers

![無題](https://user-images.githubusercontent.com/56218301/145309587-e4b30d10-1436-429f-a3de-66fcf1186cd3.png)


## Execution results

two frames

![hanger005_color_group](https://user-images.githubusercontent.com/56218301/145309728-8df4d433-c99d-4b71-a8e6-d8546d290166.png)
![hanger006_color_group](https://user-images.githubusercontent.com/56218301/145309737-f8a858b1-6aa7-46eb-ac3a-8764e77317cc.png)


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


# Warnings

Some of the python scripts take quite a long time to execute! On my i7 computer, create_shape_neighbors.py took about 30-40 min.


This is still in progress. So what you read here may be outdated and not relevant anymore. I try to update when I find deprecated stuff.

# Future plans

If you have executed some of the scripts here, you notice that it takes awful lot of time to process. So my future plan is to change my code to numpy. and then possibly to gpu.

- convert existing code to numpy.
- possibly incorporate GPU.
