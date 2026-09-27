import streamlit as st
import pandas as pd
import plotly.express as px
import ast


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Data Jobs Market Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f4f7fb;
        color: #1f2937;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0b2a4a;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Main title */
    .main-title {
        font-size: 28px;
        font-weight: 700;
        color: #0f2d4a;
        margin-bottom: 2px;
    }

    .subtitle {
        color: #374151;
        font-size: 14px;
        margin-bottom: 15px;
    }

    /* KPI cards */
    .kpi-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #d1d5db;
        box-shadow: 0 2px 7px rgba(0,0,0,0.05);
        min-height: 105px;
    }

    .kpi-title {
        color: #374151;
        font-size: 13px;
        font-weight: 600;
    }

    .kpi-value {
        color: #0f2d4a;
        font-size: 25px;
        font-weight: 700;
        margin-top: 8px;
    }

    /* Section headers */
    .section-title {
        color: #0f2d4a;
        font-size: 18px;
        font-weight: 700;
        margin-top: 12px;
        margin-bottom: 5px;
    }

    /* Insight box */
    .insight-box {
        background: white;
        border-radius: 10px;
        border: 1px solid #d1d5db;
        padding: 15px;
        min-height: 250px;
    }

    .insight-title {
        color: #0f2d4a;
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .insight-item {
        font-size: 13px;
        color: #1f2937;
        margin-bottom: 9px;
    }

    /* Streamlit labels */
    label {
        color: #1f2937 !important;
        font-weight: 600 !important;
    }

    /* Dataframe text */
    [data-testid="stDataFrame"] {
        color: #1f2937 !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #4b5563;
        font-size: 12px;
        padding: 20px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv("data_jobs_clustered.csv")

    numeric_columns = [
        "salary_minimum",
        "salary_maximum",
        "avg_salary",
        "career_growth_index",
        "skill_count",
        "applicant_count",
        "cluster"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df


df = load_data()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:22px;
            font-weight:700;
            margin-bottom:3px;">
            📊 Data Jobs
        </div>

        <div style="
            font-size:18px;
            font-weight:600;
            margin-bottom:25px;">
            Market Analysis
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 📌 Dashboard")

    selected_section = st.radio(
        "Dashboard section",
        [
            "Complete Dashboard",
            "Overview",
            "Job Analysis",
            "Location Analysis",
            "Salary Analysis",
            "Skill Analysis",
            "K-Means Clusters",
            "Detailed Analysis",
            "Export Data"
        ],
        key="dashboard_section",
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### About")

    st.caption(
        "Interactive analysis of the data-job market "
        "using Python, Streamlit, Plotly and K-Means clustering."
    )


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">Data Jobs Market Analysis Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Explore job demand, salary, skills, locations, experience and job clusters'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# FILTERS
# ============================================================

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)


with filter_col1:

    if "job_category" in df.columns:

        categories = sorted(
            df["job_category"].dropna().unique()
        )

        selected_category = st.multiselect(
            "Job Category",
            categories,
            default=[]
        )

    else:
        selected_category = []


with filter_col2:

    if "location_country" in df.columns:

        countries = sorted(
            df["location_country"].dropna().unique()
        )

        selected_country = st.multiselect(
            "Country",
            countries,
            default=[]
        )

    else:
        selected_country = []


with filter_col3:

    if "employment_type" in df.columns:

        employment_types = sorted(
            df["employment_type"].dropna().unique()
        )

        selected_employment = st.multiselect(
            "Job Type",
            employment_types,
            default=[]
        )

    else:
        selected_employment = []


with filter_col4:

    if "experience_level" in df.columns:

        experience_levels = sorted(
            df["experience_level"].dropna().unique()
        )

        selected_experience = st.multiselect(
            "Experience Level",
            experience_levels,
            default=[]
        )

    else:
        selected_experience = []


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if selected_category:
    filtered_df = filtered_df[
        filtered_df["job_category"].isin(selected_category)
    ]


if selected_country:
    filtered_df = filtered_df[
        filtered_df["location_country"].isin(selected_country)
    ]


if selected_employment:
    filtered_df = filtered_df[
        filtered_df["employment_type"].isin(selected_employment)
    ]


if selected_experience:
    filtered_df = filtered_df[
        filtered_df["experience_level"].isin(selected_experience)
    ]


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_jobs = len(filtered_df)

average_salary = (
    filtered_df["avg_salary"].mean()
    if "avg_salary" in filtered_df.columns
    else 0
)

unique_companies = (
    filtered_df["company_name"].nunique()
    if "company_name" in filtered_df.columns
    else 0
)

unique_locations = (
    filtered_df["location_city"].nunique()
    if "location_city" in filtered_df.columns
    else 0
)


# ============================================================
if selected_section in ("Complete Dashboard", "Overview"):
    # KPI CARDS
    # ============================================================
    
    st.markdown('<div id="overview"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">Market Overview</div>',
        unsafe_allow_html=True
    )
    
    k1, k2, k3, k4 = st.columns(4)
    
    
    with k1:
    
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Job Postings</div>
                <div class="kpi-value">{total_jobs:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    
    with k2:
    
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Average Salary</div>
                <div class="kpi-value">₹{average_salary / 100000:.2f} L</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    
    with k3:
    
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Unique Companies</div>
                <div class="kpi-value">{unique_companies:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    
    with k4:
    
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Unique Locations</div>
                <div class="kpi-value">{unique_locations:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    
    st.divider()
    
    
    # ============================================================
if selected_section in ("Complete Dashboard", "Job Analysis"):
    # JOB DEMAND
    # ============================================================
    
    st.markdown('<div id="job-demand"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">Job Demand Analysis</div>',
        unsafe_allow_html=True
    )
    
    c1, c2 = st.columns(2)
    
    
    # ---------------- TOP JOB ROLES ----------------
    
    with c1:
    
        role_data = (
            filtered_df["job_title"]
            .value_counts()
            .head(10)
            .sort_values()
            .reset_index()
        )
    
        role_data.columns = [
            "Job Role",
            "Postings"
        ]
    
        fig = px.bar(
            role_data,
            x="Postings",
            y="Job Role",
            orientation="h",
            color="Postings",
            color_continuous_scale=["#DCEEF5", "#12395B"],
            title="Top 10 Job Roles by Number of Postings"
        )
    
        fig.update_layout(
            height=330,
            margin=dict(l=10, r=10, t=45, b=10),
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(
                color="#1f2937"
            )
        )
    
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    
    
    # ---------------- JOB TYPE ----------------
    
    with c2:
    
        type_data = (
            filtered_df["employment_type"]
            .value_counts()
            .reset_index()
        )
    
        type_data.columns = [
            "Job Type",
            "Postings"
        ]
    
        fig = px.pie(
            type_data,
            names="Job Type",
            values="Postings",
            hole=0.55,
            color_discrete_sequence=["#12395B", "#1E5A7A", "#168AAD", "#2A9D8F", "#76C893"],
            title="Job Type Distribution"
        )
    
        fig.update_layout(
            height=330,
            margin=dict(l=10, r=10, t=45, b=10),
            paper_bgcolor="white",
            font=dict(
                color="#1f2937"
            )
        )
    
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    
    
    # ============================================================
if selected_section in ("Complete Dashboard", "Location Analysis"):
    # LOCATION
    # ============================================================
    
    st.markdown('<div id="location-analysis"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">Location Analysis</div>',
        unsafe_allow_html=True
    )
    
    c1, c2 = st.columns(2)
    
    
    with c1:
    
        location_data = (
            filtered_df["location_city"]
            .value_counts()
            .head(10)
            .sort_values()
            .reset_index()
        )
    
        location_data.columns = [
            "Location",
            "Postings"
        ]
    
        fig = px.bar(
            location_data,
            x="Postings",
            y="Location",
            orientation="h",
            color="Postings",
            color_continuous_scale=["#DCEEF5", "#12395B"],
            title="Top 10 Job Locations"
        )
    
        fig.update_layout(
            height=330,
            margin=dict(l=10, r=10, t=45, b=10),
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(
                color="#1f2937"
            )
        )
    
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    
    
    with c2:
    
        state_data = (
            filtered_df["location_state"]
            .value_counts()
            .head(10)
            .sort_values()
            .reset_index()
        )
    
        state_data.columns = [
            "State",
            "Postings"
        ]
    
        fig = px.treemap(
            state_data,
            path=["State"],
            values="Postings",
            color="Postings",
            color_continuous_scale=["#DCEEF5", "#12395B"],
            title="Top 10 States by Job Postings"
        )
    
        fig.update_layout(
            height=330,
            margin=dict(l=10, r=10, t=45, b=10),
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(
                color="#1f2937"
            )
        )
    
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    
    
    # ============================================================
if selected_section in ("Complete Dashboard", "Salary Analysis"):
    # SALARY ANALYSIS
    # ============================================================
    
    st.markdown('<div id="salary-analysis"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">Salary Analysis</div>',
        unsafe_allow_html=True
    )
    
    c1, c2 = st.columns(2)
    
    
    with c1:
    
        salary_role = (
            filtered_df
            .groupby("job_title")["avg_salary"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .sort_values()
            .reset_index()
        )
    
        # Convert salary to Lakhs
        salary_role["Average Salary Lakhs"] = (
            salary_role["avg_salary"] / 100000
        )
    
        salary_role.columns = [
            "Job Role",
            "Average Salary",
            "Average Salary Lakhs"
        ]
    
        fig = px.bar(
            salary_role,
            x="Average Salary Lakhs",
            y="Job Role",
            orientation="h",
            color="Average Salary Lakhs",
            color_continuous_scale=["#DCEEF5", "#12395B"],
            title="Average Salary by Job Role",
            text="Average Salary Lakhs"
        )
    
        fig.update_traces(
            texttemplate="₹%{x:.2f} L",
            textposition="outside"
        )
    
        fig.update_layout(
            height=330,
            margin=dict(l=10, r=10, t=45, b=10),
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(
                color="#1f2937"
            ),
            xaxis_title="Average Salary (₹ Lakhs)",
            yaxis_title="Job Role"
        )
    
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    
    
    with c2:
    
        exp_salary = (
            filtered_df
            .groupby("experience_level")["avg_salary"]
            .mean()
            .reset_index()
        )

        # Convert salary to Lakhs.
        exp_salary["Average Salary Lakhs"] = exp_salary["avg_salary"] / 100000

        fig = px.bar(
            exp_salary,
            x="experience_level",
            y="Average Salary Lakhs",
            color="Average Salary Lakhs",
            color_continuous_scale=["#DCEEF5", "#12395B"],
            title="Average Salary by Experience Level",
            text="Average Salary Lakhs"
        )

        fig.update_traces(
            texttemplate="₹%{y:.2f} L",
            textposition="outside"
        )
    
        fig.update_layout(
            height=330,
            margin=dict(l=10, r=10, t=45, b=10),
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(
                color="#1f2937"
            ),
            xaxis_title="Experience Level",
            yaxis_title="Average Salary (₹ Lakhs)"
        )
    
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    
    
    # ============================================================
if selected_section in ("Complete Dashboard", "Skill Analysis"):
    # SKILLS
    # ============================================================
    
    st.markdown('<div id="skill-analysis"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">Skills in Demand</div>',
        unsafe_allow_html=True
    )
    
    
    skills = []
    
    for value in filtered_df["skills_extracted"].dropna():
    
        try:
    
            if isinstance(value, str):
                value = ast.literal_eval(value)
    
            if isinstance(value, list):
                skills.extend(value)
    
        except:
            pass
    
    
    if skills:
    
        skill_data = (
            pd.Series(skills)
            .value_counts()
            .head(10)
            .sort_values()
            .reset_index()
        )
    
        skill_data.columns = [
            "Skill",
            "Postings"
        ]
    
        fig = px.bar(
            skill_data,
            x="Postings",
            y="Skill",
            orientation="h",
            color="Postings",
            color_continuous_scale=["#DCEEF5", "#12395B"],
            title="Top 10 Skills in Demand"
        )
    
        fig.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=45, b=10),
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(
                color="#1f2937"
            )
        )
    
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    
    
    # ============================================================
if selected_section in ("Complete Dashboard", "K-Means Clusters"):
    # K-MEANS
    # ============================================================
    
    st.markdown('<div id="cluster-analysis"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">K-Means Job Cluster Analysis</div>',
        unsafe_allow_html=True
    )
    
    c1, c2 = st.columns(2)
    
    
    with c1:
    
        cluster_data = (
            filtered_df["cluster"]
            .value_counts()
            .sort_index()
            .reset_index()
        )
    
        cluster_data.columns = [
            "Cluster",
            "Postings"
        ]
    
        cluster_data["Cluster"] = (
            "Cluster "
            + cluster_data["Cluster"].astype(str)
        )
    
        fig = px.bar(
            cluster_data,
            x="Cluster",
            y="Postings",
            color="Postings",
            color_continuous_scale=["#DCEEF5", "#12395B"],
            title="Job Postings by Cluster"
        )
    
        fig.update_layout(
            height=330,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(
                color="#1f2937"
            )
        )
    
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    
    
    with c2:
    
        sample = filtered_df.copy()
    
        if len(sample) > 5000:
            sample = sample.sample(
                5000,
                random_state=42
            )
    
        # Convert salary to Lakhs
        sample["avg_salary_lakhs"] = (
            sample["avg_salary"] / 100000
        )
    
        fig = px.scatter(
            sample,
            x="career_growth_index",
            y="avg_salary_lakhs",
            color="cluster",
            hover_data=[
                "job_title",
                "experience_level",
                "skill_count"
            ],
            title="Salary vs Career Growth by Cluster"
        )
    
        fig.update_layout(
            height=330,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(
                color="#1f2937"
            ),
            xaxis_title="Career Growth Index",
            yaxis_title="Average Salary (₹ Lakhs)"
        )
    
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    
    
    # ============================================================
if selected_section in ("Complete Dashboard", "Detailed Analysis"):
    # DETAILED ANALYSIS + INSIGHTS
    # ============================================================
    
    st.markdown(
        '<div class="section-title">Detailed Job Analysis</div>',
        unsafe_allow_html=True
    )
    
    c1, c2 = st.columns([2, 1])
    
    
    with c1:
    
        display_columns = [
            "job_title",
            "location_city",
            "company_name",
            "avg_salary",
            "experience_level",
            "employment_type",
            "skill_count",
            "cluster"
        ]
    
        available_columns = [
            col for col in display_columns
            if col in filtered_df.columns
        ]
    
        table_data = filtered_df[
            available_columns
        ].head(15).copy()
    
        # Convert salary to Lakhs in the table
        if "avg_salary" in table_data.columns:
            table_data["avg_salary"] = (
                table_data["avg_salary"] / 100000
            )
    
        st.dataframe(
            table_data,
            use_container_width=True,
            hide_index=True
        )
    
    
    with c2:
    
        top_role = (
            filtered_df["job_title"]
            .value_counts()
            .idxmax()
        )
    
        top_location = (
            filtered_df["location_city"]
            .value_counts()
            .idxmax()
        )
    
        avg_skills = (
            filtered_df["skill_count"].mean()
        )
    
        avg_growth = (
            filtered_df["career_growth_index"].mean()
        )
    
        st.markdown(
            f"""
            <div class="insight-box">
    
            <div class="insight-title">
            💡 Key Insights
            </div>
    
            <div class="insight-item">
            • Most common job role: <b>{top_role}</b>
            </div>
    
            <div class="insight-item">
            • Leading job location: <b>{top_location}</b>
            </div>
    
            <div class="insight-item">
            • Average required skills: <b>{avg_skills:.1f}</b>
            </div>
    
            <div class="insight-item">
            • Average career growth index:
            <b>{avg_growth:.1f}</b>
            </div>
    
            <div class="insight-item">
            • Dataset contains
            <b>{len(filtered_df):,}</b>
            job postings after filters.
            </div>
    
            </div>
            """,
            unsafe_allow_html=True
        )
    
    
# ============================================================
if selected_section in ("Complete Dashboard", "Export Data"):
    # DOWNLOAD
    # ============================================================
    
    st.markdown(
        '<div class="section-title">Export Data</div>',
        unsafe_allow_html=True
    )
    
    csv_data = filtered_df.to_csv(index=False)
    
    st.download_button(
        "⬇️ Download Filtered Dataset",
        csv_data,
        "filtered_job_data.csv",
        "text/csv"
    )
    
    
    # ============================================================
    # FOOTER
    # ============================================================
    
    st.markdown(
        """
        <div class="footer">
        Data Jobs Market Intelligence |
        Python • Streamlit • Plotly • K-Means
        </div>
        """,
        unsafe_allow_html=True
    )
