import streamlit as st
import time
import datetime
import random
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NexusResearch · Case File",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Case number, generated once per session ───────────────────────────────────
if "case_no" not in st.session_state:
    st.session_state.case_no = f"{random.randint(1000, 9999)}-{datetime.datetime.now().strftime('%y')}"
if "opened_on" not in st.session_state:
    st.session_state.opened_on = datetime.datetime.now().strftime("%d %b %Y")

# ── Custom CSS: Case File / Dossier Workspace ─────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Lora:ital,wght@0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
    --paper:      #ece1c4;
    --paper-dark: #e2d3a8;
    --paper-card: #f2e9d1;
    --ink:        #221d14;
    --ink-soft:   #4a4331;
    --line:       rgba(34, 29, 20, 0.22);
    --line-soft:  rgba(34, 29, 20, 0.12);
    --stamp-red:  #9a2b23;
    --stamp-blue: #2c4a6e;
    --redact:     #18140c;
}

html, body, [class*="css"] {
    font-family: 'Lora', serif;
    color: var(--ink);
}

.stApp {
    background-color: var(--paper);
    background-image:
        repeating-linear-gradient(0deg, transparent, transparent 34px, var(--line-soft) 35px),
        radial-gradient(ellipse at 15% 0%, rgba(34,29,20,0.05) 0%, transparent 55%),
        radial-gradient(ellipse at 85% 100%, rgba(34,29,20,0.05) 0%, transparent 55%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.2rem 3.2rem 4rem; max-width: 1360px; }

/* ── Folder Header ── */
.dossier-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 3px double var(--ink);
    padding-bottom: 0.9rem;
    margin-bottom: 0.4rem;
}
.dossier-title {
    font-family: 'Special Elite', monospace;
    font-size: 1.7rem;
    letter-spacing: 0.02em;
    color: var(--ink);
    text-transform: uppercase;
}
.dossier-title small {
    display: block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: var(--ink-soft);
    letter-spacing: 0.15em;
    margin-top: 0.3rem;
    text-transform: none;
}
.dossier-meta {
    text-align: right;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--ink-soft);
    line-height: 1.5;
}
.dossier-meta b { color: var(--ink); }
.dossier-subbar {
    display: flex;
    gap: 1.4rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.12em;
    color: var(--ink-soft);
    margin: 0.6rem 0 2rem;
    text-transform: uppercase;
}
.dossier-subbar span::before { content: "· "; color: var(--stamp-red); }

/* ── Intake Card ── */
.intake-card {
    background: var(--paper-card);
    border: 1px solid var(--line);
    box-shadow: 4px 4px 0 rgba(34,29,20,0.08);
    padding: 1.4rem 1.6rem 1.1rem;
    margin-bottom: 1.6rem;
    position: relative;
}
.intake-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    color: var(--stamp-red);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.stTextInput > div > div > input {
    background: transparent !important;
    border: none !important;
    border-bottom: 1.5px solid var(--ink) !important;
    border-radius: 0 !important;
    color: var(--ink) !important;
    font-family: 'Lora', serif !important;
    font-size: 1.08rem !important;
    padding: 0.4rem 0.1rem !important;
}
.stTextInput > div > div > input:focus {
    box-shadow: none !important;
    border-bottom: 1.5px solid var(--stamp-red) !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(34,29,20,0.4); font-style: italic; }

/* ── Action Button ── */
.stButton > button {
    background: var(--ink) !important;
    color: var(--paper) !important;
    font-family: 'Special Elite', monospace !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.08em !important;
    border-radius: 0 !important;
    padding: 0.75rem 1.4rem !important;
    border: 1px solid var(--ink) !important;
    text-transform: uppercase;
    width: 100%;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: var(--stamp-red) !important;
    border-color: var(--stamp-red) !important;
    color: var(--paper) !important;
}

/* ── Leads / preset chips ── */
.leads-row {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    flex-wrap: wrap;
    margin: -0.6rem 0 1.8rem;
}
.leads-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.12em;
    color: var(--ink-soft);
    text-transform: uppercase;
}
.lead-chip {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--ink-soft);
    border: 1px dashed var(--line);
    padding: 0.22rem 0.55rem;
    background: rgba(255,255,255,0.25);
}

