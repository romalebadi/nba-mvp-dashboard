# NBA MVP Dashboard

An interactive dashboard comparing NBA MVP and runner-up stats over the past 40+ years.

## Features
- **40+ seasons** of MVP vs runner-up stat comparisons
- **Line charts** tracking any stat across all seasons
- **Head-to-head breakdown** with stat differences for any selected season
- **Radar chart** visual comparison between MVP and runner-up
- **Greatest MVP season ever** ranking using a composite score
- **Team win % with vs without MVP** on the court

## Tech Stack
- Python
- Streamlit
- Plotly
- nba_api
- BeautifulSoup (Basketball Reference scraper)
- pandas

## How to Run

1. Install dependencies:
```
pip install nba_api streamlit pandas plotly scikit-learn beautifulsoup4 requests
```

2. Run the data pipeline in `NBA.ipynb` to generate the CSV files

3. Launch the dashboard:
```
streamlit run app.py
```

## Data Sources
- NBA stats via [nba_api](https://github.com/swar/nba_api)
- MVP history scraped from [Basketball Reference](https://www.basketball-reference.com)