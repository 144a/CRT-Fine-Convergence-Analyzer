# CRT-Fine-Convergence-Analyzer
A CRT fine convergence analyzing tool that uses USB microscopes to report information on convergence.

This tool is designed to work with any standard crosshatch signal, however, it is best to use the built-in signal on the monitor/TV if possible (especially in the case of Sony BVMs). To use this tool, you must have 2 things:

1) A USB microscope (this one will work: https://www.amazon.com/gp/product/B09SNSPHXX/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)

2) (optional) A way to connect to the monitor (for now only LAN for A series BVMs are supported)

Once downloaded, you will want to ensure that the camera is plugged in before running the program. 
There are 2 different use cases for this tool: basic static analysis, and automatic adjustment (Primarily for BVM A32 and D32, but other monitors will be added)

Static Analysis: 

The Green Difference Refers to the level of balance of the green beam versus the center of the red/blue beams. If the green is perfectly in the center, Green-Diff will be 0.

The Red-Blue Difference refers to the average distance between the red and blue lines. This will decrease as the beams approach each other, reaching 0 when they are perfectly in line.

Real-Time Automatic Adjustment (A32/D32 only):

Sony BVM-A32E1Wx) Start with the monitor turned on, but not in any menu. To connect the monitor to your PC, use the static IP address: 192.168.0.100, then allow the monitor to connect (checking for confirmation through the console). Once it stops the cursor, place the microscope on that cross-section and confirm both blue and red lines are detected. then press Q to allow the tool to correct the geometry. Once it is complete, move it to the next cursor location and continue until finished.

Sony BVM-A32E1Wx) To Be Finished...

TODO List:
1) Properly capture Red, Blue, and Green Beams --- Done
2) Create accurate metrics for analysis --- Done
3) Create subroutine for calibration --- Done
4) Bridge program for connection to A32 --- Done
5) Complete vertical beam analysis
6) Create total routine for calibration
7) Bridge program for connection to D32 
