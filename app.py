import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Page configuration
st.set_page_config(page_title="✨ Data Sweeper by Maira Fatima", layout="wide")

# Custom CSS for modern, fresh UI
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #74ebd5, #ACB6E5);
        font-family: 'Segoe UI', sans-serif;
        color: #333333;
    }
    h1, h2, h3, h4 {
        color: #003366;
    }
    .stButton>button {
        background-color: #003366;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #0055aa;
        transition: 0.3s;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🚀 Data Sweeper - Sterling Integrator")
st.caption("Made by **Jawad Shoukat** | Transform, Clean, and Visualize Your Data Effortlessly.")

# File uploader
st.header("📂 Upload your Files (CSV or Excel)")
uploaded_files = st.file_uploader("Choose files to upload:", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file, engine='openpyxl')
            else:
                st.error(f"Unsupported file type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"Error reading {file.name}: {e}")
            continue

        # Preview
        st.subheader(f"🔎 Preview of `{file.name}`")
        st.dataframe(df, use_container_width=True)

        # Data cleaning options
        st.markdown("---")
        st.subheader("🛠️ Data Cleaning")
        if st.checkbox(f"🧹 Clean data for `{file.name}`"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"❌ Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates removed successfully!")
                    
            with col2:
                if st.button(f"🩹 Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing values filled with column means!")

        # Select columns
        st.markdown("---")
        st.subheader("📝 Select Columns to Keep")
        columns = st.multiselect(f"Select columns from `{file.name}`", df.columns, default=df.columns)
        df = df[columns]

        # Data visualization
        st.markdown("---")
        st.subheader("📊 Quick Data Visualization")
        if st.checkbox(f"📈 Show Charts for `{file.name}`"):
            if len(df.select_dtypes(include='number').columns) >= 1:
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
            else:
                st.warning("No numeric columns to visualize.")

        # Conversion Options
        st.markdown("---")
        st.subheader("🔄 Convert and Download")
        conversion_type = st.radio(f"Choose format for `{file.name}`:", ["CSV", "Excel"], key=file.name)

        if st.button(f"💾 Convert and Download {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False, engine='openpyxl')
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)
            st.download_button(
                label=f"⬇️ Download `{file_name}`",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
        
        st.success(f"✅ `{file.name}` processed and ready!")

# Footer Section
st.markdown(
    '<div class="footer">This was created by Fatima.</div>',
    unsafe_allow_html=True
)


