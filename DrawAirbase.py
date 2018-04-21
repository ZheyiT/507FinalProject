import plotly.plotly as py
import plotly.offline as offplot
import requests
import sqlite3
import plotly.graph_objs as go
import secrets
#import pandas as pd

dbname = 'USAF.db'
mapbox_access_token = secrets.mapbox_access_token

class AirBase():

    def __init__(self, basename, lat, lon):
        self.basename = basename
        self.lat = lat
        self.lon = lon

    def __str__(self):
        printout_result = "The location of {} Airbase is lat:{}, lon:{}.".format(self.basename, self.lat, self.lon)
        return printout_result

def plot_all_air_base():
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    statement = '''
            Select BaseNAme, Latitude, Longitude
            From Airbase
            Where Latitude not like ""
        '''
    result = cur.execute(statement)

    lat_vals = []
    lon_vals = []
    text_vals = []

    for i in result:
        each_airbase = AirBase(i[0], i[1], i[2])
        lat_vals.append(each_airbase.lat)
        lon_vals.append(each_airbase.lon)
        text_vals.append(each_airbase.basename)

    data = go.Data([
        go.Scattermapbox(
            lon=lon_vals,
            lat=lat_vals,
            text=text_vals,
            mode='markers',
            marker=go.Marker(
                size=7,
                symbol='airport',
                color='blue'),
        )
    ])

    layout = go.Layout(
        title = "US Air Force Bases Around the World",
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=0,
                lon=0
            ),
            pitch=0,
            zoom=1
        ),
    )

    fig = dict(data=data, layout=layout)
#    py.plot(fig, filename='US Air Force Base Around the World')



#    trace1 = dict(
#        type='scattermapbox',
#        lon=lon_vals,
#        lat=lat_vals,
#        text=text_vals,
#        mode='markers',
#        marker=dict(
#            size=7,
#            symbol='airport',
#            color='blue'
#        ))

#    layout_geo = dict(
#        title='US Air Force Base',
#        geo=dict(
#            scope='usa',
#            projection=dict(type='albers usa'),
#            showocean=True,
#            showlakes=True,
#            showland=True,
#            landcolor="rgb(250, 250, 250)",
#            subunitcolor="rgb(100, 217, 217)",
#            countrycolor="rgb(217, 100, 217)",
#            countrywidth=3,
#            subunitwidth=3
#        ),
#    )

    conn.close()

#    fig = dict(data=[trace1], layout=layout_geo)
    #py.plot(fig, validate=False, filename='US Air Force Base Around the World')
    div = offplot.plot(fig, show_link=False, output_type="div", include_plotlyjs=False)
    return div




def plot_command_pie():
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    statement = '''
                Select CommandName, count(*)
                From Squad
                Group by CommandName
                Having CommandName not like "NO INFO"
                Order by count(*) DESC
            '''
    result = cur.execute(statement)

    text_var = []
    value_var = []

    for i in result:
        text_var.append(i[0])
        value_var.append(i[1])

    trace = go.Pie(labels=text_var, values=value_var)

    data = [trace]
    layout = go.Layout(
        title='Pie Chart of US Air Commands',
    )

    fig = go.Figure(data=data, layout=layout)
    #py.plot(fig, filename='Pie Chart of US Air Commands')
    conn.close()
    div=offplot.plot(fig, show_link=False, output_type="div", include_plotlyjs=False)
    return div

def plot_wing_bar():
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    statement = '''
                    Select WingName, count(*)
                    From Squad
                    Group by WingName
                    Having WingName not like "NO INFO"
                    Order by count(*) DESC
                    Limit 10
                '''
    result = cur.execute(statement)

    text_var = []
    value_var = []

    for i in result:
        text_var.append(i[0])
        value_var.append(i[1])

    trace0 = go.Bar(
        x=text_var,
        y=value_var,
        text=value_var,
        textposition='auto',
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity=0.6
    )

    data = [trace0]
    layout = go.Layout(
        title='Top 10 US Air Force Wings with Most Squads',
    )

    fig = go.Figure(data=data, layout=layout)
    #py.plot(fig, filename='Wing_Bar')
    conn.close()
    div = offplot.plot(fig, show_link=False, output_type="div", include_plotlyjs=False)
    return div


