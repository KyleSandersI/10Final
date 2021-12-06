import streamlit as st
import numpy as np
import pandas as pd
import os
import altair as alt
import sklearn
from pandas.api.types import is_numeric_dtype
##import altair as alt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

#df = pd.read_csv('/Users/kylesanders/Documents/Math 10/EPL_20_21.csv')
df = pd.read_csv("EPL_20_21.csv")
df = df[df["Matches"]>5]
df["G/A"] = (df["Goals"] + df["Assists"]) / df["Matches"]


# st.write(st.__version__)
# st.write(np.__version__)

st.title("English Premier League 2020 - 2021")
st.header("Top 40 Players by Age Groups")
st.caption("Here I am finding a list of Premiere League players sorting them by their G/A or goals and assist per game. I made sure to have a minimum count of 5 games so that outliers and supersubs are not reflected in the data.")
st.caption("I continue to stratify the data by age brackets:16-21, 22-26,27-30,30+. These ages are used as major professional points in players' careers for contracts, trades, and judgement of their play.")

#Age Groups for selectbox
df_21 = df[df["Age"]<=21]
df_21 = df_21.sort_values('G/A', ascending = False)
a = df_21[0:40]

a26 = df[df["Age"]<=26]
a22 = df[df["Age"]> 21]

df_22_26 = a22[a22["Age"]<=26]
df_22_26 = df_22_26.sort_values('G/A', ascending = False)
b = df_22_26[0:40]

a30 = df[df["Age"]<=30]
a27 = df[df["Age"]> 27]

df_27_30 = a27[a27["Age"]<=30]
df_27_30 = df_27_30.sort_values('G/A', ascending = False)
c= df_27_30[0:40]

a30 = df[df["Age"]> 30]
df_30 = a30
df_30 = df_30.sort_values("G/A", ascending = False)
d = df_30[0:40]

option = st.selectbox('Select age group',("16-21", "22-26", "27-30","30+"))
#st.write("", option) 


#st.selectbox("Ages", (a,b,c,d))
dictionary = {"16-21":a, "22-26":b, "27-30":c, "30+":d}
st.write("Age Groups Top 40",dictionary[option])



#Age Groups AltChart for SelectBox
chart_dataAlt = alt.Chart(a).mark_point().encode(
    alt.X("Age",
          scale = alt.Scale(domain=(16,21))
          ),y ="G/A",
      tooltip = ["G/A","Age","Name","Club"]
).properties (
    width = 300,
    height = 700,
    title = "Age 16-21")
 
chart_dataAlt2 = alt.Chart(b).mark_point().encode(
    alt.X("Age",
         scale = alt.Scale(domain=(22,26))
         ),y ="G/A",
     tooltip = ["G/A","Age","Name","Club"]
).properties (
    width = 300,
    height = 700,
    title="Age 22-26")
        
chart_dataAlt3 = alt.Chart(c).mark_point().encode(
    alt.X("Age",
         scale = alt.Scale(domain=(27,30))
         ),y ="G/A",
     tooltip = ["G/A","Age","Name","Club"]
).properties (
    width = 300,
    height = 700,
    title = "Age 27-30")

chart_dataAlt4 = alt.Chart(d).mark_point().encode(
    alt.X("Age",
         scale = alt.Scale(domain=(30,36))
         ),y ="G/A",
     tooltip = ["G/A","Age","Name","Club"]
).properties (
    width = 300,
    height = 700,
    title = "Age 30 and Older")
                
st.header("Choose an Age Group Below to reflect Top 40s")
st.caption("While the charts do not depict trends that may be predicted with linear regression, they better highlight G/A and their correlation of top players with their ages")    
option2 = st.selectbox('Select age group for Top 40 chart',("16-21", "22-26", "27-30","30+"))
#st.write('You Selected', option2) 
    
dictionary2 = {"16-21":chart_dataAlt, "22-26":chart_dataAlt2, "27-30":chart_dataAlt3, "30+":chart_dataAlt4}
#st.write("Ages Charts",dictionary2[option2])
st.altair_chart(dictionary2[option2], use_container_width=True)
     

brush = alt.selection_interval(bind='scales')
input_dropdown = alt.binding_select(options=["All Teams","Arsenal","Aston Villa", "Brighton","Burnley","Chelsea","Crystal Palace",
"Everton","Fulham","Leeds United","Leicester City","Liverpool FC","Manchester City","Manchester United","Newcastle United",
"Sheffield United","Southampton","Tottenham Hotspur","West Bromwich Albion","West Ham United","Wolverhampton Wanderers"], name='Pick by Club')
selection = alt.selection_single(fields=['Club'], bind=input_dropdown)

mins_age_chart = alt.Chart(df).mark_circle().encode(
    alt.X("Age", 
    scale = alt.Scale(domain=(16,40))),
    y='Mins',
    color=alt.condition(brush, 'Club', alt.value('lightgray')),
    size = "G/A",
    tooltip = ["G/A","Age","Name","Club"],
).properties(
    width = 800 ,
    height = 600,
    title = "G/A Production per Players of Teams"
).add_selection(
    brush,selection
).transform_filter(
    selection
    )

st.header("G/A Production per Players of Teams")    
st.caption("This chart highlights production of players by their age and minutes played. While plotting their stats in this way, G/A is the scaled size of the players production. Attached below is a selectbox of all the different teams the viewer can choose between to compare youth and veteran production and etc. The teams and their players are distinguished by their colors.")       
st.caption("Zoom and Tooltip key features are enabled")
st.altair_chart(mins_age_chart, use_container_width=True)
with st.expander("See Additional Material"):
    st.write("""Here I utilized extra Altair chart tools and expanded my knowledge on keys and labeling. While we had explored color options and tool tips, I implemented further Altair tools like domain/range control, zoom and expansion capibilities, alongside st.selectbox features for the 'Clubs' to distinguish inside the altair chart.
    """)

from sklearn.linear_model import LinearRegression
reg = LinearRegression()
reg = LinearRegression(fit_intercept=False)
import sklearn.linear_model
model = sklearn.linear_model.LinearRegression()

X = np.array(df["Mins"])
y = np.array(df["G/A"])
X = X.reshape(-1,1)
y = y.reshape(-1,1)

# reg.fit(X,y)
# reg.coef_
# reg.intercept_

st.header("Linear Regression and Predicting G/A")
st.caption("Estimating a players possible production across a season can be difficult. The regression line belows predicts X players production modeled by the Mins played and G/A per minimum 5 games of EPL players across a 38 game season.")
sc_plot = alt.Chart(df).mark_point().encode(
    y = "G/A",
    x ="Mins",
    tooltip = ["G/A","Age","Name","Club"]
).properties (
    width = 800,
    height = 600,
    title = "Linear Regression of Production per Minutes played to G/A"
  
)     
    
LinReg_Chart = sc_plot + sc_plot.transform_regression("Mins","G/A").mark_line()
st.altair_chart(LinReg_Chart, use_container_width=True)
#st.write("",LinReg_Chart)  

##Versions
# numpy  1.21.4 
# streamlit  1.2.0  
st.write("Attached Below is my Github")
st.write("https://github.com/KyleSandersI", unsafe_allow_html = True)



