# Aadhaar Pulse – UIDAI Resident Lifecycle Dashboard

<div align="center">

🇮🇳 **Indian Emblem** | **Aadhaar Logo**

**Mission:** Unlock societal trends in Aadhaar enrolment and updates by fusing migration intensity, biometric lag, and digital penetration signals into a real-time "command center" for UIDAI field and policy teams.

</div>

---

## 📌 Highlights

- **🔐 Secure Authentication System**: 
  - User login and registration with SHA-256 password encryption
  - Role-based access control (Admin, User, Analyst roles)
  - Session management with secure logout
  - JSON-based user database with credential protection
  
- **👥 Role-Based Permissions**:
  - **Admin**: Full access to all features, data export, analysis tools, and raw data explorer
  - **User**: Access to migration monitor and personalized dashboard with key metrics
  - **Analyst**: Configurable access based on organizational needs
  
- **🎨 Enhanced UI/UX**:
  - Official UIDAI portal styling with Indian emblem and Aadhaar branding
  - Crisp, readable typography with improved text rendering
  - White backgrounds with high-contrast black text for maximum visibility
  - Responsive treemap visualizations with clear district labels
  - Textured gradient backgrounds and government-style KPI cards
  
- **📊 Smart Analytics**: 
  - Winsorized metrics for data quality
  - Dual-risk scoring (Migration × Biometric Lag)
  - Rule-based AI assistant for natural language queries
  - State and district-level correlation analysis
  
- **📈 Interactive Visualizations**:
  - Migration intensity treemap with enrolment volume mapping
  - Risk assessment scatter plot with quadrant analysis
  - Digital divide heatmaps by state
  - Distribution histograms and top-N rankings
  
- **📄 Submission-Ready Reporting**: 
  - Automated PDF generation with `scripts/generate_uidai_report.py`
  - Comprehensive report structure: Problem → Data → Methodology → Insights → Code
  - Embedded charts and visual analytics

---

## 🗂️ Repository Structure

```
UIDAI-hackathon-/
├─ app.py                          # Streamlit dashboard with authentication & RBAC
├─ create_admin.py                 # Script to create initial admin users
├─ user_database.json              # User credentials database (auto-generated, encrypted)
├─ scripts/
│   └─ generate_uidai_report.py    # PDF report builder (Pandas + Matplotlib + ReportLab)
├─ src/
│   └─ data_engineering.py         # Data prep utilities
├─ artifacts/
│   ├─ final_master_data.csv       # Provided dataset (cleaned during load)
│   ├─ UIDAI_Pulse_Report.pdf      # Generated consolidated report
│   └─ report_assets/              # Charts embedded in the PDF
├─ requirements.txt                # Python dependencies
├─ run.sh                          # Quick launch script for the dashboard
├─ AUTH_README.md                  # Authentication system documentation
├─ AUTH_IMPLEMENTATION_SUMMARY.md  # Technical authentication details
├─ QUICK_START_AUTH.md             # Quick start guide for authentication
├─ RBAC_DOCUMENTATION.md           # Role-based access control guide
├─ PROJECT_SUMMARY.md              # Project overview and architecture
├─ USAGE_GUIDE.md                  # Detailed usage instructions
├─ QUICK_REFERENCE.md              # Quick reference for common tasks
├─ DEPLOYMENT_CHECKLIST.md         # Deployment preparation checklist
├─ .gitignore                      # Git ignore rules
└─ README.md                       # You are here
```

---

## 🔐 Quick Start - Login Credentials

### Default Admin Account:
- **Username:** `admin`
- **Password:** `admin123`
- **Role:** Administrator (Full Access)
- **Permissions:** 
  - All dashboard tabs (Migration Monitor, Risk Assessment, Digital Divide, Raw Data)
  - Data export functionality
  - Analysis mode and state comparison tools
  - AI Assistant with full query capabilities
  - User management (via create_admin.py)

### Default Demo Account:
- **Username:** `demo`
- **Password:** `demo123`
- **Role:** User (Limited Access)
- **Permissions:**
  - Migration Monitor tab
  - Personal Dashboard with key metrics
  - Basic filtering and state selection
  - Read-only AI Assistant

### Security Notes:
⚠️ **IMPORTANT:** Change default passwords immediately after first login!

🔒 **Password Requirements:**
- Minimum 6 characters
- Passwords are encrypted using SHA-256 hashing
- Stored securely in `user_database.json`

