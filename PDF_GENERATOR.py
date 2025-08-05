import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import pandas as pd

# Create directory for PDFs
os.makedirs('knowledge_base_samples', exist_ok=True)

def create_calpers_risk_report():
    """Create CalPERS Q4 2023 Risk Assessment Report"""
    doc = SimpleDocTemplate("knowledge_base_samples/CalPERS_Risk_Assessment_Q4_2023.pdf", pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    story.append(Paragraph("CalPERS Risk Assessment Report", title_style))
    story.append(Paragraph("Q4 2023 - Confidential", styles['Heading2']))
    story.append(Spacer(1, 0.5*inch))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", styles['Heading2']))
    summary_text = """
    The California Public Employees' Retirement System (CalPERS) portfolio demonstrates strong risk-adjusted 
    performance with a current funded ratio of 83%. Key risk metrics remain within acceptable ranges, though 
    attention is required on private equity concentration and emerging market exposure. The portfolio's 
    Value-at-Risk (VaR) stands at $18.2 billion (95% confidence, 1-month horizon), representing 4.04% of 
    total assets under management.
    """
    story.append(Paragraph(summary_text, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Risk Metrics Table
    story.append(Paragraph("Key Risk Metrics", styles['Heading2']))
    
    risk_data = [
        ['Risk Metric', 'Current Value', 'Target Range', 'Status'],
        ['Portfolio VaR (95%, 1-month)', '$18.2B (4.04%)', '< 5%', '✓ Within Range'],
        ['Tracking Error', '3.8%', '3-5%', '✓ Optimal'],
        ['Sharpe Ratio', '1.15', '> 1.0', '✓ Good'],
        ['Maximum Drawdown (3Y)', '-12.4%', '< -15%', '✓ Acceptable'],
        ['Liquidity Coverage Ratio', '142%', '> 120%', '✓ Strong'],
        ['Private Assets Allocation', '35%', '30-40%', '✓ On Target'],
        ['Currency Risk Exposure', '18.5%', '< 20%', '⚠ Monitor'],
        ['Concentration Risk (Top 10)', '8.2%', '< 10%', '✓ Diversified']
    ]
    
    table = Table(risk_data, colWidths=[2.5*inch, 1.5*inch, 1.2*inch, 1.2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    story.append(Spacer(1, 0.3*inch))
    
    # Stress Test Results
    story.append(Paragraph("Stress Test Scenarios", styles['Heading2']))
    
    stress_text = """
    Recent stress testing indicates the portfolio would experience the following impacts under adverse scenarios:
    • Global Equity Market Crash (-30%): Portfolio impact of -15.6%, funded ratio drops to 70%
    • Interest Rate Spike (+300bps): Portfolio impact of -8.2%, primarily affecting fixed income
    • Geopolitical Crisis Scenario: Portfolio impact of -11.3%, with emerging markets most affected
    • Climate Transition Risk: Long-term impact estimated at -5.7% without adaptation measures
    """
    story.append(Paragraph(stress_text, styles['Normal']))
    
    # Recommendations
    story.append(PageBreak())
    story.append(Paragraph("Risk Mitigation Recommendations", styles['Heading2']))
    
    recommendations = """
    1. REDUCE EMERGING MARKET EXPOSURE: Current allocation of 12% in emerging market equities shows 
    elevated volatility. Recommend reducing to 8-10% range and reallocating to developed markets.
    
    2. ENHANCE LIQUIDITY BUFFER: While current liquidity is adequate, increasing the buffer to 150% 
    would provide additional flexibility during market stress events.
    
    3. IMPLEMENT CURRENCY HEDGING: With 18.5% unhedged currency exposure, implement a 50% hedge ratio 
    on major currency positions (EUR, JPY, GBP) to reduce volatility.
    
    4. REVIEW PRIVATE EQUITY VINTAGE EXPOSURE: 2021-2022 vintages show concerning valuations. 
    Consider slowing deployment pace and focusing on co-investment opportunities.
    
    5. CLIMATE RISK INTEGRATION: Accelerate the integration of climate risk metrics into the 
    investment process, particularly for real estate and infrastructure holdings.
    """
    story.append(Paragraph(recommendations, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print("✓ Created: CalPERS_Risk_Assessment_Q4_2023.pdf")

def create_harvard_performance_report():
    """Create Harvard Management Company Performance Report"""
    doc = SimpleDocTemplate("knowledge_base_samples/Harvard_Performance_Report_2023.pdf", pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#8B0000'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    story.append(Paragraph("Harvard Management Company", title_style))
    story.append(Paragraph("Annual Performance Report - Fiscal Year 2023", styles['Heading2']))
    story.append(Spacer(1, 0.5*inch))
    
    # Performance Summary
    story.append(Paragraph("Performance Summary", styles['Heading2']))
    
    perf_data = [
        ['Period', 'HMC Return', 'Policy Benchmark', 'Value Added', 'AUM ($B)'],
        ['FY 2023', '2.9%', '4.1%', '-1.2%', '$53.2'],
        ['3-Year Annualized', '9.6%', '8.8%', '+0.8%', '-'],
        ['5-Year Annualized', '8.5%', '7.9%', '+0.6%', '-'],
        ['10-Year Annualized', '9.3%', '8.7%', '+0.6%', '-']
    ]
    
    table = Table(perf_data, colWidths=[1.8*inch, 1.2*inch, 1.5*inch, 1.2*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B0000')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    story.append(Spacer(1, 0.3*inch))
    
    # Asset Allocation Performance
    story.append(Paragraph("Asset Class Performance Attribution", styles['Heading2']))
    
    attrib_data = [
        ['Asset Class', 'Weight', 'Return', 'Benchmark', 'Contribution'],
        ['Public Equity', '31%', '-2.1%', '-0.8%', '-0.65%'],
        ['Private Equity', '23%', '12.4%', '15.2%', '2.85%'],
        ['Hedge Funds', '25%', '6.8%', '7.2%', '1.70%'],
        ['Real Estate', '8%', '3.2%', '4.5%', '0.26%'],
        ['Natural Resources', '3%', '-8.4%', '-6.1%', '-0.25%'],
        ['Fixed Income', '10%', '1.2%', '1.8%', '0.12%'],
        ['Total', '100%', '2.9%', '4.1%', '2.9%']
    ]
    
    table2 = Table(attrib_data)
    table2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B0000')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.grey),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table2)
    story.append(Spacer(1, 0.3*inch))
    
    # Investment Highlights
    story.append(Paragraph("Key Investment Actions - FY2023", styles['Heading2']))
    
    highlights = """
    • PRIVATE EQUITY: Committed $2.8B to 15 new funds focusing on technology and healthcare sectors. 
    Notable investments include participation in Vista Equity Partners Fund VIII and Thoma Bravo XV.
    
    • HEDGE FUND RESTRUCTURING: Reduced number of hedge fund managers from 45 to 32, concentrating 
    capital with top-performing strategies. Increased allocation to multi-strategy platforms.
    
    • REAL ASSETS: Acquired three life science properties in Cambridge totaling $450M. Expanded 
    renewable energy portfolio with $200M commitment to offshore wind projects.
    
    • PUBLIC EQUITY TRANSITION: Shifted $1.2B from active to passive strategies in developed markets, 
    reducing fees by approximately $8M annually while maintaining similar risk exposures.
    
    • ESG INTEGRATION: Achieved net-zero commitment for entire endowment by 2050. Increased 
    sustainable investments to $4.5B (8.5% of portfolio).
    """
    story.append(Paragraph(highlights, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print("✓ Created: Harvard_Performance_Report_2023.pdf")

def create_allianz_compliance_report():
    """Create Allianz Global Investors Compliance Report"""
    doc = SimpleDocTemplate("knowledge_base_samples/Allianz_Compliance_Review_2024.pdf", pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#003781'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    story.append(Paragraph("Allianz Global Investors", title_style))
    story.append(Paragraph("Regulatory Compliance Review - Q1 2024", styles['Heading2']))
    story.append(Spacer(1, 0.5*inch))
    
    # Compliance Summary
    story.append(Paragraph("Compliance Status Overview", styles['Heading2']))
    
    compliance_data = [
        ['Regulatory Framework', 'Status', 'Last Review', 'Next Review', 'Issues'],
        ['Solvency II', '✓ Compliant', '15-Jan-2024', '15-Apr-2024', '0'],
        ['GDPR', '✓ Compliant', '22-Jan-2024', '22-Jul-2024', '0'],
        ['MiFID II', '✓ Compliant', '08-Jan-2024', '08-Apr-2024', '1 Minor'],
        ['AIFMD', '✓ Compliant', '12-Dec-2023', '12-Mar-2024', '0'],
        ['SFDR', '⚠ Review Needed', '30-Nov-2023', '01-Mar-2024', '2 Pending'],
        ['Basel III', '✓ Compliant', '20-Jan-2024', '20-Apr-2024', '0'],
        ['FATCA', '✓ Compliant', '10-Jan-2024', '10-Jul-2024', '0']
    ]
    
    table = Table(compliance_data, colWidths=[1.8*inch, 1*inch, 1.3*inch, 1.3*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003781')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    story.append(Spacer(1, 0.3*inch))
    
    # Regulatory Capital Requirements
    story.append(Paragraph("Regulatory Capital Analysis", styles['Heading2']))
    
    capital_text = """
    Current Regulatory Capital Position:
    • Solvency Capital Requirement (SCR): €2.4 billion
    • Eligible Own Funds: €4.4 billion
    • Solvency Ratio: 185% (Target: >150%)
    • Minimum Capital Requirement (MCR): €1.1 billion
    • MCR Coverage: 400%
    
    The institution maintains a strong capital position with significant buffers above regulatory minimums. 
    Stress testing indicates the solvency ratio would remain above 140% even under severe adverse scenarios.
    """
    story.append(Paragraph(capital_text, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Compliance Issues and Remediation
    story.append(Paragraph("Open Compliance Items", styles['Heading2']))
    
    issues_text = """
    1. MiFID II - Best Execution Reporting
       Issue: Quarterly best execution reports missing timestamp granularity
       Impact: Low
       Remediation: System upgrade scheduled for February 2024
       Status: In Progress
    
    2. SFDR - Article 8 Product Disclosures
       Issue: Two funds require updated sustainability risk disclosures
       Impact: Medium
       Remediation: Legal review in progress, completion by March 1, 2024
       Status: Pending Legal Review
    
    3. SFDR - Principal Adverse Impact Statement
       Issue: 2024 PAI statement requires additional climate metrics
       Impact: Medium
       Remediation: Data collection underway with ESG data provider
       Status: Data Gathering Phase
    """
    story.append(Paragraph(issues_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print("✓ Created: Allianz_Compliance_Review_2024.pdf")

def create_client_meeting_notes():
    """Create client meeting notes"""
    doc = SimpleDocTemplate("knowledge_base_samples/CalPERS_Board_Meeting_Minutes_Jan2024.pdf", pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Header
    story.append(Paragraph("CalPERS Board Meeting Minutes", styles['Heading1']))
    story.append(Paragraph("Investment Committee - January 25, 2024", styles['Heading2']))
    story.append(Paragraph("Confidential - Internal Use Only", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    
    # Attendees
    story.append(Paragraph("Attendees:", styles['Heading3']))
    attendees_text = """
    • Alex King, CIO - CalPERS
    • Brad Pitt, Relationship Manager - Investment Manager
    • Meredith Grey, Deputy CIO - CalPERS  
    • Derek Shephard, Risk Manager - CalPERS
    • Christina Yang, Portfolio Manager - Investment Manager
    • Will Smith, Compliance Officer - Investment Manager
    """
    story.append(Paragraph(attendees_text, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Agenda Items
    story.append(Paragraph("Key Discussion Points:", styles['Heading3']))
    
    discussion = """
    1. PORTFOLIO PERFORMANCE REVIEW
    • Q4 2023 performance: +4.2% vs benchmark +3.8%
    • Strong performance in private equity (+15.2%) offset weakness in emerging markets (-3.1%)
    • CIO expressed satisfaction with overall results but raised concerns about EM exposure
    • ACTION: Reduce emerging market allocation from 12% to 8% by end of Q1 2024
    
    2. RISK MANAGEMENT UPDATE
    • Current funded ratio improved to 83% from 79% last year
    • VaR remains within acceptable limits at 4.04%
    • Discussion on increasing hedging ratio for currency exposure
    • ACTION: Implement 50% hedge on EUR and JPY exposures by February 15
    
    3. PRIVATE MARKETS STRATEGY
    • Board approved increasing private equity allocation ceiling to 15% (from 13%)
    • Focus on co-investments to reduce fees
    • Concern raised about 2021-2022 vintage valuations
    • ACTION: Provide detailed analysis of PE portfolio by vintage year
    
    4. ESG INTEGRATION
    • Net-zero commitment timeline discussed
    • Request for climate scenario analysis on real estate portfolio
    • Board supports increased allocation to renewable infrastructure
    • ACTION: Present comprehensive ESG integration plan at next quarterly meeting
    
    5. FEE DISCUSSION
    • Reviewed current fee structure of 35 bps
    • Discussed performance fee hurdle adjustment
    • Agreement to maintain current structure pending performance review
    
    6. OPERATIONAL MATTERS
    • New reporting requirements for SFDR compliance
    • Update on technology platform integration
    • Cybersecurity audit results - no major findings
    """
    story.append(Paragraph(discussion, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Next Steps
    story.append(Paragraph("Next Steps and Deliverables:", styles['Heading3']))
    next_steps = """
    • February 5: Deliver emerging markets transition plan
    • February 15: Complete currency hedging implementation
    • February 28: Submit private equity vintage analysis
    • March 15: Next quarterly review meeting
    • March 31: ESG integration plan presentation
    """
    story.append(Paragraph(next_steps, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print("✓ Created: CalPERS_Board_Meeting_Minutes_Jan2024.pdf")

def create_market_research_report():
    """Create market research report"""
    doc = SimpleDocTemplate("knowledge_base_samples/Private_Equity_Market_Outlook_2024.pdf", pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    story.append(Paragraph("Private Equity Market Outlook 2024", styles['Title']))
    story.append(Paragraph("Institutional Investor Research", styles['Heading2']))
    story.append(Spacer(1, 0.5*inch))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", styles['Heading2']))
    summary = """
    The private equity market enters 2024 facing a challenging environment characterized by higher interest 
    rates, valuation pressures, and reduced exit activity. However, significant dry powder ($3.9 trillion 
    globally) and improving credit markets suggest potential for increased deal activity in H2 2024. 
    Institutional investors should focus on: (1) co-investment opportunities to reduce fees, (2) secondary 
    market transactions for liquidity, and (3) sector specialists in healthcare and technology.
    """
    story.append(Paragraph(summary, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Market Statistics
    story.append(Paragraph("Market Statistics", styles['Heading2']))
    
    market_data = [
        ['Metric', '2023', '2024E', 'Change'],
        ['Global Fundraising', '$1,234B', '$1,450B', '+17.5%'],
        ['Dry Powder', '$3,720B', '$3,900B', '+4.8%'],
        ['Deal Value', '$765B', '$890B', '+16.3%'],
        ['Average Deal Size', '$780M', '$820M', '+5.1%'],
        ['Exit Value', '$456B', '$520B', '+14.0%'],
        ['Average Hold Period', '5.8 years', '6.2 years', '+6.9%'],
        ['Median Entry Multiple', '12.2x', '11.5x', '-5.7%'],
        ['IRR (Median 3-yr)', '18.5%', '16.0%', '-2.5pp']
    ]
    
    table = Table(market_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    story.append(Spacer(1, 0.3*inch))
    
    # Sector Analysis
    story.append(Paragraph("Sector Opportunities", styles['Heading2']))
    sector_analysis = """
    TOP SECTORS FOR 2024:
    
    1. HEALTHCARE TECHNOLOGY
    • Digital health platforms showing 25%+ growth
    • AI-driven drug discovery attracting premium valuations
    • Recommended allocation: 20-25% of PE portfolio
    
    2. ENTERPRISE SOFTWARE
    • SaaS businesses with 80%+ gross margins
    • Cybersecurity remains highly attractive
    • Recommended allocation: 15-20% of PE portfolio
    
    3. ENERGY TRANSITION
    • Renewable energy infrastructure
    • Battery technology and energy storage
    • Recommended allocation: 10-15% of PE portfolio
    
    SECTORS TO AVOID:
    • Traditional retail (structural headwinds)
    • Commercial real estate (office sector challenges)
    • Highly leveraged consumer discretionary
    """
    story.append(Paragraph(sector_analysis, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print("✓ Created: Private_Equity_Market_Outlook_2024.pdf")

# Generate all PDFs
if __name__ == "__main__":
    print("Generating sample knowledge base PDFs...")
    create_calpers_risk_report()
    create_harvard_performance_report()
    create_allianz_compliance_report()
    create_client_meeting_notes()
    create_market_research_report()
    print("\n✅ All PDFs created in 'knowledge_base_samples' folder")

# Custom Prompt Examples for Each Role
print("\n" + "="*60)
print("CUSTOM PROMPT EXAMPLES FOR EACH ROLE")
print("="*60)

custom_prompts = {
    "Chief Risk Officer": [
        "Analyze the correlation between our private equity allocation and overall portfolio volatility. How would a 20% drawdown in PE valuations impact our funded ratio?",
        
        "Review all compliance documents and identify any patterns of regulatory concerns across our institutional clients. What preventive measures should we implement?",
        
        "Based on recent meeting notes and risk reports, which clients show early warning signs of dissatisfaction that could lead to redemptions?",
        
        "Perform a stress test analysis assuming simultaneous shocks: equity markets -30%, interest rates +200bps, and private assets -15%. What's our worst-case funded ratio?",
        
        "Compare our risk metrics against peer institutions. Where are we outliers and should we be concerned?"
    ],
    
    "Portfolio Manager": [
        "Using performance attribution data, identify which asset classes have consistently underperformed their benchmarks over the last 3 years. Recommend specific manager changes.",
        
        "Analyze the fee efficiency of our private equity portfolio. Which funds have delivered returns that don't justify their 2/20 structure?",
        
        "Based on market outlook reports, recommend tactical tilts for the next quarter. Be specific about sizing and implementation timeline.",
        
        "Review our emerging market exposure in context of recent geopolitical developments. Should we maintain, reduce, or hedge our positions?",
        
        "Calculate the impact of moving $500M from active to passive management in developed market equities. Include fee savings and expected tracking error."
    ],
    
    "Relationship Manager": [
        "Draft talking points for upcoming CalPERS board meeting addressing their concerns about private equity valuations and funded ratio improvement strategies.",
        
        "Analyze meeting notes from the last 6 months to identify recurring client concerns. Create an action plan to address the top 3 issues.",
        
        "Based on client satisfaction scores and recent interactions, which accounts are at risk of reducing allocations? Propose retention strategies.",
        
        "Create a quarterly business review presentation highlighting our value-add beyond investment returns. Include risk management and operational excellence examples.",
        
        "Develop a communication plan for explaining our ESG integration approach to skeptical board members. Include concrete examples and performance impact."
    ],
    
    "Compliance Officer": [
        "Review all regulatory frameworks we're subject to and identify upcoming changes in 2024 that require system or process modifications.",
        
        "Analyze compliance breach patterns across our client base. What additional controls would prevent 80% of historical issues?",
        
        "Create a compliance risk scorecard for each institutional client based on their structure, jurisdiction, and investment mandates.",
        
        "Based on recent regulatory reviews, draft a remediation plan for SFDR Article 8 product disclosures with specific timelines and responsible parties.",
        
        "Assess our readiness for upcoming CSRD (Corporate Sustainability Reporting Directive) requirements. What data gaps exist?"
    ],
    
    "Client Services": [
        "Analyze service ticket data to identify the most common operational issues. Propose process improvements to reduce ticket volume by 30%.",
        
        "Create a client onboarding checklist based on lessons learned from recent implementations. Focus on avoiding common pitfalls.",
        
        "Review response time metrics and identify bottlenecks in our service delivery. Recommend staffing or system changes to improve SLAs.",
        
        "Based on client feedback, design a quarterly service scorecard that tracks metrics clients actually care about.",
        
        "Develop templates for common client requests to ensure consistent, high-quality responses while reducing response time."
    ]
}

print("\nThese prompts can be used in the 'Custom Prompt' section of the AI Analysis tab.")
print("\nEach prompt is designed to:")
print("• Leverage role-specific knowledge and permissions")
print("• Reference documents in the knowledge base")
print("• Require analysis across multiple data sources")
print("• Generate actionable insights")
print("\nThe AI will search the knowledge base for relevant documents and incorporate")
print("that context into its analysis, providing more accurate and grounded responses.")

print("\n" + "="*60)
print("KNOWLEDGE BASE USAGE TIPS")
print("="*60)

tips = """
1. DOCUMENT ORGANIZATION:
   • Use consistent naming: ClientName_DocumentType_Date.pdf
   • Tag documents with multiple relevant roles
   • Upload quarterly updates to maintain current information

2. EFFECTIVE SEARCHES:
   • Use specific terms: "CalPERS risk metrics" vs just "risk"
   • Filter by client when analyzing specific accounts
   • Search for document types: "compliance review" or "meeting notes"

3. AI INTEGRATION:
   • Always enable "Use Knowledge Base" for informed analysis
   • Reference specific time periods in prompts for historical analysis
   • Ask for comparisons across documents for trend analysis

4. ROLE-BASED STRATEGIES:
   • CRO: Focus on risk reports and compliance documents
   • PM: Emphasize performance reports and market research
   • RM: Prioritize meeting notes and client communications
   • CO: Concentrate on regulatory updates and compliance reviews

5. PROMPT ENGINEERING:
   • Be specific about the analysis needed
   • Reference document types you want analyzed
   • Ask for quantitative outputs when applicable
   • Request action items and timelines
"""

print(tips)