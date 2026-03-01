# ABC Corp Presentation — Detailed Review & Winning Strategy Guide

## PART 1: WHAT YOUR PRESENTATION COVERS WELL ✅

Your current presentation demonstrates solid understanding of the problem space. Here is what you got right:

1. **Business challenges** — You correctly identified all 5 key pain points from the brief
2. **Data sources** — You covered all 5 required sources: Clickstream, Social Media, POS, GPS/Telemetry, Inventory
3. **Customer journey funnel** — Good visualisation of the booking flow
4. **BI Dashboard** — You built an actual Power BI dashboard which demonstrates practical ability
5. **GenAI integration** — Mentioned the right use cases (chatbot, NL queries, sentiment analysis)
6. **4-phase delivery** — Correct agile approach
7. **KPIs across 4 dimensions** — Financial, Operational, Customer, Digital

---

## PART 2: CRITICAL GAPS — WHAT THE PROBLEM STATEMENT ASKED FOR THAT IS MISSING ❌

### Gap 1: Tiger's Assessment of the AWS Architecture (MAJOR GAP)
The problem statement explicitly says: *"Tiger's assessment on the client proposed architecture and its fitment to purpose"*

**What you need to add:**
The client proposed: AWS Kinesis → S3 → Snowflake → MS Power BI + SageMaker

Your assessment should include:

| Component | Client Choice | Tiger's Assessment | Recommendation |
|-----------|--------------|-------------------|----------------|
| Streaming Ingestion | Kinesis Data Streams + Firehose | ✅ Excellent fit for GPS/Clickstream real-time data | Keep — industry standard for IoT & streaming |
| API Gateway | Amazon API Gateway | ✅ Good for Social Media API ingestion | Keep — scalable and managed |
| ETL | AWS Glue + DB2/Informatica | ⚠️ Hybrid risk | Recommend: AWS Glue primary, retire DB2 legacy tool |
| Storage | S3 + Snowflake | ✅ Gold standard combination | Keep — S3 for raw lake, Snowflake for warehouse |
| ML | SageMaker | ✅ Strong choice | Keep — native AWS integration |
| BI Layer | MS Power BI | ⚠️ Needs evaluation | See Tool Selection section below |
| Orchestration | Airflow (shown) | ✅ Good for complex pipelines | Keep — open source, AWS MWAA available |
| Governance | Data Quality shown as item | ⚠️ Underspecified | Add: AWS Glue Data Catalog + Great Expectations |

**Key architectural gap to highlight:** The proposed architecture lacks a clear **Data Mesh / Domain ownership model** and has no specified **PII masking / data privacy layer** — critical for customer data (DPDP Act compliance in India).

---

### Gap 2: BI Tool Selection Approach with Pros & Cons (MAJOR GAP)
The problem asked for: *"An approach on how we would go about tool selection listing out the Pros and cons"*

**Add this table:**

| Criteria | Power BI | Tableau | Looker | AWS QuickSight |
|----------|----------|---------|--------|----------------|
| Cost | ₹700/user/mo | ₹2,800/user/mo | Custom (expensive) | ₹200/user/mo |
| Snowflake Integration | Good (native connector) | Excellent | Native (Google) | Native AWS |
| Real-time Data | Limited | Good | Good | Good |
| Mobile Experience | Good | Excellent | Average | Average |
| India Support | Strong | Good | Limited | Good |
| Learning Curve | Low | Medium | High | Low |
| Self-service | High | High | Medium | Medium |
| Embed in Apps | Limited | Good | Excellent | Good |
| **Recommendation** | **Shortlist** | **Shortlist** | Skip for now | Backup option |

**Tool Selection Process (add this as a slide):**
1. Build pilot dashboards in Power BI and Tableau using actual dummy data (2 weeks)
2. Conduct user testing with Operations team, Management, and Analysts (1 week)
3. Score each tool against 10 criteria with weighted scoring matrix
4. Compare total cost of ownership over 3 years
5. Final recommendation to client with documented justification

---

### Gap 3: Detailed KPIs with Baseline and Targets (MODERATE GAP)
Your KPIs are listed but have no baselines or targets. Add these:

