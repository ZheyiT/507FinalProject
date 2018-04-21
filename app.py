from flask import Flask, render_template, request
import DrawAirbase

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <img src="/static/USAF_pic1.jpg"/ width="700">
        <h1>US Air Force Around the World</h1>
        <ul>
            <li><a href="/map"> Map of US Airbase Around the World </a></li>
        </ul>
        <ul>
            <li><a href="/pie"> Distribution of US Air Force Commands (Pie Chart)</a></li>
        </ul>
        <ul>
            <li><a href="/bar"> Top 10 Wings with Most Squads (Bar Chart)</a></li>
        </ul>
        <ul>
            <li><a href="/range"> Combat Range of Certain Airbase in Certain Time </a></li>
        </ul>
    '''

@app.route('/map', methods=['GET', 'POST'])
def map(): 
    plotlydiv = DrawAirbase.plot_all_air_base()
    return render_template("otherplotly.html", plotlydiv=plotlydiv, pagetitle="Map of US Airbase Around the World")

@app.route('/pie', methods=['GET', 'POST'])
def pie():
    plotlydiv = DrawAirbase.plot_command_pie()
    return render_template("otherplotly.html", plotlydiv=plotlydiv, pagetitle="Distribution of US Air Force Commands (Pie Chart)")

@app.route('/bar', methods=['GET', 'POST'])
def bar():
    plotlydiv = DrawAirbase.plot_wing_bar()
    return render_template("otherplotly.html", plotlydiv=plotlydiv, pagetitle="Top 10 Wings with Most Squads (Bar Chart)")

@app.route('/range', methods=['GET', 'POST'])
def range():
    if request.method == 'POST':
        baseid = int(request.form['baseid'])
        reactiontime = float(request.form['reactiontime'])
    else:
        baseid = 37
        reactiontime = 0.5

    plotlydiv = DrawAirbase.plot_fight_range(baseid, reactiontime)
    return render_template("rangeplotly.html", plotlydiv=plotlydiv, pagetitle="Combat Range of Certain Airbase in Certain Time")


if __name__ == '__main__':
    app.run(debug=True)