# Aadhaar Pulse – UIDAI Resident Lifecycle Dashboard

<div align="center">

🇮🇳 **Indian Emblem** | **Aadhaar Logo**

**Mission:** Unlock societal trends in Aadhaar enrolment and updates by fusing migration intensity, biometric lag, and digital penetration signals into a real-time "command center" for UIDAI field and policy teams.

</div>

---

## 📌 Highlights

- **Authoritative UI**: Streamlit dashboard skinned as an official UIDAI portal with the Indian emblem, Aadhaar branding, textured background, and gov-style KPI cards.
- **Smart analytics**: Winsorized metrics, dual-risk scoring, and a rule-based AI assistant that answers questions about risks, states, and definitions.
- **Actionable visuals**: Migration treemap, risk matrix, digital divide heatmap, and raw-data explorer with CSV export.
- **Submission-ready PDF**: `scripts/generate_uidai_report.py` generates a comprehensive report (Problem → Data → Methodology → Insights → Code) with embedded charts.

---

## 🗂️ Repository Structure

```
UIDAI-hackathon-/
├─ app.py                          # Streamlit dashboard
├─ scripts/
│   └─ generate_uidai_report.py    # PDF report builder (Pandas + Matplotlib + ReportLab)
├─ src/
│   └─ data_engineering.py         # Data prep utilities
├─ artifacts/
│   ├─ final_master_data.csv       # Provided dataset (cleaned during load)
│   ├─ UIDAI_Pulse_Report.pdf      # Generated consolidated report
│   └─ report_assets/              # Charts embedded in the PDF
├─ requirements.txt                # Python dependencies
├─ .gitignore                      # Git ignore rules
└─ README.md                       # You are here
```

---

## ⚙️ Environment Setup

### 1. Clone the Repository

```bash
git clone <this-repo>
cd uidai--1
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Run the Portal

Launch the Streamlit dashboard:

```bash
python -m streamlit run app.py
```

The dashboard opens at **http://localhost:8501/**

### Sidebar Controls:
- **Region selector**: All India + individual states
- **Migration intensity slider**: 0–100%
- **Comparison mode toggle**
- **AI Chat assistant**: "Where is the highest risk?" / "Tell me about Kerala"
- **Download filtered CSV**

---

## 📊 Dashboard Tabs

### 🌍 Migration Monitor
Treemap visualizing enrolment volume and migration stress.

### ⚠️ Risk Assessment
Bubble matrix (Migration vs Biometric Lag, sized by risk score, colored by digital penetration).

### 📉 Digital Divide
Highlights districts with lowest mobile linkage.

### 🗂️ Raw Data
Filtered dataframe + CSV export button.

---

## 🧽 Data Pipeline & Cleaning

The `app.py` performs comprehensive data cleaning:

| Step | Description |
|------|-------------|
| **State/District Normalization** | Upper-cased states, Title-cased districts, removed placeholder numeric rows |
| **Ghost District Removal** | Dropped rows with Total_Enrolment ≤ 100 |
| **Winsorization** | Migration_Intensity, Biometric_Lag, Digital_Penetration capped at 100% |
| **Risk Score** | Derived as (Migration_Intensity × Biometric_Lag) / 100 |
| **Visual Columns** | KPI cards, charts, and assistant all consume the cleaned dataset |

---

## 📑 Generate the Consolidated PDF

Generate a comprehensive report with insights and visualizations:

```bash
python scripts/generate_uidai_report.py
```

**Outputs:**
- `artifacts/UIDAI_Pulse_Report.pdf`
  - Sections: Problem Statement & Approach, Dataset, Methodology, Insights & Visuals, Code & Reproducibility
- `artifacts/report_assets/` - Charts: `top_states.png`, `risk_scatter.png` (embedded in the PDF)

Use this PDF for hackathon submissions or stakeholder briefings.

---

## 💡 Key Insights (Sample)

1. **Dual-risk hotspots**: ~32% of districts exceed both 70% migration intensity and 70% biometric lag → deploy mobile enrolment kits + compliance supervisors.

2. **Correlation**: Migration intensity vs biometric lag ρ ≈ 0.42 – migrating populations strain biometric queues without proactive staffing.

3. **Digital dark spots**: Bottom 5 states have <35% digital penetration; need IVRS reminders, offline grievance desks, and assisted Aadhaar updates.

---

## 🛠 Tech Stack

| Layer | Tools |
|-------|-------|
| **Dashboard** | Streamlit, Plotly Express, Custom CSS |
| **Data** | Pandas, cached loading, winsorization |
| **AI Assistant** | Rule-based NLP (keywords + correlations) |
| **Reporting** | Pandas, Matplotlib, ReportLab PDF |
| **Styling** | UIDAI branding, Indian Emblem, Aadhaar logo, textured backgrounds |

---

## 🤖 AI Assistant Features

The built-in AI assistant can answer questions like:

- **"Where is the highest risk?"** - Shows top 5 risk districts
- **"Digital divide"** - Shows areas with low digital penetration
- **"Migration in [State]"** - State-specific migration stats
- **"Correlation"** - Shows metric correlations
- **"Help"** - Lists all available commands

---

## 📥 Data Requirements

Place your dataset at: `artifacts/final_master_data.csv`

**Required columns:**
- `State` - State name
- `District` - District name
- `Total_Enrolment` - Total Aadhaar enrolments
- `Migration_Intensity` - Migration percentage (0-100)
- `Biometric_Lag` - Biometric update lag percentage (0-100)
- `Digital_Penetration` - Digital adoption percentage (0-100)
- `Mobile_Linkage_Rate` - Mobile number linkage percentage (0-100)
- `Update_Frequency` - Update frequency percentage (0-100)

**Note:** If the dataset is missing, the app will generate sample data for demonstration purposes.

---

## 🎯 Actionable Recommendations

### Immediate Actions (0-3 months)
1. Deploy mobile enrolment kits to dual-risk districts
2. Launch biometric update camps in districts with >70% biometric lag
3. Establish 24/7 helplines in low-digital-penetration states

### Medium-term Initiatives (3-12 months)
1. Implement predictive migration models using historical data
2. Scale IVRS reminder systems for non-smartphone users
3. Partner with CSCs (Common Service Centers) for assisted updates

### Long-term Strategic Goals (1-3 years)
1. Build AI-powered risk forecasting into UIDAI operations
2. Create state-wise best practice repositories for knowledge sharing
3. Integrate IoT sensors at enrolment centers for real-time queue management

---

## 🤝 Authors & Credits

- **Team**: Aadhaar Pulse Analytics
- **Dataset**: UIDAI-provided enrolment/update extracts
- **Logos**: Government of India (Emblem) & UIDAI Aadhaar (used under fair policy reference)

For questions or enhancements, open an issue or contact the maintainers.

---

## 📄 License

This project is created for educational and hackathon purposes. All data handling complies with UIDAI guidelines and data protection regulations.

---

<div align="center">

**"From field logistics to policy intelligence, Aadhaar Pulse equips UIDAI teams with a single surveillance lens on migration, compliance, and digital readiness."**

🇮🇳 Made with ❤️ for Digital India

</div>