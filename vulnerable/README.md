# EC521_FinalProject

## Authors: Ryan Ewing, Andre Gonzaga, Nicolas Hunt, David Li

### Summary
Kodi is a free open source media player. The software runs on Linux, Mac, Windows, Android, and many smart devices. It is a platform to hold all of your videos, TV shows, music, and provides many additional services via add-ons. Although Kodi supports many mainstream add-ons providing enterprise services like Netflix and Hulu, it is also used for streaming pirated content through different third party add-ons created by the larger community. There have been concerns regarding its security, especially since these add-ons can be downloaded from anywhere. Users accessing illegitimate programs are exposed to additional risk. To download these add-ons, users often have to disable their security options in settings. We will identify vulnerabilities within the Kodi system, specifically ones introduced by insecure third party add-ons. The purpose of our project is to find vulnerabilities in popular third party Kodi apps. 

This platform will involve running Static and Dynamic analysis on a series of Kodi addons. The chosen addons will be a combination of the most popular and the most likely to have vulnerabilities. Specifically, we want to investigate add-ons that deal with sensitive user data, such as add-ons for automatic backups, and add-ons that download data onto the user’s system, like torrents or third-party content providers. We will begin by running manual versions of both types of analyses to become more familiar with the processes. Eventually, the goal will be to have automated programs that will run both types of analyses and identify potential vulnerabilities.

#### Static Analysis
* Definition: Inspecting program code in a non-runtime environment. 
* Crawl code looking for keywords and terms used in common exploits.
* Examine software to determine the origins of all code libraries within the software. This can be helpful to find if there is out of date code with known vulnerabilities within an application (commonly known as SCA analysis).
* Identify flaws and backdoor
* We want to detect SQL injections, XSS vulnerabilities, and Operating System interactions that may reveal sensitive information

#### Dynamic Analysis
* Definition: Testing a program using real-time data by monitoring the running program. A dynamic test will examine the device’s system properties, such as system memory, functional behavior, CPU usage, response time, and the overall performance of the system.
* Dynamic analysis techniques include fuzzing. This approach provides invalid, unexpected, or random data as inputs to a computer program and monitors the applications reaction.
