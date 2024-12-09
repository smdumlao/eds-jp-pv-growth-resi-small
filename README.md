
# Japan’s Local Consumption of Solar Energy: The Role of Energy Demand in Residential and Small-scale Solar Projects

## Abstract

Japan's commitment to achieving net-zero emissions by 2050 includes a target for solar photovoltaic (PV) to generate 14-16% of the nation's electricity by 2030, as outlined in the Sixth Strategic Energy Plan. To support the potential contributions of ordinary citizens, this research analyzes the factors influencing the deployment of residential and small-scale solar PV systems in Japanese municipalities, providing local government units with data-driven insights to formulate strategies for expanding solar energy. A Random Forest Regression model assesses each factor's impact on municipal solar PV capacity share. SHAP values highlight feature importance and visualize the most influential independent variables. Results indicate that local energy demand is the primary driver of solar PV installations. For residential systems, economic factors such as taxable income serve as secondary drivers, while high land values impede growth. In the case of small-scale installations, land availability becomes a critical limiting factor, particularly in regions with limited land, even when energy demand remains high. The study demonstrates that proactive local governments can overcome economic and land-use challenges through targeted subsidies, strategic partnerships, innovative use of public spaces, and strict enforcement of land-use regulations. By highlighting the significance of local energy demand and citizen involvement, this study offers valuable insights for policymakers to prioritize areas with lower energy demand and implement targeted supportive policies, thereby fostering a more balanced distribution of solar PV installations. Japan's case may serve as a reference for optimizing solar PV deployment strategies globally, contributing to the broader discourse on small-scale renewable energy expansion. 

## Supplementary Data

This repository contains the Jupyter notebooks, configuration files, and documentation necessary to replicate the analyses performed in this study.

## Notebooks

The following Jupyter notebooks were used for the analysis and modeling conducted in this study:

- [00-introduction-demand-pv-visualization](https://nbviewer.org/github/smdumlao/eds-jp-pv-growth-resi-small/blob/main/00-introduction-demand-pv-visualization.ipynb) - Visualization of the data for the introduction and methodology
- [01-eda.ipynb](https://nbviewer.org/github/smdumlao/eds-jp-pv-growth-resi-small/blob/main/01-eda.ipynb) – Initial exploratory data analysis (EDA).
- [02-extract-outlier.ipynb](https://nbviewer.org/github/smdumlao/eds-jp-pv-growth-resi-small/blob/main/02-extract-outlier.ipynb) – Random Forest Regression and Outlier Extraction.
- [03a-shap-residential.ipynb](https://nbviewer.org/github/smdumlao/eds-jp-pv-growth-resi-small/blob/main/03a-shap-residential.ipynb) – SHAP analysis for residential-scale solar projects.
- [03b-shap-small.ipynb](https://nbviewer.org/github/smdumlao/eds-jp-pv-growth-resi-small/blob/main/03b-shap-small.ipynb) – SHAP analysis for small-scale solar projects.
- [04-proactive-outlier-sel.ipynb](https://nbviewer.org/github/smdumlao/eds-jp-pv-growth-resi-small/blob/main/04-proactive-outlier-sel.ipynb) – Proactive selection of outliers for further analysis.

## Python Packages

To run the notebooks, please create a virtual environment and install the necessary Python packages:

```bash
pip install -r requirements.txt
```

## Data

The following files are necessary to run the notebooks:

- data/pv_muni_params.csv
- data/japanadmincode.csv
- data/map/jp_map_simple.geojson

**Optional Files:**

- data/map/W09-05-g_Lake.shp
- data/map/W09-05-g_Lake.shx

Please download the lake GIS files from [National Land Numerical Information](https://nlftp.mlit.go.jp/ksj/gml/data/W09/W09-05/W09-05_GML.zip) and extract them into the `data/map` folder.