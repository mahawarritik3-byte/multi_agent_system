import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NexusResearch · Grown, not scraped",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS: Greenhouse / Growth Workspace ─────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:          #f4faf1;
    --card:        #ffffff;
    --ink:         #17261b;
    --ink-soft:    #5b6f60;
    --leaf:        #4fb95c;
    --leaf-dark:   #2f8f3c;
    --sky:         #4a9de0;
    --sun:         #ff8a5c;
    --line:        rgba(23, 38, 27, 0.08);
    --line-strong: rgba(23, 38, 27, 0.14);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--ink);
}

.stApp {
    background:
        radial-gradient(ellipse 900px 500px at 8% -5%, rgba(79, 185, 92, 0.16) 0%, transparent 60%),
        radial-gradient(ellipse 800px 500px at 95% 10%, rgba(74, 157, 224, 0.12) 0%, transparent 55%),
        radial-gradient(ellipse 700px 600px at 50% 110%, rgba(255, 138, 92, 0.09) 0%, transparent 55%),
        var(--bg);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.4rem 3.4rem 4rem; max-width: 1320px; }

/* ── Hero ── */
.hero-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.4rem;
}
.hero-title {
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 2.1rem;
    letter-spacing: -0.02em;
    color: var(--ink);
}
.hero-title span {
    background: linear-gradient(120deg, var(--leaf-dark), var(--sky));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 0.95rem;
    color: var(--ink-soft);
    margin-top: 0.35rem;
}
.hero-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    background: rgba(79, 185, 92, 0.12);
    color: var(--leaf-dark);
    border: 1px solid rgba(79, 185, 92, 0.3);
    padding: 0.35rem 0.8rem;
    border-radius: 20px;
    letter-spacing: 0.03em;
}

/* ── Input Card ── */
.plant-card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 1.6rem 1.8rem;
    margin: 1.8rem 0 1.2rem;
    box-shadow: 0 12px 32px -16px rgba(23, 38, 27, 0.18);
}
.plant-label {
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    font-size: 0.85rem;
    color: var(--ink);
    margin-bottom: 0.7rem;
}

.stTextInput > div > div > input {
    background: #f7faf5 !important;
    border: 1.5px solid var(--line-strong) !important;
    border-radius: 14px !important;
    color: var(--ink) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.2rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--leaf) !important;
    box-shadow: 0 0 0 4px rgba(79, 185, 92, 0.15) !important;
}

/* ── Action Button ── */
.stButton > button {
    background: linear-gradient(135deg, var(--leaf) 0%, var(--leaf-dark) 100%) !important;
    color: #ffffff !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    border-radius: 14px !important;
    padding: 0.85rem 1.6rem !important;
    border: none !important;
    box-shadow: 0 8px 20px -8px rgba(47, 143, 60, 0.55) !important;
    width: 100%;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 26px -8px rgba(47, 143, 60, 0.65) !important;
}

/* ── Seed chips ── */
.seed-row {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    flex-wrap: wrap;
    margin-top: 0.9rem;
}
.seed-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    color: var(--ink-soft);
    letter-spacing: 0.05em;
}
.seed-chip {
    font-family: 'Inter', sans-serif;
    font-size: 0.78rem;
    color: var(--ink-soft);
    background: #f0f6ec;
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
}

/* ── Growth Path (horizontal stepper) ── */
.growth-path {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin: 2.2rem 0 2rem;
    position: relative;
}
.growth-path::before {
    content: "";
    position: absolute;
    top: 21px;
    left: 5%;
    right: 5%;
    height: 2px;
    background: var(--line-strong);
    z-index: 0;
}
.growth-node {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    position: relative;
    z-index: 1;
    padding: 0 0.5rem;
}
.growth-icon {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    background: var(--card);
    border: 2px solid var(--line-strong);
    margin-bottom: 0.6rem;
    transition: all 0.25s ease;
}
.growth-node.running .growth-icon {
    border-color: var(--sky);
    box-shadow: 0 0 0 6px rgba(74, 157, 224, 0.14);
    animation: sway 1.4s ease-in-out infinite;
}
.growth-node.done .growth-icon {
    border-color: var(--leaf);
    background: rgba(79, 185, 92, 0.12);
}
@keyframes sway {
    0%, 100% { transform: rotate(-4deg); }
    50% { transform: rotate(4deg); }
}
.growth-stage {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--ink-soft);
}
.growth-title {
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    font-size: 0.82rem;
    color: var(--ink);
    margin-top: 0.15rem;
}
.growth-node.waiting .growth-title,
.growth-node.waiting .growth-stage { color: rgba(23,38,27,0.35); }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 1.6rem;
    border-bottom: 1px solid var(--line-strong);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Sora', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    color: var(--ink-soft) !important;
    padding-bottom: 0.8rem !important;
}
.stTabs [aria-selected="true"] {
    color: var(--leaf-dark) !important;
    border-bottom-color: var(--leaf) !important;
}

/* ── Bloom (deliverable) card ── */
.bloom-card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 2.2rem 2.4rem;
    margin-top: 1.2rem;
    box-shadow: 0 16px 40px -20px rgba(23, 38, 27, 0.2);
}
.bloom-tag {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.06em;
    color: var(--leaf-dark);
    background: rgba(79, 185, 92, 0.12);
    border-radius: 20px;
    padding: 0.25rem 0.7rem;
    margin-bottom: 1rem;
}
.bloom-tag.blue { color: var(--sky); background: rgba(74, 157, 224, 0.12); }

