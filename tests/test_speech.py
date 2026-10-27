import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from pdf_to_audio.speech import SAMPLE_RATE, text_to_wav


class TextToWavTests(unittest.TestCase):
    def test_writes_kokoro_audio_chunks_to_wav(self) -> None:
        audio = [0.1, 0.2, 0.3]
        stream = MagicMock()
        sound_file = MagicMock()
        sound_file.return_value.__enter__.return_value = stream
        pipeline = MagicMock(return_value=[("texto", "fonemas", audio)])
        kokoro_module = SimpleNamespace(KPipeline=MagicMock(return_value=pipeline))
        soundfile_module = SimpleNamespace(SoundFile=sound_file)

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "nested" / "audio.wav"
            with patch.dict(
                sys.modules,
                {"kokoro": kokoro_module, "soundfile": soundfile_module},
            ):
                result = text_to_wav(
                    text="Ola",
                    output_path=output_path,
                    language="p",
                    voice="pf_dora",
                    speed=1.1,
                )

        self.assertEqual(result, output_path)
        kokoro_module.KPipeline.assert_called_once_with(lang_code="p")
        pipeline.assert_called_once_with("Ola", voice="pf_dora", speed=1.1)
        sound_file.assert_called_once_with(
            str(output_path),
            mode="w",
            samplerate=SAMPLE_RATE,
            channels=1,
            format="WAV",
        )
        stream.write.assert_called_once_with(audio)


if __name__ == "__main__":
    unittest.main()
