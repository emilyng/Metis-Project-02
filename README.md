# Social Progress Index

### Goal of project is to predict Social Progress Index using different macroeconomic indicators, gov't expenditures, and energy usages of a country. I am interested in finding the features that would help raise a higher SPI. 

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
