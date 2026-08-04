import streamlit as st
import pandas as pd
from io import BytesIO

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Inventory Order Recommendations",
    page_icon="📦",
    layout="wide"
)

# =========================
# PROFESSIONAL CSS / DESIGN SYSTEM
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, .stApp, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.stApp {
    background: #f3f5f9;
    color: #1f2d3d;
}

[data-testid="stHeader"] {
    background: transparent;
    height: 0rem;
}

[data-testid="stDecoration"] {
    display: none;
}

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    max-width: 1180px;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    width: 320px !important;
    min-width: 320px !important;
    max-width: 340px !important;
}

section[data-testid="stSidebar"] > div {
    background: #0f2540;
    padding-top: 1.4rem;
}

section[data-testid="stSidebar"] * {
    color: #d8e1ec;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ffffff;
}

section[data-testid="stSidebar"] hr {
    display: block !important;
    border: none;
    border-top: 1px solid rgba(255,255,255,0.12);
    margin: 1.1rem 0;
}

/* ---------- Hero ---------- */
.hero {
    background: linear-gradient(135deg, #0b2540 0%, #1d3f63 55%, #2a5688 100%);
    padding: 36px 40px;
    border-radius: 20px;
    color: #ffffff;
    margin-bottom: 26px;
    box-shadow: 0 16px 40px rgba(11, 37, 64, 0.28);
}

.hero h1 {
    margin: 0;
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -0.6px;
    line-height: 1.15;
}

.hero p {
    margin: 12px 0 0 0;
    font-size: 15.5px;
    color: #cdd9e7;
    max-width: 760px;
    line-height: 1.55;
}

/* ---------- Real cards (st.container(border=True)) ---------- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff;
    border: 1px solid #e6eaf0;
    border-radius: 16px;
    padding: 6px 22px 14px 22px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
    margin-bottom: 20px;
}

/* ---------- Section headers ---------- */
.section-title {
    font-size: 19px;
    font-weight: 700;
    color: #0f2540;
    margin: 10px 0 2px 0;
    letter-spacing: -0.2px;
}

.section-subtitle {
    font-size: 13.5px;
    color: #6b7c93;
    margin-bottom: 16px;
    line-height: 1.5;
}

/* ---------- Info / status boxes ---------- */
.info-box, .success-box, .warning-box, .info-box1 {
    padding: 16px 18px;
    border-radius: 12px;
    font-size: 13.5px;
    line-height: 1.6;
}

.info-box, .info-box1 {
    background: #eef5ff;
    border-left: 4px solid #2f6fed;
    color: #1f3a5f;
}

.success-box {
    background: #ecfdf5;
    border-left: 4px solid #10b981;
    color: #065f46;
}

.warning-box {
    background: #fffbeb;
    border-left: 4px solid #f59e0b;
    color: #92400e;
}

/* ---------- Metric cards ---------- */
.metric-card {
    background: #ffffff;
    border: 1px solid #e6eaf0;
    padding: 18px 20px;
    border-radius: 14px;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
    height: 100%;
}

.metric-label {
    font-size: 12.5px;
    color: #6b7c93;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    margin-bottom: 8px;
}

.metric-value {
    font-size: 30px;
    color: #0f2540;
    font-weight: 800;
    line-height: 1;
}

.metric-note {
    font-size: 11.5px;
    color: #94a3b8;
    margin-top: 8px;
}

/* ---------- Inputs ---------- */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    border: 1px solid #cdd7e4;
    background: #ffffff;
    color: #0f2540;
    padding: 0.5rem 1.1rem;
}

.stButton > button:hover {
    border-color: #2f6fed;
    color: #2f6fed;
}

