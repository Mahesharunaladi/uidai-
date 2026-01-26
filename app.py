"""
Aadhaar Pulse – UIDAI Resident Lifecycle Dashboard
A real-time command center for UIDAI field and policy teams
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats.mstats import winsorize
import numpy as np
from pathlib import Path
import hashlib
import json
import os
from datetime import datetime


st.set_page_config(
    page_title="Aadhaar Pulse - UIDAI Dashboard",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    /* Main background with texture */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .main-title {
        color: #000080;
        font-size: 2.5em;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-subtitle {
        color: #333;
        font-size: 1.2em;
        margin: 10px 0 0 0;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #FF9933;
        margin: 10px 0;
    }
    
    .kpi-value {
        font-size: 2em;
        font-weight: bold;
        color: #000080;
    }
    
    .kpi-label {
        color: #666;
        font-size: 0.9em;
        text-transform: uppercase;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #000080 0%, #000050 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 5px 5px 0 0;
        padding: 10px 20px;
        font-weight: bold;
        color: black;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FF9933;
        color: white;
    }
    
    /* Tab content area - white background */
    .stTabs [data-baseweb="tab-panel"] {
        background-color: white;
        padding: 30px;
        border-radius: 0 0 10px 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Alert boxes */
    .alert-box {
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        border-left: 5px solid;
    }
    
    .alert-critical {
        background-color: #ffe6e6;
        border-color: #ff0000;
    }
    
    .alert-warning {
        background-color: #fff4e6;
        border-color: #ff9933;
    }
    
    .alert-info {
        background-color: #e6f3ff;
        border-color: #0066cc;
    }
    
    /* Login/Register Form Styling */
    .login-container {
        max-width: 450px;
        margin: 50px auto;
        padding: 40px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .login-header {
        text-align: center;
        color: #000080;
        font-size: 2em;
        font-weight: bold;
        margin-bottom: 30px;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #FF9933 0%, #138808 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px;
        border-radius: 5px;
    }
    
    /* Input fields styling - white background */
    .stTextInput>div>div>input {
        background-color: white !important;
        color: black !important;
        border: 2px solid #ddd !important;
        border-radius: 5px !important;
        padding: 10px !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #FF9933 !important;
        box-shadow: 0 0 0 2px rgba(255, 153, 51, 0.2) !important;
    }
    
    /* Input labels */
    .stTextInput>label {
        color: #000080 !important;
        font-weight: bold !important;
    }
    
    /* Treemap text visibility enhancement */
    .js-plotly-plot .plotly text {
        text-shadow: 
            -1px -1px 0 white,
            1px -1px 0 white,
            -1px 1px 0 white,
            1px 1px 0 white,
            -2px 0 0 white,
            2px 0 0 white,
            0 -2px 0 white,
            0 2px 0 white !important;
        font-weight: 900 !important;
    }
    
    /* Make all headings in tab panels black */
    .stTabs [data-baseweb="tab-panel"] h3,
    .stTabs [data-baseweb="tab-panel"] h4,
    .stTabs [data-baseweb="tab-panel"] p {
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)



# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# User database file
USER_DB_FILE = "user_database.json"

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def register_user(username, password, email, role="user"):
    """Register a new user"""
    users = load_users()
    
    if username in users:
        return False, "Username already exists!"
    
    users[username] = {
        "password": hash_password(password),
        "email": email,
        "role": role,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    save_users(users)
    return True, "Registration successful! Please login."

def authenticate_user(username, password):
    """Authenticate user credentials"""
    users = load_users()
    
    if username not in users:
        return False, "Username not found!"
    
    if users[username]["password"] == hash_password(password):
        return True, users[username]["role"]
    
    return False, "Incorrect password!"

def logout():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_role = None

def show_login_page():
    """Display login and registration page"""
    st.markdown("""
        <div style='text-align: center; margin-bottom: 30px;'>
            <div class='main-header'>
                <h1 class='main-title'>🇮🇳 Aadhaar Pulse - UIDAI Dashboard</h1>
                <p class='main-subtitle'>Real-time Command Center for Resident Lifecycle Monitoring</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for Login and Register
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    # LOGIN TAB
    with tab1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<div class='login-header'>Login to Dashboard</div>", unsafe_allow_html=True)
            
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submit = st.form_submit_button("🔓 Login")
                
                if submit:
                    if username and password:
                        success, result = authenticate_user(username, password)
                        if success:
                            st.session_state.authenticated = True
                            st.session_state.username = username
                            st.session_state.user_role = result
                            st.success(f"✅ Welcome back, {username}!")
                            st.rerun()
                        else:
                            st.error(f"❌ {result}")
                    else:
                        st.warning("⚠️ Please enter both username and password")
    
    # REGISTER TAB
    with tab2:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<div class='login-header'>Create New Account</div>", unsafe_allow_html=True)
            
            with st.form("register_form"):
                new_username = st.text_input("Username", placeholder="Choose a username")
                new_email = st.text_input("Email", placeholder="Enter your email")
                new_password = st.text_input("Password", type="password", placeholder="Create a password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                role = st.selectbox("Role", ["user", "admin", "analyst"])
                register = st.form_submit_button("📝 Register")
                
                if register:
                    if new_username and new_email and new_password and confirm_password:
                        if new_password != confirm_password:
                            st.error("❌ Passwords do not match!")
                        elif len(new_password) < 6:
                            st.error("❌ Password must be at least 6 characters long!")
                        else:
                            success, message = register_user(new_username, new_password, new_email, role)
                            if success:
                                st.success(f"✅ {message}")
                            else:
                                st.error(f"❌ {message}")
                    else:
                        st.warning("⚠️ Please fill in all fields")
    
    # Info section
    st.markdown("---")
    st.info("🔒 **Secure Access**: All passwords are encrypted using SHA-256 hashing. Your credentials are stored securely.")

# ============================================================================
# DATA LOADING & CLEANING
# ============================================================================
@st.cache_data
def load_and_clean_data():
    """Load and clean the UIDAI dataset with comprehensive preprocessing"""
    
    # Try to load from artifacts folder
    data_path = Path("artifacts/final_master_data.csv")
    
    if not data_path.exists():
        st.error(f"❌ Dataset not found at: {data_path}")
        st.info("📝 Please ensure `artifacts/final_master_data.csv` exists in your project directory.")
        
        # Create sample data for demonstration
        sample_data = pd.DataFrame({
            'State': ['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Gujarat', 'Delhi'] * 20,
            'District': [f'District_{i}' for i in range(100)],
            'Total_Enrolment': np.random.randint(10000, 500000, 100),
            'Migration_Intensity': np.random.uniform(0, 100, 100),
            'Biometric_Lag': np.random.uniform(0, 100, 100),
            'Digital_Penetration': np.random.uniform(20, 95, 100),
            'Mobile_Linkage_Rate': np.random.uniform(40, 98, 100),
            'Update_Frequency': np.random.uniform(0, 50, 100)
        })
        df = sample_data
    else:
        df = pd.read_csv(data_path)
    
    # 1. Normalize state and district names
    if 'State' in df.columns:
        df['State'] = df['State'].astype(str).str.strip().str.upper()
    if 'District' in df.columns:
        df['District'] = df['District'].astype(str).str.strip().str.title()
    
    # 2. Remove ghost districts (enrolment <= 100)
    if 'Total_Enrolment' in df.columns:
        initial_count = len(df)
        df = df[df['Total_Enrolment'] > 100].copy()
        removed = initial_count - len(df)
        if removed > 0:
            st.sidebar.info(f"🧹 Removed {removed} ghost districts (enrolment ≤ 100)")
    
    # 3. Winsorize key metrics (cap at 0-100%)
    metrics_to_winsorize = ['Migration_Intensity', 'Biometric_Lag', 'Digital_Penetration']
    for col in metrics_to_winsorize:
        if col in df.columns:
            df[col] = df[col].clip(0, 100)
    
    # 4. Calculate derived metrics
    if 'Migration_Intensity' in df.columns and 'Biometric_Lag' in df.columns:
        df['Risk_Score'] = (df['Migration_Intensity'] * df['Biometric_Lag']) / 100
    
    # 5. Handle missing values (before creating categories)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)
    
    # 6. Create risk categories
    if 'Risk_Score' in df.columns:
        df['Risk_Category'] = pd.cut(
            df['Risk_Score'],
            bins=[0, 30, 50, 70, 100],
            labels=['Low', 'Medium', 'High', 'Critical']
        )
    
    return df


def ai_assistant(query, df):
    """Rule-based AI assistant for answering questions about the data"""
    query = query.lower()
    
    # Question patterns
    if 'highest risk' in query or 'most risk' in query:
        top_risk = df.nlargest(5, 'Risk_Score')[['State', 'District', 'Risk_Score']]
        response = "🚨 **Top 5 Highest Risk Districts:**\n\n"
        for idx, row in top_risk.iterrows():
            response += f"• **{row['District']}, {row['State']}** - Risk Score: {row['Risk_Score']:.1f}\n"
        return response
    
    elif 'digital divide' in query or 'digital penetration' in query:
        low_digital = df.nsmallest(5, 'Digital_Penetration')[['State', 'District', 'Digital_Penetration']]
        response = "📱 **Bottom 5 Districts in Digital Penetration:**\n\n"
        for idx, row in low_digital.iterrows():
            response += f"• **{row['District']}, {row['State']}** - {row['Digital_Penetration']:.1f}%\n"
        return response
    
    elif 'migration' in query and any(state in query for state in df['State'].str.lower().unique()):
        # State-specific migration query
        for state in df['State'].unique():
            if state.lower() in query:
                state_data = df[df['State'] == state]
                avg_migration = state_data['Migration_Intensity'].mean()
                response = f"🗺️ **{state} Migration Overview:**\n\n"
                response += f"• Average Migration Intensity: {avg_migration:.1f}%\n"
                response += f"• Districts: {len(state_data)}\n"
                response += f"• High Migration Districts (>70%): {len(state_data[state_data['Migration_Intensity'] > 70])}\n"
                return response
    
    elif 'correlation' in query:
        corr = df[['Migration_Intensity', 'Biometric_Lag', 'Digital_Penetration']].corr()
        response = "📊 **Key Correlations:**\n\n"
        response += f"• Migration vs Biometric Lag: {corr.loc['Migration_Intensity', 'Biometric_Lag']:.2f}\n"
        response += f"• Migration vs Digital Penetration: {corr.loc['Migration_Intensity', 'Digital_Penetration']:.2f}\n"
        response += f"• Biometric Lag vs Digital Penetration: {corr.loc['Biometric_Lag', 'Digital_Penetration']:.2f}\n"
        return response
    
    elif 'help' in query or 'what can you do' in query:
        return """
        🤖 **I can help you with:**
        
        • "Where is the highest risk?" - Show top risk districts
        • "Digital divide" - Show areas with low digital penetration
        • "Migration in [State]" - State-specific migration stats
        • "Correlation" - Show metric correlations
        • "Tell me about [State]" - General state overview
        """
    
    else:
        return "🤔 I didn't understand that. Try asking about 'highest risk', 'digital divide', 'migration', or type 'help' for more options."

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <div class="main-title">🇮🇳 Aadhaar Pulse - UIDAI Dashboard</div>
        <div class="main-subtitle">Real-time Command Center for Resident Lifecycle Monitoring</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    with st.spinner("🔄 Loading and cleaning UIDAI data..."):
        df = load_and_clean_data()
    
    
    with st.sidebar:
        # User info and logout
        st.markdown(f"### 👤 Welcome, {st.session_state.username}!")
        st.markdown(f"**Role:** {st.session_state.user_role.upper()}")
        
        if st.button("🚪 Logout"):
            logout()
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 🎛️ Control Panel")
        st.markdown("---")
        
        # Region selector
        st.markdown("#### 📍 Region Selection")
        all_states = ['All India'] + sorted(df['State'].unique().tolist())
        selected_state = st.selectbox("Select State:", all_states)
        
        # Migration intensity filter
        st.markdown("#### 🗺️ Migration Filter")
        migration_range = st.slider(
            "Migration Intensity %:",
            0, 100, (0, 100)
        )
        
        # Admin-only features
        if st.session_state.user_role == 'admin':
            # Comparison mode (admin only)
            st.markdown("#### 🔍 Analysis Mode")
            comparison_mode = st.checkbox("Enable State Comparison", value=False)
        
        st.markdown("---")
        
        # AI Assistant
        st.markdown("#### 🤖 AI Assistant")
        user_query = st.text_input("Ask me anything:", placeholder="e.g., Where is the highest risk?")
        if user_query:
            with st.expander("💬 Response", expanded=True):
                st.markdown(ai_assistant(user_query, df))
        
        st.markdown("---")
        
        # Export (admin only)
        if st.session_state.user_role == 'admin':
            st.markdown("#### 📥 Export Data")
            if st.button("Download Filtered CSV"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="💾 Download CSV",
                    data=csv,
                    file_name="uidai_filtered_data.csv",
                    mime="text/csv"
                )
    

    filtered_df = df.copy()
    
    if selected_state != 'All India':
        filtered_df = filtered_df[filtered_df['State'] == selected_state]
    
    filtered_df = filtered_df[
        (filtered_df['Migration_Intensity'] >= migration_range[0]) &
        (filtered_df['Migration_Intensity'] <= migration_range[1])
    ]
    
   
    st.markdown("### 📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Total Districts</div>
            <div class="kpi-value">{:,}</div>
        </div>
        """.format(len(filtered_df)), unsafe_allow_html=True)
    
    with col2:
        avg_risk = filtered_df['Risk_Score'].mean()
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Avg Risk Score</div>
            <div class="kpi-value">{:.1f}</div>
        </div>
        """.format(avg_risk), unsafe_allow_html=True)
    
    with col3:
        critical_districts = len(filtered_df[filtered_df['Risk_Score'] > 70])
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Critical Districts</div>
            <div class="kpi-value" style="color: #ff0000;">{:,}</div>
        </div>
        """.format(critical_districts), unsafe_allow_html=True)
    
    with col4:
        total_enrolment = filtered_df['Total_Enrolment'].sum()
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Total Enrolments</div>
            <div class="kpi-value">{:,.0f}</div>
        </div>
        """.format(total_enrolment), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Role-based tab access
    if st.session_state.user_role == 'admin':
        # Admin sees all tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🌍 Migration Monitor",
            "⚠️ Risk Assessment",
            "📉 Digital Divide",
            "🗂️ Raw Data"
        ])
    else:
        # Regular users see limited tabs
        tab1, tab2 = st.tabs([
            "🌍 Migration Monitor",
            "📊 My Dashboard"
        ])
    
    # ------------------------------------------------------------------------
    # TAB 1: MIGRATION MONITOR
    # ------------------------------------------------------------------------
    with tab1:
        st.markdown("### 🗺️ Migration Intensity Treemap")
        st.markdown("Visualizing enrolment volume and migration stress across districts")
        
        if len(filtered_df) > 0:
            # Treemap
            fig_treemap = px.treemap(
                filtered_df,
                path=['State', 'District'],
                values='Total_Enrolment',
                color='Migration_Intensity',
                color_continuous_scale='RdYlGn_r',
                title=f"Migration Intensity by District ({selected_state})"
            )
            fig_treemap.update_traces(
                textfont=dict(
                    size=16, 
                    color='black', 
                    family='Arial, Helvetica, sans-serif'
                ),
                textposition='middle center',
                marker=dict(
                    line=dict(width=2, color='white'),
                    colorbar=dict(thickness=15, len=0.7),
                    pad=dict(t=20, l=10, r=10, b=10)
                ),
                texttemplate='<b>%{label}</b>',
            )
            fig_treemap.update_layout(
                height=600,
                font=dict(size=16, color='black', family='Arial, Helvetica, sans-serif'),
                paper_bgcolor='white',
                plot_bgcolor='white',
                title=dict(
                    text=f"Migration Intensity by District ({selected_state})",
                    font=dict(size=24, color='#000080', family='Arial, Helvetica, sans-serif', weight='bold'),
                    x=0.5,
                    xanchor='center',
                    y=0.98,
                    yanchor='top'
                )
            )
            st.plotly_chart(fig_treemap, use_container_width=True, config={'displayModeBar': True})
            
            # Top migration districts
            st.markdown("#### 🔝 Top 10 High Migration Districts")
            top_migration = filtered_df.nlargest(10, 'Migration_Intensity')[
                ['State', 'District', 'Migration_Intensity', 'Total_Enrolment']
            ]
            st.dataframe(top_migration, use_container_width=True)
        else:
            st.warning("No data available for selected filters.")
    
    # ------------------------------------------------------------------------
    # TAB 2: CONDITIONAL CONTENT BASED ON ROLE
    # ------------------------------------------------------------------------
    with tab2:
        if st.session_state.user_role == 'admin':
            # ADMIN: Risk Assessment
            st.markdown("### ⚠️ Dual-Risk Matrix")
            st.markdown("Migration vs Biometric Lag - sized by risk score, colored by digital penetration")
            
            if len(filtered_df) > 0:
                # Risk scatter plot
                fig_scatter = px.scatter(
                    filtered_df,
                    x='Migration_Intensity',
                    y='Biometric_Lag',
                    size='Risk_Score',
                    color='Digital_Penetration',
                    hover_data=['State', 'District', 'Risk_Score'],
                    color_continuous_scale='RdYlGn',
                    title="Risk Assessment Matrix"
                )
                
                # Add quadrant lines
                fig_scatter.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5)
                fig_scatter.add_vline(x=70, line_dash="dash", line_color="red", opacity=0.5)
                
                fig_scatter.update_layout(height=600)
                st.plotly_chart(fig_scatter, use_container_width=True)
                
                # Risk alerts
                critical = filtered_df[
                    (filtered_df['Migration_Intensity'] > 70) & 
                    (filtered_df['Biometric_Lag'] > 70)
                ]
                
                if len(critical) > 0:
                    st.markdown("""
                    <div class="alert-box alert-critical">
                        <strong>🚨 CRITICAL ALERT:</strong> {} districts exceed BOTH 70% migration intensity 
                        AND 70% biometric lag. Immediate deployment of mobile enrolment kits recommended.
                    </div>
                    """.format(len(critical)), unsafe_allow_html=True)
                    
                    st.dataframe(
                        critical[['State', 'District', 'Migration_Intensity', 'Biometric_Lag', 'Risk_Score']],
                        use_container_width=True
                    )
            else:
                st.warning("No data available for selected filters.")
        else:
            # USER: Simple Dashboard
            st.markdown("### 📊 My Dashboard")
            st.markdown("Overview of migration statistics and key metrics")
            
            if len(filtered_df) > 0:
                # Summary statistics for users
                col1, col2 = st.columns(2)
                
                with col1:
                    avg_migration = filtered_df['Migration_Intensity'].mean()
                    st.metric("Average Migration Intensity", f"{avg_migration:.1f}%")
                    
                    total_districts = len(filtered_df)
                    st.metric("Total Districts", f"{total_districts:,}")
                
                with col2:
                    high_migration = len(filtered_df[filtered_df['Migration_Intensity'] > 70])
                    st.metric("High Migration Districts", f"{high_migration:,}")
                    
                    total_enrol = filtered_df['Total_Enrolment'].sum()
                    st.metric("Total Enrolments", f"{total_enrol:,.0f}")
                
                st.markdown("---")
                
                # Migration trend chart for users
                st.markdown("#### 📈 Migration Intensity Distribution")
                fig_hist = px.histogram(
                    filtered_df,
                    x='Migration_Intensity',
                    nbins=20,
                    title="Distribution of Migration Intensity",
                    labels={'Migration_Intensity': 'Migration Intensity (%)'}
                )
                fig_hist.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig_hist, use_container_width=True)
                
                # Top 5 districts for users
                st.markdown("#### 🔝 Top 5 Districts by Migration")
                top_5 = filtered_df.nlargest(5, 'Migration_Intensity')[
                    ['District', 'State', 'Migration_Intensity', 'Total_Enrolment']
                ]
                st.dataframe(top_5, use_container_width=True, hide_index=True)
            else:
                st.warning("No data available for selected filters.")
    
    # Admin-only tabs
    if st.session_state.user_role == 'admin':
        # ------------------------------------------------------------------------
        # TAB 3: DIGITAL DIVIDE (ADMIN ONLY)
        # ------------------------------------------------------------------------
        with tab3:
            st.markdown("### 📱 Digital Penetration Heatmap")
            st.markdown("Identifying districts with lowest mobile linkage and digital readiness")
            
            if len(filtered_df) > 0:
                # State-level aggregation
                state_digital = filtered_df.groupby('State').agg({
                    'Digital_Penetration': 'mean',
                    'Mobile_Linkage_Rate': 'mean',
                    'District': 'count'
                }).reset_index()
                state_digital.columns = ['State', 'Avg_Digital_Penetration', 'Avg_Mobile_Linkage', 'District_Count']
                state_digital = state_digital.sort_values('Avg_Digital_Penetration')
                
                # Bar chart
                fig_bar = px.bar(
                    state_digital,
                    x='State',
                    y='Avg_Digital_Penetration',
                    color='Avg_Digital_Penetration',
                    color_continuous_scale='RdYlGn',
                    title="Average Digital Penetration by State"
                )
                fig_bar.update_layout(height=500, xaxis_tickangle=-45)
                st.plotly_chart(fig_bar, use_container_width=True)
                
                # Bottom 5 states
                st.markdown("#### 📉 Bottom 5 States - Digital Dark Spots")
                bottom_states = state_digital.head(5)
                
                st.markdown("""
                <div class="alert-box alert-warning">
                    <strong>⚠️ ATTENTION:</strong> These states require IVRS reminders, 
                    offline grievance desks, and assisted Aadhaar update facilities.
                </div>
                """, unsafe_allow_html=True)
                
                st.dataframe(bottom_states, use_container_width=True)
            else:
                st.warning("No data available for selected filters.")
        
        # ------------------------------------------------------------------------
        # TAB 4: RAW DATA (ADMIN ONLY)
        # ------------------------------------------------------------------------
        with tab4:
            st.markdown("### 📋 Filtered Data Explorer")
            st.markdown(f"Showing **{len(filtered_df)}** records")
            
            # Display options
            col1, col2 = st.columns([3, 1])
            with col1:
                search_term = st.text_input("🔍 Search districts:", placeholder="Type to filter...")
            with col2:
                rows_to_show = st.selectbox("Rows per page:", [10, 25, 50, 100], index=1)
            
            # Filter by search
            display_df = filtered_df
            if search_term:
                display_df = display_df[
                    display_df['District'].str.contains(search_term, case=False) |
                    display_df['State'].str.contains(search_term, case=False)
                ]
            
            # Display dataframe
            st.dataframe(
                display_df.head(rows_to_show),
                use_container_width=True,
                height=400
            )
            
            # Export button
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Full Filtered Data",
                data=csv,
                file_name=f"uidai_export_{selected_state.replace(' ', '_').lower()}.csv",
                mime="text/csv"
            )
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p><strong>Aadhaar Pulse Analytics</strong> | Powered by UIDAI Data</p>
        <p style="font-size: 0.8em;">
            "From field logistics to policy intelligence, Aadhaar Pulse equips UIDAI teams 
            with a single surveillance lens on migration, compliance, and digital readiness."
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # Check authentication status
    if not st.session_state.authenticated:
        show_login_page()
    else:
        main()
