# Simple Dictation

This repository provides a very simple Python script for hands-free dictation. You run the script, it records your voice until you stop talking, and then it types out what you said.
I'm using it in my i3wm conf with a shortcut.

## How it Works

The script `transcribe.py` does the following:

1.  **Plays a sound:** It plays `speak.mp3` to let you know it has started recording.
2.  **Records audio:** It listens to your microphone and records what you say.
3.  **Detects silence:** When it detects a few seconds of silence, it stops recording.
4.  **Plays another sound:** It plays `transcribing.mp3` to let you know it is processing the audio.
5.  **Transcribes:** It uses OpenAI's Whisper model to convert your speech to text.
6.  **Types the text:** It simulates keyboard input to type the transcribed text into whatever application is currently in focus.

## Installation

To set up the necessary environment and install the required Python packages, simply run the installation script:

```bash
./install.sh
```

This will create a Python virtual environment in the `venv` directory and install all dependencies.

## Usage

To start the dictation script, run the following command:

```bash
./transcribe.sh
```

The script will immediately start listening for your voice.

## Configuration

You can customize the behavior of the script by modifying the following variables at the top of `transcribe.py`:

*   `SAMPLE_RATE`: The sample rate for the audio recording. Whisper requires 16kHz, so you probably want to leave this as is.
*   `CHANNELS`: The number of audio channels. `1` is for mono, `2` for stereo.
*   `SILENCE_THRESHOLD`: This determines how sensitive the silence detection is. A lower value means it will be more sensitive to background noise. You can adjust this value based on your microphone and environment.
*   `SILENCE_DURATION`: The number of seconds of silence to wait for before stopping the recording.
*   `MODEL`: The Whisper model to use for transcription. You can choose from `tiny`, `base`, `small`, `medium`, and `large`. Larger models are more accurate but slower and require more resources.
