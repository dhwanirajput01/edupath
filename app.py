"""EduPath AI - AI-Based Personalized Learning Recommendation System (Semester V prototype).

Streamlit version. All recommendation scores are SIMULATED from sample data.
No machine-learning model is trained or integrated in this prototype.
"""
import pandas as pd
import streamlit as st

st.set_page_config(page_title="EduPath AI", page_icon="🎓", layout="wide")
ss = st.session_state

# ---------------------------------------------------------------- styling
st.markdown(
    """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@600;700&display=swap');
html, body, [class*="css"] {font-family:'Inter',system-ui,sans-serif;}
h1,h2,h3 {font-family:'Playfair Display',Georgia,serif !important; color:#3A2819; font-weight:600 !important;}
.stApp {background:#F2EBDD; color:#2B1F16;}
section[data-testid="stSidebar"] {background:#2E2118;}
section[data-testid="stSidebar"] * {color:#E9DDC8 !important;}
section[data-testid="stSidebar"] h1 {color:#fff !important;}
button[kind="primary"] {background:#6B4A2F !important; color:#fff !important; border:0 !important; border-radius:10px !important;}
button[kind="secondary"] {background:#FBF8F1 !important; color:#6B4A2F !important; border:1px solid #6B4A2F !important; border-radius:10px !important;}
button:disabled {opacity:.5 !important;}
div[data-testid="stVerticalBlockBorderWrapper"] {background:#FBF8F1; border-radius:16px; border-color:#E0D3BA !important;}
div[data-testid="stProgress"] div[role="progressbar"] > div {background:#69773A !important;}
.pill {display:inline-block; background:#E6D9BF; color:#3A2819; border-radius:99px; padding:2px 11px; margin:0 6px 6px 0; font-size:12px;}
.pill.ol {background:#69773A; color:#fff;}
.pill.warn {background:#B5532D; color:#fff;}
</style>""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- sample data
DOM = {
    "ds": ("Data Science", "Turn raw data into decisions"),
    "ai": ("Artificial Intelligence", "Build systems that learn and reason"),
    "cloud": ("Cloud Computing", "Deploy and scale modern infrastructure"),
    "web": ("Web Development", "Craft fast, accessible web applications"),
    "sec": ("Cybersecurity", "Protect systems, networks and data"),
}
INT = {
    "E": ("Explore", "Discover new topics"),
    "L": ("Learn", "Understand topics from basics"),
    "R": ("Revise", "Revisit previously studied topics"),
    "P": ("Practice", "Solve questions and strengthen skills"),
}
FMT = ["Video", "Reading", "Quiz"]
MINS = [15, 30, 45, 60, 90]
_RAW = [
    (1, "Python for Data Science Essentials", "Coursera", "ds", "Python & Pandas", "Beginner", 45, "Video", "EL", .88),
    (2, "Statistics for Data Analysis", "Udemy", "ds", "Statistics", "Intermediate", 30, "Reading", "LR", .74),
    (3, "Data Cleaning Practice Set", "Kaggle Learn", "ds", "Python & Pandas", "Intermediate", 20, "Quiz", "PR", .81),
    (4, "Machine Learning Foundations", "Coursera", "ai", "Machine Learning", "Beginner", 60, "Video", "EL", .92),
    (5, "Neural Networks from Scratch", "Udemy", "ai", "Deep Learning", "Advanced", 90, "Video", "LP", .69),
    (6, "ML Concepts Quick Quiz", "GeeksforGeeks", "ai", "Machine Learning", "Intermediate", 15, "Quiz", "RP", .77),
    (7, "Introduction to AI: Reading Guide", "NPTEL", "ai", "AI Foundations", "Beginner", 25, "Reading", "EL", .71),
    (8, "Cloud Practitioner Essentials", "Coursera", "cloud", "Cloud Basics", "Beginner", 50, "Video", "EL", .86),
    (9, "Docker & Kubernetes Hands-On", "Udemy", "cloud", "Containers", "Intermediate", 75, "Video", "LP", .73),
    (10, "Cloud Architecture Notes", "freeCodeCamp", "cloud", "Cloud Basics", "Intermediate", 20, "Reading", "RE", .66),
    (11, "Modern JavaScript & React", "Udemy", "web", "React", "Intermediate", 60, "Video", "LP", .90),
    (12, "HTML & CSS Foundations", "freeCodeCamp", "web", "HTML & CSS", "Beginner", 30, "Reading", "ELR", .80),
    (13, "Frontend Challenge Questions", "LeetCode", "web", "React", "Intermediate", 25, "Quiz", "P", .72),
    (14, "Cybersecurity Fundamentals", "Coursera", "sec", "Security Basics", "Beginner", 45, "Video", "EL", .84),
    (15, "Network Security Concepts", "NPTEL", "sec", "Networking", "Intermediate", 30, "Reading", "LR", .70),
    (16, "Capture-the-Flag Practice Pack", "TryHackMe", "sec", "Security Basics", "Intermediate", 40, "Quiz", "P", .76),
]
KEYS = ("id", "t", "pl", "dom", "tp", "df", "mn", "ty", "it", "cf")
RES = [dict(zip(KEYS, r)) for r in _RAW]
BASE = {"Python & Pandas": 55, "Statistics": 32, "Machine Learning": 48, "Deep Learning": 18,
        "AI Foundations": 62, "Cloud Basics": 40, "Containers": 22, "React": 50,
        "HTML & CSS": 70, "Security Basics": 45, "Networking": 30}
SEED = [
    (1, "Review pandas DataFrames", "ds", "Python & Pandas", "daily", True),
    (2, "Solve 10 statistics problems", "ds", "Statistics", "daily", False),
    (3, "Watch lecture: gradient descent", "ai", "Machine Learning", "daily", False),
    (4, "Read AI foundations notes", "ai", "AI Foundations", "weekly", False),
    (5, "Build a data-cleaning notebook", "ds", "Python & Pandas", "weekly", False),
    (6, "Complete a small neural network lab", "ai", "Deep Learning", "monthly", False),
]
PAGES = ["Dashboard", "Learner Profile", "Explore Domains", "Learning Intent", "Recommendations",
         "Study Planner", "Progress", "Feedback", "How It Works"]

# ---------------------------------------------------------------- state
ss.setdefault("page", "Dashboard")
ss.setdefault("P", {"name": "Student", "branch": "Computer Science", "sem": "5", "cgpa": "8.2",
                    "goal": "Get internship-ready", "fmt": "Video", "min": 30,
                    "interests": ["Machine Learning", "React"]})
ss.setdefault("doms", ["ds", "ai"])
ss.setdefault("intent", "L")
ss.setdefault("topic", "All")
ss.setdefault("view", "Daily")
ss.setdefault("sel", 1)
ss.setdefault("fb", {})
ss.setdefault("nid", 100)
ss.setdefault("plan", [dict(id=i, t=t, dom=d, tp=tp, per=p, done=x) for i, t, d, tp, p, x in SEED])


# ---------------------------------------------------------------- logic
def go(page):
    ss.page = page


def topics():
    return sorted({r["tp"] for r in RES if r["dom"] in ss.doms})


def pr(tp):
    done = sum(1 for t in ss.plan if t["tp"] == tp and t["done"])
    return min(100, BASE.get(tp, 30) + 12 * done)


def weak(tp):
    skipped = any(RES[i - 1]["tp"] == tp and f["status"] == "Skipped" and f["why"] == "Too difficult"
                  for i, f in ss.fb.items())
    return pr(tp) < 40 or skipped


def overall():
    tp = topics()
    return round(sum(pr(t) for t in tp) / len(tp)) if tp else 0


def rank():
    """SIMULATED hybrid scoring: 0.6 * content-based + 0.4 * collaborative (sample values)."""
    P, out = ss.P, []
    for r in RES:
        if r["dom"] not in ss.doms:
            continue
        m = [ss.intent in r["it"], r["ty"] == P["fmt"], ss.topic == "All" or r["tp"] == ss.topic]
        fit = r["mn"] <= P["min"]
        cb = min(.98, .9 * (.35 * m[0] + .25 * m[1] + .2 * m[2] + .2 * (1 if fit else .3)) + ((r["id"] * 7) % 10) / 100)
        out.append({**r, "cb": cb, "fit": fit, "m": m, "hy": .6 * cb + .4 * r["cf"]})
    return sorted(out, key=lambda x: -x["hy"])


def why(r):
    P = ss.P
    bits = [
        r["m"][0] and f"Supports your “{INT[ss.intent][0]}” intent",
        r["m"][1] and f"matches your preferred {P['fmt'].lower()} format",
        ss.topic != "All" and r["m"][2] and f"covers your chosen topic ({r['tp']})",
        f"fits your {P['min']}-minute window" if r["fit"] else
        f"runs longer than your {P['min']}-minute window, so split it across sessions",
        f"learners with similar interactions rated it {round(r['cf'] * 100)}% (simulated)",
    ]
    return "; ".join(b for b in bits if b) + "."


def toggle(i):
    for t in ss.plan:
        if t["id"] == i:
            t["done"] = not t["done"]


def add_plan(r):
    per = "daily" if r["mn"] <= 45 else "weekly"
    ss.nid += 1
    ss.plan.append(dict(id=ss.nid, t=r["t"], dom=r["dom"], tp=r["tp"], per=per, done=False, src=r["id"]))
    st.toast(f"Added to your {per} planner")


def start(rid):
    ss.sel = rid
    st.toast("Opening resource (simulated). Rate it when you finish.")
    go("Feedback")


def pick_domain(d):
    if d in ss.doms:
        ss.doms.remove(d)
    elif len(ss.doms) < 2:
        ss.doms.append(d)
    else:
        st.toast("Deselect a domain first. Exactly two are allowed.")
    ss.topic = "All"


def revise(tp):
    ss.intent, ss.topic = "R", tp
    go("Recommendations")


# ---------------------------------------------------------------- ui helpers
def head(title, sub):
    st.title(title)
    st.caption(sub)


def pills(*items):
    return "".join(f'<span class="pill">{i}</span>' for i in items)


def task_cb(t, pfx):
    st.checkbox(f"{t['t']}  ·  {t['tp']}", value=t["done"], key=f"{pfx}{t['id']}",
                on_change=toggle, args=(t["id"],))


def pref(pfx):
    P = ss.P
    P["fmt"] = st.radio("Preferred content format", FMT, index=FMT.index(P["fmt"]),
                        horizontal=True, key=pfx + "fmt")
    P["min"] = st.radio("Available time (minutes)", MINS, index=MINS.index(P["min"]),
                        horizontal=True, key=pfx + "min")


def simulated_banner():
    st.info("Prototype notice: scores are simulated from sample data. "
            "No machine-learning model has been trained or integrated.")


# ---------------------------------------------------------------- pages
def page_dashboard():
    P = ss.P
    head(f"Welcome back, {P['name']}", "Your personalised learning overview for today.")
    cols = st.columns(3)
    with cols[0].container(border=True):
        st.subheader("Overall progress")
        st.metric("Mastery across your two domains", f"{overall()}%")
        st.progress(overall())
    for col, d in zip(cols[1:], ss.doms):
        tp = [r["tp"] for r in RES if r["dom"] == d]
        v = round(sum(pr(x) for x in set(tp)) / len(set(tp)))
        with col.container(border=True):
            st.subheader(DOM[d][0])
            st.caption(DOM[d][1])
            st.progress(v)
            st.caption(f"{v}% complete")
    a, b = st.columns(2)
    with a.container(border=True):
        st.subheader("Today’s tasks")
        today = [t for t in ss.plan if t["per"] == "daily" and t["dom"] in ss.doms]
        for t in today:
            task_cb(t, "d_")
        if not today:
            st.write("No daily tasks yet. Add one from the planner.")
        st.button("Open study planner", on_click=go, args=("Study Planner",), key="d_pl")
    with b.container(border=True):
        st.subheader("Recommended activities")
        for r in rank()[:3]:
            st.markdown(f"**{r['t']}**  \n{r['pl']} · {r['ty']} · {r['mn']} min · "
                        f"score {round(r['hy'] * 100)} (simulated)")
        c1, c2 = st.columns(2)
        c1.button("View all recommendations", on_click=go, args=("Recommendations",),
                  type="primary", key="d_rec")
        c2.button("Start onboarding", on_click=go, args=("Learner Profile",), key="d_on")


def page_profile():
    P = ss.P
    head("Learner Profile Setup", "Tell EduPath AI about your background so recommendations fit you.")
    with st.container(border=True):
        a, b = st.columns(2)
        with a:
            P["name"] = st.text_input("Full name", P["name"], key="p_name")
            branches = ["Computer Science", "Information Technology", "Electronics", "Data Science"]
            P["branch"] = st.selectbox("Branch", branches, index=branches.index(P["branch"]), key="p_br")
            sems = ["3", "4", "5", "6", "7"]
            P["sem"] = st.radio("Semester", sems, index=sems.index(P["sem"]), horizontal=True, key="p_sem")
            P["cgpa"] = st.text_input("CGPA", P["cgpa"], key="p_cg")
        with b:
            goals = ["Get internship-ready", "Strengthen fundamentals", "Prepare for placements",
                     "Build projects", "Pursue higher studies"]
            P["goal"] = st.selectbox("Learning goal", goals, index=goals.index(P["goal"]), key="p_goal")
            pref("p_")
        allt = sorted({r["tp"] for r in RES})
        P["interests"] = st.multiselect("Learning interests", allt, default=P["interests"], key="p_int")
        if st.button("Save and choose domains", type="primary", key="p_save"):
            st.toast("Profile saved")
            go("Explore Domains")
            st.rerun()


def page_domains():
    head("Explore Domains", "Select exactly two learning domains to focus on.")
    cols = st.columns(5)
    for col, (k, (name, blurb)) in zip(cols, DOM.items()):
        on = k in ss.doms
        with col.container(border=True):
            st.subheader(name)
            st.caption(blurb)
            st.button("Selected ✓" if on else "Select", key=f"dm_{k}", on_click=pick_domain, args=(k,),
                      type="primary" if on else "secondary", use_container_width=True)
    st.write(f"**{len(ss.doms)}/2 selected**")
    st.button("Continue to learning intent", disabled=len(ss.doms) != 2, type="primary",
              on_click=go, args=("Learning Intent",), key="dm_next")


def set_intent(k):
    ss.intent = k


def page_intent():
    head("Learning Intent", "What would you like to do right now?")
    cols = st.columns(4)
    for col, (k, (name, blurb)) in zip(cols, INT.items()):
        on = ss.intent == k
        with col.container(border=True):
            st.subheader(name)
            st.caption(blurb)
            st.button("Selected ✓" if on else "Choose", key=f"in_{k}", on_click=set_intent, args=(k,),
                      type="primary" if on else "secondary", use_container_width=True)
    with st.container(border=True):
        pref("i_")
        st.button("Get recommendations", type="primary", on_click=go, args=("Recommendations",), key="in_go")


def page_recs():
    P = ss.P
    head("Personalised Recommendations", f"Intent: {INT[ss.intent][0]} · {P['fmt']} · {P['min']} min")
    simulated_banner()
    opts = ["All"] + topics()
    ss.topic = st.radio("Topic", opts, index=opts.index(ss.topic) if ss.topic in opts else 0,
                        horizontal=True, key="r_topic")
    for i, r in enumerate(rank()):
        with st.container(border=True):
            a, b = st.columns([5, 2])
            a.markdown(f"### #{i + 1}  {r['t']}")
            b.markdown(f'<span class="pill ol">Hybrid {round(r["hy"] * 100)} · simulated</span>',
                       unsafe_allow_html=True)
            st.markdown(pills(r["pl"], r["tp"], r["df"], f"{r['mn']} min", r["ty"]), unsafe_allow_html=True)
            st.caption(f"Content-based {round(r['cb'] * 100)} · Collaborative {round(r['cf'] * 100)} (simulated)")
            with st.expander("Why recommended?"):
                st.write(why(r))
            added = any(t.get("src") == r["id"] for t in ss.plan)
            c1, c2, _ = st.columns([1.3, 1, 3])
            c1.button("Added to plan" if added else "Add to Study Plan", key=f"add{r['id']}",
                      disabled=added, on_click=add_plan, args=(r,), type="primary")
            c2.button("Start Learning", key=f"st{r['id']}", on_click=start, args=(r["id"],))
    st.button("Go to study planner", on_click=go, args=("Study Planner",), key="r_pl")


def page_planner():
    head("Personalised Study Planner", "Plan and track tasks for each of your two domains.")
    views = ["Daily", "Weekly", "Monthly"]
    rk = {"daily": 0, "weekly": 1, "monthly": 2}
    ss.view = st.radio("View", views, index=views.index(ss.view), horizontal=True, key="pl_view")
    vis = [t for t in ss.plan if rk[t["per"]] <= rk[ss.view.lower()] and t["dom"] in ss.doms]
    pc = round(sum(t["done"] for t in vis) / len(vis) * 100) if vis else 0
    st.progress(pc)
    st.write(f"**{pc}% completed**")
    for col, d in zip(st.columns(2), ss.doms):
        with col.container(border=True):
            mine = [t for t in vis if t["dom"] == d]
            st.subheader(f"{DOM[d][0]}  ({sum(t['done'] for t in mine)}/{len(mine)} done)")
            for t in mine:
                task_cb(t, "p_")
            if not mine:
                st.caption("No tasks in this view.")
            with st.form(f"add_{d}", clear_on_submit=True):
                txt = st.text_input("Add a task", key=f"txt_{d}", placeholder="Add a task…")
                if st.form_submit_button("Add") and txt.strip():
                    ss.nid += 1
                    ss.plan.append(dict(id=ss.nid, t=txt.strip(), dom=d, tp="Custom",
                                        per=ss.view.lower(), done=False))
                    st.rerun()
    st.button("View progress", on_click=go, args=("Progress",), type="primary", key="pl_pg")


def page_progress():
    head("Progress Monitoring", "Topic-wise mastery, pending work and areas that need revision.")
    mine = [t for t in ss.plan if t["dom"] in ss.doms]
    done = [t for t in mine if t["done"]]
    pend = [t for t in mine if not t["done"]]
    a, b = st.columns(2)
    with a.container(border=True):
        st.subheader("Overall mastery")
        m1, m2, m3 = st.columns(3)
        m1.metric("Mastery", f"{overall()}%")
        m2.metric("Completed", len(done))
        m3.metric("Pending", len(pend))
        st.progress(overall())
    with b.container(border=True):
        st.subheader("Study minutes, last 7 days (sample)")
        data = [35, 50, 20, 60, 45, 30, len(done) * 15]
        st.bar_chart(pd.DataFrame({"Minutes": data}, index=[f"D{i}" for i in range(1, 7)] + ["Today"]),
                     color="#69773A", height=170)
    a, b = st.columns(2)
    with a.container(border=True):
        st.subheader("Topic-wise progress")
        for tp in topics():
            badge = ' <span class="pill warn">Weak</span>' if weak(tp) else ""
            st.markdown(f"**{tp}** — {pr(tp)}%{badge}", unsafe_allow_html=True)
            st.progress(pr(tp))
    with b.container(border=True):
        st.subheader("Weak topics to revise")
        wk = [t for t in topics() if weak(t)]
        for tp in wk:
            x, y = st.columns([3, 1])
            x.write(tp)
            y.button("Revise", key=f"rv_{tp}", on_click=revise, args=(tp,))
        if not wk:
            st.write("No weak topics. Well done.")
        st.subheader("Completed")
        for t in done:
            st.write(f"✓ {t['t']}")
        if not done:
            st.caption("Nothing completed yet.")
        st.subheader("Pending")
        for t in pend:
            st.write(f"• {t['t']}")


def page_feedback():
    head("Feedback and Profile Update",
         "Your feedback is stored in this session’s local state and sharpens future recommendations.")
    a, b = st.columns(2)
    with a.container(border=True):
        st.subheader("Rate a resource")
        ids = [r["id"] for r in RES]
        rid = st.selectbox("Resource", ids, index=ids.index(ss.sel), key="fb_sel",
                           format_func=lambda i: f"{RES[i - 1]['t']} ({RES[i - 1]['pl']})")
        ss.sel = rid
        rate = st.feedback("stars", key=f"fb_rate{rid}")
        use = st.radio("Was it useful?", ["Useful", "Not Useful"], index=None, horizontal=True, key=f"fb_use{rid}")
        status = st.radio("Completion status", ["Completed", "In progress", "Skipped"], horizontal=True,
                          key=f"fb_st{rid}")
        reason = ""
        if status == "Skipped":
            reason = st.selectbox("Reason for skipping",
                                  ["Too difficult", "Too long", "Not relevant", "Prefer another format"],
                                  key=f"fb_why{rid}")
        if st.button("Submit feedback", type="primary", key="fb_go"):
            if rate is None or use is None:
                st.warning("Please give a star rating and choose Useful or Not Useful.")
            else:
                ss.fb[rid] = dict(rate=rate + 1, use=use, status=status, why=reason)
                st.toast("Feedback recorded")
    with b.container(border=True):
        st.subheader("Update learner preferences")
        pref("f_")
        st.caption("Changes apply to recommendations immediately.")
        st.button("See updated recommendations", on_click=go, args=("Recommendations",), key="fb_rec")
        st.subheader("Recorded feedback")
        if ss.fb:
            st.dataframe(pd.DataFrame([
                {"Resource": RES[i - 1]["t"], "Rating": f"{f['rate']}★", "Useful?": f["use"],
                 "Status": f["status"], "Skip reason": f["why"]} for i, f in ss.fb.items()]),
                hide_index=True, use_container_width=True)
        else:
            st.caption("No feedback yet.")


def page_about():
    head("How It Works", "The recommendation methodology proposed for this project.")
    st.warning("Simulated prototype. This demo uses sample data and hand-assigned scores. No TF-IDF, "
               "similarity or collaborative model has been trained or run. The methods below describe "
               "the proposed design.")
    items = [
        ("Content-Based Filtering", "Resource titles and descriptions are converted to TF-IDF vectors. "
         "Cosine similarity compares them with the learner’s interest profile: cos(θ) = A·B / (‖A‖‖B‖)."),
        ("Collaborative Filtering", "Learners with similar interaction histories (ratings, completions) "
         "are identified, and resources they valued are suggested."),
        ("Hybrid Recommendation", "Both scores are combined, e.g. 0.6 × content + 0.4 × collaborative. "
         "The prototype applies this weighting to simulated values."),
    ]
    for col, (t, d) in zip(st.columns(3), items):
        with col.container(border=True):
            st.subheader(t)
            st.write(d)
    with st.container(border=True):
        st.subheader("Prototype pipeline")
        st.write("Profile and intent → domain filter → score (simulated) → rank → add to plan → "
                 "track progress → feedback → updated preferences.")
    with st.container(border=True):
        st.subheader("Simulated vs. actual")
        st.write("Simulated here: content and collaborative scores, rankings, progress baselines and weekly "
                 "activity. Real in this prototype: interface state, filtering by your selections, planner "
                 "updates, task completion and feedback recording.")


# ---------------------------------------------------------------- app shell
st.sidebar.title("EduPath AI")
st.sidebar.caption("PERSONALISED LEARNING")
st.sidebar.radio("Navigate", PAGES, key="page", label_visibility="collapsed")
st.sidebar.caption("Prototype · simulated scores")

{
    "Dashboard": page_dashboard, "Learner Profile": page_profile, "Explore Domains": page_domains,
    "Learning Intent": page_intent, "Recommendations": page_recs, "Study Planner": page_planner,
    "Progress": page_progress, "Feedback": page_feedback, "How It Works": page_about,
}[ss.page]()
