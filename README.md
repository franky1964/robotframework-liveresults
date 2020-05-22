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

 - Step 3 options to be used:
   > - Change the default value to open the browser:             robot --listener LiveResults:True
   > - Activate option to capture videos of test execution:      robot --listener LiveResults:False:True
   > - Change the timer value for autorefresh in HTML page:      robot --listener LiveResults:False:False:60
   > - Change the filename of the generated HTML page:           robot --listener LiveResults:False:False:15:myPage.html

---

Available Results:
 - The default name of the page is "RF_LiveResults.html', it is located in the same directory as 'report.html' and 'log.html'
 - The result "PASS" or "FAIL" contains a link to the detailed testcase log
 - "BLOCKED" is set as testcase result if the Testsuite Setup was executed with an error
 - "SKIP" is already added for any future version of Robot Framework supporting this status
 - In case of captured videos the column "Critical' contains a link to the captured video of the testcase execution 
   (the following library has to be installed for this option: <a href="https://github.com/mihaiparvu/ScreenCapLibrary">ScreenCapLibrary</a>)
---

*Screenshot*

<img src="/LiveResults.jpg" alt="LiveResults">
