# Disaster Relief
### HoosHacks, 2-28-2019

## Problem Description

Even with a growing amount of open source real-time information on the effects of natural disasters, it's difficult to plan and allocate resources for disaster relief. 

With the recent spike in natural disasters, acquiring real time data about the natural disaster alone is not sufficient in providing the necessary responsiveness, resources, and bandwidth to deal with the repercussions. Disaster preparedness and relief applications need to provide not only real-time data of the disaster, but also need to account for the lack of communication, the amount of resources needed in affected areas, subsequent relief actions that need to be taken, and an efficient exchange between the victims and the rescuers in a time of need. 

Existing disaster relief applications successfully provide real time tracking of the disaster, but fail to bridge the gap between "assessing the affected area" and then "taking appropriate subsequent actions" quick and efficiently and relaying this information back to a central database. Modern emergency management systems fail in their design to provide a constant, reliable communication system between victims and rescuers, and lack a cohesive program for bridging the gap between real-time rescue and relief efforts. 

Disaster preparedness and response can be viewed as three independent problems: assessing the disaster relief area, determining the amount of resources/what resources are needed on the basis of reliable communication between the victim and the rescuers in real-time, and then quickly communicating that information back to a central database. Existing disaster relief applications only target the first problem, failing to provide a cohesive system that connects real-time tracking and the relief response.

## Solution Description

The scope and requirements for disaster relief vary with each disaster. As a result, there is not a single cohesive system that can provide a personalized approach to disaster relief for each situation. Each disaster relief procedure will vary depending on the magnitude of the disaster, the economic profile of the affected area, and the existing resources and technology that already serve as disaster relief measures. 

Project Clear Skies provides developers with a system that can aggregate real time data about the disaster from a variety of social media sources giving the developer the ability to perform rapid searches using key words and features of the disaster. Currently, there are many existing APIs that provide real time tracking of the natural disaster, but there is no central database where this information can be collected and analyzed quickly and efficiently in order to take appropriate action in response to a disaster. In the case of a natural disaster, social media platforms are updated very frequently. 

Clear Skies uses the **Rest API** to provide developers with a system that can filter data from social media platforms in real time. The application uses the **Google Vision API**, **Tensor Flow**, and **machine learning** for image classification giving first time responders an accurate assessment of the severity of the affected area to reach victims and allocate resources more efficiently. The application also provides additional information based on textual and image analysis such as location of the disaster, severity of the situation, the type of disaster and additional tags. 

As a result, Clear Skies would provide a fast and efficient way to pool the data into a central database providing first responders with a way to quickly identify the targeted and affected areas to facilitate efficient communication between the victims and the rescuers.

### Use Cases:

**Scenario 1**: Hurricane Maria struck in 2017 and revealed some major flaws in diaster preparedness and relief. The lack of proper response measures cost the Puerto Rican economy upwards of $95 billion that damaged an already ailing economy. This case study provides a prime example of where a standardized disaster relief and preparedness procedure would not be applicable due to Puerto Rico's already weak economy, lack of existing disaster relief infrastructure, and lack of resources to faciliate efficient communication. At the time of the disaster, there is a time lag between the the communication between the victims and the first responders, and no quick and efficient way to accurately assess the situation. 

**Solution**: The Clear Skies API takes in real time data from Twitter posts, (both textual and image based) and outputs information regarding the date and location of the tweet, the type of disaster, the severity of the situation, and affected areas. Clear Skies uses the Google Cloud Vision API and Tensorflow to perform image classification on the image data. Users can query the database to further filter the tweets by keyword searches. This provides a centralized database to accumulate useful data from Twitter to provide first responders with an accurate assessment of the disaster in real time. 

## Feature List
1. Image classification to determine severity of the disaster using Tensorflow and the Google Cloud Vision API. The image is classified into one of three categories: severe, mild and non-relevant information. 
2. Gives the user the ability to query the incoming, classified Twitter data
3. Categorization and classification of Twitter data to extract key information of the disaster in real time including the type of disaster, location, severity of the disaster, and additional tags/labels describing the relevant data
4. Language Processing to extract location data from the textual data to tag each post with an approximate location of the disaster. 
