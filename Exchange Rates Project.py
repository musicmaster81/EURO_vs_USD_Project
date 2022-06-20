# For this project, we wish to analyze the value of the Euro compared to the US Dollar from 1999-2022. This analysis is
# particularly relevant as the Federal Reserve's FOMC is currently in a rate hiking season. In fact, the FOMC just voted
# to raise interest rates by 75bps, the largest hike in almost 30 years. This has caused a strengthening of the USD,
# thus causing the value of the Euro to drop. The project is also meant to showcase my matplotlib graph construction
# skills.

# First, we import our required libraries and modules.
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as style

# We then define the path of our data set on our local computer.
file_path = r'C:\Python\Data Sets\euro-daily-hist_1999_2022.csv'

# We then create a dataframe from our data and examine its structure: the first and last 5 rows should suffice.
exchange_rates = pd.read_csv(file_path)
print(exchange_rates.head())
print("\n")
print(exchange_rates.tail())
print("\n")

# Let's take a look at some of the more intricate details using the info method.
print(exchange_rates.info())
print("\n")

# The US dollar and datetime column names appear a bit peculiar. Let's change their names to something more intuitive.
exchange_rates.rename(columns={'[US dollar ]': 'US_dollar',
                      'Period\\Unit:': 'Time'}, inplace=True)

# We also wish to convert all time entries to datetime objects.
exchange_rates['Time'] = pd.to_datetime(exchange_rates['Time'])
exchange_rates.sort_values('Time', inplace=True)  # This places the values in a time ascending order.
exchange_rates.reset_index(drop=True, inplace=True)  # We use our new datetime column as the index and drop the original

# Since the only currency we are interested in is the USD, let's create a new dataframe where we drop all the others.
euro_to_dollar = exchange_rates[["Time", "US_dollar"]]

# Let's take a look at our new dataframe.
print(euro_to_dollar.head(10))
print("\n")

# We also wish to see if there are any NaN or miscellaneous values.
print(euro_to_dollar['US_dollar'].value_counts())
print("\n")

# We have quite a few "-" values. Let's get rid of those entries using a boolean array.
num_bool = euro_to_dollar['US_dollar'] != '-'  # Create a boolean array where all "-" values equate to False.
euro_to_dollar = euro_to_dollar[num_bool]  # Assign only the True column back to our euro_to_dollar dataframe.

# Let's check to see if we removed the missing value rows.
print(euro_to_dollar['US_dollar'].value_counts())
print("\n")

# Success! Now, we wish to cast the values in the US_dollar column as floats to make calculations simpler.
euro_to_dollar = euro_to_dollar.astype({"US_dollar": 'float64'})

# Let's check to make sure our values in the US_dollar column are of a float type.
euro_to_dollar.info()

# Now that our USD column is a float, let's plot an exploratory chart to see the trend of the Euro to the USD.
plt.plot(euro_to_dollar['Time'], euro_to_dollar['US_dollar'])
plt.xlabel("Time Period from 1999 to 2022")
plt.ylabel("Value of the Euro")
plt.title("Value Trend of the Euro Compared to the USD")
plt.show()

# From the graph above, we can tell that the values appear to be very sporadic. Let's create a rolling mean column to
# smooth out the trend line and use this column for our explanatory graph.
euro_to_dollar['rolling_mean'] = euro_to_dollar['US_dollar'].rolling(30).mean()  # Creates a 30day rolling avg column.
print(euro_to_dollar.head(30))
print("\n")

# We are now ready to begin the plotting of our explanatory chart. As mentioned in the project outline, the goal is to
# examine the value of the USD compared to the Euro during the Recession and the COVID-19 Pandemic to see what effect
# the slashing of interest rates has on the USD. We create 3 dataframes for our time periods of interest.
recession = euro_to_dollar.copy()[(euro_to_dollar['Time'].dt.year >= 2006) & (euro_to_dollar['Time'].dt.year <= 2009)]
pandemic = euro_to_dollar.copy()[(euro_to_dollar['Time'].dt.year >= 2020) & (euro_to_dollar['Time'].dt.year <= 2021)]
not_pandemic = euro_to_dollar.copy()[euro_to_dollar['Time'].dt.year >= 2016]

# We now begin to plot our explanatory chart.
style.use('fivethirtyeight')  # Changes the style of our chart.
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(6, 8))  # Prepare to create a grid chart for our 2 graphs.

# Here we plot our original graph that tracks the 30 day rolling average from 1999-2022. We also use the color blue.
ax1.plot(euro_to_dollar['Time'], euro_to_dollar['rolling_mean'],
         color='#0000ff', linewidth=1.35)

# Add a Title to our graph to explain what we are looking at.
ax1.text(10500.0, 1.67, "Euro-to-Dollar Trend From 1999-2022", size=14, weight='bold')
ax1.text(10500.0, 1.62, "The US Dollar was weakest during the 2008 Recession when rates were low", size=12)

# We remove the ytick labels and replace them with our own values to maximize the data-to-ink ratio.
ax1.set_yticklabels([])
y = 1.0
for label in ['1.0', '1.1', '1.2', '1.3', '1.4', '1.5']:
     ax1.text(9970.0, y, label, alpha=0.5, size=10)
     y += 0.1

# We now create a shaded area to highlight the period that roughly illustrates the 2008 Recession
ax1.axvspan(xmin=13150.0, xmax=14610.0, ymin=0.09, alpha=0.3, color='grey')

# We now layer a line in red over the blue line during the Recession time frame using our recession dataframe.
ax1.plot(recession['Time'], recession['rolling_mean'], color='#af0b1e', linewidth=2.0)

# Creates some space between our top and bottom graphs.
plt.subplots_adjust(hspace=0.6)

# We now plot the EUR/USD 30day rolling average from 2016 to 2022. We use the color green for that line.
ax2.plot(not_pandemic['Time'], not_pandemic['rolling_mean'], color='#A6D785', linewidth=1.5)

# Similar to above, we give it a title and subtitle to explain what we are looking at.
ax2.text(16750.0, 1.28, 'Euro-to-Dollar Trend During the Pandemic', size=14, weight='bold')
ax2.text(16750.0, 1.265, 'The USD weakened due to rates dropping from pandemic stimulus', size=12)

# We remove the x and y tick labels to maximize our data-to-ink ratio.
ax2.set_xticklabels([])
ax2.set_yticklabels([])

# We replace our tick labels.
x = 16772.5
for year in ['2016', '2018', '2020', '2022']:
     ax2.text(x, 1.03, year, alpha=0.6, size=12)
     x += 730
y = 1.055
for value in ['1.05', '1.10', '1.15', '1.20']:
     ax2.text(16650.0, y, value, alpha=0.6, size=10)
     y += .05

# We then plot our pandemic-era 30day rolling average line in red over the green line.
ax2.plot(pandemic['Time'], pandemic['rolling_mean'], color='#af0b1e', linewidth=2.0)

# We highlight the period of time the roughly measures the length of the pandemic.
ax2.axvspan(xmin=18260.0, xmax=18990.0, ymin=0.09, color='grey', alpha=0.3)
plt.show()

# As one can see from the graph, whenever the FOMC attempts to stimulate the economy by slashing rates (evidenced by the
# Recession and Pandemic), the Euro grows very strong compared to the USD. However, it is also worth noting that during
# time of QT, notably at the beginning of 2022, the USD markedly strengthens against the Euro. 
