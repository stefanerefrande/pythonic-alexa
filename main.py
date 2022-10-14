import pyaudio
import structlog as structlog
import websockets
import asyncio
import base64
import json
from helper import ask_computer


logger = structlog.get_logger(__name__)

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# AssemblyAI API info
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
auth_key = "auth_key"


class PythonicAlexa:

    def websocket_connection(self):
        return websockets.connect(
            URL,
            extra_headers=(("Authorization", auth_key),),
            ping_interval=5,
            ping_timeout=20
        )

    def check_audio_connection(self):
        audio = pyaudio.PyAudio()
        recording = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER
        )
        logger.info(
            "Receiving default input device information:",
            audio.get_default_input_device_info()
        )
        return recording

    async def set_messages(self):
        logger.info(f'Connecting websocket to url ${URL}')
        websocket = self.websocket_connection

        async with websocket:
            await asyncio.sleep(0.1)
            logger.info("Starting session...")
            session_beginning = await websocket.recv()
            logger.info("Sending messages ...", session_beginning)

    async def send_messages(self):
        connection = self.connect_audio()
        websocket = self.websocket_connection()
        while True:
            try:
                data = connection.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                data = base64.b64encode(data).decode("utf-8")
                json_data = json.dumps({"audio_data": str(data)})
                await websocket.send(json_data)

            except websockets.exceptions.ConnectionClosedError as error:
                print(error)
                assert error.code == 4008
                break
            await asyncio.sleep(0.01)
        return True

    async def receive_messages(self):
        websocket = self.websocket_connection()
        while True:
            try:
                result_str = await websocket.recv()
                result = json.loads(result_str)
                prompt = result['text']

                if prompt and result['message_type'] == 'FinalTranscript':
                    logger.info("User:", prompt)

                    answer = ask_computer(prompt)
                    logger.info("Pythonic Alexa:", answer)

            except websockets.exceptions.ConnectionClosedError as error:
                print(error)
                assert error.code == 4008
                break
    send_result, receive_result = await asyncio.gather(send_messages(), receive_messages())

    asyncio.run(send_messages())
    asyncio.run(receive_messages())
