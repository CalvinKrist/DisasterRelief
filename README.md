# Disaster Relief
### HoosHacks, 2-28-2019

## Problem Description

Even with a growing amount of open source real-time information on the effects of natural disasters, it's difficult to plan and allocate resources for disaster relief. 

With the recent spike in natural disasters, acquiring real time data about the natural disaster alone is not sufficient in providing the necessary responsiveness, resources, and bandwidth to deal with the repercussions. Disaster preparedness and relief applications need to provide not only real-time data of the disaster, but also need to account for the lack of communication, the amount of resources needed in affected areas, subsequent relief actions that need to be taken, and an efficient exchange between the victims and the rescuers in a time of need. 

Existing disaster relief applications successfully provide real time tracking of the disaster, but fail to bridge the gap between "assessing the affected area" and then "taking appropriate subsequent actions" quick and efficiently and relaying this information back to a central database. Modern emergency management systems fail in their design to provide a constant, reliable communication system between victims and rescuers, and lack a cohesive program for bridging the gap between real-time rescue and relief efforts. 

Disaster preparedness and response can be viewed as three independent problems: assessing the disaster relief area, determining the amount of resources/what resources are needed on the basis of reliable communication between the victim and the rescuers in real-time, and then quickly communicating that information back to a central database. Existing disaster relief applications only target the first problem, failing to provide a cohesive system that connects real-time tracking the relief response.

## Solution Description

The scope and requirements for disaster relief vary with each disaster. As a result, there is not a single cohesive system that can provide a personalized approach to disaster relief for each situation. Each disaster relief procedure will vary depending on the magnitude of the disaster, the economic profile of the affected area, and the existing resources and technology that already serve as disaster relief measures. 

Project Clear Skies provides developers with a system that can aggregate real time data about the disaster from a variety of social media sources giving the developer access to analyze it, and implement individualized applications and modules on the basis of analysis that quickly address the situation. Currently, there are many existing APIs that provide real time tracking of the natural disaster, but there is no central database where this information can be collected and analyzed quickly and efficiently in order to take appropriate action in response to a disaster. In the case of a natural disaster, social media platforms are updated very frequently. Clear Skies uses the Rest API to provide developers with a system that can filter data from social media platforms in real time. The application uses the Google Vision API, tensor flow, and machine learning for image classification giving first time responders an accurate assessment of the severity of the affected area to reach victims and allocate resources more efficiently. The application also provides additional information based on textual and image analysis such as location of the disaster, severity of the situation, the type of disaster and additional tags. 

As a result, Clear Skies would provide a fast and efficient way to pool the data into a central database giving the developer access to analyze the data, quickly identify the targeted and affected areas to facilitate efficient communication between the victims and the rescuers, and give first responders a better understanding of the situation in real time. 

Clear Skies is targeting and addressing the three problems outlined in the Problem Description: accurate assessment, efficient communication between the victims and the rescuers, and efficient communication of the reccommended assesment back to first responders to take appropriate action. 


### Use Cases:

2. Scenario 1: Hurricane Maria struck in 2017 and revealed some major flaws in diaster preparedness and relief. The lack of proper response measures cost the Puerto Rican economy upwards of $95 billion that damaged an already ailing economy. This case study provides a prime example of where a standardized disaster relief and preparedness procedure would not be applicable due to Puerto Rico's already weak economy, lack of existing disaster relief infrastructure, and lack of resources to faciliate efficient communication. At the time of the disaster, there is a time lag between the the communication between the victims and the first responders, and no quick and efficient way to accurately assess the situation. 

2a. Solution Use: The Clear Skies API takes in real time data from Twitter posts, (both textual and image based) and outputs information regarding the date and location of the tweet, the type of disaster, the severity of the situation and the  recommendation on the damage done, affected areas, amount of resrouces needed, priority areas that will most likely have the most people--- first responders should reach out to these areas first. This would provide a quick way of assesing the sitaution, coming up with an accurate estimation of resources needed/affected areas, relay this information back to first responders. 

## Feature List
1. Image classification to determine severity of the disaster
2. Language Processing for location data
3. Categorization and classification of Twitter data to extract key information of the disaster in real time including the type of disaster, location, severity of the disaster, and additional tags/labels describing the image

## Program Architecture

## Sources
