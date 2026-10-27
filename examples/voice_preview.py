from pathlib import Path

from pdf_to_audio.speech import text_to_wav


VOICE_SAMPLES = {
    "af_heart": "Which voice do you prefer? This is the first voice from my test.",
    "am_eric": "Or do you prefer this one? This is the second voice from my test.",
    "am_puck": "Or maybe this one? This is the third voice from my test.",
    "af_nicole": "Or finally this one? This is the last voice from my test.",
}


def main() -> None:
    output_dir = Path("voice_samples")
    for voice, text in VOICE_SAMPLES.items():
        output_path = output_dir / f"{voice}.wav"
        text_to_wav(
            text=text,
            output_path=output_path,
            language="a",
            voice=voice,
            speed=1.1,
        )
        print(f"Amostra gerada: {output_path}")


if __name__ == "__main__":
    main()
