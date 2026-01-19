# Aadhaar Pulse - Quick Start Guide

## 🚀 Getting Started

### Option 1: Using the Run Script (Recommended)

```bash
./run.sh
```

This will automatically:
- Set up the virtual environment
- Install dependencies
- Launch the dashboard

### Option 2: Manual Setup

```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the dashboard
python -m streamlit run app.py
```

### Option 3: Generate PDF Report Only

```bash
source .venv/bin/activate
python scripts/generate_uidai_report.py
```

---

## 📊 Dashboard Features

### **Sidebar Controls**

1. **Region Selection**
   - Select "All India" for nationwide view
   - Choose specific states for focused analysis

2. **Migration Filter**
   - Adjust slider to filter districts by migration intensity (0-100%)

3. **Analysis Mode**
   - Enable "State Comparison" for side-by-side analysis

4. **AI Assistant**
   - Ask natural language questions:
     - "Where is the highest risk?"
     - "Digital divide"
     - "Migration in Maharashtra"
     - "Correlation"
     - "Help"

5. **Export Data**
   - Click "Download Filtered CSV" to export current view

---

## 📋 Dashboard Tabs

### 🌍 **Tab 1: Migration Monitor**
- **Treemap Visualization**: Shows enrolment volume and migration stress
- **Top 10 Districts**: Lists areas with highest migration intensity
- **Use Case**: Identify regions requiring mobile enrolment units

### ⚠️ **Tab 2: Risk Assessment**
- **Dual-Risk Matrix**: Scatter plot of Migration vs Biometric Lag
- **Critical Alerts**: Highlights districts exceeding 70% threshold on both metrics
- **Use Case**: Prioritize resource deployment and compliance teams

### 📉 **Tab 3: Digital Divide**
- **State-level Bar Chart**: Average digital penetration by state
- **Bottom 5 States**: Digital dark spots requiring intervention
- **Use Case**: Plan IVRS systems and offline assistance programs

### 🗂️ **Tab 4: Raw Data**
- **Searchable Table**: Filter and explore complete dataset
- **Pagination**: View 10-100 rows at a time
- **Export**: Download filtered data in CSV format
- **Use Case**: Detailed analysis and custom reporting

---

## 🤖 AI Assistant Commands

| Query | Response |
|-------|----------|
| "highest risk" | Shows top 5 districts by risk score |
| "digital divide" | Shows bottom 5 districts in digital penetration |
| "migration in [State]" | State-specific migration statistics |
| "correlation" | Shows correlation matrix between metrics |
| "help" | Lists all available commands |

---

## 📈 Understanding the Metrics

### **Migration Intensity (%)**
- Measures population mobility in a district
- **High (>70%)**: Requires mobile enrolment units
- **Medium (40-70%)**: Standard monitoring
- **Low (<40%)**: Stable population

### **Biometric Lag (%)**
- Percentage of residents with outdated biometric data
- **Critical (>70%)**: Deploy update camps immediately
- **Warning (50-70%)**: Schedule regular updates
- **Good (<50%)**: Maintain current processes

### **Risk Score**
- Formula: `(Migration Intensity × Biometric Lag) / 100`
- **Critical (>70)**: Immediate intervention needed
- **High (50-70)**: Priority monitoring
- **Medium (30-50)**: Regular review
- **Low (<30)**: Standard operations

### **Digital Penetration (%)**
- Measures mobile linkage and digital service adoption
- **Good (>70%)**: Digital-first approach viable
- **Medium (50-70%)**: Hybrid approach needed
- **Low (<50%)**: Focus on offline channels

---

## 📑 Generating the PDF Report

The comprehensive PDF report includes:
- Problem Statement & Approach
- Dataset Overview & Statistics
- Methodology & Data Pipeline
- Key Insights with Visualizations
- Actionable Recommendations
- Code & Reproducibility Section

### Generate Report:

```bash
source .venv/bin/activate
python scripts/generate_uidai_report.py
```

**Output Locations:**
- PDF Report: `artifacts/UIDAI_Pulse_Report.pdf`
- Charts: `artifacts/report_assets/`

---

## 🎯 Common Use Cases

### **Use Case 1: Emergency Resource Allocation**

**Scenario**: UIDAI needs to deploy 50 mobile enrolment kits urgently.

**Steps**:
1. Open dashboard
2. Go to "Risk Assessment" tab
3. Review districts in red zone (top-right quadrant)
4. Use AI Assistant: "Where is the highest risk?"
5. Export top 50 districts using "Download CSV"
6. Share with field teams

---

### **Use Case 2: State-level Performance Review**

**Scenario**: Monthly review meeting with state coordinators.

**Steps**:
1. Select specific state from sidebar
2. Review all 4 tabs for comprehensive overview
3. Use AI Assistant: "Migration in [State Name]"
4. Generate PDF report for documentation
5. Share insights with stakeholders

---

