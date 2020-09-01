"""
Grouped boxplots
================
_thumb: .66, .45
"""
import matplotlib.pyplot as plt

import seaborn as sns
sns.set(style="ticks", palette="pastel")

# Load the example tips dataset
tips = sns.load_dataset(data_home="/home/roit/datasets/seaborn",name='tips')

# Draw a nested boxplot to show bills by day and time
sns.boxplot(x="day", y="total_bill",
            hue="smoker", palette=["m", "g"],
            data=tips)
sns.despine(offset=10, trim=True)

plt.show()