import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi as yts
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="AI Video Summarizer", page_icon="📝")
st.title("📹 YouTube Video Summarizer")

# 2. Input Fields
video_url = st.text_input("1. Paste YouTube URL:", placeholder="https://youtu.be/...")
# Pro-tip: Keep your new API key private!
api_key = st.text_input("2. Enter your NEW Groq API Key:", type="password")

def extract_video_id(url):
    """Handles standard, mobile, and shared YouTube links"""
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        return url.split("/")[-1].split("?")[0]

# 3. Main Logic
if st.button("Generate Summary"):
    if not video_url or not api_key:
        st.warning("Please enter both the URL and your API Key.")
    else:
        try:
            with st.spinner("Fetching transcript from YouTube..."):
                v_id = extract_video_id(video_url)
                
                # Using 'yts' prevents the 'no attribute' error you saw
                transcript_data = yts.get_transcript(v_id)
                full_text = " ".join([item['text'] for item in transcript_data])
            
            with st.spinner("AI is summarizing..."):
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Summarize this technical transcript into 5 clear bullet points."},
                        {"role": "user", "content": full_text}
                    ],
                    model="llama3-8b-8192",
                )
                
                st.subheader("Video Summary:")
                st.write(response.choices[0].message.content)
                st.success("Done!")

        except Exception as e:
            # This captures the specific error if it happens again
            st.error(f"Error Details: {e}")
            st.info("Check if the video has 'Captions' enabled in YouTube settings.")
