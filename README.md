# Disaster Releif
### HoosHacks, 2-28-2019

## Problem Description

Even with a growing amount of open source real-time information on the effects of natural disasters, it's difficult to plan and allocate resources for disaster relief. 

With the recent spike in natural disasters, acquiring real time data about the natural disaster alone is not sufficient in providing the necessary responsiveness, resources, and bandwidth to deal with the repercussions. Disaster preparedness and relief applications need to provide not only real-time data of the disaster, but also need to account for the lack of communication, the amount of resources needed in affected areas, subsequent relief actions that need to be taken, and an efficient exchange between the victims and the rescuers in a time of need. 

Existing disaster relief applications successfully provide real time tracking of the disaster, but fail to bridge the gap between "assessing the affected area" and then "taking appropriate subsequent actions" quick and efficiently and relaying this information back to a central database. Modern emergency management systems fail in their design to provide a constant, reliable communication system between victims and rescuers, and lack a cohesive program for bridging the gap between real-time rescue and relief efforts. 

Disaster preparedness and response can be viewed as three independent problems: assessing the disaster relief area, determining the amount of resources/what resources are needed on the basis of reliable communication between the victim and the rescuers in real-time, and then quickly communicating that information back to a central database. Existing disaster relief applications only target the first problem, failing to provide a cohesive system that connects real-time tracking the relief response.

## Solution Description

The scope and requirements for disaster relief vary with each disaster. As a result, there is not a single cohesive system that can provide a personalized approach to disaster relief for each situation. Each disaster relief procedure will vary depending on the magnitude of the disaster, the economic profile of the affected area, and the existing resources and technology that already serve as disaster relief measures. 

(name of application) provides developers with a system that can aggregate real time data about the disaster from a variety of sources giving the developer access to analyze it, and implement individualized applications and modules on the basis of analysis that quickly address the situation. Currently, there are many existing APIs that provide real time tracking of the natural disaster, but there is no central database where this information can be collected and analyzed quickly and efficiently in order to take appropriate action in response to a disaster. In the case of a natural disaster, a recommendation on the amount of resources needed is dependent not only on the magnitude of the disaster, but also on the economic profile of the area, the population, and the existing resources present in the area. As a result, (name of application) would provide a fast and efficient way to pool the data into a central database giving the developer access to analyze the data, quickly identify the targeted and affected areas to facilitate efficient communication between the victims and the rescuers, and provide a recommendation to first responders on the amount of resources that are needed. 

(name of application) is targeting and addressing the three problems outlined in the Problem Description: accurate assessment, efficient communication between the victims and the rescuers, and efficient communication of the reccommended assesment back to first responders to take appropriate action. 


### Use Cases:

1. Scenario 1: An organization helps provide aid when disease breaks out in poorer countries. They provide aid in a wide variety of countries, need to pull funding from many sources internationally, and may need to quickly respond to very serious pandemics. They use tools like GIT and in-house applications to help analyze the seriousness of outbreaks and determine how to allocate resources in order to provide relief. They likely need to split those resources between multiple relief zones at once.

1a. With (name of application), they could . .  .
* Automatically send data on how many resources they have to the platform. For example, donations collection at local shelters and stored as CSVs (a likely format) could be automatically imported into databases accessible from our platform
* Port existing applications to our platform and enable them to draw on the real-time data provided by their organization as well as many other open-source, real-time information platforms
* Display their applications as a module in our platform. Perhaps those applications are further split into different modules, so that one can be useful in developing plans for providing aid in one country while another module is tailored towards another country. 

2. Scenario 2: Hurricane Maria struck in 2017 and revealed some major flaws in diaster preparedness and relief. The lack of proper response measures cost the Puerto Rican economy upwards of $95 billion that damaged an already ailing economy. This case study provides a prime example of where a standardized disaster relief and preparedness procedure would not be applicable due to Puerto Rico's already weak economy, lack of existing disaster relief infrastructure, and lack of resources to faciliate efficient communication. At the time of the disaster, there is a time lag between the the communication between the victims and the first responders, no quick and efficient way to accurately assess the situation and make a reccomendation on the resources needed on the basis of the damage done and the economic profile of the area. 

2a. With (name of application), take in real time data and other stats of the area, and possibly images of the affected areas, output a recommendation on the damage done, affected areas, amount of resrouces needed, priority areas that will most likely have the most people--- first responders should reach out to these areas first. This would provide a quick way of assesing the sitaution, coming up with an accurate estimation of resources needed/affected areas, relay this information back to first responders. 

### Questions about the use case

1. Who uses the module aspect of the platform? Is it a developer, someone who is trained and technically savvy but not necessarily a developer or sys-admin, or is it someone with little technical experience who perhaps spends more time in a managerial position determining how much money to send to which project? The answer to this question should heavily impact the way the modules are designed. For example, if the users are developers or tech-savy people they could resemble queries to `Splunk`, which allow users to search multiple databases in useful ways and analyze them within a SQL-like query. Or perhaps the users aren't tech-savy and boxes displaying dollar amounts and graphs would be more useful.

2. How do the modules actually help? They need to somehow enable people to respond more quickly to disasters. How long does it normally take, where is most of that time spent, what has been the effect of open-source, real-time information like the Facebook API? Where does the disconnect between information gathering and carrying out a plan come from and how can we minimize that disconnect with these modules?

3. Developers will be making this "personalized" disaster relief app before the disaster strikes so there is an assumption that this relies on accurate weather estimates of the incoming disaster, the module would then serve as a harness that takes in real time data from the source and outputs reccomendations and priorities based on criteria mentioned above (damage done, affected area, economic profile, existing resources etc.) and quickyl relays this infromation back to a central database, for the communication issue, since this app already quickly identifies affected areas and notifies the first responders of exactly where to reach out to (to communicate with victims)----- this app is not directly providing communication between victims and responders, there is a TON of stuff out there like that that already exists. Instead, its facilitating the process in the case where victims have lost access to their technology, how would first responders find these people???? They would do this based on the reccomendation from our app---- this is also where google maps comes into play, it would be interesting to do some image processing if there is a noticeable difference of pre/after damage from the image, also would be useful to look into how first responders find these people becuase current systems of communication between victims and first responders all assume they have access to their phones and can use an app------- not very realistic/is not always the case. So that was my thought process behind how we can "facilitate communication" assuming victims have lost access to their tech. 

## Feature List

## Program Architecture

## Sources
