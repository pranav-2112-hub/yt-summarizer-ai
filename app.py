import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from groq import Groq

# Page Setup
st.set_page_config(page_title="AI Video Summarizer", page_icon="📝")
st.title("📹 YouTube Video Summarizer")
st.markdown("Summarize any YouTube video using AI (Llama 3).")

# Input Fields
video_url = st.text_input("1. Paste YouTube URL:")
api_key = st.text_input("2. Enter Groq API Key:", type="password")

def extract_video_id(url):
    """Helper to get the ID from various YouTube URL formats"""
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        return url.split("/")[-1]

def get_summary(text, key):
    """Sends transcript to Groq AI for processing"""
    client = Groq(api_key=key)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes YouTube videos into clear bullet points."
            },
            {
                "role": "user",
                "content": f"Please summarize this transcript: {text}",
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

# Main App Button
if st.button("Generate Summary"):
    if not video_url or not api_key:
        st.warning("Please provide both a URL and your API Key.")
    else:
        try:
            with st.spinner("Extracting transcript..."):
                v_id = extract_video_id(video_url)
                # Correct function call: YouTubeTranscriptApi.get_transcript(v_id)
                transcript_data = YouTubeTranscriptApi.get_transcript(v_id)
                full_text = " ".join([item['text'] for item in transcript_data])
            
            with st.spinner("AI is thinking..."):
                summary = get_summary(full_text, api_key)
                st.subheader("Results:")
                st.success("Summary Generated!")
                st.write(summary)
                
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.info("Tip: Make sure the video has 'Captions' or 'Subtitles' enabled on YouTube.")
