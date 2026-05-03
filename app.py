import streamlit as st
import youtube_transcript_api  # Simple import
from groq import Groq

# 1. Setup
st.set_page_config(page_title="AI Video Summarizer", page_icon="📹")
st.title("📹 YouTube Video Summarizer")

# 2. Inputs
video_url = st.text_input("1. Paste YouTube URL:")
api_key = st.text_input("2. Enter your Groq API Key:", type="password")

def extract_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return url.split("/")[-1].split("?")[0]

# 3. Main Logic
if st.button("Generate Summary"):
    if not video_url or not api_key:
        st.warning("Please provide both the URL and API Key.")
    else:
        try:
            with st.spinner("Fetching transcript..."):
                v_id = extract_id(video_url)
                
                # --- THIS IS THE FIX ---
                # We call: library.ClassName.function()
                data = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(v_id)
                full_text = " ".join([item['text'] for item in data])
            
            with st.spinner("AI is summarizing..."):
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Summarize this into 5 bullet points."},
                        {"role": "user", "content": full_text}
                    ],
                    model="llama3-8b-8192",
                )
                st.subheader("Summary:")
                st.write(response.choices[0].message.content)
                st.success("Done!")

        except Exception as e:
            st.error(f"Error: {e}")