def plot_fight_range(BaseId, hour):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    statement = '''
                    SELECT A.MaxSpeed, A.CombatRadius, B.Latitude, B.Longitude, A.AircraftName, B.BaseName, S.SquadName
                    FROM Squad AS S
                    JOIN Aircraft  AS A ON S.BattleAircraftCode = A.AircraftName
                    JOIN Airbase AS B ON B.BaseName = S.BaseNAme
                    WHERE B.Id = {}
                '''.format(BaseId)
    result = cur.execute(statement)

    meaningful_count = 0
    meaningful_n = 0
    meaningful_result = ()
    for i in result:
        if i[4] != "NA":
            meaningful_count +=1
            meaningful_result = i
    if meaningful_count == 0:
        return "No Fighter Jet in this Airbase! Please try another base."
    else:
        plane_result = meaningful_result
        MaxSpeed = plane_result[0]
        CombatRadius = plane_result[1]
        Lat = plane_result[2]
        Lon = plane_result[3]
        Aircraft = plane_result[4]
        Base = plane_result[5]
        Squad = plane_result[6]

        FR = hour * MaxSpeed
        if FR > CombatRadius:
            FR = CombatRadius
            #unit: KM

        ###Old Method
        trace1 = dict(
            type='scattergeo',
            locationmode='ISO-3',
            lon=[Lon],
            lat=[Lat],
            text=[Base],
            mode='markers',
            marker=dict(
                size=10,
                symbol='star',
                color='blue'
            ))

        trace2 = dict(
            type='scattergeo',
            locationmode='ISO-3',
            lon=[Lon],
            lat=[Lat],
            text=["Range of fighter jet from the base can react in {} hour".format(hour)],
            mode='markers',
            marker=dict(
                size=FR/5,
                symbol='circle-open',
                color='red'
            ))

        center_lat = Lat
        center_lon = Lon

        lat_axis = [Lat - 40, Lat + 40]
        lon_axis = [Lon - 40, Lon + 40]

        layout = dict(
            title= "Range of {}'s {} fighter jet from {} can react in {} hour ({}km)".format(Squad, Aircraft, Base, hour, FR),
            geo=dict(
                scope='world',
                projection=dict(type='equirectangular'),
                showocean=True,
                showlakes=True,
                showland=True,
                showsubunits= True,
                landcolor="rgb(250, 250, 250)",
                subunitcolor="rgb(100, 217, 217)",
                countrycolor="rgb(217, 100, 217)",
                lataxis={'range': lat_axis},
                lonaxis={'range': lon_axis},
                center={'lat': center_lat, 'lon': center_lon},
                countrywidth=3,
                subunitwidth=3
            ),
        )
        fig1 = dict(data=[trace1, trace2], layout=layout)



        ###New Method

        data = go.Data([
            go.Scattermapbox(
                lon=[Lon],
                lat=[Lat],
                text=[Base],
                mode='markers',
                marker=go.Marker(
                    size=10,
                    symbol='airport',
                    color='blue'),
            ),

            go.Scattermapbox(
                lon=[Lon],
                lat=[Lat],
                text=[Base],
                mode='markers',
                opacity= 0.5,
                marker=go.Marker(
                    size=FR/10,
                    color='yellow'),
            )
        ])

        layout = go.Layout(
            title= "Range of {}'s {} fighter jet from {} can react in {} hour ({}km)".format(Squad, Aircraft, Base, hour, FR),
            autosize=True,
            hovermode='closest',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=dict(
                    lat=Lat,
                    lon=Lon
                ),
                pitch=0,
                zoom=2
            ),
        )

        fig = dict(data=data, layout=layout)

        #py.plot(fig, validate=False, filename='Base Reaction Range')
        conn.close()
        div = offplot.plot(fig, show_link=False, output_type="div", include_plotlyjs=False)
        return div









#plot_all_air_base()
#plot_command_pie()
#plot_wing_bar()
#plot_fight_range(4, 1)

# 37 Airbse in Florida
# 4 Airbase in Asia
# 7 No Fight Jet in this Airbase
