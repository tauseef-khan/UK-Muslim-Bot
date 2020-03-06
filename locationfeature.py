import pandas as pd
from math import sin, cos, sqrt, atan2, radians

# I believe the mosque data is read everytime a method in this file is used
filepath = "MosquesMar20Extended_interpreted.csv"
mosque_df = pd.read_csv(filepath, encoding="latin1")

# method to calculate distance between two co-ordinates using Haversine formula
# mehod poached/borrowed from this StackOverflow question...
# ...https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
def haversine(lon1, lat1, lon2, lat2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    
    return distance

def getClosestMosques(userLat, userLon):

	closestMasjidsData = []

	originalUserLat = userLat
	originalUserLon = userLon

	userLat = radians(userLat)
	userLon = radians(userLon)

	# create dataframe to store distances from user's location
	columns = ['Distance']
	masjid_distance = pd.DataFrame(columns=columns)


	# calculate distances to each masjid in 'mosque_df'
	for index, row in mosque_df.iterrows():
	    
	    #extract masjid lat and lon
	    mosqueLat = radians(row['Latitude'])
	    mosqueLon = radians(row['Longitude'])
	    
	    # calculate distance to masjid
	    distance = haversine(mosqueLon, mosqueLat, userLon, userLat)
	    
	    # append distance to 'masjid_distance' dataframe
	    masjid_distance = masjid_distance.append({'Distance':distance}, ignore_index=True)


	# sort distance into ascending order
	masjid_distance_sorted = masjid_distance.sort_values(['Distance'], ascending=True)

	# get top 5 smallest distance
	masjid_distance_sorted_indexes = masjid_distance_sorted.index.values[:5]


	# store masjid details for user to see
	count = 0
	for index in masjid_distance_sorted_indexes:

		distance = "*Distance: *" + str(masjid_distance_sorted.values[count].round(3)) + " km"
		count = count + 1

		masjidLat = mosque_df.iloc[index]['Latitude']
		masjidLon = mosque_df.iloc[index]['Longitude']

		masjidName = mosque_df.iloc[index]['[Key]_Address_Line_1']
		masjidName = "*Name & Addr: *" + masjidName[masjidName.find("]")+1:]

		masjidCapacity = "*Capacity: *" + str(mosque_df.iloc[index]['Capacity'])
		masjidWomen = "*Women facilities: *" + mosque_df.iloc[index]['Women facility']
		masjidUsage = "*Usage: *" + mosque_df.iloc[index]['Masjid usage']
		masjidMultifaith = "*Multi-faith: *" + mosque_df.iloc[index]['Multi-faith']
		masjidTheme = "*Theme: *" + mosque_df.iloc[index]['Theme']
		masjidManagement = "*Management: *" + mosque_df.iloc[index]['Management']
		mapUrl = generateMapUrl(originalUserLat, originalUserLon, masjidLat, masjidLon)

		message_text = masjidName + '\n' + masjidCapacity + '\n' + masjidWomen + '\n' + masjidUsage + '\n' + masjidMultifaith + '\n' + masjidTheme + '\n' + masjidManagement + '\n' + distance + "\n" + mapUrl

		closestMasjidsData.append(message_text)

	return closestMasjidsData

def generateMapUrl(userLat, userLon, masjidLat, masjidLon):

	generatedUrl = "(" + "https://www.google.com/maps/dir/?api=1&origin=" + str(userLat) + "," + str(userLon) + "&destination=" + str(masjidLat) + "," + str(masjidLon) + ")"

	return "[Get Directions]" + generatedUrl