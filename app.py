+import json
+
+import streamlit as st
+
+from pyseoanalyzer import analyze
+
+
+st.set_page_config(page_title="Python SEO Analyzer", page_icon="📈", layout="wide")
+st.title("Python SEO & GEO Analyzer")
+st.caption("Run SEO analysis from a simple Streamlit interface.")
+
+with st.sidebar:
+    st.header("Configuration")
+    site = st.text_input("Site URL", placeholder="https://example.com")
+    sitemap = st.text_input("Sitemap URL (optional)", placeholder="https://example.com/sitemap.xml")
+
+    analyze_headings = st.checkbox("Analyze heading tags (h1-h6)", value=False)
+    analyze_extra_tags = st.checkbox("Analyze extra tags", value=False)
+    follow_links = st.checkbox("Follow internal links", value=True)
+    run_llm_analysis = st.checkbox("Run LLM analysis", value=False)
+
+    run = st.button("Analyze site", type="primary", use_container_width=True)
+
+if run:
+    if not site:
+        st.error("Please provide a site URL.")
+    else:
+        with st.spinner("Analyzing site..."):
+            result = analyze(
+                site,
+                sitemap_url=sitemap or None,
+                analyze_headings=analyze_headings,
+                analyze_extra_tags=analyze_extra_tags,
+                follow_links=follow_links,
+                run_llm_analysis=run_llm_analysis,
+            )
+
+        st.success("Analysis complete")
+
+        col1, col2, col3 = st.columns(3)
+        col1.metric("Pages analyzed", len(result.get("pages", [])))
+        col2.metric("Keywords found", len(result.get("keywords", [])))
+        col3.metric("Total time (s)", f"{result.get('total_time', 0):.2f}")
+
+        with st.expander("Top keywords", expanded=True):
+            st.dataframe(result.get("keywords", [])[:50], use_container_width=True)
+
+        with st.expander("Pages", expanded=False):
+            st.json(result.get("pages", []))
+
+        with st.expander("Duplicate pages", expanded=False):
+            st.json(result.get("duplicate_pages", []))
+
+        st.download_button(
+            "Download JSON",
+            data=json.dumps(result, indent=2),
+            file_name="seo_analysis.json",
+            mime="application/json",
+            use_container_width=True,
+        )
+else:
+    st.info("Enter configuration in the sidebar and click **Analyze site**.")