| KPI | Current Baseline | Target (12 months) | Data Source |
|-----|-----------------|-------------------|-------------|
| Fleet Utilization % | 57.3% (from data) | 72% | Telemetry + Inventory |
| Booking Conversion Rate | 36.7% (from data) | 45% | Clickstream |
| Avg Customer Rating | 3.78★ (from data) | 4.5★ | POS Bookings |
| Maintenance Incidents | Reactive (0 predictive) | 80% predicted | Telemetry |
| Report Generation Time | 2-3 days (manual) | Real-time | Platform |
| Revenue per Vehicle/Month | ₹13,400 (from data) | ₹16,000 | POS + Inventory |
| Social Campaign CPConv | ₹380 (from data) | ₹280 | Social Media |

---

### Gap 4: How KPIs Are Measured Periodically (MODERATE GAP)
Add a measurement cadence table:

| Frequency | What Gets Measured | Who Reviews |
|-----------|-------------------|-------------|
| Real-time | Fleet status, active bookings, GPS alerts | Operations Team |
| Daily | Conversion rate, revenue, maintenance alerts | Operations + Management |
| Weekly | Campaign performance, driver behaviour, KPI trends | Marketing + Fleet Mgr |
| Monthly | Full KPI scorecard, forecast vs actuals | Senior Leadership |
| Quarterly | Strategic KPIs, model performance, ROI review | Executive Committee |

---

### Gap 5: Incremental Release Plan is Too Vague (MINOR GAP)
Add specific sprint/timeline details:

| Phase | Duration | Key Deliverables | Success Gate |
|-------|----------|-----------------|--------------|
| Phase 0: Discovery | Weeks 1-2 | Data assessment, stakeholder interviews, current state mapping | Sign-off on architecture |
| Phase 1: Foundation | Weeks 3-8 | AWS setup, data ingestion pipelines, basic POS dashboard | Live data flowing to Snowflake |
| Phase 2: Customer Intel | Weeks 9-14 | Clickstream analytics, social media dashboard, conversion funnel | Conversion rate visibility live |
| Phase 3: Fleet Intelligence | Weeks 15-20 | GPS tracking, maintenance alerts, inventory dashboard | Predictive maintenance alerts firing |
| Phase 4: AI/Intelligent | Weeks 21-26 | GenAI Smart Hub, dynamic pricing, demand forecasting | NL queries functional for managers |
| Phase 5: Optimize | Ongoing | Model tuning, new use cases, adoption monitoring | KPI targets achieved |

---

## PART 3: DIFFERENTIATORS — WHAT WILL SEPARATE YOU FROM OTHER CANDIDATES 🏆

### Differentiator 1: Show Live Working Software (THE BIGGEST WIN)
**This is what this Streamlit app is for.**
Most candidates will present static PowerPoints. You walk in with a LIVE, WORKING dashboard showing:
- Real analysis from the actual dummy data
- Predictive ML models
- GenAI simulation with natural language queries
- Professional UI

Say this in the interview: *"Rather than just describing what we would build, we took the initiative to actually build a prototype using the provided data. Let me show you what the end product would look like."*

---

### Differentiator 2: India-Specific Context
Add a slide on India-specific nuances:
- **DPDP Act 2023** compliance — personal data protection requirements for customer GPS and booking data
- **GST compliance** — rental invoices, e-way bills need to be in the data model
- **UPI payment data** integration opportunity (Razorpay, PayU) for payment analytics
- **Bharat-tier cities** — growth opportunity in Tier 2/3 cities (Indore, Coimbatore, Nagpur)
- **Festival demand patterns** — Diwali, Navratri, IPL season demand spikes (your data confirms this)
- **WhatsApp Business API** — many Indian customers prefer WhatsApp over formal apps; add as a booking/notification channel

---

### Differentiator 3: Quantified Business Impact
Instead of saying "improve conversion," say:
*"Based on the dummy data analysis, fixing the payment step drop-off (47% abandonment) could recover ₹8-12L/quarter at current traffic levels."*

