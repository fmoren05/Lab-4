# Lab 4
 
In this experiment, we implemented a real-time scheduler to enable multitasking and control two motors simultaneously. This was done by modifying the example file which utilized Cotask to run two separate tasks, each in charge of controlling a motor. Each task ran the motor at the same Kp of 0.003 and setpoint of 50000. We evaluated the control system's performance by adjusting the period and analyzing step response plots. When one motor control task was run too slowly, noticeable degradation occurred. Based on these observations, we recommend a specific speed for proper operation. We will talk about this below with our plots. Overall, the two-motor control system demonstrated effective performance within the recommended task run rate, ensuring smooth operation of the motors. 


In the plot below, we graphed the response of the task 1 motor when each task was running at a period of 10. As noted by the graph, the system has a clean response with no noticeable overshoot as it approaches a steady state. This is the period we recommend running the multitasking for the best performance.

![10period](https://github.com/fmoren05/Lab-4/assets/156385950/f0680dcc-6f79-4ca8-83ab-2e01726c0d71)

In this next response, we ran each task for a period of 20. Although running slower, there is not much of a difference noted yet when compared to the first plot. A small overshoot bump appears to form but it does not cause too much of an effect on the performance.

![20period (2)](https://github.com/fmoren05/Lab-4/assets/156385950/85f2569c-d4ac-4f06-8793-59341953c63e)

Now with a period of 25, the bump is more noticeable and the linear portion is starting to appear shaky.

![25period](https://github.com/fmoren05/Lab-4/assets/156385950/b73d49e9-f25d-48a6-8df1-fc51af682f13)

A period of 45 shows an even larger overshoot as it approaches steady state.

![45period](https://github.com/fmoren05/Lab-4/assets/156385950/53058d45-80ef-4710-b952-890bace77c1f)

Finally, we tested a period of 100 and noticed a sharper overshoot.

![100period](https://github.com/fmoren05/Lab-4/assets/156385950/1731f100-6ad4-417b-91e4-2ee04126049c)

From these tests, we noticed that a larger period results in a larger overshoot, and it can cause the response to appear more shaky rather than a clean slope.

