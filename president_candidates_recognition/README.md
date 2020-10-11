<p align="center">
<img src="https://github.com/dataworkshop/dw-olsztyn-project/raw/master/president_candidates_recognition/img/wyborywtvLogoNoWirus.png" width="400"/>
</p>

## Project description

The project consists in analyzing the content broadcast by the three largest TV stations in Poland: TVP (public television), TVN and Polsat (private television). 
Our application monitored the content that was shown to viewers 24 hours a day.
When one of the presidential candidates appeared on the screen, a record was created in the database with information about the day, time, candidate and television station on which he appeared. 
Based on the data, the application generates interactive charts that allow to analyze the collected information.

## Project tasks
1. Preparation of described photos and encodings of candidates' faces as a recognition base
2. Launching a system for image processing, face detection and recognition of desired people in parallel for many video sources
3. Collecting detection information in an external database
4. Preparation of the application with summary and visualization of results

## Results

* Interactive [application](http://wyborywtv.herokuapp.com/) 
* Examples of detection - 
[1](samples/video)
[2](samples/screenshots)
[3](saved_montages%2F2020-05-01%2023%3A02%3A51.jpg)


## Disclaimer 

Machine learning algorithms (ML) are a sensational solution and can replace us in many tedious and boring tasks. 
However, they are not free from imperfections. 
For this reason, in some cases, it is possible to notice the detection of candidates in places where they were not there. 
Although we are constantly striving to improve the quality of the ML model, we will never be able to guarantee 100% accuracy.

The implementation of the project respects the ideological difference of each person. We do not support any of the election candidates.

## Project environment

To create environment with conda, use

     $ conda env create --file environment.yml 

To activate this environment, use

     $ conda activate president_candidates_recognition

 To deactivate an active environment, use

     $ conda deactivate
