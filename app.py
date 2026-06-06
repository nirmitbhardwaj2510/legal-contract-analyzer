import streamlit as st
import tempfile
import os
import math

st.set_page_config(
    page_title="LexAI — Contract Risk Analyzer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');
:root {
    --bg:#0a0a0f; --surface:#111118; --card:#16161f; --border:#2a2a3a;
    --accent:#c9a96e; --accent2:#7c6af7;
    --red:#ff4d6d; --yellow:#ffd166; --green:#06d6a0;
    --text:#e8e8f0; --muted:#6b6b80;
}
* { box-sizing:border-box; }
.stApp { background:var(--bg) !important; font-family:'DM Sans',sans-serif; }
#MainMenu, footer, header { visibility:hidden; }
.block-container { padding:0 !important; max-width:100% !important; }

.hero { background:linear-gradient(135deg,#0a0a0f 0%,#111128 50%,#0a0a0f 100%); border-bottom:1px solid var(--border); padding:48px 64px 40px; position:relative; overflow:hidden; }
.hero::before { content:''; position:absolute; top:-50%; left:-10%; width:500px; height:500px; background:radial-gradient(circle,rgba(124,106,247,0.08) 0%,transparent 70%); pointer-events:none; }
.badge { display:inline-flex; align-items:center; gap:6px; background:rgba(201,169,110,0.1); border:1px solid rgba(201,169,110,0.3); color:var(--accent); font-family:'DM Mono',monospace; font-size:11px; letter-spacing:2px; text-transform:uppercase; padding:6px 14px; border-radius:2px; margin-bottom:20px; }
.hero-title { font-family:'Playfair Display',serif; font-size:clamp(36px,5vw,64px); font-weight:900; color:var(--text); line-height:1.05; margin:0 0 16px; letter-spacing:-1px; }
.hero-title span { color:var(--accent); font-style:italic; }
.hero-sub { color:var(--muted); font-size:16px; font-weight:300; max-width:520px; line-height:1.6; margin:0; }
.hero-stats { display:flex; gap:40px; margin-top:36px; padding-top:36px; border-top:1px solid var(--border); }
.stat { display:flex; flex-direction:column; gap:4px; }
.stat-num { font-family:'Playfair Display',serif; font-size:28px; font-weight:700; color:var(--text); }
.stat-label { font-family:'DM Mono',monospace; font-size:10px; letter-spacing:1.5px; text-transform:uppercase; color:var(--muted); }
.main-content { padding:48px 64px; max-width:1200px; margin:0 auto; }
.section-label { font-family:'DM Mono',monospace; font-size:11px; letter-spacing:3px; text-transform:uppercase; color:var(--muted); margin-bottom:24px; padding-bottom:12px; border-bottom:1px solid var(--border); }

/* DASHBOARD */
.dashboard { background:var(--card); border:1px solid var(--border); border-radius:12px; padding:36px; margin-bottom:40px; }
.dashboard-title { font-family:'Playfair Display',serif; font-size:22px; color:var(--text); margin-bottom:28px; }
.dashboard-grid { display:grid; grid-template-columns:200px 1fr 1fr; gap:24px; align-items:center; }
.health-score-wrap { display:flex; flex-direction:column; align-items:center; gap:8px; }
.health-label { font-family:'DM Mono',monospace; font-size:11px; letter-spacing:1.5px; text-transform:uppercase; color:var(--muted); text-align:center; }
.metric-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
.metric-box { background:rgba(255,255,255,0.02); border:1px solid var(--border); border-radius:8px; padding:16px 20px; }
.metric-value { font-family:'Playfair Display',serif; font-size:32px; font-weight:700; line-height:1; margin-bottom:4px; }
.metric-value.red { color:var(--red); }
.metric-value.yellow { color:var(--yellow); }
.metric-value.green { color:var(--green); }
.metric-value.accent { color:var(--accent); }
.metric-name { font-family:'DM Mono',monospace; font-size:10px; letter-spacing:1.5px; text-transform:uppercase; color:var(--muted); }
.bar-section { display:flex; flex-direction:column; gap:16px; }
.bar-row { display:flex; flex-direction:column; gap:6px; }
.bar-label-row { display:flex; justify-content:space-between; align-items:center; }
.bar-name { font-family:'DM Mono',monospace; font-size:11px; color:var(--muted); text-transform:uppercase; letter-spacing:1px; }
.bar-val { font-family:'DM Mono',monospace; font-size:11px; color:var(--text); }
.bar-track { height:6px; background:rgba(255,255,255,0.05); border-radius:3px; overflow:hidden; }
.bar-fill { height:100%; border-radius:3px; }
.bar-fill.high { background:var(--red); }
.bar-fill.medium { background:var(--yellow); }
.bar-fill.low { background:var(--green); }

/* RISK CARDS */
.risk-card { background:var(--card); border-radius:8px; border:1px solid var(--border); padding:28px 32px; margin-bottom:16px; position:relative; overflow:hidden; }
.risk-card::before { content:''; position:absolute; left:0; top:0; bottom:0; width:3px; }
.risk-card.high::before { background:var(--red); }
.risk-card.medium::before { background:var(--yellow); }
.risk-card.low::before { background:var(--green); }
.risk-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:20px; }
.risk-category { font-family:'DM Mono',monospace; font-size:11px; letter-spacing:2px; text-transform:uppercase; color:var(--muted); }
.risk-badge { font-family:'DM Mono',monospace; font-size:11px; letter-spacing:1px; text-transform:uppercase; padding:4px 12px; border-radius:2px; font-weight:500; }
.risk-badge.high { background:rgba(255,77,109,0.15); color:var(--red); border:1px solid rgba(255,77,109,0.3); }
.risk-badge.medium { background:rgba(255,209,102,0.15); color:var(--yellow); border:1px solid rgba(255,209,102,0.3); }
.risk-badge.low { background:rgba(6,214,160,0.15); color:var(--green); border:1px solid rgba(6,214,160,0.3); }
.risk-content { display:grid; grid-template-columns:1fr 1fr; gap:20px; }
.risk-block { background:rgba(255,255,255,0.02); border:1px solid var(--border); border-radius:6px; padding:16px 20px; }
.risk-block-label { font-family:'DM Mono',monospace; font-size:10px; letter-spacing:1.5px; text-transform:uppercase; color:var(--accent); margin-bottom:8px; }
.risk-block-text { color:var(--text); font-size:13px; line-height:1.6; font-weight:300; }
.clause-box { background:rgba(0,0,0,0.3); border:1px solid var(--border); border-radius:6px; padding:16px 20px; margin-top:16px; font-family:'DM Mono',monospace; font-size:11px; color:var(--muted); line-height:1.7; }
.clause-label { font-size:10px; letter-spacing:1.5px; text-transform:uppercase; color:var(--accent2); margin-bottom:8px; }
.summary-bar { background:var(--card); border:1px solid var(--border); border-radius:8px; padding:24px 32px; display:flex; align-items:center; justify-content:space-between; margin-bottom:32px; }
.summary-title { font-family:'Playfair Display',serif; font-size:18px; color:var(--text); }
.summary-pills { display:flex; gap:12px; }
.pill { display:flex; align-items:center; gap:6px; padding:6px 16px; border-radius:100px; font-family:'DM Mono',monospace; font-size:12px; font-weight:500; }
.pill.high { background:rgba(255,77,109,0.15); color:var(--red); }
.pill.medium { background:rgba(255,209,102,0.15); color:var(--yellow); }
.pill.low { background:rgba(6,214,160,0.15); color:var(--green); }
.upload-zone { background:var(--card); border:2px dashed var(--border); border-radius:8px; padding:48px; text-align:center; }
.upload-icon { font-size:48px; margin-bottom:16px; display:block; }
.upload-title { font-family:'Playfair Display',serif; font-size:22px; color:var(--text); margin-bottom:8px; }
.upload-sub { color:var(--muted); font-size:13px; font-family:'DM Mono',monospace; }
.powered { text-align:center; padding:32px; border-top:1px solid var(--border); margin-top:48px; }
.powered-text { font-family:'DM Mono',monospace; font-size:11px; letter-spacing:2px; text-transform:uppercase; color:var(--muted); }
.powered-text span { color:var(--accent); }
</style>
""", unsafe_allow_html=True)

def make_health_gauge(score):
    radius = 60
    cx, cy = 80, 80
    circumference = 2 * math.pi * radius
    dash = (score / 100) * circumference
    gap = circumference - dash
    if score >= 70:
        stroke = "#06d6a0"
        label = "HEALTHY"
    elif score >= 40:
        stroke = "#ffd166"
        label = "CAUTION"
    else:
        stroke = "#ff4d6d"
        label = "HIGH RISK"
    return f"""
    <svg width="160" height="160" viewBox="0 0 160 160">
      <circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="#2a2a3a" stroke-width="10"/>
      <circle cx="{cx}" cy="{cy}" r="{radius}" fill="none"
        stroke="{stroke}" stroke-width="10"
        stroke-dasharray="{dash:.1f} {gap:.1f}"
        stroke-linecap="round"
        transform="rotate(-90 {cx} {cy})"/>
      <text x="{cx}" y="{cy-6}" text-anchor="middle"
        font-family="Playfair Display,serif"
        font-size="28" font-weight="700" fill="#e8e8f0">{score}</text>
      <text x="{cx}" y="{cy+16}" text-anchor="middle"
        font-family="DM Mono,monospace"
        font-size="9" letter-spacing="2" fill="{stroke}">{label}</text>
    </svg>"""

def make_bar(label, count, total, level):
    pct = int((count / total) * 100) if total > 0 else 0
    return f"""
    <div class="bar-row">
        <div class="bar-label-row">
            <span class="bar-name">{label}</span>
            <span class="bar-val">{count} clauses</span>
        </div>
        <div class="bar-track">
            <div class="bar-fill {level}" style="width:{pct}%"></div>
        </div>
    </div>"""

# ── HERO ──
st.markdown("""
<div class="hero">
    <div class="badge">⚖ LexAI &nbsp;·&nbsp; Powered by Cohere</div>
    <h1 class="hero-title">Legal Contract<br><span>Risk Analysis</span></h1>
    <p class="hero-sub">Upload any contract PDF. Our RAG pipeline identifies risky clauses instantly — liability, IP, termination, and more.</p>
    <div class="hero-stats">
        <div class="stat"><span class="stat-num">6</span><span class="stat-label">Risk Categories</span></div>
        <div class="stat"><span class="stat-num">30s</span><span class="stat-label">Analysis Time</span></div>
        <div class="stat"><span class="stat-num">RAG</span><span class="stat-label">Pipeline</span></div>
        <div class="stat"><span class="stat-num">100%</span><span class="stat-label">AI Powered</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-content">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Step 01 — Upload Document</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")

if uploaded_file is None:
    st.markdown("""
    <div class="upload-zone">
        <span class="upload-icon">📄</span>
        <div class="upload-title">Drop your contract here</div>
        <div class="upload-sub">Supports PDF · Any contract type · Max 50MB</div>
    </div>""", unsafe_allow_html=True)

if uploaded_file is not None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.success(f"✅ **{uploaded_file.name}** uploaded successfully")
        analyze_btn = st.button("⚖️ Analyze Contract Risks", type="primary", use_container_width=True)

    if analyze_btn:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        st.markdown('<div class="section-label" style="margin-top:40px;">Step 02 — AI Analysis</div>', unsafe_allow_html=True)

    with st.spinner("🔍 Analyzing with Cohere RAG pipeline..."):
        from analyzer import analyze_contract
        results = analyze_contract(tmp_path)

        high_c = sum(1 for r in results if "RISK LEVEL: HIGH" in r["analysis"])
        med_c  = sum(1 for r in results if "RISK LEVEL: MEDIUM" in r["analysis"])
        low_c  = len(results) - high_c - med_c
        total  = len(results)
        health = max(0, 100 - (high_c * 25) - (med_c * 10) - (low_c * 2))

        # ── DASHBOARD ──
        st.markdown('<div class="section-label" style="margin-top:40px;">Contract Health Dashboard</div>', unsafe_allow_html=True)

        gauge = make_health_gauge(health)
        bars  = make_bar("High Risk", high_c, total, "high") + \
                make_bar("Medium Risk", med_c, total, "medium") + \
                make_bar("Low Risk", low_c, total, "low")

        st.markdown(f"""
        <div class="dashboard">
            <div class="dashboard-title">Contract Health Overview</div>
            <div class="dashboard-grid">
                <div class="health-score-wrap">
                    {gauge}
                    <div class="health-label">Health Score</div>
                </div>
                <div class="metric-grid">
                    <div class="metric-box"><div class="metric-value red">{high_c}</div><div class="metric-name">High Risk</div></div>
                    <div class="metric-box"><div class="metric-value yellow">{med_c}</div><div class="metric-name">Medium Risk</div></div>
                    <div class="metric-box"><div class="metric-value green">{low_c}</div><div class="metric-name">Low Risk</div></div>
                    <div class="metric-box"><div class="metric-value accent">{total}</div><div class="metric-name">Total Analyzed</div></div>
                </div>
                <div class="bar-section">{bars}</div>
            </div>
        </div>""", unsafe_allow_html=True)

        # ── RISK CARDS ──
        st.markdown('<div class="section-label">Step 03 — Detailed Risk Report</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="summary-bar">
            <div class="summary-title">Risk Analysis Complete — {total} Categories Analyzed</div>
            <div class="summary-pills">
                <div class="pill high">🔴 {high_c} High</div>
                <div class="pill medium">🟡 {med_c} Medium</div>
                <div class="pill low">🟢 {low_c} Low</div>
            </div>
        </div>""", unsafe_allow_html=True)

        for risk in results:
            analysis = risk["analysis"]
            if "RISK LEVEL: HIGH" in analysis:
                level, badge_text = "high", "HIGH RISK"
            elif "RISK LEVEL: MEDIUM" in analysis:
                level, badge_text = "medium", "MEDIUM RISK"
            else:
                level, badge_text = "low", "LOW RISK"

            plain_english = warning = ""
            for line in analysis.split("\n"):
                if "PLAIN ENGLISH:" in line:
                    plain_english = line.replace("PLAIN ENGLISH:", "").strip()
                elif "WARNING:" in line or "WARNINGS:" in line:
                    warning = line.replace("WARNINGS:", "").replace("WARNING:", "").strip()

            clause_preview = risk["chunks"][0][:300] + "..." if risk["chunks"] else ""

            st.markdown(f"""
            <div class="risk-card {level}">
                <div class="risk-header">
                    <div class="risk-category">{risk['category'].upper()}</div>
                    <div class="risk-badge {level}">{badge_text}</div>
                </div>
                <div class="risk-content">
                    <div class="risk-block">
                        <div class="risk-block-label">Plain English</div>
                        <div class="risk-block-text">{plain_english or 'See analysis below'}</div>
                    </div>
                    <div class="risk-block">
                        <div class="risk-block-label">⚠ Warning</div>
                        <div class="risk-block-text">{warning or 'Review carefully'}</div>
                    </div>
                </div>
                <div class="clause-box">
                    <div class="clause-label">📋 Relevant Contract Clause</div>
                    {clause_preview}
                </div>
            </div>""", unsafe_allow_html=True)

        os.unlink(tmp_path)

        st.markdown("""
        <div class="powered">
            <div class="powered-text">Powered by <span>Cohere Embed v3 + Command R+</span> · RAG Pipeline · LangChain + ChromaDB</div>
        </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)