/* ── Folder Tabs (agent nodes) ── */
.tabs-heading {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.15em;
    color: var(--stamp-red);
    text-transform: uppercase;
    margin-bottom: 0.9rem;
}
.folder-tab {
    position: relative;
    background: var(--paper-card);
    border: 1px solid var(--line);
    border-left: 4px solid var(--line);
    padding: 0.85rem 1rem 0.85rem 1rem;
    margin-bottom: 0.65rem;
    transition: border-color 0.2s ease;
}
.folder-tab.running { border-left-color: var(--stamp-blue); }
.folder-tab.done { border-left-color: var(--stamp-red); }
.exhibit-id {
    font-family: 'Special Elite', monospace;
    font-size: 0.7rem;
    color: var(--ink-soft);
    letter-spacing: 0.08em;
}
.exhibit-title {
    font-family: 'Lora', serif;
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--ink);
    margin-top: 0.15rem;
}
.exhibit-status {
    position: absolute;
    top: 0.85rem;
    right: 0.9rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    padding: 0.12rem 0.4rem;
    border: 1px solid transparent;
}
.st-wait { color: rgba(34,29,20,0.35); border-color: var(--line-soft); }
.st-run  { color: var(--stamp-blue); border-color: var(--stamp-blue); animation: typecursor 1.1s steps(2) infinite; }
.st-ok   { color: var(--stamp-red); border-color: var(--stamp-red); transform: rotate(-3deg); font-weight: 700; }

@keyframes typecursor {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.25; }
}

/* ── Tabs (output sections) ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 1.8rem;
    border-bottom: 2px solid var(--ink);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase;
    color: var(--ink-soft) !important;
    padding-bottom: 0.7rem !important;
}
.stTabs [aria-selected="true"] {
    color: var(--stamp-red) !important;
    border-bottom-color: var(--stamp-red) !important;
}

/* ── Report page ── */
.report-page {
    background: var(--paper-card);
    border: 1px solid var(--line);
    box-shadow: 6px 6px 0 rgba(34,29,20,0.07);
    padding: 2.4rem 2.6rem;
    margin-top: 1.3rem;
    position: relative;
    font-family: 'Lora', serif;
    line-height: 1.7;
}
.report-page::before {
    content: "";
    position: absolute;
    inset: 10px;
    border: 1px solid var(--line-soft);
    pointer-events: none;
}
.report-stamp {
    position: absolute;
    top: 1.6rem;
    right: 2.2rem;
    font-family: 'Special Elite', monospace;
    font-size: 0.95rem;
    letter-spacing: 0.1em;
    color: var(--stamp-red);
    border: 3px solid var(--stamp-red);
    padding: 0.3rem 0.8rem;
    transform: rotate(-6deg);
    opacity: 0.85;
    text-transform: uppercase;
}
.report-stamp.blue { color: var(--stamp-blue); border-color: var(--stamp-blue); }

/* ── Redacted loading placeholder ── */
.redacted-line {
    height: 0.95rem;
    background: var(--redact);
    margin: 0.5rem 0;
    opacity: 0.88;
}

/* ── Source log entries ── */
.log-entry {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: var(--ink-soft);
    border-left: 2px solid var(--line);
    padding: 0.2rem 0 0.2rem 0.8rem;
    margin-bottom: 0.3rem;
}

.footer-note {
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    color: var(--ink-soft);
    margin-top: 4rem;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)


# ── Render Folder Tab ────────────────────────────────────────────────────────
def render_tab(exhibit: str, title: str, state: str):
    label_map = {
        "waiting": ("STANDING BY", "st-wait"),
        "running": ("IN PROGRESS", "st-run"),
        "done":    ("FILED ✓", "st-ok"),
    }
    label, cls = label_map.get(state, ("STANDING BY", "st-wait"))
    tab_cls = {"running": "running", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="folder-tab {tab_cls}">
        <span class="exhibit-status {cls}">{label}</span>
        <div class="exhibit-id">EXHIBIT {exhibit}</div>
        <div class="exhibit-title">{title}</div>
    </div>
    """, unsafe_allow_html=True)


def render_redacted_block(lines=4):
    widths = [random.randint(45, 96) for _ in range(lines)]
    html = "".join(f'<div class="redacted-line" style="width:{w}%;"></div>' for w in widths)
    st.markdown(html, unsafe_allow_html=True)


# ── State Init ────────────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="dossier-header">
    <div class="dossier-title">
        🗂️ Nexus Research — Case File
        <small>MULTI-AGENT SYNTHESIS DIVISION</small>
    </div>
    <div class="dossier-meta">
        CASE NO. <b>{st.session_state.case_no}</b><br>
        OPENED <b>{st.session_state.opened_on}</b>
    </div>
</div>
<div class="dossier-subbar">
    <span>4 EXHIBITS</span>
    <span>SEARCH → EXTRACT → SYNTHESIZE → REVIEW</span>
    <span>STATUS: {"ACTIVE" if st.session_state.running else ("CLOSED" if st.session_state.done else "OPEN")}</span>
</div>
""", unsafe_allow_html=True)


