import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

###################### INFO ##############################

#This script works assuming a database is made, where the data is made up of alternating columns of time and current for repeated potential step experiments.
#The script will select only the negative data points corresponding to the reduction, then perform an integration on each step to find the charge.
#All charges are finally combined in order to find the total charge for all depositions.

#Import data
data = pd.read_csv("Data.csv")

#Remove spaces from column titles
data.columns = data.columns.str.replace(' /', '_')

#define columns
cols = data.columns

#Find column titles
column_headers = list(data.columns.values)

#Select negative values
column_headers = list(data.columns.values)
pulse = data.query(column_headers[1]+' < 0')

#Make array for integration
no_cols = pulse.count(axis='columns') #counts the number of columns in the dataframe and exports the count per row into the dataframe 'no_cols'
max_cols = no_cols.iloc[0] #selects the first row value from 'no_cols'. all rows have the same no. values, so this is the total number of columns
t_array = np.arange(0,max_cols,2) #range of column numbers for all of the time columns
i_array = np.arange(1,max_cols,2) #as above for current

#Iteratively integrate through dataframe
integral_array = [] #make empty array
for i in range(len(t_array)):
    this_integral = np.trapz(pulse[cols[i_array[i]]], x=pulse[cols[t_array[i]]]) #integrate the nth current vs the nth time throughout the datagrame
    integral_array.append(this_integral) #append each integral to the master array

integral_total = np.sum(integral_array) #sum the array to get the total integral
integral_C = integral_total/1e6
print('Q = '+str(integral_total)+' \u03BCC = '+str(integral_C)+' C')


#Plot transients
fig, (ax0, ax1) = plt.subplots(2,1)
ax0.plot(data[cols[0]], data[cols[1]], label='data')
ax0.plot(pulse[cols[0]], pulse[cols[1]], label='integrated range')
for i in range(len(t_array)):#Plot all transients one on top of the other in the second sub plot
    ax1.plot(data[cols[t_array[i]]],data[cols[i_array[i]]])
ax0.set_xlabel("t / s")
ax0.set_ylabel("I / $\mu$A")
ax0.legend()
ax1.set_xlabel("t / s")
ax1.set_ylabel("I / $\mu$A")

fig.tight_layout()

plt.show()

print("Done")
