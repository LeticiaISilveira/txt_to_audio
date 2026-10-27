from pathlib import Path


SAMPLE_RATE = 24_000


def text_to_wav(
    text: str,
    output_path: Path,
    language: str = "p",
    voice: str = "pf_dora",
    speed: float = 1.0,
) -> Path:
    """Gera um WAV usando Kokoro e retorna o caminho do arquivo criado."""
    from kokoro import KPipeline
    import soundfile as sf

    output_path.parent.mkdir(parents=True, exist_ok=True)
    pipeline = KPipeline(lang_code=language)
    audio_chunks = pipeline(text, voice=voice, speed=speed)

    with sf.SoundFile(
        str(output_path),
        mode="w",
        samplerate=SAMPLE_RATE,
        channels=1,
        format="WAV",
    ) as output_file:
        wrote_audio = False
        for _, _, audio in audio_chunks:
            output_file.write(audio)
            wrote_audio = True

    if not wrote_audio:
        output_path.unlink(missing_ok=True)
        raise RuntimeError("O Kokoro nao gerou nenhum trecho de audio.")

    return output_path
