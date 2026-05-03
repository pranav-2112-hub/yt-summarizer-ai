import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="AI Video Summarizer", page_icon="📝")

st.title("📹 YouTube Video Summarizer")
st.markdown("Summarize any YouTube video using AI. **Zero local memory used!**")

# 2. Sidebar for API Key (Keeping it organized)
with st.sidebar:
    st.title("Settings")
    groq_api_key = st.text_input("Enter Groq API Key:", type="password")
    st.info("Get your free key at console.groq.com")

# 3. User Input
video_url = st.text_input("Paste YouTube Video URL:")

# 4. Logic to extract Transcript
def get_transcript(url):
    try:
        # Extract the video ID from the URL (the part after v=)
        video_id = url.split("v=")[-1].split("&")[0]
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        # Join all pieces of text into one long string
        full_text = " ".join([item['text'] for item in transcript_data])
        return full_text
    except Exception as e:
        return f"Error: Could not get transcript. (Check if captions are enabled on the video)"

# 5. Execution Button
if st.button("Generate Summary"):
    if not groq_api_key:
        st.warning("Please enter your Groq API Key in the sidebar!")
    elif not video_url:
        st.warning("Please paste a YouTube URL!")
    else:
        with st.spinner("Processing video content..."):
            # Get the text
            transcript = get_transcript(video_url)
            
            if "Error:" in transcript:
                st.error(transcript)
            else:
                # Send text to Groq Cloud AI
                try:
                    client = Groq(api_key=groq_api_key)
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a helpful assistant that summarizes YouTube videos into clear bullet points."
                            },
                            {
                                "role": "user",
                                "content": f"Please summarize this video transcript: {transcript}"
                            }
                        ],
                        model="llama3-8b-8192", # Using the fast Llama 3 model
                    )
                    
                    # Display the Result
                    st.success("Summary Ready!")
                    st.markdown("---")
                    st.write(chat_completion.choices[0].message.content)
                    
                except Exception as ai_err:
                    st.error(f"AI Error: {ai_err}")