### Creating Additional Users:
```bash
# Run the admin creation script
python create_admin.py

# Or register via the dashboard's Register tab
```

For comprehensive authentication documentation, see:
- [AUTH_README.md](AUTH_README.md) - Complete authentication guide
- [RBAC_DOCUMENTATION.md](RBAC_DOCUMENTATION.md) - Role-based access control details
- [QUICK_START_AUTH.md](QUICK_START_AUTH.md) - Quick setup guide

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

### Quick Launch:

**Using the launch script (recommended):**
```bash
chmod +x run.sh
./run.sh
```

**Or manually:**
```bash
streamlit run app.py
# or
python -m streamlit run app.py
```

The dashboard opens at **http://localhost:8501/**

### First-Time Login:
1. Open http://localhost:8501/ in your browser
2. You'll see the login page with two tabs: **Login** and **Register**
3. Use default credentials (admin/admin123 or demo/demo123) or create a new account
4. After successful login, you'll be redirected to the main dashboard

### Sidebar Controls:
- **👤 User Profile**: Displays username and role with logout button
- **📍 Region Selection**: Filter by All India or specific states
- **🗺️ Migration Filter**: Slider to filter districts by migration intensity (0-100%)
- **🔍 Analysis Mode** (Admin Only): Enable state comparison features
- **🤖 AI Assistant**: Natural language queries about data insights
- **📥 Export Data** (Admin Only): Download filtered datasets as CSV

### Role-Based Dashboard Views:

**Admin View (4 Tabs):**
1. 🌍 Migration Monitor
2. ⚠️ Risk Assessment
3. 📉 Digital Divide
4. 🗂️ Raw Data

**User View (2 Tabs):**
1. 🌍 Migration Monitor
2. 📊 My Dashboard

---

## 📊 Dashboard Tabs

### 🌍 Migration Monitor (All Users)
**Interactive treemap visualization** showing enrolment volume and migration stress across districts.

**Features:**
- Color-coded by migration intensity (red = high, green = low)
- Size represents total enrolment numbers
- Hierarchical view: State → District
- White background with crisp, readable black text labels
- Top 10 high migration districts table
- Hover tooltips with detailed metrics

**Use Cases:**
- Identify migration hotspots requiring mobile enrolment units
- Compare district-level migration patterns within states
- Prioritize resource allocation based on enrolment volume

---

### ⚠️ Risk Assessment (Admin Only)
**Dual-risk scatter plot matrix** analyzing Migration Intensity vs Biometric Lag.

**Features:**
- Bubble size indicates risk score (Migration × Biometric Lag / 100)
- Color gradient shows digital penetration levels
- Quadrant lines at 70% for critical risk identification
- Interactive hover data showing district details
- Critical alert system for dual-risk districts (>70% on both metrics)

**Actionable Insights:**
- Districts in top-right quadrant need immediate intervention
- Mobile enrolment kits deployment recommendations
- Compliance supervisor allocation priorities

---

### 📊 My Dashboard (Regular Users Only)
**Personalized analytics dashboard** with simplified metrics and visualizations.

**Features:**
- 4 key performance metrics displayed as cards
- Migration intensity distribution histogram
- Top 5 districts by migration ranking
- Summary statistics for filtered region
- Clean, easy-to-understand interface

**Perfect For:**
- Field officers monitoring their assigned regions
- Quick overview of migration trends
- Non-technical stakeholders needing high-level insights

---

### 📉 Digital Divide (Admin Only)
**State-level digital penetration analysis** highlighting connectivity gaps.

**Features:**
- Horizontal bar chart of average digital penetration by state
- Color-coded from red (low) to green (high)
- Bottom 5 states identification (Digital Dark Spots)
- Mobile linkage rate comparisons
- District count per state

**Recommendations:**
- IVRS reminder systems for low-digital-penetration areas
- Offline grievance desk requirements
- Assisted Aadhaar update facility locations

---

### 🗂️ Raw Data (Admin Only)
**Comprehensive data explorer** with search and export capabilities.

**Features:**
- Full filtered dataset display
- Real-time search by district or state name
- Configurable rows per page (10/25/50/100)
- CSV export for filtered results
- Complete metadata visibility

**Use Cases:**
- Detailed analysis in external tools (Excel, R, Python)
- Report generation and documentation
- Data validation and quality checks
- Custom analytics and model building

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

