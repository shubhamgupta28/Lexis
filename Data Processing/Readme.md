#Data Processing

All files in this folder were used to converting geoQuery Dataset into Documents which made processing ,easier for the chatbot.


GEOQUERY
====================
state('florida','fl','tallahassee',9746.0e+3,68664,27,'jacksonville','miami','tampa','st. petersburg').
state('georgia','ga','atlanta',5463.0e+3,58.9e+3,4,'atlanta','columbus','savannah','macon').
state('hawaii','hi','honolulu',964.0e+3,6471,50,'honolulu','ewa','koolaupoko','wahiawa').

After Convertion
====================
THe captial of state Florida is tallahassee.
Cities in Florida are Miami,Tampa,St. Petersburg,Jacksonville.
The state id of state Florida is 27.
The state code of state Florida is FL


##MountainAndStateDataConversion.py
Written by Shubham Gupta, to convert Mountain and State Data geoquery into sentences.

##GeoQueryToJSON.py	
Written by Sagar Narang, to convert GeoQuery Prolog data into JSON format.

##WikipediaFetch.py	
Written by Sagar Narang, to Fetch Wikipedia Data about all the states in USA and save them into MongoDB.

##geobase.txt	
Actual geoquery Dataset.