# Yolov4 with BITVehicle_Dataset example
**A full example of how to use yolov4 to train a module to recognize vehicles in given images**

**1) Download the [dataset](https://drive.google.com/file/d/1suu7qXFQVPYL4hPOX_fbqSn35VQI2iH2/view?usp=sharing)**  
**1.1) Put run.py and the extracted file you downloaded in the same folder**  
**1.2) Create dataset empty folder and move all the images to it (Dont put the readme.txt file in here it should only contain the images)**  
**1.3) Create test and train empty folders inside BITVehicle_Dataset**  
**1.3.1) Your BITVehicle_Dataset folder should look like [this]** (https://photos.app.goo.gl/HAvRtUWQVJyPax899)  
**1.4) Open run.py and install required libraries then change the pathes in code according to your folder directory**  
**1.5) run the code and wait untill it finishes**  
  
Now you should have a train and test folders full of images and txt files those will be your train and test datasets in yolov4

## Now lets get into yolov4

**2)clone [yolov4](https://github.com/AlexeyAB/darknet#yolo-v4-and-yolo-v3v2-for-windows-and-linux) into your desired directory**  
In this tutorial we will be building darknet in windows (for building on linux please refer to [AlexeyAB](https://github.com/AlexeyAB/darknet#yolo-v4-and-yolo-v3v2-for-windows-and-linux) steps for linux installation)

### Requirements

**1) CUDA 10.0: https://developer.nvidia.com/cuda-toolkit-archive (please note that you will need to download version 10.0 specifically for this to work**  
**2) OpenCV >= 2.4** : [Download OpenCv](https://opencv.org/releases/)  
**2.1) After downloading and installing opencv from your start menu type "edit the system enviroment variables" and go to enviroment variables then set system variable OpenCV_DIR = C:\opencv\build - where are the include and x64 folders** [image](https://user-images.githubusercontent.com/4096485/53249516-5130f480-36c9-11e9-8238-a6e82e48c6f2.png)  
**3) cuDNN : https://developer.nvidia.com/rdp/cudnn-archive (please download the version that applies to CUDA 10.0)**  
**3.1) Apply steps described here -> https://docs.nvidia.com/deeplearning/sdk/cudnn-install/index.html#installwindows**  
**4) Make sure your GPU has CC >=3.0 support **[GPU with CC](https://en.wikipedia.org/wiki/CUDA#GPUs_supported)

##### Okey now that we have all the required software we can build darknet to start training our dataset  
Open windows powershell and navigate (using the cd command) to your darknet directory that you cloned then type ./build.sp1 (note that this command will not work on cmd) this will take a while 

#### now lets prepare our data for training  

**1) We are going to be using yolov4 in this tutorial so we will use pre trained yolov4 conv weights [download this](https://drive.google.com/open?id=1JKF-bdIklxOOVy-2Cr5qdvjgGpmGfcbp) after downloading move this file to the darknet directory**
**2) Go to darknet/cfg and copy and paste yolov4-custom.cfg and change its name to yolov4-vehicle.cfg**  
**2.1) Open yolov4-vehicle.cfg in a text editor like notepad++ or atom and start editing according to the next steps**  
  2.1.1) Change line batch to batch=64  
  2.1.2) Change line subdivisions to subdivisions=16  
  2.1.3) Change line max_batches to (number of classes*2000) in our case this is 12000 because we have 6 classes in this training set (note that this number should not be less than the training set images and not less that 6000)  
  2.1.4) Change line steps to 80% and 90% of max_batches (in our case this would be 9600,10800)  
  2.1.5) Set network size to width=416 and height=416 (you can increase this by the multiplies of 32 if you have a decent GPU)  
  2.1.6) Change line classes=80 to your number of objects in each of 3 yolo-layers(note that there are 3 places where the value classes needs to be changed/after every [yolo],in our case this value should be 6 because we have 6 classes)  
  2.1.7) Change [filters=255] to filters=(classes + 5)x3 in the 3 [convolutional] before each [yolo] layer, keep in mind that it only has to be the last [convolutional] before each of the [yolo] layers.(againg there are 3 places where filters should be changed before each [yolo] in the [convolutional] area,in this example this value is (6+5)*3 = 33)  
  ###### Notes:if you get the error out of memory you can try lowering the batch size from 64 to 32,16 or 8 and/or you can increase the subdivions size to 32 or more,if you want to increase Precision you can increase the size of the network by increasing the width,height and increasing the batch and subdivision counts
  **3) Now we need to create vehicle.names and vehicle.data files lets start with vehicle.names**
    3.1) Go to Darknet/data and create a new file named vehicle.names then open it with your text editor then type the classes names (every class in a diffrent line it should look contain this:  
Bus  
Microbus  
Minivan  
Sedan  
SUV  
Truck  
)  
  3.2)now lets create vehicle.data and edit it with your text editor to look like [this](https://photos.app.goo.gl/yn3gWrJpWVU92uGZ6)  
  as you can see in this image we are missing a /backup folder so lets create it in the darknet directory (go to darknet directory and create new empty folder called backup)  
**4) Now we need to move our train and test sets to the darknet/data directory**  
  4.1) First take train.txt,text.txt,test folder,train folder and move them to Darknet/data directory.  
  4.2) The code above creates a train.txt file with all training images pathes **relative** to Darknet directory example->data/vehicle/image_name.jpg so we need to change the train folder name to vehicle (or you can open the train.txt file in notepad++ and edit all lines from data/vehicle/image_name to data/train/image_name you can use alt to edit multiple lines)  
  4.3) If you open test.txt you can see that it has all the test images pathes again **relative** to Darknet directory and it has it in data/test/image_name.jpg format so we dont need to change anything in here  
  #### Now we are ready to start training our module  
  Open cmd from start menu and navigate ( using the cd command ) to the darknet directory and then run the following command:  
  **darknet.exe detector train data/obj.data cfg/yolov4-vehicle.cfg yolov4.conv.137**  
  If you get a could not load error for any of the above change the path according to the error, this command should start the training of your module you will get a new window with a graph and a panel that contains the loss value,number of iterations and the max batch the program will keep running until number o iterations = max_batches  
  #### When should you stop training  
  A good time to stop is when the loss function stops decreasing the program saves a yolov4-vehicle_last.weights every 100 iterations in the backup folder and a yolov4-vehicle_xxxx.weights every 1000 iterations, you can use this files to continue the training by runing the command again but changing **yolov4.conv.137** to **backup/yolov4-vehicle_last.weights or backup/yolov4-vehicle_xxxx.weights**  
  #### Testing our module
  To test our module we run the following command in cmd (in the Darknet directory):
  **darknet.exe detector map data/vehicle.data cfg/yolov4-vehicle.cfg backup/yolov4-vehicle_xxxx.weights**  
  this command maps the results and shows percentages of predictions of every class after 100 iterations (if you use the backup/yolov4-vehicle_last.weights) in the command above you will see that we get low percentage results but if you use the backup/yolov4-vehicle_xxxx.weights if xxxx is 2000 for example those percentage values will rocket up to 85-95%  
  #### Testing with other images  
  If you want to try your own images you might move the image you want to the module to predict to the darknet/data directory then you can run the command below 
  **darknet.exe detector test data/vehicle.data cfg/yolov4-vehicle.cfg backup/yolov4-vehicle_xxxx.weights**  
  After running this command it will ask for your image path if you have your image in the Darknet/data directory you can type data/image_name (with image extension)  
  This will run the module prediction on your image and then will open the image showing you the result.
  
   
