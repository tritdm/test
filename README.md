# 3D position calculation and visualization
## Install prerequisite packets
>pip install -r requirements.txt
## Formula used
In the first reference, there is a formula to find x-axis of 2 intersection spheres have same y-axis and z-axis

Depend on the above formula, we can use a points as origin and 3 points on 3 axis, then we can use origin and 1 in 3 of them to find the corresponding axis
## Operation
### Test mode
Config TEST_MODE to True

Config data in data.txt as format

0, 		0, 		0		, distance

x_axis, 0, 		0		, distance

0, 		y_axis, 0		, distance

0, 		0, 		z_axis	, distance

>python3 position.py data.txt
### Config anchor positions before using serial mode
Config x_axis, y_axis, z_axis

Anchor positions will have format

0, 		0, 		0

x_axis, 0, 		0

0, 		y_axis, 0

0, 		0, 		z_axis
### Serial mode
Config TEST_MODE to False

Connect serial (remember to adjust baudrate) and transmit data, change data format to fit the use

>python3 position.py
# Reference
https://mathworld.wolfram.com/Sphere-SphereIntersection.html?fbclid=IwAR2CTEeBz8VtI9EcXxcPEeetI1HhnNDanEgR0EyoSUpTcILVaMQjrWcjjmM

https://github.com/jremington/UWB-Indoor-Localization_Arduino
