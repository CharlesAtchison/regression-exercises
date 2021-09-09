import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import combinations

from scipy.stats import pearsonr, spearmanr


def plot_variable_pairs(df, save=False):
    '''Takes df and returns relplot, lmplot and jointplot for all 2 pair combinations, returns a markdown text
    set save=True if you'd like to save the figures (this defaults to False so you don't overwrite anything)
    '''
    
    # Create all 2 axis combinations from the dataframe
    all_combs = set(list(combinations(df.columns, 2)))
    
    result_list = list()
    
    for n, comb in enumerate(all_combs):
        
        # Change the value to the number of plots you'd like to include in each row
        num_of_plots = 3
        fig_row = n // num_of_plots
        
        # set your x and y value
        x = comb[0]
        y = comb[1]
        print('Plotting: ', x, y)
        
        # stores resulting images in dict
        temp_dict = dict()
        
        # Create Relplot
        plt1 = sns.relplot(x=x, y=y, data=df)
        # Set the title for relplot
        plt1.fig.suptitle(f'{x} v {y} Relplot')
        # Save Relplot to images folder
        if save:
            plt.savefig(f'images/{x}_v_{y}_0.png')
        # Add relpot to the temp list to be added to the df dict at the end
        temp_dict['<center>relplot</center>'] =  f'![{x}_v_{y}relplot](images/{x}_v_{y}_0.png)'
        
        # Create Lmplot
        plt2 = sns.lmplot(x=x, y=y, data=df, line_kws={'color': 'red'})
        # Set title for lmplot
        plt2.fig.suptitle(f'{x} v {y} Lmplot')
        # Save the Lmplot to images folder
        if save:
            plt.savefig(f'images/{x}_v_{y}_1.png')
        # Add lmplot to the temp list to be added to the df dict at the end
        temp_dict['<center>lmplot</center>'] =  f'![{x}_v_{y}lmplot](images/{x}_v_{y}_1.png)'
        
        # Create Jointplot
        plt3 = sns.jointplot(x=x, y=y, data=df, kind='reg', height=5, line_kws={'color': 'red'})
        # Set the title for jointplot
        plt3.fig.suptitle(f'{x} v {y} Jointplot')
        # Save the jointplot to images folder
        if save:
            plt.savefig(f'images/{x}_v_{y}_2.png')
        # add joinplot to temp_list to e added to the df dict at end
        temp_dict['<center>jointplot</center>'] =  f'![{x}_v_{y}jointplot](images/{x}_v_{y}_2.png)'
        
        # Add temp_dict to define the row and add to df list 
        result_list.append(temp_dict)
    
    # Convert the list of dicts to a pd.DataFrame and set the index to the 1st col
    result = pd.DataFrame(result_list).set_index('<center>relplot</center>')
    
    # Return result as markdown to be pasted in markdown.
    return result.to_markdown()

def plot_categorical_and_continuous_vars(df, categorical, continuous, save=False):
    '''Takes df, categorical & continuous list names and returns markdown text and figures for all combinations of the two
    set save=True if you'd like to save the figures (this defaults to False so you don't overwrite anything)
    '''
    
    # Create all 2 axis combinations from the dataframe
    all_combs = [(cat, cont) for cat in categorical for cont in continuous]
    
    result_list = list()
    
    for n, comb in enumerate(all_combs):
        
        # Change the value to the number of plots you'd like to include in each row
        num_of_plots = 3
        fig_row = n // num_of_plots
        
        # set your x and y value
        x = comb[0]
        y = comb[1]
        print('Plotting: ', x, y)
        
        # stores resulting images in dict
        temp_dict = dict()
        
        # Create Boxenplot
        plt1 = sns.catplot(x=x, y=y, data=df, kind='boxen')
        # Set the title for Boxen
        plt1.fig.suptitle(f'{x} v {y} Boxen Plot')
        # Save Boxen to images folder
        if save:
            plt.savefig(f'images/boxen{x}_v_{y}_0.png')
        # Add relpot to the temp list to be added to the df dict at the end
        temp_dict['<center>Boxen</center>'] =  f'![{x}_v_{y}boxen](images/boxen{x}_v_{y}_0.png)'

        # Create Violinplot
        plt1 = sns.catplot(x=x, y=y, data=df, kind='violin')
        # Set the title for relplot
        plt1.fig.suptitle(f'{x} v {y} Violin Plot')
        # Save Relplot to images folder
        if save:
            plt.savefig(f'images/violin{x}_v_{y}_0.png')
        # Add relpot to the temp list to be added to the df dict at the end
        temp_dict['<center>Violin</center>'] =  f'![{x}_v_{y}violin](images/violin{x}_v_{y}_0.png)'

        # Create Barplot
        plt1 = sns.catplot(x=x, y=y, data=df, kind='bar')
        # Set the title for bar
        plt1.fig.suptitle(f'{x} v {y} Bar Plot')
        # Save Bar to images folder
        if save:
            plt.savefig(f'images/bar{x}_v_{y}_0.png')
        # Add relpot to the temp list to be added to the df dict at the end
        temp_dict['<center>Bar</center>'] =  f'![{x}_v_{y}bar](images/bar{x}_v_{y}_0.png)'
        
        # Add temp_dict to define the row and add to df list 
        result_list.append(temp_dict)
    
    # Convert the list of dicts to a pd.DataFrame and set the index to the 1st col
    result = pd.DataFrame(result_list).set_index('<center>Violin</center>')
    
    # Return result as markdown to be pasted in markdown.
    return result.to_markdown()