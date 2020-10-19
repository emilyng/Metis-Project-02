# Social Progress Index

## Inadequacies of GDP
GDP has been a long-serving measure for economists to indicate the success of a country. However, it fails to capture overall societal progress. It treats all types of spending the same and ignores the costs of consequences. [Social Progress Imperative](https://www.socialprogress.org/) created the Social Progress Index (SPI) as a new way to measure genuine wellbeing of a country. 

## GDP and SPI Correlation
Although economic factors don’t go directly into SPI, there is a strong correlation between GDP and SPI. 
However, a large GDP does not guarantee a high SPI. In fact, Costa Rica, the United States, and Singapore have similar SPIs but have a wide range of GDPs. 

![GDPvSPI_2019](https://raw.githubusercontent.com/emilyng/Social_Progress_Index/master/Plots/GDPvSPI_2019.svg)

From 2014-2019, the United States have been steadily increasing in GDP per capita while decreasing in SPI. In fact, the US showed to have the 2nd biggest **decrease** in SPI during this time frame. 

![US_increasing_GDP_line](https://raw.githubusercontent.com/emilyng/Social_Progress_Index/master/Plots/US_GDP.svg)


|     Top   Decreasing Countries    |     SPI   ‘19-’14 Difference    |
|-----------------------------------|:-------------------------------:|
|                      Nicaragua    |               -2.73             |
|                United   States    |               -1.12             |
|                         Brazil    |               -0.72             |
|                        Hungary    |               -0.32             |
|                       Columbia    |               -0.25             |


### The goal of project is to predict Social Progress Index using different macroeconomic indicators, gov't expenditures, and energy usages of a country as a way to gain an insight on how and what factors influence SPI. 

## Technicals
~Project is separated into 2 distinct parts: web scraping section and modeling section. ~

### For web scraping portion, execute:
```python write_files.py```
to run the code for multiple world factbook .json files taken from iancoleman.io/exploring-the-cia-world-factbook and his github repo on CIA World Factbook unofficial API. 

It will write out .csv files for each file name defined in ```write_files.py```. Each file corresponds to a specfic time the world factbook was scrapped by iancoleman. Calls in ```Scrape.py``` and ```ColumnNames.py``` to retrieve specified elements from webpage. 

### Cleaning Data.ipynb
```Cleaning Data.ipynb``` cleans out all data by filling in missing values with interpolation and backfilling. It then filters out only specified years of interest (2013-2018 for this project) and groups each feature dataset into a pivot table and pickles it. 

### Merging Data.ipynb
```Merging Data.ipynb``` compiles and merges all separate datasets into one full dataframe containing all features and target and stores it into a pickle object. 

### EDA + Plots.ipynb
```EDA + Plots.ipynb``` does some exploratory data analysis on full dataset and contains some useful plots. 

### Modeling.ipynb
```Modeling.ipynb``` contains all steps in the modeling process including different approaches to finding the best model using sklearn and train_test_split. It also contains some modelign using statsmodels, but is not used in final model. It tests out simple linear models, ridge models, lasso models, and polynomial regressions. In the ```CONCLUSION: FINAL TEST SCORES (using Linear Model)``` section of the notebook is the final best model, r_score and other metrics as well as resulting coefficients from linear regression. This model is pickled as best_fit_model.pkl.

Metis-Project-02 Presentation powerpoint is saved as pdf in this repo.
