import streamlit as st
import pandas as pd
import altair as alt

@st.cache
def load(url):
    return pd.read_json(url)

df = load("https://cdn.jsdelivr.net/npm/vega-datasets@2/data/penguins.json")

# df = pd.read_json("https://cdn.jsdelivr.net/npm/vega-datasets@2/data/penguins.json")

if st.checkbox("Show Raw Data"):
    st.write(df)

scatter = alt.Chart(df).mark_circle(size=100).encode(
    alt.X("Flipper Length (mm)", scale=alt.Scale(zero=False)),
    alt.Y("Body Mass (g)", scale=alt.Scale(zero=False)),
    alt.Color("Species")
)

st.write(scatter)
st.write("# Selection Types")

# picked = alt.selection_single(on="mouseover", empty="none")
# picked = alt.selection_multi()
# picked = alt.selection_interval(encodings=["x"])
# picked = alt.selection_single(fields=["Species", "Island"])
input_dropdown = alt.binding_select(options=["Adelie", "Chinstrap", "Gentoo"], name="Species of ")
picked = alt.selection_single(encodings=["color"], bind=input_dropdown)

# picked = alt.selection_multi(on="mouseover")

st.write(scatter.encode(
    color=alt.condition(picked, "Species:N", alt.value("lightgray"))
).add_selection(picked))

st.write("## Binding selection to scales")

scales = alt.selection_interval(bind="scales", encodings=["x"])
st.write(scatter.add_selection(scales))

st.write("## Filter data")

brush = alt.selection_interval(encodings=["x"])

st.write(scatter.add_selection(brush) & alt.Chart(df).mark_bar().encode(
    alt.X("Body Mass (g)", bin=True),
    alt.Y("count()"),
    alt.Color("Species")
).transform_filter(brush))

st.write("## Movie data")

movies = load("https://cdn.jsdelivr.net/npm/vega-datasets@2/data/movies.json")