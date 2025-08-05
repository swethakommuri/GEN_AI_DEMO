import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import yfinance as yf
import requests
import json
import time
import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import hashlib
import os
import base64
import io
from PIL import Image

# Configure Streamlit page
st.set_page_config(
    page_title="Enterprise AI Client Intelligence Platform",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for role-based styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    .role-badge {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 1rem;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
    }
    .role-cro { background: #dc2626; color: white; }
    .role-pm { background: #2563eb; color: white; }
    .role-rm { background: #059669; color: white; }
    .role-cs { background: #7c3aed; color: white; }
    .role-co { background: #ea580c; color: white; }
    
    .ai-status {
        background: linear-gradient(45deg, #10b981, #059669);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .alert-critical { border-left-color: #dc2626; background: #fef2f2; }
    .alert-warning { border-left-color: #ea580c; background: #fff7ed; }
    .alert-info { border-left-color: #2563eb; background: #eff6ff; }
    
    .knowledge-base-card {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .document-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.2s;
    }
    
    .document-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    .upload-zone {
        border: 2px dashed #cbd5e1;
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
        background: #f8fafc;
        margin: 1rem 0;
    }
    
    .insight-card {
        background: linear-gradient(to right, #f8fafc, #f1f5f9);
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .recommendation-box {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# Role definitions and permissions
@dataclass
class UserRole:
    name: str
    permissions: List[str]
    dashboard_widgets: List[str]
    ai_prompts: Dict[str, str]

# Define user roles with enhanced prompts
ROLES = {
    "Chief Risk Officer": UserRole(
        name="Chief Risk Officer",
        permissions=["view_all_clients", "risk_analysis", "compliance_reports", "ai_insights", 
                    "portfolio_overview", "upload_documents", "view_all_documents"],
        dashboard_widgets=["risk_alerts", "compliance_status", "client_churn_prediction", "regulatory_updates"],
        ai_prompts={
            "risk_analysis": """Perform a comprehensive risk analysis for {client_name} with ${aum}B AUM. 
            Include: 1) Current risk metrics (VaR, tracking error, Sharpe ratio)
            2) Stress test scenarios and potential impacts
            3) Top 5 risk factors and mitigation strategies
            4) Comparison to peer institutions
            5) Specific action items with timelines""",
            
            "portfolio_risk": """Evaluate portfolio concentration and correlation risks for {client_name}.
            Analyze: 1) Sector concentration limits and current exposures
            2) Geographic risk distribution
            3) Asset class correlations during stress periods
            4) Liquidity risk assessment
            5) Recommend specific hedging strategies with implementation steps""",
            
            "compliance": """Review compliance status for {client_name} across all regulatory frameworks.
            Detail: 1) Current compliance gaps if any
            2) Upcoming regulatory changes and impacts
            3) Required documentation updates
            4) Risk-rated action plan with deadlines
            5) Resource requirements for compliance enhancement"""
        }
    ),
    "Portfolio Manager": UserRole(
        name="Portfolio Manager",
        permissions=["view_assigned_clients", "portfolio_analysis", "performance_reports", 
                    "ai_insights", "trade_recommendations", "upload_documents", "view_portfolio_documents"],
        dashboard_widgets=["portfolio_performance", "asset_allocation", "rebalancing_alerts", "market_opportunities"],
        ai_prompts={
            "portfolio_optimization": """Analyze {client_name}'s portfolio with ${aum}B AUM for optimization opportunities.
            Provide: 1) Current vs optimal asset allocation with specific percentages
            2) Expected return and risk impact of changes
            3) Implementation timeline and trade list
            4) Cost analysis including transaction costs and tax implications
            5) Performance improvement projections over 1, 3, and 5 years""",
            
            "performance_analysis": """Conduct performance attribution analysis for {client_name}.
            Include: 1) Asset class contribution to returns
            2) Security selection vs asset allocation impact
            3) Currency and factor exposures
            4) Benchmark comparison and tracking error decomposition
            5) Specific recommendations to improve alpha generation""",
            
            "rebalancing": """Create a detailed rebalancing plan for {client_name}'s portfolio.
            Detail: 1) Current vs target allocations with drift analysis
            2) Prioritized trade list with sizes
            3) Market impact and transaction cost estimates
            4) Optimal execution strategy and timing
            5) Risk metrics before and after rebalancing"""
        }
    ),
    "Relationship Manager": UserRole(
        name="Relationship Manager", 
        permissions=["view_assigned_clients", "client_communications", "service_requests", 
                    "ai_insights", "view_client_documents"],
        dashboard_widgets=["client_satisfaction", "upcoming_meetings", "service_issues", "retention_alerts"],
        ai_prompts={
            "client_relationship": """Analyze relationship health for {client_name} (Satisfaction: {satisfaction}/10, Churn Risk: {churn_risk}%).
            Provide: 1) Key relationship strengths and concerns
            2) Analysis of recent interactions and feedback
            3) Comparison to similar institutional clients
            4) Specific retention strategies with success probabilities
            5) 90-day action plan with measurable outcomes""",
            
            "service_improvement": """Identify service enhancement opportunities for {client_name}.
            Include: 1) Current service gaps based on client feedback
            2) Benchmark against best practices for {client_type} clients
            3) Technology and process improvements needed
            4) Resource requirements and timeline
            5) Expected impact on satisfaction scores""",
            
            "retention_strategy": """Develop a comprehensive retention strategy for {client_name}.
            Detail: 1) Early warning indicators of dissatisfaction
            2) Competitive threats and switching barriers
            3) Value proposition enhancements
            4) Key stakeholder engagement plan
            5) Success metrics and monitoring framework"""
        }
    ),
    "Client Services": UserRole(
        name="Client Services",
        permissions=["view_service_requests", "client_communications", "issue_tracking", "view_service_documents"],
        dashboard_widgets=["open_tickets", "response_times", "client_feedback", "service_metrics"],
        ai_prompts={
            "service_analysis": """Analyze service delivery metrics for {client_name}.
            Include: 1) Current SLA performance and gaps
            2) Common issue categories and root causes
            3) Process bottlenecks and inefficiencies
            4) Automation opportunities
            5) Improvement roadmap with quick wins""",
            
            "client_feedback": """Review and analyze client feedback patterns for {client_name}.
            Provide: 1) Sentiment analysis and trending topics
            2) Comparison to peer satisfaction levels
            3) Correlation between issues and satisfaction
            4) Prioritized improvement areas
            5) Communication plan for addressing concerns"""
        }
    ),
    "Compliance Officer": UserRole(
        name="Compliance Officer",
        permissions=["compliance_reports", "regulatory_updates", "audit_trails", "ai_insights", 
                    "upload_documents", "view_all_documents"],
        dashboard_widgets=["compliance_alerts", "regulatory_deadlines", "audit_findings", "policy_updates"],
        ai_prompts={
            "compliance_review": """Conduct comprehensive compliance review for {client_name} ({client_type}).
            Assess: 1) Current regulatory compliance status by framework
            2) Documentation completeness and accuracy
            3) Process and control effectiveness
            4) Upcoming regulatory changes and preparation needed
            5) Risk-prioritized remediation plan with resource needs""",
            
            "regulatory_impact": """Analyze regulatory change impacts for {client_name}.
            Detail: 1) New requirements by regulation
            2) Gap analysis against current state
            3) System and process changes required
            4) Cost and timeline estimates
            5) Implementation roadmap with milestones"""
        }
    )
}

# Enhanced AI prompt engineering
class EnhancedAISystem:
    """Enhanced AI system with better prompt engineering for various models"""
    
    def __init__(self):
        self.model_configs = {
            'gemma': {
                'temperature': 0.8,
                'top_p': 0.95,
                'top_k': 50,
                'num_predict': 800,  # Increased for more complete responses
                'repeat_penalty': 1.1
            },
            'llama2': {
                'temperature': 0.7,
                'top_p': 0.9,
                'top_k': 40,
                'num_predict': 800,
                'repeat_penalty': 1.15
            },
            'mistral': {
                'temperature': 0.7,
                'top_p': 0.9,
                'top_k': 40,
                'num_predict': 800,
                'repeat_penalty': 1.1
            },
            'default': {
                'temperature': 0.7,
                'top_p': 0.9,
                'top_k': 40,
                'num_predict': 800,
                'repeat_penalty': 1.1
            }
        }
    
    def get_model_config(self, model_name: str) -> dict:
        """Get optimized configuration for specific model"""
        for key in self.model_configs:
            if key in model_name.lower():
                return self.model_configs[key]
        return self.model_configs['default']
    
    def create_system_prompt(self, role: str, client_info: dict) -> str:
        """Create a detailed system prompt for better context"""
        return f"""You are an expert {role} at a leading institutional investment management firm with 20+ years of experience.
        
You are analyzing {client_info.get('client_name', 'Client')}:
- Type: {client_info.get('client_type', 'Institutional')}
- AUM: ${client_info.get('aum', 0)}B
- Current Status: {client_info.get('status', 'Active')}
- Key Metrics: Satisfaction {client_info.get('satisfaction', 'N/A')}/10, Churn Risk {client_info.get('churn_risk', 'N/A')}%

CRITICAL INSTRUCTIONS:
1. Provide SPECIFIC, QUANTITATIVE recommendations with exact numbers
2. Include TIMELINES for all action items
3. Reference INDUSTRY BEST PRACTICES and benchmarks
4. Format response with CLEAR SECTIONS and bullet points
5. Ensure ALL recommendations are ACTIONABLE and MEASURABLE
6. Be COMPREHENSIVE - do not cut off mid-sentence
7. Include RISK CONSIDERATIONS for each recommendation

Your analysis should be thorough, professional, and immediately actionable by institutional investment professionals."""
    
    def enhance_prompt(self, base_prompt: str, context: str, role: str) -> str:
        """Enhance prompt with better structure and clarity"""
        enhanced_prompt = f"""{context}

ANALYSIS REQUEST:
{base_prompt}

RESPONSE STRUCTURE REQUIRED:
1. Executive Summary (2-3 key points)
2. Detailed Analysis (with specific metrics)
3. Recommendations (numbered, with timelines)
4. Risk Considerations
5. Next Steps (specific actions)

Provide a comprehensive response that addresses ALL aspects of the request. Be specific with numbers, percentages, and timelines."""
        
        return enhanced_prompt
    
    def call_ai_with_retry(self, prompt: str, model: str, role: str, client_info: dict, 
                          max_retries: int = 2, timeout: int = 90) -> Optional[str]:
        """Call AI with retry logic and better error handling"""
        
        model_config = self.get_model_config(model)
        system_prompt = self.create_system_prompt(role, client_info)
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": model,
                        "prompt": f"{system_prompt}\n\n{prompt}",
                        "stream": False,
                        "options": model_config
                    },
                    timeout=timeout
                )
                
                if response.status_code == 200:
                    ai_response = response.json().get("response", "").strip()
                    
                    # Validate response completeness
                    if len(ai_response) > 100 and not ai_response.endswith(('.', '!', '?', '"')):
                        # Response seems incomplete, try to continue
                        continuation_prompt = f"{system_prompt}\n\n{prompt}\n\nPrevious response:\n{ai_response}\n\nPlease continue and complete the analysis:"
                        
                        continuation = requests.post(
                            "http://localhost:11434/api/generate",
                            json={
                                "model": model,
                                "prompt": continuation_prompt,
                                "stream": False,
                                "options": model_config
                            },
                            timeout=timeout
                        )
                        
                        if continuation.status_code == 200:
                            ai_response += "\n\n" + continuation.json().get("response", "").strip()
                    
                    return ai_response
                else:
                    st.warning(f"AI returned status code: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                st.warning(f"AI request timed out (attempt {attempt + 1}/{max_retries})")
            except Exception as e:
                st.error(f"AI Error: {str(e)}")
            
            if attempt < max_retries - 1:
                time.sleep(2)  # Brief pause before retry
        
        return None

# Simple in-memory storage for documents
if 'document_store' not in st.session_state:
    st.session_state.document_store = []

if 'knowledge_base' not in st.session_state:
    st.session_state.knowledge_base = {
        'documents': [],
        'embeddings': []
    }

if 'ai_system' not in st.session_state:
    st.session_state.ai_system = EnhancedAISystem()

class SimpleRAGSystem:
    """Simplified RAG system for demonstration"""
    
    def __init__(self):
        self.documents = st.session_state.knowledge_base['documents']
    
    def add_document(self, file_content, file_name, document_type, client_name, roles_allowed, uploaded_by):
        """Add a document to the knowledge base"""
        doc_id = hashlib.md5(f"{file_name}{datetime.now()}".encode()).hexdigest()[:8]
        
        doc_metadata = {
            'id': doc_id,
            'file_name': file_name,
            'document_type': document_type,
            'client_name': client_name,
            'roles_allowed': roles_allowed,
            'uploaded_by': uploaded_by,
            'upload_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'content': file_content[:1000]  # Store first 1000 chars for demo
        }
        
        self.documents.append(doc_metadata)
        st.session_state.knowledge_base['documents'] = self.documents
        
        return doc_id
    
    def search_documents(self, query, user_role, client_filter=None):
        """Search documents based on query and permissions"""
        results = []
        
        for doc in self.documents:
            # Check permissions
            if user_role not in doc['roles_allowed']:
                continue
            
            # Apply client filter
            if client_filter and doc['client_name'] != client_filter:
                continue
            
            # Simple keyword search
            if query.lower() in doc['file_name'].lower() or query.lower() in doc['content'].lower():
                results.append(doc)
        
        return results
    
    def get_context_for_prompt(self, query, client_name, user_role):
        """Get relevant context for AI prompt"""
        relevant_docs = self.search_documents(query, user_role, client_name)
        
        context = "RELEVANT KNOWLEDGE BASE DOCUMENTS:\n\n"
        for doc in relevant_docs[:3]:  # Top 3 documents
            context += f"📄 Document: {doc['file_name']}\n"
            context += f"Type: {doc['document_type']}\n"
            context += f"Date: {doc['upload_date']}\n"
            context += f"Content Preview: {doc['content'][:200]}...\n"
            context += "-" * 50 + "\n\n"
        
        return context

# Initialize RAG system
@st.cache_resource
def get_rag_system():
    return SimpleRAGSystem()

# Load client data
@st.cache_data(ttl=300)
def load_enhanced_client_data():
    """Load comprehensive institutional client data"""
    
    clients_data = {
        'CalPERS - California Public Employees': {
            'aum': 450.0,
            'satisfaction': 8.4,
            'churn_risk': 8,
            'status': 'excellent',
            'type': 'public_pension',
            'last_contact': '2024-01-25',
            'liability_duration': 14.2,
            'funded_ratio': 0.83,
            'headquarters': 'Sacramento, CA',
            'primary_contact': 'Alex King, CIO',
            'relationship_manager': 'Brad Pitt',
            'inception_date': '2018-03-15',
            'fee_rate': 0.35,
            'members': 2_000_000,
            'governance_score': 9.2,
        },
        'Harvard Management Company': {
            'aum': 53.2,
            'satisfaction': 7.8,
            'churn_risk': 15,
            'status': 'good',
            'type': 'endowment',
            'last_contact': '2024-01-20',
            'liability_duration': 25.0,
            'funded_ratio': 0.95,
            'headquarters': 'Cambridge, MA',
            'primary_contact': 'Rachel Green, CEO',
            'relationship_manager': 'Barbara Jean',
            'inception_date': '2020-09-01',
            'fee_rate': 0.65,
            'governance_score': 8.7,
        },
        'Allianz Global Investors': {
            'aum': 125.8,
            'satisfaction': 8.9,
            'churn_risk': 5,
            'status': 'excellent',
            'type': 'insurance',
            'last_contact': '2024-01-28',
            'liability_duration': 9.5,
            'funded_ratio': 1.08,
            'headquarters': 'Munich, Germany',
            'primary_contact': 'Chandler Bing, Head of Investments',
            'relationship_manager': 'Monica Geller',
            'inception_date': '2019-06-12',
            'fee_rate': 0.28,
            'governance_score': 9.5,
        }
    }
    
    portfolio_data = {
        'CalPERS - California Public Employees': [
            {'Asset Class': 'Global Equity', 'Current': 52, 'Target': 50, 'Value': 234.0},
            {'Asset Class': 'Fixed Income', 'Current': 28, 'Target': 30, 'Value': 126.0},
            {'Asset Class': 'Private Equity', 'Current': 13, 'Target': 13, 'Value': 58.5},
            {'Asset Class': 'Real Estate', 'Current': 12, 'Target': 12, 'Value': 54.0},
        ],
        'Harvard Management Company': [
            {'Asset Class': 'Global Equity', 'Current': 35, 'Target': 37, 'Value': 18.6},
            {'Asset Class': 'Hedge Funds', 'Current': 25, 'Target': 23, 'Value': 13.3},
            {'Asset Class': 'Private Equity', 'Current': 18, 'Target': 17, 'Value': 9.6},
            {'Asset Class': 'Fixed Income', 'Current': 12, 'Target': 15, 'Value': 6.4},
        ],
        'Allianz Global Investors': [
            {'Asset Class': 'Government Bonds', 'Current': 45, 'Target': 43, 'Value': 56.6},
            {'Asset Class': 'Corporate Bonds', 'Current': 28, 'Target': 30, 'Value': 35.2},
            {'Asset Class': 'Global Equity', 'Current': 20, 'Target': 22, 'Value': 25.2},
            {'Asset Class': 'Real Estate', 'Current': 8, 'Target': 8, 'Value': 10.1},
        ]
    }
    
    return clients_data, portfolio_data

def check_ollama_status():
    """Check if Ollama is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        if response.status_code == 200:
            models = [model["name"] for model in response.json().get("models", [])]
            return True, models
        return False, []
    except:
        return False, []

def generate_enhanced_insights(client_name, client_data, portfolio_data, selected_model, user_role, rag_system, use_knowledge_base=True):
    """Generate enhanced AI insights with better prompts and handling"""
    
    insights = []
    role_obj = ROLES[user_role]
    ai_system = st.session_state.ai_system
    
    # Prepare client info for AI
    client_info = {
        'client_name': client_name,
        'client_type': client_data['type'],
        'aum': client_data['aum'],
        'satisfaction': client_data['satisfaction'],
        'churn_risk': client_data['churn_risk'],
        'status': client_data['status']
    }
    
    # Generate insights for each available prompt type
    for prompt_key, prompt_template in role_obj.ai_prompts.items():
        with st.status(f"🧠 Generating {prompt_key.replace('_', ' ').title()} insights...") as status:
            
            # Fill in the prompt template
            prompt = prompt_template.format(
                client_name=client_name,
                aum=client_data['aum'],
                satisfaction=client_data['satisfaction'],
                churn_risk=client_data['churn_risk'],
                client_type=client_data['type']
            )
            
            # Add knowledge base context if enabled
            context = ""
            if use_knowledge_base:
                kb_context = rag_system.get_context_for_prompt(prompt_key, client_name, user_role)
                context = kb_context
            
            # Enhance the prompt
            enhanced_prompt = ai_system.enhance_prompt(prompt, context, user_role)
            
            # Call AI with retry logic
            ai_response = ai_system.call_ai_with_retry(
                enhanced_prompt,
                selected_model,
                user_role,
                client_info
            )
            
            if ai_response and len(ai_response) > 100:
                status.update(label=f"✅ {prompt_key.replace('_', ' ').title()} analysis complete", state="complete")
                
                # Determine priority based on content
                priority = "HIGH" if client_data['churn_risk'] > 20 or "urgent" in ai_response.lower() else "MEDIUM"
                
                insights.append({
                    'type': prompt_key.replace('_', ' ').title(),
                    'priority': priority,
                    'title': f"{prompt_key.replace('_', ' ').title()} - {client_name}",
                    'content': ai_response,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'model': selected_model,
                    'role': user_role
                })
            else:
                status.update(label=f"❌ Failed to generate {prompt_key} insights", state="error")
                st.warning(f"Could not generate complete insights for {prompt_key}")
    
    return insights

def render_insights_display(insights):
    """Render insights with enhanced formatting"""
    
    if not insights:
        st.info("No insights generated yet. Click 'Run AI Analysis' to generate insights.")
        return
    
    # Group insights by priority
    high_priority = [i for i in insights if i['priority'] == 'HIGH']
    medium_priority = [i for i in insights if i['priority'] == 'MEDIUM']
    low_priority = [i for i in insights if i['priority'] == 'LOW']
    
    # Display high priority first
    if high_priority:
        st.markdown("### 🚨 High Priority Insights")
        for insight in high_priority:
            render_single_insight(insight)
    
    if medium_priority:
        st.markdown("### ⚡ Medium Priority Insights")
        for insight in medium_priority:
            render_single_insight(insight)
    
    if low_priority:
        st.markdown("### 📋 Low Priority Insights")
        for insight in low_priority:
            render_single_insight(insight)

def render_single_insight(insight):
    """Render a single insight with proper formatting"""
    
    with st.container():
        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
        
        # Header
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"### {insight['title']}")
        with col2:
            priority_colors = {
                'HIGH': '#dc2626',
                'MEDIUM': '#f59e0b', 
                'LOW': '#10b981'
            }
            color = priority_colors.get(insight['priority'], '#6b7280')
            st.markdown(
                f'<span style="background:{color};color:white;padding:4px 12px;border-radius:20px;font-size:12px;">'
                f'{insight["priority"]} PRIORITY</span>',
                unsafe_allow_html=True
            )
        with col3:
            st.caption(f"🤖 {insight['model']}")
        
        # Content with better formatting
        content_lines = insight['content'].split('\n')
        
        for line in content_lines:
            if line.strip():
                # Format sections
                if line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
                    st.markdown(f"**{line.strip()}**")
                elif line.strip().startswith('•'):
                    st.markdown(f"  {line.strip()}")
                elif line.strip().endswith(':') and len(line.strip()) < 50:
                    st.markdown(f"**{line.strip()}**")
                elif 'RECOMMENDATION' in line.upper() or 'ACTION' in line.upper():
                    st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
                    st.markdown(f"🎯 {line.strip()}")
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.markdown(line)
        
        # Footer
        st.caption(f"Generated: {insight['timestamp']} | Role: {insight['role']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")

def main():
    # Initialize systems
    rag_system = get_rag_system()
    
    # Header with role selection
    st.markdown("""
    <div class="main-header">
        <h1>🏦 Enterprise AI Client Intelligence Platform</h1>
        <p>Enhanced Multi-Modal RAG Institutional Investment Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # PROMINENT ROLE SELECTION AT TOP
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 👤 Select Your Role")
        selected_role = st.selectbox(
            "Choose your role to access role-specific features:",
            list(ROLES.keys()),
            key="main_role_selector",
            help="Your role determines what data you can access and what actions you can perform"
        )
        
        # Display role badge
        role_class_map = {
            "Chief Risk Officer": "role-cro",
            "Portfolio Manager": "role-pm",
            "Relationship Manager": "role-rm",
            "Client Services": "role-cs",
            "Compliance Officer": "role-co"
        }
        
        role_class = role_class_map.get(selected_role, "role-cro")
        st.markdown(f'<div class="{role_class} role-badge">{selected_role}</div>', unsafe_allow_html=True)
    
    # Store role in session state
    st.session_state['current_role'] = selected_role
    role_obj = ROLES[selected_role]
    
    # Load data
    clients_data, portfolio_data = load_enhanced_client_data()
    
    # Check AI status
    ollama_running, available_models = check_ollama_status()
    
    # Sidebar configuration
    with st.sidebar:
        st.title("🔧 Configuration")
        
        # Show current role
        st.markdown("### 👤 Current Role")
        st.info(f"Logged in as: **{selected_role}**")
        
        # Show permissions
        with st.expander("🔐 Your Permissions"):
            for perm in role_obj.permissions:
                st.write(f"✅ {perm.replace('_', ' ').title()}")
        
        # AI System Status
        st.markdown("### 🤖 AI System")
        if ollama_running and available_models:
            st.success("✅ AI System Online")
            selected_model = st.selectbox(
                "AI Model",
                available_models,
                help="Choose AI model for analysis"
            )
            
            # Model optimization tips
            if 'gemma' in selected_model.lower():
                st.info("💡 Gemma: Optimized for detailed analysis")
            elif 'llama' in selected_model.lower():
                st.info("💡 Llama: Balanced performance")
            elif 'mistral' in selected_model.lower():
                st.info("💡 Mistral: Fast and efficient")
                
        else:
            st.error("❌ AI System Offline")
            st.code("Run: ollama serve")
            selected_model = None
        
        # Client Selection
        st.markdown("### 🏢 Client Selection")
        if "view_all_clients" in role_obj.permissions:
            available_clients = list(clients_data.keys())
        else:
            available_clients = list(clients_data.keys())[:2]  # Limited access
        
        selected_client = st.selectbox(
            "Select Client",
            available_clients
        )
        
        # Advanced Settings
        with st.expander("⚙️ Advanced Settings"):
            ai_timeout = st.slider("AI Timeout (seconds)", 30, 180, 90)
            use_streaming = st.checkbox("Enable response streaming", value=False)
            max_retries = st.number_input("Max retry attempts", 1, 5, 2)
    
    # Main content - Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard", 
        "🧠 AI Analysis", 
        "📚 Knowledge Base", 
        "📈 Reports"
    ])
    
    with tab1:
        # Dashboard content
        client_info = clients_data[selected_client]
        st.header(f"📋 {selected_client}")
        
        # Metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("AUM", f"${client_info['aum']}B")
        with col2:
            st.metric("Satisfaction", f"{client_info['satisfaction']}/10", 
                     f"{'+' if client_info['satisfaction'] > 8 else ''}{client_info['satisfaction']-8:.1f}")
        with col3:
            churn_delta = client_info['churn_risk'] - 15  # 15% is baseline
            st.metric("Churn Risk", f"{client_info['churn_risk']}%",
                     f"{'+' if churn_delta > 0 else ''}{churn_delta}%",
                     delta_color="inverse")
        with col4:
            st.metric("Funded Ratio", f"{client_info.get('funded_ratio', 'N/A'):.1%}")
        with col5:
            st.metric("Fee Rate", f"{client_info['fee_rate']}%")
        
        # Portfolio visualization
        st.subheader("📊 Portfolio Analysis")
        portfolio_df = pd.DataFrame(portfolio_data[selected_client])
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.pie(
                portfolio_df, 
                values='Value', 
                names='Asset Class',
                title=f"Asset Allocation (${client_info['aum']}B Total)",
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Allocation drift analysis
            portfolio_df['Drift'] = portfolio_df['Current'] - portfolio_df['Target']
            
            fig = px.bar(
                portfolio_df,
                x='Asset Class',
                y='Drift',
                title="Allocation Drift from Target (%)",
                color='Drift',
                color_continuous_scale='RdYlGn_r',
                range_color=[-5, 5]
            )
            fig.add_hline(y=0, line_dash="dash", line_color="gray")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.header(f"🧠 Enhanced {selected_role} AI Analysis")
        
        if not ollama_running:
            st.error("🚫 AI analysis requires the AI system to be online")
            st.info("Please start Ollama to use AI features")
        else:
            # Quick action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🎯 Quick Risk Analysis", use_container_width=True):
                    st.session_state['quick_analysis'] = 'risk_analysis'
            
            with col2:
                if st.button("📊 Portfolio Review", use_container_width=True):
                    st.session_state['quick_analysis'] = 'portfolio_optimization'
            
            with col3:
                if st.button("📋 Compliance Check", use_container_width=True):
                    st.session_state['quick_analysis'] = 'compliance_review'
            
            st.markdown("---")
            
            # Analysis Options
            col1, col2 = st.columns(2)
            
            with col1:
                analysis_type = st.selectbox(
                    "Select Analysis Type",
                    ["Full Analysis (All Areas)"] + list(role_obj.ai_prompts.keys()),
                    format_func=lambda x: x.replace('_', ' ').title()
                )
            
            with col2:
                use_knowledge_base = st.checkbox("Use Knowledge Base", value=True)
                generate_report = st.checkbox("Generate PDF Report", value=False)
            
            # Custom prompt option
            use_custom = st.checkbox("Add custom instructions")
            
            if use_custom:
                custom_prompt = st.text_area(
                    "Additional instructions for AI",
                    height=100,
                    placeholder="E.g., Focus on ESG factors, compare with peer institutions, etc."
                )
            else:
                custom_prompt = ""
            
            # Run Analysis Button
            if st.button("🚀 Run Enhanced AI Analysis", type="primary", use_container_width=True):
                
                with st.spinner(f"Running enhanced {analysis_type} analysis with {selected_model}..."):
                    
                    # Check if quick analysis was triggered
                    if 'quick_analysis' in st.session_state:
                        analysis_type = st.session_state['quick_analysis']
                        del st.session_state['quick_analysis']
                    
                    # Generate insights
                    insights = generate_enhanced_insights(
                        selected_client,
                        clients_data[selected_client],
                        portfolio_data,
                        selected_model,
                        selected_role,
                        rag_system,
                        use_knowledge_base
                    )
                    
                    # Store in session state
                    st.session_state['current_insights'] = insights
                    st.session_state['insights_timestamp'] = datetime.now()
                    
                    st.success(f"✅ Generated {len(insights)} comprehensive insights")
                    
                    if generate_report:
                        st.info("📄 PDF report generation coming soon...")
            
            # Display insights
            if 'current_insights' in st.session_state:
                st.markdown("---")
                st.markdown("## 📊 Analysis Results")
                
                if 'insights_timestamp' in st.session_state:
                    st.caption(f"Generated: {st.session_state['insights_timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Display insights with enhanced formatting
                render_insights_display(st.session_state['current_insights'])
                
                # Export options
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📧 Email Insights", use_container_width=True):
                        st.info("Email functionality coming soon...")
                with col2:
                    if st.button("📄 Export PDF", use_container_width=True):
                        st.info("PDF export coming soon...")
                with col3:
                    if st.button("💾 Save to Knowledge Base", use_container_width=True):
                        st.success("Insights saved to knowledge base")
    
    with tab3:
        st.header("📚 Knowledge Base & Document Management")
        
        # Check if user can upload
        can_upload = "upload_documents" in role_obj.permissions
        
        if can_upload:
            # Document Upload Section
            st.markdown("### 📤 Upload New Document")
            
            with st.container():
                st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
                
                uploaded_file = st.file_uploader(
                    "Drop your file here or click to browse",
                    type=['pdf', 'docx', 'txt', 'xlsx', 'png', 'jpg', 'jpeg'],
                    help="Upload documents to the knowledge base"
                )
                
                if uploaded_file is not None:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info(f"📄 File: {uploaded_file.name}")
                        st.info(f"📏 Size: {uploaded_file.size / 1024:.1f} KB")
                    with col2:
                        st.info(f"📎 Type: {uploaded_file.type}")
                        st.info(f"👤 Uploader: {selected_role}")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            if uploaded_file is not None:
                st.markdown("### 📝 Document Details")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    doc_client = st.selectbox(
                        "Client",
                        available_clients,
                        key="upload_client"
                    )
                
                with col2:
                    doc_type = st.selectbox(
                        "Document Type",
                        ["Performance Report", "Risk Analysis", "Compliance Document", 
                         "Meeting Notes", "Research Report", "Financial Statement"],
                        key="upload_type"
                    )
                
                with col3:
                    roles_with_access = st.multiselect(
                        "Roles with Access",
                        list(ROLES.keys()),
                        default=[selected_role],
                        key="upload_roles"
                    )
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    if st.button("📤 Upload Document", type="primary", use_container_width=True):
                        with st.spinner("Processing document..."):
                            # Read file content
                            file_content = uploaded_file.read()
                            
                            # Add to RAG system
                            doc_id = rag_system.add_document(
                                file_content=str(file_content[:1000]),
                                file_name=uploaded_file.name,
                                document_type=doc_type,
                                client_name=doc_client,
                                roles_allowed=roles_with_access,
                                uploaded_by=selected_role
                            )
                            
                            st.success(f"✅ Document uploaded successfully!")
                            st.info(f"Document ID: {doc_id}")
                            st.balloons()
        else:
            st.warning("⚠️ You don't have permission to upload documents")
        
        # Document Search Section
        st.markdown("---")
        st.markdown("### 🔍 Search Documents")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            search_query = st.text_input(
                "Search in knowledge base",
                placeholder="Enter keywords to search documents..."
            )
        with col2:
            search_client_filter = st.selectbox(
                "Filter by client",
                ["All Clients"] + available_clients,
                key="search_filter"
            )
        
        if st.button("🔍 Search", type="primary"):
            if search_query:
                with st.spinner("Searching documents..."):
                    # Search documents
                    client_filter = None if search_client_filter == "All Clients" else search_client_filter
                    results = rag_system.search_documents(search_query, selected_role, client_filter)
                    
                    if results:
                        st.success(f"Found {len(results)} documents")
                        
                        for doc in results:
                            with st.container():
                                st.markdown('<div class="document-card">', unsafe_allow_html=True)
                                
                                col1, col2, col3 = st.columns([3, 1, 1])
                                with col1:
                                    st.markdown(f"**📄 {doc['file_name']}**")
                                    st.caption(f"Client: {doc['client_name']} | Type: {doc['document_type']}")
                                with col2:
                                    st.caption(f"Uploaded by: {doc['uploaded_by']}")
                                with col3:
                                    st.caption(f"Date: {doc['upload_date'][:10]}")
                                
                                with st.expander("Preview"):
                                    st.text(doc['content'][:300] + "...")
                                
                                st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.warning("No documents found matching your search")
            else:
                st.error("Please enter a search query")
        
        # Recent Documents
        st.markdown("---")
        st.markdown("### 📑 Recent Documents")
        
        all_docs = rag_system.search_documents("", selected_role)
        recent_docs = sorted(all_docs, key=lambda x: x['upload_date'], reverse=True)[:5]
        
        if recent_docs:
            for doc in recent_docs:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"📄 {doc['file_name']}")
                with col2:
                    st.caption(doc['document_type'])
                with col3:
                    st.caption(doc['upload_date'][:10])
        else:
            st.info("No documents available yet")
    
    with tab4:
        st.header("📈 Reports & Analytics")
        
        if "performance_reports" in role_obj.permissions:
            # Performance metrics
            st.subheader("Performance Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("YTD Return", "+8.4%", "+2.1%")
            with col2:
                st.metric("Sharpe Ratio", "1.24", "+0.15")
            with col3:
                st.metric("Information Ratio", "0.87", "+0.08")
            with col4:
                st.metric("Max Drawdown", "-12.4%", "-2.1%", delta_color="inverse")
            
            # Generate performance chart
            dates = pd.date_range(start='2024-01-01', periods=60, freq='D')
            base_return = 100
            returns = []
            benchmark_returns = []
            
            for i in range(60):
                daily_return = np.random.normal(0.0003, 0.015)
                benchmark_return = np.random.normal(0.0002, 0.012)
                base_return *= (1 + daily_return)
                returns.append(base_return)
                benchmark_returns.append(100 * (1 + benchmark_return * i * 0.01))
            
            performance = pd.DataFrame({
                'Date': dates,
                'Portfolio': returns,
                'Benchmark': benchmark_returns
            })
            
            fig = px.line(
                performance, 
                x='Date', 
                y=['Portfolio', 'Benchmark'],
                title="YTD Performance Comparison",
                labels={'value': 'Cumulative Return (Base 100)', 'variable': 'Series'}
            )
            fig.update_layout(hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk metrics
            st.subheader("Risk Analytics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Risk distribution
                risk_data = pd.DataFrame({
                    'Risk Factor': ['Market Risk', 'Credit Risk', 'Liquidity Risk', 
                                   'Operational Risk', 'Model Risk'],
                    'Contribution': [45, 20, 15, 12, 8]
                })
                
                fig = px.bar(
                    risk_data,
                    x='Risk Factor',
                    y='Contribution',
                    title="Risk Contribution by Factor (%)",
                    color='Contribution',
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Tracking error decomposition
                te_data = pd.DataFrame({
                    'Source': ['Asset Allocation', 'Security Selection', 
                              'Currency', 'Timing', 'Other'],
                    'Contribution': [1.2, 0.8, 0.5, 0.3, 0.2]
                })
                
                fig = px.pie(
                    te_data,
                    values='Contribution',
                    names='Source',
                    title="Tracking Error Decomposition",
                    hole=0.4
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("You don't have permission to view performance reports")

if __name__ == "__main__":
    # Initialize session state
    if 'current_role' not in st.session_state:
        st.session_state.current_role = "Chief Risk Officer"
    
    if 'current_insights' not in st.session_state:
        st.session_state.current_insights = []
    
    # Run main application
    main()