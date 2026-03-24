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

## Screenshots

![MVP vs Runner-Up 40 Years of Stats](screenshots/MVP%20vs.%20Runner-Up%20(40%20Years%20of%20Stats).png)
![Screenshot 2](screenshots/Screenshot%202026-03-23%20203527.png)
![Screenshot 3](screenshots/Screenshot%202026-03-23%20203539.png)
![Screenshot 4](screenshots/Screenshot%202026-03-23%20203551.png)
![Screenshot 5](screenshots/Screenshot%202026-03-23%20203603.png)
![Screenshot 6](screenshots/Screenshot%202026-03-23%20203620.png)
![Screenshot 7](screenshots/Screenshot%202026-03-23%20203652.png)
![Screenshot 8](screenshots/Screenshot%202026-03-23%20203707.png)
![Screenshot 9](screenshots/Screenshot%202026-03-23%20203720.png)