import urllib.request

def menu_options():
    print('Menu')
    print('(S)earch for an NOAA station ID')
    print('(L)ookup the weather at a station')
    print('(D)isplay the menu again')
    print('(Q)uit')

#function to remove tags from station ID list
def remove_pretag(text):
    cut = text.index(':')
    return text[(cut + 2):]

#function to remove xml tags
def remove_tag(text):
    copy = text[:]
    copy = copy[(copy.index('>') + 1):]
    copy = copy[:(copy.index('<'))]
    return copy


#search for a Station ID by name
def find_Match(listOfStations, stationName):
    queryList = []
    for item in listOfStations:
        if stationName in item[0]:
            queryList.append(item)
    return queryList

#parse and display a list of found Station IDs
def display_query_list(query_list):
    if query_list:
        print('Results: \n')
        for item in query_list:
            print(item[0] + ',', item[4], 'Station ID: ', item[2])
    else:
        print('Sorry, no matches were found.  :(')



choice = 'd'
while choice != 'q' and choice != 'Q':
    if choice == 's' or choice == 'S':
        #open station list file
        inFile = open('stations.yml', 'rt')
        stationList = inFile.read()
        stationList = stationList.split('- xml_url:')
        del stationList[0]
        #parse station into form: [Name, Latitude, ID, Longitude, State]
        for x in range(len(stationList)):
            stationList[x] = stationList[x].split('\n')
            del stationList[x][0]
            del stationList[x][-1]
            for y in range(len(stationList[x])):
                stationList[x][y] = remove_pretag(stationList[x][y])
        #Ask for a station and display results
        query = input('What is the name of the station you are searching for? ')
        display_query_list(find_Match(stationList, query))
        choice = input('option: ')
    elif choice == 'l' or choice == 'L':
        #get the station ID to lookup
        print('Florence, SC - KFLO')
        print('Oviedo, FL - KORL')
        station = input('What is the NOAA weather station ID: ')
        #get the url
        NOAAurl = 'http://w1.weather.gov/xml/current_obs/' + station + '.xml'
        #open the .xml file
        inFile = urllib.request.urlopen(NOAAurl)
        text = inFile.read()
        text = str(text)
        Lines = text.split('\\n')
        #get weather info
        for line in Lines:
            if '<station_id>' in line:
                StationID = remove_tag(line)
            elif '<location>' in line:
                Location = remove_tag(line)
            elif '<weather>' in line:
                Weather = remove_tag(line)
            elif '<temp_f>' in line:
                Fahrenheit = remove_tag(line)
            elif '<temp_c>' in line:
                Celsius = remove_tag(line)
        #display weather info
        print('NOAA Station ID:', StationID)
        print(Location)
        print('Weather:', Weather)
        print(Fahrenheit, 'degrees Fahrenheit')
        print(Celsius, 'degrees Celsius')
        choice = input('option: ')
    elif choice == 'd' or choice == 'D':
        menu_options()
        choice = input('option: ')