# ── Split Workspace Layout ───────────────────────────────────────────────────
col_workspace, col_tabs = st.columns([2.5, 1.1], gap="large")

with col_workspace:
    st.markdown('<div class="intake-card">', unsafe_allow_html=True)
    st.markdown('<div class="intake-label">Subject of Inquiry</div>', unsafe_allow_html=True)
    c_in, c_btn = st.columns([3.5, 1.2], gap="small")
    with c_in:
        topic = st.text_input(
            "Target Subject",
            placeholder="e.g. Autonomous AI agent frameworks, 2026",
            key="topic_input",
            label_visibility="collapsed"
        )
    with c_btn:
        run_btn = st.button("Open Investigation", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="leads-row">
        <span class="leads-label">Prior Leads:</span>
        <span class="lead-chip">Multi-agent LLM systems</span>
        <span class="lead-chip">Generative AI in healthcare</span>
        <span class="lead-chip">Quantum hardware 2026</span>
    </div>
    """, unsafe_allow_html=True)

    res = st.session_state.results
    if res or st.session_state.running:
        tab1, tab2, tab3 = st.tabs(["Field Report", "Peer Review", "Source Log"])

        with tab1:
            if "writer" in res:
                st.markdown('<div class="report-page">', unsafe_allow_html=True)
                st.markdown('<div class="report-stamp">Filed</div>', unsafe_allow_html=True)
                st.markdown(res["writer"])
                st.markdown('</div>', unsafe_allow_html=True)

                st.download_button(
                    label="Export Report (.md)",
                    data=res["writer"],
                    file_name=f"case_{st.session_state.case_no}_report.md",
                    mime="text/markdown",
                )
            elif st.session_state.running:
                st.markdown('<div class="report-page">', unsafe_allow_html=True)
                render_redacted_block(6)
                st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            if "critic" in res:
                st.markdown('<div class="report-page">', unsafe_allow_html=True)
                st.markdown('<div class="report-stamp blue">Reviewed</div>', unsafe_allow_html=True)
                st.markdown(res["critic"])
                st.markdown('</div>', unsafe_allow_html=True)
            elif st.session_state.running:
                st.markdown('<div class="report-page">', unsafe_allow_html=True)
                render_redacted_block(4)
                st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            if "search" in res:
                st.markdown('<div class="log-entry">SEARCH NODE — output captured</div>', unsafe_allow_html=True)
                with st.expander("View raw search log", expanded=False):
                    st.code(res["search"], language="markdown")
            if "reader" in res:
                st.markdown('<div class="log-entry">EXTRACTOR NODE — output captured</div>', unsafe_allow_html=True)
                with st.expander("View raw extraction log", expanded=False):
                    st.code(res["reader"], language="markdown")
            if not res:
                st.markdown('<div class="log-entry">Awaiting first transmission…</div>', unsafe_allow_html=True)

with col_tabs:
    st.markdown('<div class="tabs-heading">Case Progress</div>', unsafe_allow_html=True)

    r = st.session_state.results

    def get_state(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    render_tab("A", "Web Intelligence Sweep", get_state("search"))
    render_tab("B", "Source Content Extraction", get_state("reader"))
    render_tab("C", "Synthesis & Drafting", get_state("writer"))
    render_tab("D", "Quality Review", get_state("critic"))


# ── Execution Loop ────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Enter a subject of inquiry before opening the case.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # Step 1
    with st.spinner("Exhibit A — sweeping open sources…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    # Step 2
    with st.spinner("Exhibit B — extracting source content…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # Step 3
    with st.spinner("Exhibit C — drafting the field report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    # Step 4
    with st.spinner("Exhibit D — quality review in progress…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-note">
    Nexus Research — Multi-Agent Case Management System
</div>
""", unsafe_allow_html=True)
