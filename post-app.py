import os
import streamlit as st
import google.generativeai as genai

# Configure the API key directly
google_api_key = st.secrets["google_api_key"]

# Set up the model
generation_config = {
    "temperature": 0.7,  # Adjust for more or less creativity
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 400,  # Adjust as needed for social media post length
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="""
    You are an AI content creator specialized in producing high-quality, engaging social media posts for various industries. When a user selects an industry and provides a topic, your task is to create a compelling post tailored to that field. Your output should reflect the following guidelines:

    Start with a captivating hook that draws the reader in and sets the tone for the post.
    Use a friendly, conversational tone that balances professionalism and approachability.
    Include emojis to add personality and visual interest, enhancing readability.
    Incorporate bullet points or short sections to structure content clearly and make it easy to scan.
    End with a call-to-action or a prompt for engagement, such as a question or invitation to comment.
    Conclude with relevant hashtags to increase discoverability and reach.
    Your goal is to create posts that are not just informative but resonate with readers, encouraging them to engage, share, and take action. The content should sound authentic, align with current trends, and demonstrate thought leadership in the chosen industry.


    """,
)

# Streamlit UI
st.title("💡Expertise-Driven Content Bot")

st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #a63187;  /* Change this to your desired background color */
    }
    .sidebar .sidebar-content {
        background-color: #a63187;  /* Change this to match the main background */
    }
    .sidebar .sidebar-content .stInfo {
        background-color: #a63187;  /* Custom background color for the info box */
        padding: 10px;  /* Add padding for a better look */
        border-radius: 5px;  /* Rounded corners */
    }
    .sidebar .sidebar-content {
        background-color: #f0f4f8;  /* Change this to match the main background */
    }
    .stButton>button {
        background-color: #a63187;  /* Button background color */
        color: white;  /* Button text color */
        border: none;  /* Remove border */
        border-radius: 8px;  /* Rounded corners */
        padding: 10px 20px;  /* Padding inside button */
        font-size: 16px;  /* Font size */
        transition: background-color 0.3s;  /* Smooth transition for hover effect */
    }
    .stButton>button:hover {
        background-color: #591048;  /* Darker color on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("About This App")
st.sidebar.info(
    """
    This app generates engaging social media posts tailored to specific industries. 

    **Features:**
    - Select an industry from the dropdown.
    - Enter a specific topic to create a relevant post.
    - Get creative, high-quality content generated in seconds.

    **Industries Supported:**
    - AI Engineer
    - SEO Expert
    - Data Scientist
    - Web Developer
    - Marketing & Advertising
    - Machine Learning
    - Natural Language Processing (NLP)

    **How to Use:**
    1. Choose an industry.
    2. Enter a topic.
    3. Click "Generate Expert Post" to see your post!
    """
)
# Dropdown for selecting industry
industry = st.selectbox("Select an industry:", ["AI Engineer", "SEO Expert", "Data Scientist", "Web Developer","Marketing & Advertising","Machine Learning","Natural Language Processing (NLP)"])

# Text input for the topic
topic = st.text_input("Enter a specific topic you want to create a post about:")

# Button to generate the post
if st.button("Generate Post"):
    if industry and topic:
        with st.spinner("Generating content..."):
            # Start a new chat session
            chat_session = model.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": [
                            f"Industry: {industry}\nTopic: {topic}\nCreate a social media post."
                        ],
                    }
                ]
            )
            
            # Send the request and get a response
            response = chat_session.send_message("Create a post")
            
            # Display the generated post
            st.subheader("Generated Post:")
            st.write(response.text)
    else:
        st.warning("Please select an industry and enter a topic.")
