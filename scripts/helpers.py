#functions that will be reused often

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(path="../data/processed/f1_clean.csv"):
    return pd.read_csv(path)

def plot_avg_pitstops(df,circuit_col='Circuit', pit_col='TotalPitStops'):
    avg_pits= df.groupby(circuit_col)[pit_col].mean().sort_values(ascending=False)
    sns.barplot(x=avg_pits.values, y=avg_pits.index)
    plt.xlabel('Average Number of Pit Stops')
    plt.ylabel('Circuit')
    plt.title('Average Number of Pit Stops per Circuit')
    plt.show()
    