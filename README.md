# Nassau Candy Distributor — Shipping Route Efficiency Analysis

## Project Overview
An interactive data analytics project that evaluates factory-to-customer shipping routes, shipment lead times, shipping modes, and regional performance for Nassau Candy Distributor.

## Objectives
- Analyze shipping lead times and shipment volumes.
- Compare shipping performance across shipping modes and regions.
- Identify routes with relatively higher and lower lead times.
- Explore geographic patterns and potential shipping bottlenecks.
- Present findings through an interactive Streamlit dashboard.

## Key Features
- Interactive filters for region, shipping mode, date range, and delay threshold.
- KPI metrics and shipping performance visualizations.
- Factory-to-customer route analysis.
- State-level and regional shipping analysis.
- Exploratory data analysis using Python.

## Tech Stack
- Python
- Pandas and NumPy
- Plotly
- Streamlit
- Jupyter Notebook

## Project Files
- `app2.py` — interactive Streamlit dashboard
- `analysis.ipynb` — exploratory data analysis and calculations
- `Research_Paper.docx` — project methodology, findings, and limitations
- `Executive_Summary.docx` — concise project summary
- `requirements.txt` — Python dependencies
- `map.png` — project map visualization

## Run Locally
1. Clone this repository.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Ensure the processed dataset is available at `data/processed_shipping_data.csv`.
4. Launch the dashboard:
   `streamlit run app2.py`

## Data Note
The dataset is excluded from this repository pending verification of redistribution permission. The dashboard requires the processed dataset to run. Shipping lead times are calculated from the dates supplied in the source dataset; unusual date ranges and the provisional delay threshold should be considered when interpreting results.

## Limitations
The route map represents approximate geographic connections rather than verified road routes. Results depend on the quality and consistency of the supplied dataset.

## Author
Pranav Shukla