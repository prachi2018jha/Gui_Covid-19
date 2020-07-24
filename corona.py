import matplotlib.pyplot as plt
import pandas as pd
from countryinfo import CountryInfo
from tkinter import *
win=Tk()
win.geometry("520x300")
win.title("Covid-19 Tracker ")
def plotdata():
    try:
        country=data.get()
        country=country.strip()
        country=country.replace(" ",",").split(",")
        countries=[]
        for x in country:
            countries.append(x)
        df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv', parse_dates=['Date'])
        df = df[df['Country'].isin(countries)]
        #Creating a Summary Column
        df['Cases'] = df[['Confirmed', 'Recovered', 'Deaths']].sum(axis=1)
        #Restructuring our Data
        df = df.pivot(index='Date', columns='Country', values='Cases')
        countries = list(df.columns)
        covid = df.reset_index('Date')
        covid.set_index(['Date'], inplace=True)
        covid.columns = countries
        #Calculating Rates per 100,000
        populations={}
        for i in countries:
            c=CountryInfo(i)
            populations[i]=c.population()
        percap = covid.copy()
        for country in list(percap.columns):
            percap[country] = percap[country]/populations[country]*100000
        #Generating Colours 
        colors={}
        j=0
        col = ['#045275', '#089099' ,'#DC3977', '#7C1D6F','#7CCBA2'] 
        for i in countries:
            colors[i]=col[j]
            j+=1
        plt.style.use('fivethirtyeight')
        percapplot = percap.plot(figsize=(12,8), color=list(colors.values()), linewidth=5, legend=False)
        percapplot.grid(color='#d4d4d4')
        percapplot.set_xlabel('Month',color='brown')
        percapplot.set_ylabel('# of Cases per 100,000 People',color='brown')
        for country in list(colors.keys()):
            percapplot.text(x = percap.index[-1], y = percap[country].max(), color = colors[country], s = country, weight = 'bold')
        percapplot.text(x = percap.index[2], y = percap.max().max()+45, s = "Covid-19 Comparison Graph Between Countries \nIncludes Current Cases, Recoveries, and Deaths", fontsize = 18, color='brown', alpha = .75)
        plt.show()
    except Exception as e:
        print("Country data not present ")

win.configure( bg="light goldenrod")
l1=Label(win,text="Enter the name of five countries for \n comparison of covid-19 cases",font="Verdana 17 bold",foreground='medium violet red')
l1.place(x=20,y=10)
data=StringVar()
entry=Entry(win, textvariable=data,font=("Calibri",15), width=28)
entry.place(x=125,y=100)
b1=Button(win,text="Get plots",height=2,width=15, font=("Calibri",12), fg='indianred',command=plotdata)
b1.pack(side=RIGHT, padx=5, pady=5)
b1.place(x=209,y=160)
win.mainloop()
