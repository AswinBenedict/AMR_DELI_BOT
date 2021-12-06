# AMR_DELI_BOT
- Go to the src of your workspace
```
cd catkin_ws/src
```
- create a package say 'apf'
```
catkin_create_pkg apf rospy geometry_msgs sensor_msgs nav_msgs
```
- create a folder scripts
```
mkdir scripts && cd scripts
```
- paste the virtual_obstacle file then make it into a executable
```
chmod +x virtual_obstacle.py
```
- Mention it in the CMakelists file 
----------------------------------------------------------------------------------

### Sensors Used
- Laser
  - For finding distances to obstacles
- Odometry
  - It will have the position and orientation, we will use the position of the bot for the attractive forces
