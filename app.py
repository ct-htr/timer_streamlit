import streamlit as st
import time
from datetime import datetime
from datetime import timedelta
import re
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(layout="wide")

st.markdown("""
            <style>
            .big-font {
                font-size:200px !important;
                text-align: center;
            }
            </style>
            """, unsafe_allow_html=True)
st.markdown("""
            <style>
            .centerText {
                text-align: center;
            }
            </style>
            """, unsafe_allow_html=True)
st.markdown("""
            <style>
            .noticeText {
                font-size: 30px;
                text-align: center;
            }
            </style>
            """, unsafe_allow_html=True)


# settingsTab, timerTab, stopwatchTab = st.tabs(["Settings", "Timer", "Stopwatch"])
timerTab, stopwatchTab = st.tabs(["Timer", "Stopwatch"])
inputH = inputM = inputS = 0
timerTitle = ""
start = end = datetime.now()
last15 = last5 = endWarning = timeAppend = False
confirmExtend = False
examStart = examEnd = "0000"
last15String = "<p class=noticeText><b>Last 15 minutes.</b><br>You are not allowed to leave until the end of the exam.</p>"
endWarningString = "<h1 class=centerText>Time's up, pens down.</h1><p class=noticeText>Please stay in your seat and pay attention to further instructions.</p>"
secBypass = 0
#############
with st.sidebar:
    
    with st.form("Setting Form"):
        st.header("Settings")
        timerTitle = st.text_input("Timer title")
        timerCol1, timerCol2, timerCol3 = st.columns([1, 1, 1], vertical_alignment = "center")
        examStart = timerCol1.text_input("Start time")
        examEnd = timerCol2.text_input("End time")
        secBypass = timerCol3.number_input("Add seconds")
        
        last15 = st.checkbox("last 15 minutes warning")
        last5 = st.checkbox("last 5 minutes warning")
        endWarning = st.checkbox("end of timer warning")
        submitted = st.form_submit_button("Submit")
    
    tDelta = timedelta(seconds=1)
    if re.search(r'^[0-9]{4}$', examStart) and re.search(r'^[0-9]{4}$', examEnd):
        start = datetime.strptime(examStart, '%H%M')
        end = datetime.strptime(examEnd, '%H%M')
        tDelta = end - start + timedelta(seconds=secBypass)
    
        
    
    
#############

with timerTab:

    st.markdown(f'<h1 class=centerText>{timerTitle if timerTitle != "" else "Timer"}</h1>', unsafe_allow_html=True)
    st.markdown(f'<h3 class=centerText>Time allowed: {tDelta.seconds/60:.0f} minutes</h3>', unsafe_allow_html=True)

    with st.container(border=True):
        timeContainer = st.container()
        countdownText = timeContainer.empty()
        countdownText.markdown(f'<p class="big-font">{tDelta}</p>', unsafe_allow_html=True)
    
 
    pad_A, timerCol1, timerCol2, timerCol3, pad_b = st.columns([0.14, 0.08, 0.48, 0.08, 0.14], vertical_alignment = "top")
    
    noticeMessage = timerCol2.empty()
    
    startTimer = timerCol1.button("Start Timer", use_container_width=True)
    stopTimer = timerCol3.button("Stop Timer", use_container_width=True)
    noticeDisplay = timerCol2.empty()
    #startTimer = st.toggle("test")
    # st.markdown('#')
    # with st.expander("Adjustments"):
    #     expandNote = st.text_input("Test expander:")
    #     st.write(expandNote)
    
    if startTimer:
        startTime = datetime.now()
        endTime = startTime + tDelta
        while datetime.now() < endTime:
            timeLeft = endTime - datetime.now()
            # pad_A.write(timeLeft.seconds/60)
            countdownText.markdown(f'<p class="big-font">{str(timeLeft).split(".")[0]}</p>', unsafe_allow_html=True)
            if (timeLeft.seconds/60) == 15 and last15 == True:
                noticeMessage.markdown(last15String, unsafe_allow_html=True)    
            
            time.sleep(.2)
        countdownText.markdown(f'<p class="big-font">0:00:00</p>', unsafe_allow_html=True)
        if(endWarning):
            noticeMessage.markdown(endWarningString, unsafe_allow_html=True)  
        
#############
with stopwatchTab:
    st.header("Stopwatch")
    with st.container(border=True):
        elapsedTimePlaceholder = st.empty()
        elapsedTimePlaceholder.markdown("# 0.00")
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1], vertical_alignment = "center")
    startStopwatch = col2.button("Start")
    stopStopwatch = col4.button("Stop")

    
    if startStopwatch:
        startTime = time.time()
        while True:
            currentTime = time.time()
            elapsedTime = currentTime - startTime
            elapsedTimePlaceholder.markdown(f'# {elapsedTime:.2f}')
            time.sleep(.01)