### **Use Case 3: Digital Penetration Campaign**

**Scenario**: Planning awareness campaigns for low-digital states.

**Steps**:
1. Go to "Digital Divide" tab
2. Identify bottom 5 states
3. Filter by each state to see district-level data
4. Export CSV for each state
5. Plan IVRS and offline grievance mechanisms

---

## 🔧 Troubleshooting

### Dashboard Won't Start

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Try running on different port
streamlit run app.py --server.port 8502
```

### Data Not Loading

- Ensure `artifacts/final_master_data.csv` exists
- Check file format matches required columns
- Review console for error messages

### Charts Not Displaying

```bash
# Install/update visualization libraries
pip install --upgrade plotly matplotlib seaborn
```

### PDF Generation Fails

```bash
# Install reportlab separately
pip install --upgrade reportlab pillow
```

---

## 📥 Data Format Requirements

Your CSV file should have these columns:

```csv
State,District,Total_Enrolment,Migration_Intensity,Biometric_Lag,Digital_Penetration,Mobile_Linkage_Rate,Update_Frequency
MAHARASHTRA,Mumbai,2500000,85.4,72.3,89.5,92.1,45.2
```

**Column Definitions:**
- `State`: State name (will be converted to UPPERCASE)
- `District`: District name (will be converted to Title Case)
- `Total_Enrolment`: Number of Aadhaar registrations (integer)
- `Migration_Intensity`: 0-100 percentage
- `Biometric_Lag`: 0-100 percentage
- `Digital_Penetration`: 0-100 percentage
- `Mobile_Linkage_Rate`: 0-100 percentage
- `Update_Frequency`: 0-100 percentage

---

## 🔐 Security & Compliance

- All data is processed locally
- No external API calls for data processing
- CSV exports contain only filtered data
- Follow UIDAI data handling guidelines
- Ensure proper access controls on exported files

---

## 📞 Support & Feedback

For issues, enhancements, or questions:
1. Check the troubleshooting section above
2. Review the README.md file
3. Open an issue in the repository
4. Contact the Aadhaar Pulse Analytics team

---

## 🎓 Best Practices

### For Dashboard Users:
1. **Start Broad**: Begin with "All India" view, then drill down
2. **Use Filters**: Leverage migration slider to focus on specific ranges
3. **Export Often**: Download data for offline analysis
4. **Ask Questions**: Use AI Assistant for quick insights

### For Policy Teams:
1. **Regular Reviews**: Weekly dashboard reviews recommended
2. **PDF Reports**: Generate monthly reports for documentation
3. **Trend Analysis**: Compare data over time periods
4. **Stakeholder Sharing**: Use exported CSVs for presentations

### For Field Teams:
1. **Risk Priority**: Focus on Critical risk districts first
2. **State Focus**: Use state filters for regional operations
3. **Mobile First**: Check migration treemap for deployment planning
4. **Digital Gaps**: Review digital divide tab for training needs

---

## 📊 Sample Queries & Interpretations

### Query: "Where is the highest risk?"
**Interpretation**: Shows districts requiring immediate attention. These districts likely have high migration AND high biometric lag.

**Action Items**:
- Deploy mobile enrolment kits
- Schedule biometric update camps
- Assign compliance supervisors

---

### Query: "Digital divide"
**Interpretation**: Shows districts with lowest digital penetration. Residents may struggle with online services.

**Action Items**:
- Set up IVRS reminder systems
- Establish offline grievance desks
- Train staff for assisted updates
- Partner with local CSCs

---

### Query: "Migration in Maharashtra"
**Interpretation**: Provides Maharashtra-specific migration statistics including average intensity and number of high-migration districts.

**Action Items**:
- Review state-level resource allocation
- Compare with neighboring states
- Plan capacity expansion if needed

---

## 🎯 Performance Tips

### For Faster Dashboard Loading:
1. **Filter Early**: Use sidebar filters before exploring tabs
2. **Limit Data**: Work with state-level data when possible
3. **Close Unused Tabs**: Focus on one tab at a time
4. **Cache Clearing**: Restart dashboard if performance degrades

### For Large Datasets:
1. **Pre-filter CSV**: Remove unnecessary columns/rows before loading
2. **Use Pagination**: In Raw Data tab, limit rows per page
3. **Export Subsets**: Download filtered data rather than full dataset

---

## 📚 Additional Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Plotly Visualization**: https://plotly.com/python/
- **Pandas Guide**: https://pandas.pydata.org/docs/
- **UIDAI Website**: https://uidai.gov.in

---

## 🔄 Updates & Maintenance

### Updating Dependencies:

```bash
source .venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Pulling Latest Code:

```bash
git pull origin main
pip install -r requirements.txt
```

---

<div align="center">

**Happy Analyzing! 🇮🇳**

*"From field logistics to policy intelligence, Aadhaar Pulse equips UIDAI teams with a single surveillance lens."*

</div>
