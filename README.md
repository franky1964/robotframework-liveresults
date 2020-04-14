# Robotframework Live Results
Robot Framework Listener to get Live Results in a web page while RF execution is in progress
[![HitCount](http://hits.dwyl.com/franky1964/RF-LiveResults.svg)](http://hits.dwyl.com/franky1964/RF-LiveResults)

> Uses ROBOT_LISTENER_API_VERSION = 3
    
Steps to Use:

 - Step 1: Installation:
   > - Download or clone this repo
   > -   or Copy `LiveResults` folder to your project 
   > -   or use 'pip install git+https://github.com/franky1964/robotframework-liveresults.git'

 - Step 2: Execute test case/suites using LiveResults Listener
   > - `robot --listener LiveResults Tests` 

 - Step 3 Options to be used:
   > - Chnage default page name 'RF_Live_Results.html' by using: robot --listener LiveResults:myPage.html Tests
   > - Default refresh time cn be changed by using:              robot --listener LiveResults:myPage.html:40 Tests
   > - Option if browser is opened can be changed by using:      robot --listener LiveResults:myPage.html:5:false Tests
   > - Option if videos of test execution should be captured:    robot --listener LiveResults:myPage.html:5:true:true Tests

---

Available Results:

 - to be done..

---

*Screenshot*

<img src="/LiveLogs.jpg" alt="LiveLogs">
