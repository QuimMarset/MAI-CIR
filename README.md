# Cognitive Interaction with Robots (CIR)

## Master in Artificial Intelligence - UPC

This repository contains the project we had to do for the CIR elective course. The idea was to develop an AI-related Human-Robot interaction application.
We started by defining some research questions we wanted to answer (i.e. the project's goals) and identifying the target audience for our application. 
Then we defined a null and alternative hypothesis for each of those research questions, and using statistical tests, we would try to refute the null hypotheses. 
By refuting them, we would demonstrate the objectives we wanted to achieve with our application.
To perform the statistical tests, we would need to define quantitative or qualitative variables we would obtain values by testing the application with real users and getting their feedback.

We implemented an application to facilitate the autonomous learning of American Sign Language (ASL). We wanted to demonstrate that learning through our application brings some benefits over other methods,
like simply watching videos. In particular, we wanted to answer the following research questions:
* Does the learning progress depend on the learning methodology used?
* Does the learning easiness depend on the learning methodology used?

We understand progress as how well the user learns the different signs and ease of learning as how easy the learning becomes.

The user would learn the signs using a lesson system similar to the one from Duolingo. We divided the application into several lessons, each featuring a set of signs. Each lesson consisted of 4 parts:
* Learning the signs by watching videos (i.e. featuring a person performing the sign)
* Practise, using several games (e.g. a memory game), to get used to the different signs.
* Practise, using a sign detector, to learn to perform the signs correctly. The sign detector consists of a camera recording the user performing the sign, and an AI model detecting the sign using the recorded video. The user would start by deciding the sign to practise, and by repeating it several times until the sign detector detects it correctly, the user would learn to perform the sign.
* Evaluating the learning performance through a final test consisting of a mix of games and sign detection.

We created 4 lessons, with increased difficulty, featuring the following set of signs:
* Numbers from 0 to 9
* Vowels
* Consonants from B to J
* Random words (e.g. "yes" and "chair")

Some of those signs are static, meaning they consist of a single pose (e.g. the numbers), while others are dynamic and require a particular sequence of poses (e.g. the words). For this reason, we cannot train a single AI model to recognize them all, as some would receive an image as input, while others a sequence of frames from which it would detect the sign (e.g. leveraging a recurrent layer). In particular, we used 3 AI models:
* One to recognize the numbers we trained ourselves from scratch.
* One to recognize the vowels and consonants we took from https://github.com/fmahoudeau/MiCT-RANet-ASL-FingerSpelling.
* One to recognize the words we took from https://github.com/matyasbohacek/spoter.

The application only works on PCs, as the AI models were not trained to work on smartphones, and training some from scratch was a hassle. Moreover, we only introduced those 4 lessons as the users would need to go through all to test the application for us to perform the statistical study.

The application was developed on Python, leveraging Kivy to perform the graphical interface, and Pytorch to implement the AI models. The repository contains the code to build the application and the final report contains the statistical study and a more extended explanation of the whole project itself. 

We built the application following this tutorial: https://www.youtube.com/watch?v=NEko7jWYKiE.

However, it can be a little difficult, so we directly link the zip containing one already built: https://drive.google.com/file/d/1tXmfzXayHxXS7BODbdnSRHWYbVOQ8BJx/view?usp=drive_link. 

To execute the application, you only need to extract the ZIP file and double-click the executable file App_full/App/Application, which has a floppy disk icon.
