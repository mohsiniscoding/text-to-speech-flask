## run this file first if you are setting up flask for first time
from ruth_tts_transformer.api import TTS
tts = TTS()
tts.generate("You guys are bunch of care takers!")
file_name = tts.parse() + ".wav"