| Layer | Tools | Purpose |
|-------|-------|---------|
| **Frontend** | Streamlit 1.28+ | Interactive web dashboard framework |
| **Authentication** | Python hashlib (SHA-256) | Secure password encryption |
| **User Management** | JSON file-based storage | Lightweight user database |
| **Access Control** | Session state + RBAC | Role-based permissions system |
| **Data Processing** | Pandas 2.0+ | Data manipulation and analysis |
| **Visualization** | Plotly Express 5.17+ | Interactive charts (treemap, scatter, bar, histogram) |
| **Styling** | Custom CSS | UIDAI branding, Indian color scheme, responsive design |
| **AI Assistant** | Rule-based NLP | Keyword matching + correlation analysis |
| **Reporting** | ReportLab + Matplotlib | PDF generation with embedded charts |
| **Caching** | Streamlit @cache_data | Performance optimization for data loading |

### Key Dependencies:
```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
numpy>=1.24.0
scipy>=1.11.0
matplotlib>=3.7.0
reportlab>=4.0.0
```

### Performance Features:
- **Data caching**: Streamlit's @cache_data decorator for fast reloads
- **Lazy loading**: Charts rendered only when tabs are accessed
- **Optimized filtering**: In-memory operations for real-time responsiveness
- **Session persistence**: User authentication state maintained across interactions

---

## 🤖 AI Assistant Features

The built-in AI assistant provides intelligent insights through natural language queries.

### Available Commands:

**Risk Analysis:**
```
"Where is the highest risk?"
"Show me the most risky districts"
```
→ Returns top 5 districts by risk score with state and metrics

**Digital Penetration:**
```
"Digital divide"
"Show areas with low digital penetration"
```
→ Lists bottom 5 districts in digital adoption with percentages

**State-Specific Analysis:**
```
"Migration in Maharashtra"
"Tell me about Kerala"
"What's happening in Delhi?"
```
→ Provides state-level migration statistics, district counts, and high-migration areas

**Correlation Analysis:**
```
"Correlation"
"Show me the correlations"
```
→ Displays correlation coefficients between:
- Migration Intensity vs Biometric Lag
- Migration Intensity vs Digital Penetration
- Biometric Lag vs Digital Penetration

**Help & Documentation:**
```
"Help"
"What can you do?"
```
→ Shows all available commands and examples

### How It Works:
- **Rule-based NLP**: Pattern matching with keyword detection
- **Real-time Analysis**: Queries current filtered dataset
- **Context-Aware**: Respects sidebar filters and state selection
- **Interactive**: Expandable response panels with formatted output

### Use Cases:
- Quick insights without navigating through tabs
- Natural language exploration of data patterns
- Training material for non-technical users
- Automated report generation support

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

### Security & Privacy:
- ✅ SHA-256 password encryption
- ✅ No plaintext credential storage
- ✅ Session-based authentication
- ✅ Role-based access control
- ✅ Secure logout functionality
- ✅ Data protection best practices

### Disclaimer:
This dashboard is a demonstration project and should not be used with real sensitive data without proper security audits and compliance reviews.

---

## 📚 Additional Documentation

- **[AUTH_README.md](AUTH_README.md)** - Complete authentication system guide
- **[RBAC_DOCUMENTATION.md](RBAC_DOCUMENTATION.md)** - Role-based access control details
- **[QUICK_START_AUTH.md](QUICK_START_AUTH.md)** - Quick setup for authentication
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview and architecture
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Detailed usage instructions
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Pre-deployment preparation

---

## 🐛 Troubleshooting

### Common Issues:

**Problem:** "Command not found: streamlit"
```bash
# Solution: Install in virtual environment
pip install streamlit
# Or use: python -m streamlit run app.py
```

**Problem:** Login page shows "Username not found"
```bash
# Solution: Create initial users
python create_admin.py
```

**Problem:** Text in treemap is blurry
```bash
# Solution: Already fixed in latest version
# Update to latest commit with improved font rendering
git pull origin cmmoit
```

**Problem:** Role permissions not working
```bash
# Solution: Clear browser cache and re-login
# Check user_database.json for correct role assignment
```

---

<div align="center">

**"From field logistics to policy intelligence, Aadhaar Pulse equips UIDAI teams with a single surveillance lens on migration, compliance, and digital readiness."**

🇮🇳 Made with ❤️ for Digital India

</div>