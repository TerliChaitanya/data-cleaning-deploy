import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page Config (must come first)
st.set_page_config(page_title="🧹 Data Cleaning App", page_icon="🧼", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #E3F2FD, #BBDEFB); /* Ice Blue → Light Sky Blue */
        color: black;
    }

    /* Main background */
    .stApp {
        background: #E3F2FD; /* Ice Blue */
    }

    /* Buttons */
    .stButton>button {
        background-color: #3F51B5; /* Indigo */
        color: white;
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #5C6BC0; /* Soft Violet-Blue */
        transform: scale(1.05);
    }

    /* Headers */
    h1, h2, h3 {
        color: #283593; /* Midnight Blue */
        font-family: 'Segoe UI', sans-serif;
    }

    /* Cards */
    .card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if "clean_df" not in st.session_state:
    st.session_state.clean_df = None

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Choose a page",
    [
        "📂 Upload Data",
        "🔍 Data Overview",
        "🧹 Handle Missing Values",
        "🔁 Handle Duplicates",
        "📊 Outlier Detection",
        "📝 Fix Categories",
        "💾 Download Data"
    ]
)

# 📂 Upload Data
if page == "📂 Upload Data":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("📤 Upload your Dataset")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state.clean_df = df.copy()
        st.success("✅ File uploaded successfully!")
        st.dataframe(df.head(20))
    st.markdown('</div>', unsafe_allow_html=True)

# 🔍 Data Overview
elif page == "🔍 Data Overview":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("📊 Dataset Overview")
    
    if st.session_state.clean_df is not None:
        df = st.session_state.clean_df
        st.write("🔹 Shape:", df.shape)
        st.write("🔹 Missing values per column:")
        st.write(df.isnull().sum())

        st.subheader("📈 Data Distribution")
        num_cols = df.select_dtypes(include=np.number).columns
        if len(num_cols) > 0:
            col = st.selectbox("Select numeric column", num_cols)
            bins = st.slider("Select number of bins", 10, 100, 40)

            # Histogram with KDE
            fig = px.histogram(
                df, 
                x=col, 
                nbins=bins, 
                marginal="box",  # adds boxplot below
                opacity=0.75,
                color_discrete_sequence=["#4CAF50"], # green theme
                title=f"Distribution of {col}"
            )

            fig.update_layout(
                bargap=0.05,
                template="plotly_white",
                xaxis_title=col,
                yaxis_title="Count"
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ No numeric columns found.")
    else:
        st.warning("⚠️ Please upload a dataset first.")
    
    st.markdown('</div>', unsafe_allow_html=True)


# 🧹 Handle Missing Values
elif page == "🧹 Handle Missing Values":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("🩹 Handle Missing Values")
    if st.session_state.clean_df is not None:
        df = st.session_state.clean_df
        st.write(df.isnull().sum())

        col = st.selectbox("Select column", df.columns)
        option = st.radio("Choose a strategy", ["Remove Rows", "Fill with Mean", "Fill with Median", "Fill with Mode"])

        if st.button("Apply"):
            if option == "Remove Rows":
                df = df.dropna(subset=[col])
            elif option == "Fill with Mean":
                if df[col].dtype in ['int64','float64']:
                    df[col] = df[col].fillna(df[col].mean())
            elif option == "Fill with Median":
                if df[col].dtype in ['int64','float64']:
                    df[col] = df[col].fillna(df[col].median())
            elif option == "Fill with Mode":
                df[col] = df[col].fillna(df[col].mode()[0])

            st.session_state.clean_df = df
            st.success("✅ Missing values handled successfully!")
            st.dataframe(df.head(20))
    else:
        st.warning("⚠️ Please upload a dataset first.")
    st.markdown('</div>', unsafe_allow_html=True)

# 🔁 Handle Duplicates
elif page == "🔁 Handle Duplicates":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("🔁 Handle Duplicates")
    if st.session_state.clean_df is not None:
        df = st.session_state.clean_df
        dup_count = df.duplicated().sum()
        st.info(f"🔍 Found {dup_count} duplicate rows")
        if dup_count > 0 and st.button("Remove Duplicates"):
            df = df.drop_duplicates()
            st.session_state.clean_df = df
            st.success(f"✅ Removed {dup_count} duplicate rows")
    else:
        st.warning("⚠️ Please upload a dataset first.")
    st.markdown('</div>', unsafe_allow_html=True)

# 📊 Outlier Detection
elif page == "📊 Outlier Detection":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("🚨 Outlier Detection")
    if st.session_state.clean_df is not None:
        df = st.session_state.clean_df
        num_cols = df.select_dtypes(include=np.number).columns
        if len(num_cols) > 0:
            col = st.selectbox("Select numeric column", num_cols)
            Q1, Q3 = df[col].quantile([0.25, 0.75])
            IQR = Q3 - Q1
            lower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR
            outliers = df[(df[col] < lower) | (df[col] > upper)]

            st.warning(f"⚠️ Found {len(outliers)} outliers")
            fig = px.box(df, y=col, title=f"Boxplot of {col}")
            st.plotly_chart(fig, use_container_width=True)

            strategy = st.radio("Handling Strategy", ["Remove", "Replace with NaN", "Clip to Boundary"])
            if st.button("Apply Outlier Handling"):
                if strategy == "Remove":
                    df = df[(df[col] >= lower) & (df[col] <= upper)]
                elif strategy == "Replace with NaN":
                    df.loc[(df[col] < lower) | (df[col] > upper), col] = np.nan
                elif strategy == "Clip to Boundary":
                    df[col] = np.where(df[col] < lower, lower, df[col])
                    df[col] = np.where(df[col] > upper, upper, df[col])

                st.session_state.clean_df = df
                st.success("✅ Outliers handled successfully!")
                fig2 = px.box(df, y=col, title=f"Boxplot of {col} after handling")
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("⚠️ No numeric columns found.")
    else:
        st.warning("⚠️ Please upload a dataset first.")
    st.markdown('</div>', unsafe_allow_html=True)

# 📝 Fix Categories
elif page == "📝 Fix Categories":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("🔠 Fix Inconsistent Categories")
    if st.session_state.clean_df is not None:
        df = st.session_state.clean_df
        cat_cols = df.select_dtypes(include="object").columns
        if len(cat_cols) > 0:
            col = st.selectbox("Select categorical column", cat_cols)
            if col:
                unique_vals = df[col].unique()
                mapping = {}
                st.write("Current unique values:", unique_vals)
                for val in unique_vals:
                    new_val = st.text_input(f"Replace '{val}' with:", val, key=f"{col}_{val}")
                    mapping[val] = new_val
                if st.button("Apply Mapping"):
                    df[col] = df[col].replace(mapping)
                    st.session_state.clean_df = df
                    st.success("✅ Categories cleaned up successfully!")
                    st.write("Updated unique values:", df[col].unique())
        else:
            st.warning("⚠️ No categorical columns found.")
    else:
        st.warning("⚠️ Please upload a dataset first.")
    st.markdown('</div>', unsafe_allow_html=True)

# 💾 Download Data
elif page == "💾 Download Data":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("📥 Download Cleaned Dataset")
    if st.session_state.clean_df is not None:
        csv = st.session_state.clean_df.to_csv(index=False).encode("utf-8")
        st.download_button("💾 Download CSV", csv, "cleaned_dataset.csv", "text/csv")
    else:
        st.warning("⚠️ No dataset available.")
    st.markdown('</div>', unsafe_allow_html=True)
