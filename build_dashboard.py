import os
import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    if os.path.exists("page_metrics.csv"):
        data = pd.read_csv("page_metrics.csv")
    else:
        data = pd.DataFrame(columns=["URL", "LCP", "TBT", "Date"])
    return data

def show_data_table(data):
    st.write(data)

def visualize_data(data):
    fig = px.histogram(data, x='URL', y=['LCP', 'TBT'], barmode='group', title='Сравнение метрик',
                       labels={'variable': 'Метрика', 'URL': 'Ссылка'}).update_layout(yaxis_title='Значение метрики')
    st.plotly_chart(fig)

def main():
    st.title('Сравнение метрик LCP и TBT')
    data = load_data()
    show_data_table(data)
    visualize_data(data)

### ЗАПУСКАТЬ ЧЕРЕЗ "streamlit run build_dashboard.py" в консоли
if __name__ == "__main__":
    main()
