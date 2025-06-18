import os

os.environ["STREAMLIT_SERVER_ENABLE_FILE_WATCHER"] = "false"
os.makedirs("./offload", exist_ok=True)

import librosa
import streamlit as st
from pytubefix import YouTube


from config import BaseConfig as config
from src.audio_transcription import AudioTranscription
from src.utils import convert_to_wav
from src.core import create_session
from src.crud import create_audio, get_audio
from src.models import Audio

from src.models.data_types import AudioSource
from src.llm_summarize import TextSummarizer


# Konfiguracja aplikacji Streamlit
st.set_page_config(layout="wide")
st.title("🎧 Transkrypcja i Podsumowanie Audio")

session = create_session()

SAVE_DIR = config.DATA_DIR
TRANSCRIPTION_MODEL = config.AUDIO_TRANSCRIPTION_MODEL

for key in ["wav_path", "source", "url"]:
    if key not in st.session_state:
        st.session_state[key] = None

if not os.path.exists(SAVE_DIR):
    try:
        os.makedirs(SAVE_DIR)
        st.success(f"📁 Utworzono folder: {SAVE_DIR}")
    except Exception as e:
        st.error(f"❌ Nie udało się utworzyć folderu: {e}")

st.title("YouTube Audio Downloader lub własny plik")

uploaded_file = st.file_uploader(
    "📂 Dodaj plik audio z komputera (MP4, MP3 itp.)",
    type=["mp4", "mp3", "wav", "webm"],
)

url = st.text_input("🔗 Wklej link do YouTube (film max 5 minut):")

if uploaded_file:
    st.success("✅ Plik załadowany.")
    st.audio(uploaded_file)

    save_path = os.path.join(SAVE_DIR, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    wav_path = convert_to_wav(save_path)

    st.success(f"✅ Plik zapisany jako WAV: {wav_path}")
    st.audio(wav_path)
    st.download_button(
        label="📥 Pobierz ten plik WAV",
        data=open(wav_path, "rb").read(),
        file_name=os.path.basename(wav_path),
        mime="audio/wav",
    )

    st.session_state.wav_path = wav_path
    st.session_state.source = AudioSource.UPLOADED
    st.session_state.url = None

elif url:
    try:
        yt = YouTube(url)
        video_length = yt.length
        minutes = video_length // 60
        seconds = video_length % 60
        st.write(f"🎬 Film trwa: {minutes} minut i {seconds} sekund.")

        if video_length > 300:
            st.error("⛔ Film jest dłuższy niż 5 minut. Nie można pobrać.")
        else:
            if st.button("📥 Pobierz całe audio"):
                audio_stream = (
                    yt.streams.filter(only_audio=True).order_by("abr").desc().first()
                )
                safe_title = "".join(c for c in yt.title if c.isalnum() or c in " _-")[
                    :40
                ]
                save_path = os.path.join(SAVE_DIR, f"{safe_title}.mp4")

                audio_stream.download(
                    output_path=SAVE_DIR, filename=f"{safe_title}.mp4"
                )
                wav_path = convert_to_wav(save_path)

                st.success(f"✅ Gotowe! Plik zapisany jako WAV:\n`{wav_path}`")
                st.audio(wav_path)

                st.session_state.wav_path = wav_path
                st.session_state.source = AudioSource.YOUTUBE
                st.session_state.url = url

    except Exception as e:
        st.error(f"❌ Błąd: {e}")

if st.session_state.wav_path and os.path.exists(st.session_state.wav_path):
    if st.button("📝 Transkrybuj i streść ten plik audio"):
        try:
            audio_data, sr = librosa.load(
                st.session_state.wav_path, sr=16000, duration=None
            )
            transcription_oper = AudioTranscription(TRANSCRIPTION_MODEL)
            text = transcription_oper.text_transcription(audio_data, sr)

            summarizer = TextSummarizer()
            summary = summarizer.summarize(text)

            audio = Audio(
                title=os.path.basename(st.session_state.wav_path).split(".")[0],
                audio_source=st.session_state.source,
                audio_url=(
                    st.session_state.url
                    if st.session_state.source == AudioSource.YOUTUBE
                    else None
                ),
                transcription=text,
                summary=summary,
            )
            audio = create_audio(session, audio)

            st.success("📝 Transkrypcja zakończona pomyślnie!")
            col1, col2 = st.columns(2)

            audio = get_audio(session, audio.id)

            with col1:
                st.text_area("📜 Transkrypcja:", value=audio.transcription, height=400)

            with col2:
                st.text_area("📄 Podsumowanie:", value=audio.summary, height=400)
            st.success("📚 Podsumowanie gotowe!")

        except Exception as e:
            st.error(f"❌ Błąd podczas transkrypcji lub podsumowania: {e}")
            print("Error:\n\n", e, "\n\n")