Calculate these from your actual data and show them.

---

### Differentiator 4: The "Tiger Assessment" Angle
Position yourselves as critical thinkers, not just yes-people. Call out one genuine risk in the client's architecture:

*"While the AWS architecture is well-designed, we noticed there is no explicit Data Privacy layer. Given the DPDP Act 2023, customer GPS data and booking history are classified personal data. We recommend adding AWS Macie for PII detection and column-level encryption in Snowflake before any personal data flows into the analytics layer."*

This shows maturity and builds trust.

---

### Differentiator 5: Visio / Architecture Flowchart
The problem statement asks for architecture assessment. Create a clear end-to-end flow:

**End-to-End Data Journey:**
```
[Source Systems]
 ├── POS Booking System ──────────────────────────────┐
 ├── Website / App (Clickstream) ────── Kinesis Stream─┤
 ├── GPS / IoT Sensors ──────────────── Kinesis Stream─┤──► S3 Raw Zone (Data Lake)
 ├── Social Media APIs ─── API Gateway ──────────────┤       │
 └── Inventory / ERP ────── AWS DMS ─────────────────┘       │
                                                              ▼
                                                    AWS Glue (ETL)
                                                    + Data Quality Checks
                                                              │
                                                              ▼
                                                    S3 Curated Zone
                                                              │
                                                              ▼
                                              Snowflake Data Warehouse
                                              ├── Feature Store (SageMaker)
                                              └── Semantic Layer
                                                              │
                                            ┌─────────────────┼─────────────────┐
                                            ▼                 ▼                 ▼
                                       Power BI          SageMaker ML      GenAI Hub
                                      Dashboards          Models            (LLM API)
                                            │                 │                 │
                                            └─────────────────┴─────────────────┘
                                                              │
                                                      Business Users
                                           (Operations / Management / Analysts)
```

---

## PART 4: PRESENTATION DELIVERY TIPS FOR THE 15-MINUTE SLOT

**Minutes 0-2:** Open with business impact, not tech. Start with:
*"ABC Corp is losing approximately ₹X lakhs monthly due to idle fleet, reactive maintenance, and abandoned bookings. In 15 minutes, I'll show you exactly how we solve each of these, and I'll show you a working prototype."*

**Minutes 2-5:** Business Context, Problem Statement, Proposed Strategy Roadmap

**Minutes 5-8:** Technical Architecture (AWS assessment, tool selection approach)

**Minutes 8-11:** LIVE DEMO of the Streamlit app (this is your biggest differentiator)

**Minutes 11-13:** GenAI integration, ML models, KPIs

**Minutes 13-15:** Why us — summarise with current state vs future state table

**For Q&A (15 mins):** Likely questions and how to answer them:
- "Why Snowflake over Redshift?" → Snowflake's separation of compute and storage = cost efficient for variable workloads. Better multi-cloud support if ABC Corp expands beyond AWS.
- "How long would Phase 1 take?" → 6-8 weeks for initial data pipelines + basic dashboard, with a working MVP visible after Week 4.
- "What if data quality is poor?" → We include data quality gates in the AWS Glue pipeline using Great Expectations or AWS Glue Data Quality. No data moves to the warehouse without passing quality checks.
- "How do you ensure GDPR/DPDP compliance?" → We implement column-level encryption, PII tagging via AWS Macie, role-based access control in Snowflake, and maintain a data lineage audit trail.

---

## PART 5: QUICK WINS TO ADD IN THE NEXT 24 HOURS

1. **Add the AWS Architecture Assessment slide** — show the table from Part 2, Gap 1
2. **Add the BI Tool Selection table** — show Power BI vs Tableau with recommendation
3. **Add KPI baselines and targets** — quantify everything with numbers from the data
4. **Add India-specific context** — DPDP Act, UPI, WhatsApp, festival seasonality
5. **Practice the Streamlit demo** — know every page cold, have backup screenshots
6. **Prepare 3 quantified business impact statements** — ₹ numbers make you memorable

---

*Good luck with your interview — the combination of a thorough presentation AND a live working prototype should make you stand out significantly from other candidates.*
