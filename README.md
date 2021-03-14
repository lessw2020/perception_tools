# perception_tools
additional utils for working with Unity perception package, which generates synthetic images for AI training.

 
First up - perception to coco converter for 2D bounding boxes.

Perception outputs all the data in their own format, 
but for most object detection, coco format is the default bounding box annotation format.
</b>
## Usage:
provide the path to the perception dir, and a name for the output coco file.

A ready to use/train with coco file is created, in the dataset directory.

![convert_perception](https://user-images.githubusercontent.com/46302957/111054947-9138b080-8425-11eb-88e5-ced6d082de38.JPG)



