import shutil
import subprocess
import sys
from pathlib import Path


SAMPLE_RATE = 24_000
VOICE_TEST_PHRASES = {
    "p": "Olá! Esta é uma frase de teste para verificar a voz selecionada.",
    "a": "Hello! This is a short test to check the selected voice.",
}


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


def play_wav(audio_path: Path) -> None:
    """Reproduz um WAV usando o player de audio disponivel no sistema."""
    if sys.platform == "win32":
        import winsound

        winsound.PlaySound(str(audio_path), winsound.SND_FILENAME)
        return

    players = {
        "darwin": ("afplay",),
        "linux": ("aplay", "paplay"),
    }
    candidates = players.get(sys.platform)
    if candidates is None:
        raise RuntimeError(f"Reproducao de audio nao suportada em {sys.platform}.")

    player = next((shutil.which(candidate) for candidate in candidates if shutil.which(candidate)), None)
    if player is None:
        names = " ou ".join(candidates)
        raise RuntimeError(
            f"Nenhum reprodutor de audio encontrado. Instale ou disponibilize {names}."
        )

    try:
        subprocess.run([player, str(audio_path)], check=True)
    except subprocess.CalledProcessError as error:
        raise RuntimeError(f"Nao foi possivel reproduzir {audio_path}.") from error
