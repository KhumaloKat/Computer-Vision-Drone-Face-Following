***Face following***

## FEATURES

-Sending remote controls to the Tello drone without the use of any controller.

-Using a face-tracking module to control the Tello drone.

## INSTALLATION:

***IDE***

-Pycharm Community Edition.

***Packages installed***

-Mediapipe.

-cvzone library.-version 1.5.6

-Opencv-python.

-Tellopy.

-Pillow.

***Components***

-DJI Tello drone

***HOW IT WORKS***

- Firstly, by using the tellopy library you can enable the drone and send the remote controls to it by connecting your WLAN to the DJI Tello drone.
- Important functions that should be enabled on the Tello drone are the stream functions, which enable you to use the live feed camera on the Tello for face detection using media-pipe and reading all the components needed for the implementation of this project which are the Z value, X value, and Y.
- The drone detects the face and creates a box that covers all the features that identify as face features(*in simple terms*) and sets the middle of your face as the midpoint in this case your nose.
- For the X value, it detects the change that happens horizontally
- Y value detects the changes that happen vertically
- Z value you set a distance between you and the drone that needs to be maintained and any changes happening are also detected
- All those changes are recorded by the Compiler and using the PID function from the cvzone library, they are converted to speed, and it is inverted so the drone moves towards the center of the face again or to its initial point.
  


