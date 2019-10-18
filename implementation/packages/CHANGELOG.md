# Change Log
All notable changes to this project will be documented in this file.

<br />

##  Version 0.1.0 
######[2019-08-20] Kick-start POC Prototype

##### BUGS
- Chromedriver outputs "DevTools listening" message in the console 
even when in silent mode (verbose=False). Apparently, to get rid of 
that message, it is necessary to override a Selenium service as 
described in in the following thread (Aug 2019):
https://stackoverflow.com/questions/47751529/how-do-i-suppress-console-cmd-error-messages-in-python 

##### KNOWN-ISSUES
- Case the input variable scripts need to be executed in a defined 
order, it will be necessary to index the files in the input path 
and explicitly require the desired order in the initialization 
parameters (or make sure all files are named in alphabetical order)
- It is not clear how (or even if it is possible) to mix two or more 
input variables scripts, if necessary
- Selenium: WebDriverException is thrown when the browser UI gets 
closed while still loading
