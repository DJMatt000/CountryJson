from flask import Flask, url_for, render_template,request
import os
import json
from markupsafe import Markup
app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_main():
    return render_template('home.html')

@app.route("/p1")
def render_page1():
    countrieslist = get_countries("country","country-by-capital-city.json")
    #print(countries)
    if"country" in request.args:
        with open('country-by-capital-city.json') as country_data:
            countriescities = json.load(country_data)
        with open('country-by-government-type.json') as country_data:
            countriesgovernment = json.load(country_data)
        with open('country-by-population.json') as country_data:
            countriespopulation = json.load(country_data)
        with open('country-by-surface-area.json') as country_data:
            countriesarea = json.load(country_data)
        with open('country-by-region-in-world.json') as country_data:
            countrieslocation = json.load(country_data)
        with open('country-by-continent.json') as country_data:
            countriescontinent = json.load(country_data)
        country = request.args.get("country")
       
        city = ""
        for c in countriescities:
            if c["country"] == country:
                city = c["city"]
        government = ""
        for c in countriesgovernment:
            if c["country"] == country:
                government = c["government"]
        population = ""        
        for c in countriespopulation:
            if c["country"] == country:
                population = c["population"]
        area = ""        
        for c in countriesarea:
            if c["country"] == country:
                area = c["area"]
        location = ""        
        for c in countrieslocation:
            if c["country"] == country:
                location = c["location"]
        continent = ""        
        for c in countriescontinent:
            if c["country"] == country:
                continent = c["continent"]
 
        
        return render_template('page1.html', showing = "yes",countries=countrieslist,city=city,government=government, population=population,area=area,location=location,continent=continent)
    return render_template('page1.html', countries=countrieslist)
    

@app.route("/p2")
def render_page2():
    get_countrieslist = get_countries("Country","global_development.json")
    if "country" in request.args:
        country = request.args.get("country")
        data = get_data(country)
        title=country + Markup("'s total population 1980-2013")
        print(title)
        return render_template('page2.html', countries=get_countrieslist, showing = "yes", data=data,title=title)
    return render_template('page2.html', countries=get_countrieslist)

    
def get_countries(key,file):
    """Return a list of countries abbreviations from the demographic data."""
    with open(file) as country_data:
        countries = json.load(country_data)
    countrieslist=[]
    for c in countries:
       if c[key] not in countrieslist:
           countrieslist.append(c[key])
    return countrieslist
def get_data(country):
    """Return a list of countries abbreviations from the demographic data."""
    with open('global_development.json') as country_data:
        countries = json.load(country_data)
    countriesdata={}
    for c in countries:
        if c["Country"] == country:
            if c["Year"] not in countriesdata:
                countriesdata[c["Year"]] = c["Data"]["Health"]["Total Population"]
    print(countriesdata) 
    graph_points = ""
    for key, value in countriesdata.items(): 
        graph_points = graph_points + Markup("{x:" + str(key) + ", y:" + str(value) + "}, ")
    graph_points = graph_points[:-2]
    return graph_points
if __name__=="__main__":
    app.run(debug=False)
