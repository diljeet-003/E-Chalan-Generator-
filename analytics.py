import pandas as pd
import matplotlib.pyplot as plt

def violation_analysis():

    df = pd.read_csv("dataset/traffic_data.csv")

    counts = df['violation_type'].value_counts()

    counts.plot(kind='bar')

    plt.title("Traffic Violations Analysis")
    plt.xlabel("Violation Type")
    plt.ylabel("Count")

    plt.show()