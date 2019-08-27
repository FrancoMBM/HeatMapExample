import folium
import numpy as np
from folium.plugins import MarkerCluster
import pandas as pd
from folium import CircleMarker, Circle
from folium.plugins import HeatMap
import csv

COORDINATES = (38.904722, -77.016389)
map = folium.Map(location=COORDINATES, zoom_start=12)


class HeatMapCreator(object):



    def __init__(self, crimedata, grp, offense_name):
        ''' crimedata is a string'''
        '''grp and offense_data are variables. offense_name is a string'''
        self.crimedata = pd.read_csv(crimedata)
        self.grp = grp
        self.offense_name = offense_name
        #self.cluster_grp = cluster_grp
        #self.color = color

    def configuration(self):
        self.crimedata['LATITUDE'] = list(self.crimedata['LATITUDE'].astype(float))
        self.crimedata['LONGITUDE'] = list(self.crimedata['LONGITUDE'].astype(float))
        self.crimedata['offense-text'] = list(self.crimedata['offense-text'])

    def offense_text(self):

        self.grp = folium.FeatureGroup(name = self.offense_name)
        self.heat_df_offense = self.crimedata[['offense-text']]
        self.heat_df_offense = self.heat_df_offense.dropna(axis = 0, subset = ['offense-text'])
        self.heat_df_offense = self.crimedata[['LATITUDE', 'LONGITUDE', 'offense-text']]
        self.heat_df_offense = self.heat_df_offense.dropna(axis=0, subset=['LATITUDE','LONGITUDE','offense-text'])

        self.offense_data = self.heat_df_offense[(self.heat_df_offense['offense-text'] == self.offense_name)]
        self.offense_data = self.offense_data[['LATITUDE', 'LONGITUDE']]
        self.offense_data = [[round(row['LATITUDE'], 3),round(row['LONGITUDE'], 3)] for index, row in self.offense_data.iterrows()]
        self.grp.add_child(folium.plugins.HeatMap(data = self.offense_data, radius = 10, blur = 10))
        map.add_child(self.grp)




offenses = ['motor vehicle theft', 'theft', 'auto theft', 'burglary', 'arson', 'assault with weapon', 'homicide', 'sex abuse', 'robbery']
#colors = ['green', 'blue', 'darkgreen', 'purple', 'yellow', 'pink', 'black', 'red', 'orange']

for i in offenses:
    i = HeatMapCreator('DC_Crime_Official2.csv', 'data', i)
    i.configuration()
    i.offense_text()

folium.LayerControl().add_to(map)
map.save('Testmap.html')
