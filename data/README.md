# Data 

## Available Data
- `pv_muni_params.csv` - Main dataset used in this study. It has the data for electricity demand, available land, land value, solar PV capacity, solar PV generation, and solar PV Penetration Rate.

## Sources

- Japan Adminstrative Region
    - Source: [National Land Numerical Information](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-v3_1.html)
    - Filename: [N03-20230101_GML.zip](https://nlftp.mlit.go.jp/ksj/gml/data/N03/N03-2023/N03-20230101_GML.zip)
    - Processing: Simplified to reduce file size
- Japan Statistical Data
    - Sources: Japan e-Stat: [Municipal](https://www.e-stat.go.jp/en/regional-statistics/ssdsview/municipality), [Prefectural](https://www.e-stat.go.jp/en/regional-statistics/ssdsview/prefectures)
    - Data: Habitable Area [B1103], Building Land [B120103], Cultivated Lad [C3107], Taxable Income [C120110], Land Value [C5401]
- Solar PV Penetration Rate
    - Source: [Organization for Cross-regional Coordination of Transmission Operators(OCCTO)](https://www.occto.or.jp/keitoujouhou/)
    - Processing: Data is taken from each electric power company
- Solar PV Power Generation
    - Source: [PyPSA Atlite](https://atlite.readthedocs.io/en/latest/)
    - Processing: Extracted annual power generation [kWh/kW] for Japan in 2020 using ERA5 dataset. 
- Installed PV Capacity in Japan
    - Source: Agency for Natural Resources and Energy - [FIT/FIP Website](https://www.fit-portal.go.jp/PublicInfoSummary)
    - Processing: Data at the end of each year (December) were extracted.
- Electricity Demand in Japan
    - Source: Agency for Natural Resources and Energy - [Energy Statistics](https://www.enecho.meti.go.jp/statistics/electric_power/ep002/xls/2022/6-2-2022.xlsx)
    - Processing: Annual Data was extracted



