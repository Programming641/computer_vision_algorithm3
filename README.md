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
- execute find_rpt_ptn_shapes.py
- execute recreate_rpt_ptn_shapes.py
- execute find_rpt_ptn_shapes2.py
- execute recreate_rpt_ptn_shapes.py

You need to provide image filename as needed. Please see above.

### Execution Results examples

Original Image

![dog](https://user-images.githubusercontent.com/56218301/146460923-3a92db6e-a0c4-4a37-9637-6d9e8f10ce13.png)
![dog_clr_grp](https://user-images.githubusercontent.com/56218301/146460935-5a73c5dc-e4ad-4dba-8fcd-fda84206c40e.png)

![147](https://user-images.githubusercontent.com/56218301/146707275-c8e7dd24-5f59-4081-8424-8f4b3476807c.png)
![967](https://user-images.githubusercontent.com/56218301/146707279-50fb2a3f-c73a-44e9-b6c5-60731787d791.png)
![2900](https://user-images.githubusercontent.com/56218301/146707291-b9e980d7-e9dc-4fbb-88c3-0aaef42593b7.png)
![17614](https://user-images.githubusercontent.com/56218301/146707296-104b82c9-f72c-40c8-95f3-b5cfce247c16.png)
![19007](https://user-images.githubusercontent.com/56218301/146707303-292ebefe-cd36-4478-b374-b6471f04066c.png)
![22122](https://user-images.githubusercontent.com/56218301/146707308-0fcde6e1-bc9e-49c9-b5a3-21ada745159b.png)
![28743](https://user-images.githubusercontent.com/56218301/146707313-2ec1e890-bfdd-4a3d-9f03-ecfac16e61da.png)
![30102](https://user-images.githubusercontent.com/56218301/146707319-a3f66c28-922e-4056-b30d-7574a1ccefef.png)
![31574](https://user-images.githubusercontent.com/56218301/146707326-dcaf50b3-2ce8-4bc1-91a4-8f8ac5b0ed8a.png)
![40259](https://user-images.githubusercontent.com/56218301/146707338-93959270-4066-492a-89d6-2a5f1410c7d5.png)
![42519](https://user-images.githubusercontent.com/56218301/146707345-e7b6ed36-fe80-4000-8f91-3cb65913898d.png)
![42723](https://user-images.githubusercontent.com/56218301/146707347-2e0e7a04-6308-459c-9860-39137f1bb9e7.png)
![49118](https://user-images.githubusercontent.com/56218301/146707364-b419c046-276c-41f2-ba31-a8ab47e4284d.png)
![59606](https://user-images.githubusercontent.com/56218301/146707375-57c60d6f-5e9c-46ab-81f6-6b03e582f37d.png)
![61860](https://user-images.githubusercontent.com/56218301/146707377-9e5efc12-56e6-4b74-ae07-ca02636f959c.png)
![65718](https://user-images.githubusercontent.com/56218301/146707380-f877bff5-ee68-4c71-8096-574218be7cbb.png)
![67142](https://user-images.githubusercontent.com/56218301/146707384-9302962f-d4d3-46b2-8b75-2a22e69dcb24.png)
![79569](https://user-images.githubusercontent.com/56218301/146707392-9e5008df-f35f-4888-8d5c-e5130e3dec6f.png)
![81829](https://user-images.githubusercontent.com/56218301/146707396-b4b429da-488b-4161-9bfa-abf780efb394.png)
![92730](https://user-images.githubusercontent.com/56218301/146707405-a206db5b-f3e0-4fc5-a8f3-2817cc14c3fd.png)
![92861](https://user-images.githubusercontent.com/56218301/146707411-457211a7-4f3e-48be-991c-714449add172.png)
![92875](https://user-images.githubusercontent.com/56218301/146707415-4874b31e-de04-479d-9f13-7ff2fa7c1549.png)
![94996](https://user-images.githubusercontent.com/56218301/146707428-48167560-dc5d-4cc3-900d-103eb4ad7454.png)
![97296](https://user-images.githubusercontent.com/56218301/146707431-fe1faf07-cd0f-4e55-ad41-8a13ad23975e.png)
![98430](https://user-images.githubusercontent.com/56218301/146707436-082ef351-1fe9-4219-b57b-dfedac8e5d89.png)
![99684](https://user-images.githubusercontent.com/56218301/146707449-985dd23a-20ad-4e05-b187-ed4b093c1dcb.png)
![100018](https://user-images.githubusercontent.com/56218301/146707451-9c7ca572-dbef-4a35-bb96-d2e91ad55fe9.png)
![104535](https://user-images.githubusercontent.com/56218301/146707463-cc83dca1-0ad7-44f2-af05-6ecd01558c1a.png)
![107972](https://user-images.githubusercontent.com/56218301/146707465-ba7358ef-d3de-47dd-b8a3-cb31c884eb48.png)
![108743](https://user-images.githubusercontent.com/56218301/146707468-c7590b69-b10d-424f-ac37-55f09d9e6696.png)
![110832](https://user-images.githubusercontent.com/56218301/146707471-a0ab7afa-6f7e-4879-8b28-3244d0ebf23b.png)
![134062](https://user-images.githubusercontent.com/56218301/146707482-1cf036d9-8e64-48ab-9b67-eab93ea344fc.png)





# Video Analysis






## Requirement

- You need frames from video

At least two consecutive frames are needed.

you can use **ffmpeg** to get frames from the video

example video

https://user-images.githubusercontent.com/56218301/140649130-48e34f72-b9c7-4533-877d-94d96134cf73.mp4

## pixel change analysis between video frames ( usually between two consecutive frames from the same video )

### running examples

original image1 original image2

![1_clrgrp](https://user-images.githubusercontent.com/56218301/160788385-38ca6232-4da6-4390-a812-61c8dbc96f2a.png)
![2_clrgrp](https://user-images.githubusercontent.com/56218301/160788396-436991c0-1027-4b96-b5ff-8caa668d86ce.png)


taking difference between frames above

![diff12result1](https://user-images.githubusercontent.com/56218301/160788480-e0ec30f6-fac7-48cf-8ade-0b31c67d3ceb.png)
![diff12result2](https://user-images.githubusercontent.com/56218301/160788496-14a8bf87-ec82-43b5-a10a-f59624693d61.png)


**another example**

![birdflying1](https://user-images.githubusercontent.com/56218301/160788687-bc9e5be6-d146-4b41-932e-8f806ca02b21.png)
![birdflying2](https://user-images.githubusercontent.com/56218301/160788722-189dac54-6aad-4a13-b6eb-4de6e64c210c.png)


![birdflying1_clr_grp](https://user-images.githubusercontent.com/56218301/160788748-39ab3395-6e28-4699-a339-334d8a3b713e.png)
![birdflying2_clr_grp](https://user-images.githubusercontent.com/56218301/160788759-69168a2e-35c2-4f19-bf27-61efc7558879.png)

![diff12result1](https://user-images.githubusercontent.com/56218301/160788785-b54ff963-6a0c-4b57-8a36-b090b3aa3dc8.png)
![diff12result2](https://user-images.githubusercontent.com/56218301/160788795-a4598c9d-78bb-4b55-930a-01fa6345f94d.png)






### instruction

1. execute putting_pixels_into_color_groups revision 2.py on *two consequtive* images/frames.
2. execute finding_shapes.py on both images/frames.
3. make sure to provide image and shape directory

execute findimage_pixelchange.py


execute process_pixch_btnframes.py

## matching algorithm between object( or named as "shape" in this program ) in image1 and object in image2

### instruction

Once you obtain the frames from video, you need to execute finding_shapes.py and so on the same as image analysis written above.

1. execute putting_pixels_into_color_groups revision 2.py on *two consequtive* images/frames.
2. execute finding_shapes.py on both images/frames.
3. execute recreate_shapes.py
this is option but I recommend to do it because you would not know if you get the right shape from both images/frames.
4. execute find_shapes_in_diff_frames test.py. you need to provide images/frames in this file.

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
