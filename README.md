# Disaster Releif
### HoosHacks, 2-28-2019

## Problem Description

Even with a growing amount of open source real-time information on the effects of natural disasters, it's difficult to plan and allocate resources for disaster relief. 

With the recent spike in natural disasters, acquiring real time data about the natural disaster alone is not sufficient in providing the necessary responsiveness, resources, and bandwidth to deal with the repercussions. Disaster preparedness and relief applications need to provide not only real-time data of the disaster, but also need to account for the lack of communication, the amount of resources needed in affected areas, subsequent relief actions that need to be taken, and an efficient exchange between the victims and the rescuers in a time of need. 

Existing disaster relief applications successfully provide real time tracking of the disaster, but fail to bridge the gap between "assessing the affected area" and then "taking appropriate subsequent actions" quick and efficiently and relaying this information back to a central database. Modern emergency management systems fail in their design to provide a constant, reliable communication system between victims and rescuers, and lack a cohesive program for bridging the gap between real-time rescue and relief efforts. 

Disaster preparedness and response can be viewed as three independent problems: assessing the disaster relief area, determining the amount of resources/what resources are needed on the basis of reliable communication between the victim and the rescuers in real-time, and then quickly communicating that information back to a central database. Existing disaster relief applications only target the first problem, failing to provide a cohesive system that connect real-time tracking the relief response.

## Solution Description

A system that can aggregate data from a variety of sources, provide programmer access to the data, and allow programmers to implement modules to analyze and display information as desired.

### Use Case:

An organization helps provide aid when disease breaks out in poorer countries. They provide aid in a wide variety of countries, need to pull funding from many sources internationally, and may need to quickly respond to very serious pandemics. They use tools like GIT and in-house applications to help analyze the seriousness of outbreaks and determine how to allocate resources in order to provide relief. They likely need to split those resources between multiple relief zones at once.

With our application, they could . .  .
* Automatically send data on how many resources they have to the platform. For example, donations collection at local shelters and stored as CSVs (a likely format) could be automatically imported into databases accessible from our platform
* Port existing applications to our platform and enable them to draw on the real-time data provided by their organization as well as many other open-source, real-time information platforms
* Display their applications as a module in our platform. Perhaps those applications are further split into different modules, so that one can be useful in developing plans for providing aid in one country while another module is tailored towards another country. 

### Questions about the use case

1. Who uses the module aspect of the platform? Is it a developer, someone who is trained and technically savvy but not necessarily a developer or sys-admin, or is it someone with little technical experience who perhaps spends more time in a managerial position determining how much money to send to which project? The answer to this question should heavily impact the way the modules are designed. For example, if the users are developers or tech-savy people they could resemble queries to `Splunk`, which allow users to search multiple databases in useful ways and analyze them within a SQL-like query. Or perhaps the users aren't tech-savy and boxes displaying dollar amounts and graphs would be more useful.
2. How do the modules actually help? They need to somehow enable people to respond more quickly to disasters. How long does it normally take, where is most of that time spent, what has been the effect of open-source, real-time information like the Facebook API? Where does the disconnect between information gathering and carrying out a plan come from and how can we minimize that disconnect with these modules?

## Feature List

## Program Architecture

## Sources
