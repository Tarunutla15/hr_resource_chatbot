# # frontend/streamlit_app.py
# import streamlit as st
# import requests

# API_URL = "http://127.0.0.1:8000"

# st.set_page_config(page_title="HR Assistant Demo", layout="centered")
# st.title("🔎 HR Resource Query Chatbot (Demo)")

# query = st.text_input("Enter an HR query:", value="Find Python developers with 3+ years experience in healthcare")
# top_k = st.slider("Number of candidates to retrieve", min_value=1, max_value=5, value=3)

# if st.button("Search"):
#     with st.spinner("Querying backend..."):
#         payload = {"query": query, "top_k": top_k}
#         try:
#             r = requests.post(f"{API_URL}/chat/", json=payload, timeout=30)
#             r.raise_for_status()
#             data = r.json()
#             st.markdown("### Chatbot response")
#             st.write(data.get("answer"))
#             st.markdown("### Candidates (structured)")
#             for c in data.get("candidates", []):
#                 emp = c["employee"]
#                 st.write(f"**{emp['name']}** — {emp.get('role','')} ({emp.get('experience_years')} yrs) — {emp.get('availability')}")
#                 st.write("Skills: " + ", ".join(emp.get("skills", [])))
#                 st.write("Projects: " + ", ".join(emp.get("projects", [])))
#                 st.write("---")
#         except Exception as exc:
#             st.error(f"Request failed: {exc}")

# frontend/streamlit_app.py
import streamlit as st
import requests
import time

# Configuration
API_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="HR Resource Chatbot", layout="wide", page_icon="🔎")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .candidate-card {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        background-color: #f8f9fa;
    }
    .availability-available {
        color: #28a745;
        font-weight: bold;
    }
    .availability-busy {
        color: #dc3545;
        font-weight: bold;
    }
    .availability-on_notice {
        color: #ffc107;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">🔎 HR Resource Query Chatbot</h1>', unsafe_allow_html=True)
    
    # Sidebar for settings and examples
    with st.sidebar:
        st.header("ℹ️ How to Use")
        st.write("""
        Enter natural language queries like:
        - "Find Python developers with 3+ years experience"
        - "Who has worked on healthcare projects?"
        - "React Native developers available now"
        - "People with AWS and Docker experience"
        """)
        
        st.header("⚙️ Settings")
        top_k = st.slider("Number of candidates to show", min_value=1, max_value=10, value=5)
        
        st.header("📋 Example Queries")
        example_queries = [
            "Find Python developers with 3+ years experience",
            "Who knows React and AWS?",
            "ML engineers with healthcare experience",
            "Available developers with Docker knowledge",
            "People who worked on chatbot projects"
        ]
        
        for example in example_queries:
            if st.button(example, key=example):
                st.session_state.query_input = example

    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Initialize session state for query input
        if 'query_input' not in st.session_state:
            st.session_state.query_input = "Find Python developers with 3+ years experience"
        
        query = st.text_input(
            "Enter your HR query:",
            value=st.session_state.query_input,
            placeholder="e.g., Find developers with Python and AWS experience",
            key="query_input"
        )
        
        if st.button("🔍 Search", type="primary", use_container_width=True):
            if not query.strip():
                st.warning("Please enter a query first!")
            else:
                with st.spinner("🔍 Searching for the best candidates..."):
                    try:
                        payload = {"query": query, "top_k": top_k}
                        start_time = time.time()
                        
                        r = requests.post(f"{API_URL}/chat/", json=payload, timeout=30)
                        r.raise_for_status()
                        data = r.json()
                        
                        response_time = time.time() - start_time
                        
                        # Display results
                        st.success(f"Found {len(data.get('candidates', []))} candidates in {response_time:.2f}s")
                        
                        # Chatbot response
                        st.markdown("### 💬 Chatbot Response")
                        st.write(data.get("answer", "No response generated."))
                        
                        # Structured candidate results
                        st.markdown("### 👥 Matching Candidates")
                        
                        if not data.get("candidates"):
                            st.info("No candidates found matching your criteria.")
                        else:
                            for i, c in enumerate(data.get("candidates", [])):
                                emp = c["employee"]
                                score = c.get("score", 0)
                                
                                # Availability styling
                                availability = emp.get("availability", "").lower()
                                if availability == "available":
                                    avail_class = "availability-available"
                                elif availability == "busy":
                                    avail_class = "availability-busy"
                                elif availability == "on_notice":
                                    avail_class = "availability-on_notice"
                                else:
                                    avail_class = ""
                                
                                with st.container():
                                    st.markdown(f'<div class="candidate-card">', unsafe_allow_html=True)
                                    
                                    col_a, col_b = st.columns([3, 1])
                                    with col_a:
                                        st.markdown(f"**{emp['name']}**")
                                        st.write(f"*{emp.get('role', 'No role specified')}*")
                                    with col_b:
                                        st.markdown(f"<span class='{avail_class}'>{availability.upper()}</span>", 
                                                   unsafe_allow_html=True)
                                        st.write(f"Score: {score:.3f}")
                                    
                                    st.write(f"**Experience:** {emp.get('experience_years', 'N/A')} years")
                                    
                                    st.write("**Skills:** " + ", ".join(emp.get("skills", [])))
                                    st.write("**Projects:** " + ", ".join(emp.get("projects", [])))
                                    
                                    if emp.get("notes"):
                                        st.write(f"**Notes:** {emp.get('notes')}")
                                    
                                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Connection error: {e}")
                        st.info("Make sure the backend server is running on http://127.0.0.1:8000")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.markdown("### 📊 Quick Stats")
        st.info("""
        **Dataset Info:**
        - 16+ employees
        - Various tech roles
        - Skills tracking
        - Availability status
        """)
        
        st.markdown("### 🎯 Search Tips")
        st.write("""
        - Use specific skills: "Python", "React", "AWS"
        - Mention experience: "3+ years", "senior"
        - Reference projects: "healthcare", "e-commerce"
        - Check availability: "available now", "not busy"
        """)

if __name__ == "__main__":
    main()