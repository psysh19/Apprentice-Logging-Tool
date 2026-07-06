"""
Views for the Apprenticeship Activity Log.

The KSB list is defined here as plain data so the templates stay simple.
Each entry is (code, short_label, full_description). The full description is
shown as a tooltip on hover so the form does not get overwhelming.
"""

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect, render

# Grouped so the form can render three tidy sections.
KSB_GROUPS = [
    (
        "Knowledge",
        [
            ("K1", "DS in context of CS, stats & software engineering",
             "The context of Data Science and the Data Science community in relation to computer science, statistics and software engineering. How differing schools of thought in these disciplines have driven new approaches to data systems."),
            ("K2", "Governance, security, ethics & GDPR",
             "How Data Science operates within data governance, data security and communications; how it improves an organisation's processes; how data and analysis may exhibit bias; how ethics, compliance and international regulations (including GDPR) affect Data Science work."),
            ("K3.1", "Data processing & storage (on-premise/cloud)",
             "Key platforms for data and analysis: data processing and storage, including on-premise and cloud technologies."),
            ("K3.2", "Database systems (relational, warehousing, NoSQL, real-time)",
             "Database systems including relational, data warehousing & OLAP, NoSQL and real-time approaches; the pros and cons of each."),
            ("K3.3", "Data-driven decision making",
             "Data-driven decision making and the good use of evidence and analytics in making choices and decisions."),
            ("K4.1", "Statistical & mathematical models",
             "Designing, implementing and optimising analytical algorithms using statistical and mathematical models and methods."),
            ("K4.2", "Predictive analytics, ML, AI, optimisation, automation",
             "Advanced and predictive analytics, machine learning and AI techniques, simulations, optimisation and automation."),
            ("K4.3", "Computer vision & NLP",
             "Applications such as computer vision and Natural Language Processing."),
            ("K4.4", "Resource constraints & trade-offs",
             "Awareness of computing and organisational resource constraints and trade-offs in selecting models, algorithms and tools."),
            ("K4.5", "Dev standards: programming, testing, source control",
             "Development standards, including programming practice, testing and source control."),
            ("K5.1", "Sources of data",
             "Sources of data including files, operational systems, databases, web services, open data, government data, news and social media."),
            ("K5.2", "Data formats, structures & delivery (incl. unstructured)",
             "Data formats, structures and delivery methods, including unstructured data."),
            ("K5.3", "Common patterns in real-world data",
             "Common patterns in real-world data."),
        ],
    ),
    (
        "Skills",
        [
            ("S1", "Reformulate problems & apply scientific method",
             "Identify and clarify organisational problems and reformulate them into Data Science problems. Devise solutions, seek stakeholder feedback, apply scientific methods (experiment design, measurement, hypothesis testing) and gather requirements collaboratively."),
            ("S2", "Data engineering & governance",
             "Perform data engineering: source, access, explore, profile, pipeline, combine, transform and store data, and apply governance (quality control, security, privacy)."),
            ("S3", "Programming, reproducible & version-controlled code",
             "Use appropriate programming languages and tools for data manipulation, analysis, visualisation and integration. Develop reproducible analysis and robust code to software development standards, including version control."),
            ("S4", "Modelling & statistical validation",
             "Use analysis and models to improve outcomes: statistical analysis, correlation vs causation, feature selection and engineering, machine learning, optimisation and simulation, validated with statistical testing."),
            ("S5", "Implement solutions; cloud vs on-premise; ROI; scaling",
             "Implement data solutions using relevant architectures and design patterns; evaluate cloud vs on-premise; determine the value of data; assess value for money and ROI; scale systems; evaluate emerging trends."),
            ("S6", "Communicate, visualise & make recommendations",
             "Find, present and communicate outputs with high impact through storytelling tailored to the audience; visualise data to tell actionable narratives; make recommendations to decision makers."),
            ("S7", "Build collaborative relationships",
             "Develop and maintain collaborative relationships at strategic and operational levels using organisational empathy, active listening and trust development."),
            ("S8", "Project delivery & management",
             "Use project delivery techniques and tools appropriate to the project and organisation. Plan, organise and manage resources to run a small Data Science project and enable effective change."),
        ],
    ),
    (
        "Behaviours",
        [
            ("B1", "Inquisitive approach",
             "Curiosity to explore new questions, opportunities, data and techniques; tenacity to improve methods; relentless creativity in approach to solutions."),
            ("B2", "Empathy, ethics & diversity",
             "Empathy and positive engagement to enable working in multidisciplinary teams, championing ethics and diversity in data work."),
            ("B3", "Adaptability & pragmatism",
             "Adaptability and dynamism when responding to varied tasks and timescales, and pragmatism in real-world scenarios."),
            ("B4", "Problems in context of organisation goals",
             "Consideration of problems in the context of organisation goals."),
            ("B5", "Impartial, hypothesis-driven, honest",
             "An impartial, scientific, hypothesis-driven approach, rigorous analysis methods, and integrity in presenting data and conclusions truthfully."),
            ("B6", "Keeping up to date & community",
             "A commitment to keeping up to date with current thinking and maintaining personal development, including collaborating with the data science community."),
        ],
    ),
]


def activity(request, page):
    total = settings.ACTIVITY_PAGES
    if page < 1 or page > total:
        raise Http404("No such activity page.")

    context = {
        "ksb_groups": KSB_GROUPS,
        "page": page,
        "total": total,
        "page_range": range(1, total + 1),
        "is_first": page == 1,
        "prev_page": page - 1 if page > 1 else None,
        "next_page": page + 1 if page < total else None,
    }
    return render(request, "logbook/activity.html", context)


def home(request):
    return redirect("activity", page=1)
