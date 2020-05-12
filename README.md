# Virtual Gaming: CoviFitness [Virtual Covid Game]
This is an extension to the Covid Raccoon that I developed in extension to Covid Raccoon Game. Good news is that you can play it virtually!
**CoviFitness** is a 2D fun, interactive and awaring game made for kids and individuals to play the game with real time moves.

> **Are you also getting bored and lazy this covid?**
> **Do you have a habbit of skippinig morning walks?**
> **Is your exercise getting rescheduled due to your sleep cycle?**
> **Do you also want flexible timing for work-out?**

Well in that case, **CoviFitness** is a must try!

### Installation Instructions
Open Terminal and type the following command:

> pip install -r requirements.txt

Once all the dependencies are installed, open the terminal and type the command:

> python3 CoronaIntegrated.py

### Calibrations

When you run the code, the following text will appear on your screen:

![](instructions/Calibration.jpg)

Don't move during this process, it tries to detect the face and accordingly do the calibration. Note that most of the movements are defined based on the facial orientation.

Once the Calibration is successful, you will see this window:

![](instructions/Calibration2.jpg)

This will end by popping a cv2 window which will proceed to calibration, this is for calibrating the bending height, make sure your camera is positioned in such a way that your chin must be above this blue line.
These lines are added with time delay so that they won't get changed quickly and allow for reaction time. In case you want to bring down the height even more you can modify this line of code in [CoronaIntegrated.py](CoronaIntegrated.py).
The popup screen looks like this:

![](instructions/HeightCalibration.jpg)

Move your right hand to the top-right box to lower the line, move your left hand to the top-left box to raise the height, once you're satisfied, move both of the hands to complete the calibration process.

Once the calibration is complete the following screen pops up:

![](instructions/gamescreen.jpg)

Now enjoy the game, jump to make your character jump and crouch to make it crouch. Note that currently these controls are calibrated and the other control (like boxing gesture is in test mode).

## Project Components

1. Computer Vision (OpenCV python)
2. Pygame (For building intutive 2D game)

## Inspiration

I have always been curious about learning new things, whether it be related to stem or something else (though, I am always inclined towards STEM). Game Dev is a booming field and seems to have a promising future if correctly used.

Video games are no more just a source of fun and entertainment, today we can use this virtual technology (especially in fields of AR and VR) to make use of this tech and create a real-life learning experience. From the very beginning, this has caught my attention to the field of gaming. This project is one such attempt to demonstrate how these things can actually change the way we live.

Though I am well versed with other Development (App-Dev/ Web-Dev/ Designing) and Instrumentation Tech (IoT/ Robotics etc.) but Game-Dev was always something which I wanted to learn, and that's what turned me to try it here for the first time after creating a very basic 2D game [covid raccoon](https://github.com/sedhha/covidRaccoon).

## What it does?
