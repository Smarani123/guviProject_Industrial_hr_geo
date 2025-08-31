# Industrial Human Resource Geo-Visualization

**Goal**: Update and visualize industrial classification of main and marginal workers (Census 2011 NIC) by state, sex, area, and industry cluster using NLP grouping. Build an interactive Streamlit dashboard with Plotly.

## Project Structure
```
industrial_hr_geo_vis/
├─ data/                    # raw CSVs + merged_industrial_workers.csv
├─ src/
│  ├─ data_loader.py        # robust CSV loader/merger + NLP grouping
│  └─ utils.py              # helpers (PEP8 compliant)
├─ app/
│  └─ streamlit_app.py      # Streamlit dashboard
├─ docs/                    # exported EDA charts
├─ requirements.txt
└─ README.md
```

## Quickstart
```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

## EDA Highlights
- Top states by **main workers** include West Bengal and Rajasthan.
- Dominant groupings include **Construction**, **Retail**, and **Education & Health**.
- Included charts in `docs/` and an aggregated CSV `data/merged_industrial_workers.csv`.

## Notes
- NLP grouping uses simple keyword rules over `nic_name`. You can refine rules in `src/utils.py`.
- All code is modular and PEP8-friendly.
