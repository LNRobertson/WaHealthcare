# WaHealthcare

Preidcting provider complaints with public data. 


#### -- Project Status: [Active / InProgress] 

[(Table of Contents)](#table-of-contents)

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/Ileriayo/markdown-badges/blob/b9bb4c77516e158af331c0a6e1b2f81e8fd22aa1/LICENSE)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)

<br>

## Project Intro/Objective

<br>

--------
Table of Contents
------------
- [Project Intro/Objective](#project-introobjective)
- [Project Organization](#project-organization)


Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    ├── environment.yml    <- The requirements file for reproducing the analysis environment,         
    │                         e.g.generated with `pip freeze > requirements.txt`
    ├── app                        
    │
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   ├── raw            <- The original, immutable data dump.
    │   ├── sqlite         <- Load flat files
    │   ├── ETL            <- Create view and query data
    ├── docs v             <- A default Sphinx project; see sphinx-doc.org for details
    │ 
    ├── expirementation    <- Strategy development
    │ 
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │ 
    ├── src                <- Source code for use in this project.API & Feature Engineering
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py│   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │ 
    ├── tests              <- API and feature engineering
    │ 
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io