.stDownloadButton > button {
    background: linear-gradient(135deg, #2f6fed 0%, #1b53cc 100%);
    color: #ffffff;
    border: none;
    border-radius: 10px;
    padding: 0.7rem 1rem;
    font-weight: 700;
    box-shadow: 0 10px 20px rgba(47, 111, 237, 0.25);
}

.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #1b53cc 0%, #1645ad 100%);
    color: #ffffff;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HERO
# =========================
st.markdown("""
<div class="hero">
    <h1>📦 Inventory Order Recommendations</h1>
    <p>Upload your inventory file, set a default safety factor, optionally provide item-level factors,
    and export a clean replenishment recommendation report.</p>
</div>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR PARAMETERS
# =========================
with st.sidebar:
    st.markdown("## ⚙️ Parameters")
    st.markdown("Set the planning values below.")

    months = st.number_input(
        "Months",
        min_value=1.0,
        value=17.0,
        step=0.5,
        format="%.1f"
    )

    default_factor = st.number_input(
        "Default FACTOR",
        min_value=0.0,
        value=6.0,
        step=0.1,
        format="%.1f"
    )

    st.markdown("---")

    st.markdown("### Factor Rule")
    st.markdown(
        f"""
        By default, the app applies this factor to all items: **Default FACTOR = {default_factor}**

        You may optionally upload a Safety Factor File to use different factors per item.
        """
    )

    st.markdown("---")

    st.markdown("### Formula")
    st.markdown(
        """
        **In order** \n
        = PO not Shipped + PR Approved Qty + PO Qty + Blanket PO Qty + Qty to Recieve - Advanced Reserved

        **Forcasted** \n
        = Stock Available Quantity + In order

        **Sales 25&26** \n
        = Qty Sold + Qty Sold PYear + Cons. Qty + Cons. Qty New

        **Safety** \n
        = ROUND(Sales 25&26 / Months) × FACTOR

        **Order**
        = Safety - Forcasted
        """
    )

# =========================
# FILE UPLOAD CARD
# =========================
with st.container(border=True):
    left, right = st.columns([1.4, 1])

    with left:
        st.markdown('<div class="section-title">📂 Upload Files</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtitle">Upload the main inventory file. The safety factor file is optional.</div>',
            unsafe_allow_html=True
        )

        upload_col1, upload_col2 = st.columns(2)

        with upload_col1:
            uploaded_file = st.file_uploader(
                "Main Inventory File",
                type=["xlsx"]
            )

        with upload_col2:
            sf_file = st.file_uploader(
                "Optional Safety Factor File",
                type=["xlsx"]
            )

    with right:
        st.markdown("""
        <div class="info-box">
            <strong>Main file:</strong> Required inventory report<br><br>
            <strong>Safety file:</strong> Optional item-level factor file<br><br>
            <strong>Default behavior:</strong> One factor applied to all items<br><br>
            <strong>Zero-only columns:</strong> Removed automatically
        </div>
        """, unsafe_allow_html=True)

    if uploaded_file and sf_file:
        st.success("✅ Main file and safety factor file uploaded. Item-level factors will be used.")
    elif uploaded_file:
        st.info("ℹ️ Main file uploaded. The default FACTOR from the sidebar will be applied to all items.")
    else:
        st.warning("⚠️ Please upload the main inventory file to generate the inventory report.")

# =========================
# MAIN LOGIC
# =========================
if uploaded_file:

    # -------------------------
    # LOAD MAIN DATA
    # -------------------------
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    # -------------------------
    # REQUIRED MAIN FILE COLUMNS
    # -------------------------
    required_columns = [
        "Item No.1",
        "Description",
        "Stock Available Quantity",
        "Advanced Reserved",
        "PR Approved Qty",
        "PO Qty",
        "PO not Shipped",
        "Qty to Recieve",
        "Qty Sold",
        "Qty Sold PYear",
        "Cons. Qty",
        "Cons. Qty New",
        "Blanket PO Qty"
    ]

    missing_cols = [c for c in required_columns if c not in df.columns]

    if missing_cols:
        with st.container(border=True):
            st.error(f"❌ Missing columns in main file: {missing_cols}")
            st.write("Detected columns:", df.columns.tolist())
        st.stop()

    # -------------------------
    # KEEP ONLY NEEDED COLUMNS
    # -------------------------
    df = df[required_columns].copy()

    # -------------------------
    # CLEAN ITEM NUMBER
    # -------------------------
    df["Item No.1"] = df["Item No.1"].astype(str).str.strip()

    # -------------------------
    # DEFAULT FACTOR MODE
    # -------------------------
    df["Safety stock factor"] = default_factor
    missing_factor_count = 0
    factor_source = "Default FACTOR"

    # -------------------------
    # OPTIONAL SAFETY FACTOR FILE
    # -------------------------
    if sf_file:
        safety_df = pd.read_excel(sf_file)
        safety_df.columns = safety_df.columns.str.strip()

        required_sf_cols = [
            "Item No.1",
            "Safety stock factor"
        ]

        missing_sf = [c for c in required_sf_cols if c not in safety_df.columns]

        if missing_sf:
            with st.container(border=True):
                st.error(f"❌ Missing columns in safety factor file: {missing_sf}")
                st.write("Detected columns:", safety_df.columns.tolist())
            st.stop()

        safety_df = safety_df[required_sf_cols].copy()

        safety_df["Item No.1"] = safety_df["Item No.1"].astype(str).str.strip()

        safety_df["Safety stock factor"] = pd.to_numeric(
            safety_df["Safety stock factor"],
            errors="coerce"
        )

        safety_df = safety_df.drop_duplicates(
            subset=["Item No.1"],
            keep="first"
        )

        df = df.drop(columns=["Safety stock factor"]).merge(
            safety_df,
            on="Item No.1",
            how="left"
        )

        missing_factor_count = df["Safety stock factor"].isna().sum()

        df["Safety stock factor"] = df["Safety stock factor"].fillna(default_factor)

        factor_source = "Uploaded item-level FACTOR file"

    # -------------------------
    # NUMERIC CONVERSION
    # -------------------------
    numeric_columns = [
        "Stock Available Quantity",
        "Advanced Reserved",
        "PR Approved Qty",
        "PO Qty",
        "PO not Shipped",
        "Qty to Recieve",
        "Qty Sold",
        "Qty Sold PYear",
        "Cons. Qty",
        "Cons. Qty New",
        "Safety stock factor",
        "Blanket PO Qty"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # =========================
    # SAFETY FACTOR MANAGEMENT
    # =========================
    with st.container(border=True):
        st.markdown('<div class="section-title">✏️ Safety Factor Management</div>', unsafe_allow_html=True)

        if sf_file:
            st.markdown(
                '<div class="section-subtitle">Item-level safety factors are loaded from the optional safety factor file. Missing factors use the default FACTOR from the sidebar.</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="section-subtitle">The default FACTOR from the sidebar is applied to all items. You can still edit factors before exporting.</div>',
                unsafe_allow_html=True
            )

        status_col1, status_col2 = st.columns(2)

        with status_col1:
            st.markdown(f"""
            <div class="success-box">
                <strong>Factor source:</strong> {factor_source}<br>
                <strong>Default FACTOR:</strong> {default_factor}
            </div>
            """, unsafe_allow_html=True)

        with status_col2:
            if sf_file and missing_factor_count > 0:
                st.markdown(f"""
                <div class="warning-box">
                    <strong>Missing item factors:</strong> {missing_factor_count}<br>
                    These items were filled with the default FACTOR.
                </div>
                """, unsafe_allow_html=True)
            elif sf_file:
                st.markdown("""
                <div class="success-box">
                    <strong>Safety factor file:</strong> Uploaded<br>
                    All matched items were processed successfully.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="info-box1">
                    <strong>Safety factor file:</strong> Not uploaded<br>
                    The default FACTOR is applied to every item.
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height: 6px'></div>", unsafe_allow_html=True)

        if "edit_mode" not in st.session_state:
            st.session_state.edit_mode = False

        edit_button_label = "Hide Safety Factor Editor" if st.session_state.edit_mode else "Edit Safety Factors"

        if st.button(edit_button_label):
            st.session_state.edit_mode = not st.session_state.edit_mode

        if st.session_state.edit_mode:
            edit_df = df[
                [
                    "Item No.1",
                    "Description",
                    "Safety stock factor"
                ]
            ].copy()

            edited = st.data_editor(
                edit_df,
                column_config={
                    "Item No.1": st.column_config.TextColumn(
                        "Item No.1",
                        disabled=True
                    ),
                    "Description": st.column_config.TextColumn(
                        "Description",
                        disabled=True
                    ),
                    "Safety stock factor": st.column_config.NumberColumn(
                        "Safety stock factor",
                        min_value=0.0,
                        step=0.1,
                        format="%.2f"
                    )
                },
                use_container_width=True,
                height=350,
                hide_index=True
            )

            df["Safety stock factor"] = pd.to_numeric(
                edited["Safety stock factor"],
                errors="coerce"
            ).fillna(default_factor).values

    # -------------------------
    # CALCULATIONS
    # -------------------------
    df["In order"] = df["PO not Shipped"] + df["PR Approved Qty"] + df["PO Qty"] + df["Qty to Recieve"] + df["Blanket PO Qty"] - df["Advanced Reserved"]

    df["Forcasted"] = df["Stock Available Quantity"] + df["In order"]

    df["Sales 25&26"] = (
        df["Qty Sold"]
        + df["Qty Sold PYear"]
        + df["Cons. Qty"]
        + df["Cons. Qty New"]
    )

    df["Safety"] = ((df["Sales 25&26"] / months).round(0) * df["Safety stock factor"])

    df["FACTOR"] = df["Safety stock factor"]

    df["order"] = df["Safety"] - df["Forcasted"]

    # -------------------------
    # FINAL COLUMN ORDER
    # -------------------------
    final_columns = [
        "Item No.1",
        "Description",
        "Stock Available Quantity",
        "In order",
        "Advanced Reserved",
        "Forcasted",
        "Qty Sold",
        "Qty Sold PYear",
        "PO not Shipped",
        "Blanket PO Qty",
        "Cons. Qty",
        "Cons. Qty New",
        "Sales 25&26",
        "Safety",
        "FACTOR",
        "order"
    ]

    df = df[final_columns]

    # -------------------------
    # REMOVE COLUMNS THAT CONTAIN ONLY 0
    # Keep item and description columns.
    # -------------------------
    protected_columns = [
        "Item No.1",
        "Description"
    ]

    for col in df.columns.tolist():
        if col not in protected_columns:
            numeric_col = pd.to_numeric(df[col], errors="coerce").fillna(0)

            if (numeric_col == 0).all():
                df.drop(columns=[col], inplace=True)

    # =========================
    # SUMMARY SECTION
    # =========================
    with st.container(border=True):
        st.markdown('<div class="section-title">📊 Report Summary</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtitle">A quick overview of the processed inventory file.</div>',
            unsafe_allow_html=True
        )

        total_items = len(df)
        total_safety = int(df["Safety"].sum()) if "Safety" in df.columns else 0
        items_to_order = int((df["order"] > 0).sum()) if "order" in df.columns else 0
        total_order_qty = int(df.loc[df["order"] > 0, "order"].sum()) if "order" in df.columns else 0

        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Items</div>
                <div class="metric-value">{total_items:,}</div>
                <div class="metric-note">Rows processed</div>
            </div>
            """, unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Missing Factors</div>
                <div class="metric-value">{missing_factor_count:,}</div>
                <div class="metric-note">Filled with default factor</div>
            </div>
            """, unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Items to Order</div>
                <div class="metric-value">{items_to_order:,}</div>
                <div class="metric-note">Items where order &gt; 0</div>
            </div>
            """, unsafe_allow_html=True)

        with m4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Order Qty</div>
                <div class="metric-value">{total_order_qty:,}</div>
                <div class="metric-note">Sum of positive order qty</div>
            </div>
            """, unsafe_allow_html=True)

    # =========================
    # RESULTS SECTION
    # =========================
    with st.container(border=True):
        top_left, top_right = st.columns([2, 1])

        with top_left:
            st.markdown('<div class="section-title">📋 Processed Results</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="section-subtitle">Review the calculated inventory recommendations before exporting.</div>',
                unsafe_allow_html=True
            )

        with top_right:
            search_text = st.text_input(
                "Search item or description",
                placeholder="Type to filter...",
                label_visibility="collapsed"
            )

        display_df = df.copy()

        if search_text:
            search_text = search_text.lower()

            display_df = display_df[
                display_df["Item No.1"].astype(str).str.lower().str.contains(search_text, na=False)
                | display_df["Description"].astype(str).str.lower().str.contains(search_text, na=False)
            ]

        st.dataframe(
            display_df,
            use_container_width=True,
            height=520
        )

    # =========================
    # EXPORT SECTION
    # =========================
    with st.container(border=True):
        export_left, export_right = st.columns([2, 1])

        with export_left:
            st.markdown('<div class="section-title">⬇️ Export Report</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="section-subtitle">Download the complete processed file as Excel. Search filtering does not affect the exported file.</div>',
                unsafe_allow_html=True
            )

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="All Items")

            if "order" in df.columns:
                to_order_df = df[df["order"] > 0].copy()
            else:
                to_order_df = df.iloc[0:0].copy()

            to_order_df.to_excel(writer, index=False, sheet_name="Items to Order")
        output.seek(0)

        with export_right:
            st.download_button(
                label="📥 Download Excel Report",
                data=output,
                file_name="processed_inventory.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
