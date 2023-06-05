import pandas as pd
import streamlit as st
from datetime import datetime
from PIL import Image

image = Image.open("sunwire.jpg")
new_image = image.resize((325, 170))
st.image(new_image)

st.header(":blue[Welcome To Your Personal Dashboard]")
# Displaying today's date and time
current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
st.markdown(f":green[{current_time}]")


total = 90
answered = 15
avg = 20
st.subheader(":blue[Call Stats]")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Call Volume", total)
with col2:
    st.metric("You have answered", answered)
with col3:
    st.metric("Average Handel Time", 20)
with col4:
    st.metric("Your Average Handel Time", 15)

st.divider()

st.subheader(":blue[Shipment Stats]")
create = 20
processed = 10
remain = create - processed

col5, col6, col7 = st.columns(3)
with col5:
    st.metric("You have created", f"{create}")
with col6:
    st.metric("Shipment Processed",f"{processed}")
with col7:
    st.metric("Remain",f"{remain}")

st.divider()

st.subheader(":blue[Batch Stats]")

batches_created = 30
batches_processed = 20
batches_remain = batches_created - batches_processed

col8, col9, col10 = st.columns(3)
with col8:
    st.metric("Batches Created", f"{batches_created}")
with col9:
    st.metric("Batches Processed", f"{batches_processed}")
with col10:
    st.metric("Batches Remaining", f"{batches_remain}")

st.divider()

st.subheader(":blue[Ticket Stats]")

tickets_opened = 100
tickets_closed = 80
tickets_past_due = 10
percentage_completed = round((tickets_closed / tickets_opened) * 100)

col11, col12, col13, col14 = st.columns(4)
with col11:
    st.metric("Tickets Opened", f"{tickets_opened}")
with col12:
    st.metric("Tickets Closed", f"{tickets_closed}")
with col13:
    st.metric("% Completed", f"{percentage_completed}%")
with col14:
    st.metric("Past Due Tickets", f"{tickets_past_due}")

st.divider()
