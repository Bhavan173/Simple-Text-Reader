import edge_tts
import asyncio
from io import BytesIO

voices = {
           'William':'en-AU-WilliamMultilingualNeural',
           'Neerja':'en-IN-NeerjaExpressiveNeural',
           'Ava':'en-US-AvaNeural',
           'Christopher':'en-US-ChristopherNeural',
           'Michelle':'en-US-MichelleNeural'
    }

async def speech(text,voice):
    unwanted_symbols = "***>"
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.translate(str.maketrans('', '', unwanted_symbols))

    #output = "Test.mp3"
    audio_buffer = BytesIO()
    print(f"Generating speech with {voice}")
    voice = voices[voice]
    comm = edge_tts.Communicate(text,voice = voice)
    # await(comm.save(output))
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            audio_buffer.write(chunk['data'])
    audio_buffer.seek(0)
    return audio_buffer