/* ── Skeleton growing bars (loading) ── */
.grow-bar {
    height: 0.85rem;
    border-radius: 6px;
    background: linear-gradient(90deg, #eef4ea 25%, #e2eedd 37%, #eef4ea 63%);
    background-size: 400% 100%;
    animation: shimmer 1.4s ease infinite;
    margin: 0.55rem 0;
}
@keyframes shimmer {
    0% { background-position: 100% 50%; }
    100% { background-position: 0 50%; }
}

.footer-note {
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: var(--ink-soft);
    margin-top: 4rem;
}
</style>
""", unsafe_allow_html=True)


# ── Growth stage config ───────────────────────────────────────────────────────
STAGES = [
    ("search",  "🔍", "SEED",   "Web Sweep"),
    ("reader",  "🌱", "SPROUT", "Extraction"),
    ("writer",  "🌿", "BUD",    "Synthesis"),
    ("critic",  "🌸", "BLOOM",  "Review"),
]


def render_growth_path(results: dict, running: bool):
    def get_state(step):
        if not results:
            return "waiting"
        if step in results:
            return "done"
        if running:
            keys = [s[0] for s in STAGES]
            for k in keys:
                if k not in results:
                    return "running" if k == step else "waiting"
        return "waiting"

    nodes_html = ""
    for key, icon, stage, title in STAGES:
        state = get_state(key)
        nodes_html += f"""
        <div class="growth-node {state}">
            <div class="growth-icon">{icon}</div>
            <div class="growth-stage">{stage}</div>
            <div class="growth-title">{title}</div>
        </div>
        """
    st.markdown(f'<div class="growth-path">{nodes_html}</div>', unsafe_allow_html=True)


def render_grow_bars(n=4):
    widths = [92, 78, 85, 60][:n] if n <= 4 else [80] * n
    html = "".join(f'<div class="grow-bar" style="width:{w}%;"></div>' for w in widths)
    st.markdown(html, unsafe_allow_html=True)


# ── State Init ────────────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-row">
    <div>
        <div class="hero-title">🌱 Nexus<span>Research</span></div>
        <div class="hero-sub">Plant a topic. Four agents tend it into a finished report.</div>
    </div>
    <div class="hero-pill">GREENHOUSE MODE</div>
</div>
""", unsafe_allow_html=True)


# ── Intake Card ───────────────────────────────────────────────────────────────
st.markdown('<div class="plant-card">', unsafe_allow_html=True)
st.markdown('<div class="plant-label">What should we grow today?</div>', unsafe_allow_html=True)
c_in, c_btn = st.columns([3.5, 1.2], gap="small")
with c_in:
    topic = st.text_input(
        "Target Subject",
        placeholder="e.g. Autonomous AI agent frameworks in 2026",
        key="topic_input",
        label_visibility="collapsed"
    )
with c_btn:
    run_btn = st.button("Plant & Grow 🌿", use_container_width=True)

st.markdown("""
<div class="seed-row">
    <span class="seed-label">QUICK SEEDS:</span>
    <span class="seed-chip">Multi-agent LLM systems</span>
    <span class="seed-chip">Generative AI in healthcare</span>
    <span class="seed-chip">Quantum hardware 2026</span>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# ── Growth Path ───────────────────────────────────────────────────────────────
render_growth_path(st.session_state.results, st.session_state.running)


# ── Output Space ──────────────────────────────────────────────────────────────
res = st.session_state.results
if res or st.session_state.running:
    tab1, tab2, tab3 = st.tabs(["🌸 Report", "🔎 Review", "🌾 Growth Log"])

    with tab1:
        if "writer" in res:
            st.markdown('<div class="bloom-card">', unsafe_allow_html=True)
            st.markdown('<span class="bloom-tag">FULLY GROWN</span>', unsafe_allow_html=True)
            st.markdown(res["writer"])
            st.markdown('</div>', unsafe_allow_html=True)

            st.download_button(
                label="Export Report (.md)",
                data=res["writer"],
                file_name=f"nexus_research_{int(time.time())}.md",
                mime="text/markdown",
            )
        elif st.session_state.running:
            st.markdown('<div class="bloom-card">', unsafe_allow_html=True)
            st.markdown('<span class="bloom-tag">STILL GROWING…</span>', unsafe_allow_html=True)
            render_grow_bars(4)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        if "critic" in res:
            st.markdown('<div class="bloom-card">', unsafe_allow_html=True)
            st.markdown('<span class="bloom-tag blue">PEER REVIEWED</span>', unsafe_allow_html=True)
            st.markdown(res["critic"])
            st.markdown('</div>', unsafe_allow_html=True)
        elif st.session_state.running:
            st.markdown('<div class="bloom-card">', unsafe_allow_html=True)
            render_grow_bars(3)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        if "search" in res:
            with st.expander("🔍 Web Sweep output", expanded=False):
                st.code(res["search"], language="markdown")
        if "reader" in res:
            with st.expander("🌱 Extraction output", expanded=False):
                st.code(res["reader"], language="markdown")


# ── Execution Loop ────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Plant a topic first — the field's still empty.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # Step 1
    with st.spinner("Seed — sweeping the web for sources…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    # Step 2
    with st.spinner("Sprout — extracting the deepest source…"):
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
    with st.spinner("Bud — drafting the report…"):
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
    with st.spinner("Bloom — final review…"):
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
    NexusResearch · Multi-Agent Research, Grown Not Scraped
</div>
""", unsafe_allow_html=True)
