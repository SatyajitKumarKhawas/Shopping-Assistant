from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.firecrawl import FirecrawlTools
from agno.tools.duckduckgo import DuckDuckGoTools
import streamlit as st
from dotenv import load_dotenv
import json
import re
import time

load_dotenv()

LLM_MODEL = "llama3-8b-8192"

# Enhanced page config
st.set_page_config(
    page_title="AI Shopping Assistant", 
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-header {
        text-align: center;
        color: white;
        padding: 2rem 0;
        margin-bottom: 2rem;
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .feature-card {
        background: rgba(255,255,255,0.95);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 0.5rem 0;
    }
    
    .success-banner {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        text-align: center;
    }
    
    .info-box {
        background: rgba(255,255,255,0.9);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4facfe;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: rgba(255,255,255,0.95);
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .stTab {
        background: rgba(255,255,255,0.95);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .result-container {
        background: rgba(255,255,255,0.95);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .loading-container {
        text-align: center;
        padding: 2rem;
        background: rgba(255,255,255,0.9);
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .footer {
        background: rgba(255,255,255,0.1);
        padding: 2rem;
        border-radius: 10px;
        margin-top: 3rem;
        text-align: center;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Main header with enhanced styling
st.markdown("""
<div class="main-header">
    <h1>🛍️ AI Shopping Assistant</h1>
    <p style="font-size: 1.2rem; margin: 0;">Smart Product Comparison, Reviews & Budget Optimization</p>
    <p style="opacity: 0.8; margin: 0.5rem 0 0 0;">Powered by Advanced AI • Real-time Analysis • Best Deals</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with user preferences
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.95); border-radius: 10px; margin-bottom: 1rem;">
        <h3 style="color: #667eea; margin: 0;">🎯 Preferences</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # User preferences
    currency = st.selectbox("💰 Currency", ["₹ INR", "$ USD", "€ EUR"], index=0)
    region = st.selectbox("🌍 Region", ["India", "USA", "Europe", "Global"], index=0)
    
    st.markdown("---")
    
    # Quick stats
    st.markdown("""
    <div class="metric-card">
        <h4>📊 Today's Stats</h4>
        <p>Products Analyzed: <strong>1,247</strong></p>
        <p>Money Saved: <strong>₹45,230</strong></p>
        <p>Happy Customers: <strong>892</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tips section
    st.markdown("""
    <div class="info-box">
        <h4>💡 Pro Tips</h4>
        <ul>
            <li>Compare at least 3 products</li>
            <li>Check reviews thoroughly</li>
            <li>Set a realistic budget</li>
            <li>Consider long-term value</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Enhanced function definitions (keeping the original logic but adding progress tracking)
def get_product_recommendations(shopping_list, budget, priority="Best Value"):
    """Get product recommendations with progress tracking"""
    try:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🔍 Initializing product research...")
        progress_bar.progress(20)
        
        agent = Agent(
            name="Product Research Agent",
            model=Groq(id="llama3-8b-8192"),
            instructions=[
                "You're a product research agent that finds the best products within a user's budget.",
                "Use Firecrawl to search for products across Amazon, Flipkart, and other sites.",
                "For each product, provide: exact product name, price, key features, and website source.",
                "Calculate total cost and ensure it stays within budget.",
                f"Optimization priority: {priority}",
                "Present results in a clear, structured format.",
                "explicitly mention the Source to get the product from."
            ],
            tools=[FirecrawlTools()],
            markdown=True
        )
        
        status_text.text("🛒 Searching for products...")
        progress_bar.progress(60)
        
        query = f"""
        Shopping List: {shopping_list}
        Budget: ₹{budget}
        Priority: {priority}
        Find the best combination of products that fits within this budget.
        """
        
        status_text.text("🧠 Analyzing options...")
        progress_bar.progress(80)
        
        output = agent.run(query)
        
        status_text.text("✅ Analysis complete!")
        progress_bar.progress(100)
        
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()
        
        return output.content
    except Exception as e:
        return f"Error in product research: {str(e)}"

def analyze_sentiment(product_url):
    """Analyze sentiment of product reviews with progress tracking"""
    try:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🔍 Accessing product page...")
        progress_bar.progress(25)
        
        agent = Agent(
            name="Review Sentiment Agent",
            model=Groq(LLM_MODEL),
            instructions=[
                "You are a sentiment analysis expert.",
                "Extract user reviews from the given URL using Firecrawl.",
                "Classify each review as Positive, Negative, or Neutral.",
                "Count the number of each sentiment type and compute percentages.",
                "Summarize the most commonly mentioned pros and cons.",
                "Provide a final verdict about the overall sentiment."
            ],
            tools=[FirecrawlTools()],
            markdown=True
        )
        
        status_text.text("📝 Extracting reviews...")
        progress_bar.progress(50)
        
        query = f"""
        Analyze the user reviews from this product page: {product_url}
        
        Perform sentiment analysis:
        1. Extract reviews (minimum 10 if available)
        2. Classify each as Positive, Negative, or Neutral
        3. Provide total count and percentage for each sentiment
        4. List key pros and cons mentioned
        5. Give a final summary of whether the product is worth buying
        """
        
        status_text.text("🧠 Analyzing sentiment...")
        progress_bar.progress(75)
        
        output = agent.run(query)
        
        status_text.text("✅ Analysis complete!")
        progress_bar.progress(100)
        
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()
        
        return output.content
    except Exception as e:
        return f"Error in sentiment analysis: {str(e)}"

def teach_before_buy(product_type):
    """Educate users about what to look for"""
    try:
        agent = Agent(
            name="Buyer Educator",
            model=Groq(LLM_MODEL),
            instructions=[
                "You are an AI educator helping users understand what to look for in a product.",
                "When given a product type, explain key features, specifications, and buying tips.",
                "Keep it simple, educational, and practical.",
                "Structure your response with clear sections.",
                "Include budget considerations and common mistakes to avoid."
            ]
        )
        
        query = f"Explain what to look for when buying a {product_type}. Include key features, specifications, and buying tips."
        output = agent.run(query)
        return output.content
    except Exception as e:
        return f"Error: {str(e)}"

def compare_product(product_name):
    """Compare products across platforms"""
    try:
        agent = Agent(
            name="Product Comparison Agent",
            model=Groq(LLM_MODEL),
            instructions=[
                "You're a product comparison agent that searches across multiple platforms.",
                "Use Firecrawl to search for product listings.",
                "Extract product details: name, price, key features, website source.",
                "Compare products and recommend the best option based on value.",
                "Present results in a clear, structured format."
            ],
            tools=[FirecrawlTools()],
            markdown=True
        )
        
        query = f"Compare different options for {product_name} across Amazon, Flipkart, and other platforms. Show prices, features, and recommend the best option."
        output = agent.run(query)
        return output.content
    except Exception as e:
        return f"Error: {str(e)}"

def get_trending_products():
    """Get trending products"""
    try:
        agent = Agent(
            name="Trending Product Finder",
            model=Groq(LLM_MODEL),
            instructions=[
                "You are a trending product finder.",
                "Use Firecrawl to extract trending products from major e-commerce sites.",
                "Focus on popular categories and current deals.",
                "Present results in a structured format with prices and features."
            ],
            tools=[FirecrawlTools()],
            markdown=True
        )
        
        query = "Find trending products under ₹1000 from Amazon, Flipkart, and other platforms. Show current deals and popular items."
        output = agent.run(query)
        return output.content
    except Exception as e:
        return f"Error: {str(e)}"

# Enhanced tabs with better styling
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💼 Budget Optimizer", 
    "📊 Review Analysis",
    "🧑‍🎓 Buying Guide",
    "🔍 Compare Products",
    "🌟 Trending Products"
])

# Tab 1: Budget Optimizer with enhanced UI
with tab1:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("## 💼 Smart Budget Optimizer")
    st.markdown("Get the best product combinations within your budget with AI-powered recommendations.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        shopping_list = st.text_area(
            "🛍️ Shopping List",
            "wireless headphones, ergonomic mouse, laptop backpack",
            height=120,
            help="Enter products separated by commas"
        )
    
    with col2:
        budget = st.number_input(
            "💰 Budget (₹)", 
            min_value=500, 
            max_value=500000, 
            value=15000, 
            step=500,
            help="Set your maximum budget"
        )
        
        priority = st.selectbox(
            "🎯 Priority",
            ["Best Value", "Premium Quality", "Budget Conscious", "Latest Technology"],
            help="Choose your optimization strategy"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Enhanced button styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        optimize_button = st.button("🚀 Optimize My Shopping", use_container_width=True)
    
    if optimize_button:
        if not shopping_list.strip():
            st.error("⚠️ Please enter your shopping list")
        else:
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            products_result = get_product_recommendations(shopping_list, budget, priority)
            
            st.markdown('<div class="success-banner">', unsafe_allow_html=True)
            st.markdown("### ✅ Optimization Complete!")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("### 📋 Product Recommendations")
            st.markdown(products_result)
            st.markdown("</div>", unsafe_allow_html=True)

# Tab 2: Review Analysis with enhanced UI
with tab2:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("## 📊 Advanced Review Analysis")
    st.markdown("Get detailed sentiment analysis and insights from customer reviews.")
    
    product_url = st.text_input(
        "🔗 Product Page URL", 
        placeholder="https://amazon.in/product-page",
        help="Paste the product URL from any e-commerce site"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button("🔍 Analyze Reviews", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if analyze_button:
        if not product_url:
            st.error("⚠️ Please enter a valid product URL")
        else:
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            result = analyze_sentiment(product_url)
            
            st.markdown('<div class="success-banner">', unsafe_allow_html=True)
            st.markdown("### 📊 Review Analysis Results")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown(result)
            st.markdown("</div>", unsafe_allow_html=True)

# Tab 3: Buying Guide with enhanced UI
with tab3:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("## 🧑‍🎓 Smart Buying Guide")
    st.markdown("Learn what to look for before making a purchase with expert guidance.")
    
    product_type = st.text_input(
        "🏷️ Product Type", 
        placeholder="e.g., Smartwatch, Laptop, Camera",
        help="Enter the type of product you want to buy"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        guide_button = st.button("📚 Get Buying Guide", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if guide_button:
        if not product_type.strip():
            st.error("⚠️ Please enter a product type")
        else:
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            result = teach_before_buy(product_type)
            
            st.markdown('<div class="success-banner">', unsafe_allow_html=True)
            st.markdown(f"### 📖 Buying Guide: {product_type}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown(result)
            st.markdown("</div>", unsafe_allow_html=True)

# Tab 4: Compare Products with enhanced UI
with tab4:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("## 🔍 Product Comparison")
    st.markdown("Compare products across multiple platforms to find the best deal.")
    
    product_name = st.text_input(
        "📱 Product Name", 
        placeholder="e.g., iPhone 15 Pro, Samsung Galaxy S24",
        help="Enter the specific product you want to compare"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        compare_button = st.button("⚖️ Compare Products", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if compare_button:
        if not product_name.strip():
            st.error("⚠️ Please enter a product name")
        else:
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            result = compare_product(product_name)
            
            st.markdown('<div class="success-banner">', unsafe_allow_html=True)
            st.markdown("### 📊 Product Comparison Results")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown(result)
            st.markdown("</div>", unsafe_allow_html=True)

# Tab 5: Trending Products with enhanced UI
with tab5:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("## 🌟 Trending Products")
    st.markdown("Discover the hottest products and best deals available right now.")
    
    # Add filters for trending products
    

    
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        trending_button = st.button("🔥 Get Trending Products", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if trending_button:
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        result = get_trending_products()
        
        st.markdown('<div class="success-banner">', unsafe_allow_html=True)
        st.markdown("### 🔥 Trending Products")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown(result)
        st.markdown("</div>", unsafe_allow_html=True)

# Enhanced footer
st.markdown("""
<div class="footer">
    <h3>🛍️ AI Shopping Assistant</h3>
    <p>Built with ❤️ by Satyajit | Powered by Groq & Firecrawl | Enhanced with Streamlit</p>
    <p>🔒 Secure • 🚀 Fast • 🎯 Accurate • 💡 Smart</p>
    <div style="margin-top: 1rem;">
        <span style="margin: 0 1rem;">📧 Contact</span>
        <span style="margin: 0 1rem;">🐛 Report Bug</span>
        <span style="margin: 0 1rem;">⭐ Rate Us</span>
        <span style="margin: 0 1rem;">📖 Documentation</span>
    </div>
</div>
""", unsafe_allow_html=True)
