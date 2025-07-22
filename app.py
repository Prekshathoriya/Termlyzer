import streamlit as st
from utils.parser import extract_text_from_pdf, extract_text_from_url, get_clean_text
from utils.summarizer import generate_summary
from utils.risk_detector import detect_risky_clauses

st.set_page_config(page_title="Termlyzer", layout="wide")

st.title("📄 Termlyzer – Decode Legal Jargon, Instantly!")
st.markdown("Upload Terms & Conditions, Privacy Policy, or any contract to get a simplified summary and risk report.")

# --- Sidebar for Input ---
st.sidebar.header("📥 Input Options")
input_type = st.sidebar.radio("Choose Input Type:", ["📄 Upload PDF", "📝 Paste Text", "🌐 Enter URL"])

uploaded_file = None
input_text = ""
input_url = ""

if input_type == "📄 Upload PDF":
    uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])
elif input_type == "📝 Paste Text":
    input_text = st.sidebar.text_area("Paste your document text here:")
elif input_type == "🌐 Enter URL":
    input_url = st.sidebar.text_input("Enter a public URL:")

# --- Analysis Trigger ---
if st.sidebar.button("🔍 Analyze Document"):
    raw_text = ""

    if input_type == "📄 Upload PDF" and uploaded_file is not None:
        raw_text = extract_text_from_pdf(uploaded_file)
    elif input_type == "📝 Paste Text" and input_text.strip():
        raw_text = input_text
    elif input_type == "🌐 Enter URL" and input_url.strip():
        raw_text = extract_text_from_url(input_url)

    cleaned_text = get_clean_text(raw_text)

    if cleaned_text:
        st.success("✅ Document processed successfully!")

        # --- Show Original Text ---
        with st.expander("📃 View Extracted Document Text"):
            st.text_area("Extracted Text:", cleaned_text, height=300)

        # --- Generate Summary ---
        with st.spinner("🔎 Generating Summary..."):
            summary = generate_summary(cleaned_text)
            if summary:
                st.subheader("📌 Simplified Summary")
                for bullet in summary:
                    st.markdown(f"- {bullet}")
            else:
                st.warning("No summary generated.")

        # --- Risky Clause Detection ---
        risky_clauses = detect_risky_clauses(cleaned_text)
        st.subheader("🚨 Flagged Risky Clauses")

        if risky_clauses:
            for item in risky_clauses:
                st.markdown(f"🔴 **[{item['tag']}]** {item['clause']}")
        else:
            st.success("✅ No risky clauses detected!")

        # --- Download
        st.subheader("📤 Download Report")
        full_summary = "\n".join(summary)
        report = f"--- SUMMARY ---\n{full_summary}\n\n--- RISKY CLAUSES ---\n" + \
                 "\n".join([f"[{c['tag']}] {c['clause']}" for c in risky_clauses])
        st.download_button("Download Summary Report", data=report, file_name="termlyzer_summary.txt")
    else:
        st.error("❌ Could not extract or summarize the text. Please check your input.")
