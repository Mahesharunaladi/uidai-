# Quick Reference Card - Aadhaar Pulse

## 🚀 One-Line Commands

### Start Dashboard
```bash
./run.sh
```
Opens at: http://localhost:8501

### Generate PDF Report
```bash
source .venv/bin/activate && python scripts/generate_uidai_report.py
```

### Install Dependencies
```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

---

## 📊 Dashboard Quick Guide

### Sidebar Filters
| Filter | Purpose | Range |
|--------|---------|-------|
| **Region** | Select state or All India | 20 states + All India |
| **Migration** | Filter by migration % | 0-100% slider |
| **Comparison** | Enable state comparison | Toggle checkbox |

### Tabs
1. **🌍 Migration Monitor** - Treemap + Top 10 list
2. **⚠️ Risk Assessment** - Scatter matrix + Alerts
3. **📉 Digital Divide** - State comparison + Bottom 5
4. **🗂️ Raw Data** - Table + CSV export

### AI Assistant Queries
- `"highest risk"` → Top 5 risk districts
- `"digital divide"` → Low digital penetration areas
- `"migration in [State]"` → State-specific stats
- `"correlation"` → Metric relationships
- `"help"` → Full command list

---

## 🎯 Key Metrics

### Risk Score Formula
```
Risk Score = (Migration Intensity × Biometric Lag) / 100
```

### Risk Categories
| Score | Category | Action Required |
|-------|----------|-----------------|
| 0-30 | Low | Standard monitoring |
| 30-50 | Medium | Regular review |
| 50-70 | High | Priority attention |
| 70-100 | Critical | Immediate intervention |

---

## 🔧 Common Tasks

### 1. Find High-Risk Districts
```
1. Go to "Risk Assessment" tab
2. Look for red zones (top-right quadrant)
3. Use AI: "Where is the highest risk?"
4. Export with "Download CSV"
```

### 2. State Performance Review
```
1. Select state from sidebar
2. Review all tabs
3. Note KPI changes
4. Generate PDF report
```

### 3. Export Data
```
1. Apply filters in sidebar
2. Go to "Raw Data" tab
3. Click "Download Filtered CSV"
```

---

## 📁 File Locations

| What | Where |
|------|-------|
| Dashboard | `app.py` |
| PDF Generator | `scripts/generate_uidai_report.py` |
| Data | `artifacts/final_master_data.csv` |
| PDF Output | `artifacts/UIDAI_Pulse_Report.pdf` |
| Charts | `artifacts/report_assets/` |

---

## 🆘 Quick Troubleshooting

### Dashboard won't start?
```bash
rm -rf .streamlit/cache
source .venv/bin/activate
streamlit run app.py
```

### Missing packages?
```bash
source .venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Port 8501 busy?
```bash
streamlit run app.py --server.port 8502
```

---

## 📞 Help

- **Full Documentation**: See `README.md`
- **Detailed Guide**: See `USAGE_GUIDE.md`
- **Project Summary**: See `PROJECT_SUMMARY.md`
- **Deployment**: See `DEPLOYMENT_CHECKLIST.md`

---

**Dashboard Status**: ✅ LIVE at http://localhost:8501

**Version**: 1.0.0 | **Date**: January 19, 2026
