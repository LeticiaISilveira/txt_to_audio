import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pdf_to_audio import cli
from pdf_to_audio.speech import VOICE_TEST_PHRASES


class VoiceTestCliTests(unittest.TestCase):
    def test_generates_and_plays_default_portuguese_voice_test(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "voice-test.wav"
            with (
                patch.object(
                    sys,
                    "argv",
                    ["pdf-to-audio", "--test-voice", "--output", str(output_path)],
                ),
                patch.object(cli, "text_to_wav") as text_to_wav,
                patch.object(cli, "play_wav") as play_wav,
            ):
                cli.main()

        text_to_wav.assert_called_once_with(
            text=VOICE_TEST_PHRASES["p"],
            output_path=output_path,
            language="p",
            voice="pf_dora",
            speed=1.0,
        )
        play_wav.assert_called_once_with(output_path)


if __name__ == "__main__":
    unittest.main()
