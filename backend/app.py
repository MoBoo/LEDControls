from typing import Optional

from fastapi import FastAPI, status, Response
from fastapi.middleware.cors import CORSMiddleware

import asyncio
from collections import deque

from pydantic import BaseModel
from rpi_ws281x import PixelStrip, Color

app = FastAPI()
queue = deque()

# LED strip configuration:
LED_COUNT = 16  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
pip install fastapi uvicornLED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

LED_STRIP = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
LED_STRIP.begin()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def color_wipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        await asyncio.sleep(wait_ms / 1000.0)


async def theater_chase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            await asyncio.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


async def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        await asyncio.sleep(wait_ms / 1000.0)


async def rainbow_cycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        await asyncio.sleep(wait_ms / 1000.0)


async def theater_chase_rainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            await asyncio.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


async def set_led_brightness(strip, brightness: int):
    """Change brightness of led strip."""
    if not (0 < brightness <= 255):
        raise ValueError("Value for brightness must be between 0 and 255.")
    strip.setBrightness(brightness)
    strip.show()


async def led_control_loop(loop):
    task = None
    while True:
        try:
            fn = queue.pop()
            if task:
                task.cancel()
        except IndexError:
            await asyncio.sleep(1)
            continue
        task = loop.create_task(fn)


class ChangeBrightnessRequest(BaseModel):
    value: int


class ChangePatternRequest(BaseModel):
    pattern: str
    color: Optional[str] = None


def color_from_string(hex_string: str) -> Color:
    if hex_string.startswith("#"):
        hex_string = hex_string[1:]
    r, g, b = tuple(int(hex_string[i:i + 2], 16) for i in (0, 2, 4))
    return Color(red=r, green=g, blue=b)


@app.post("/pattern")
async def post_pattern(data: ChangePatternRequest):
    if data.pattern == "solid":
        color = color_from_string(data.color)
        queue.append(color_wipe(LED_STRIP, color, 10))
    elif data.pattern == "rainbow":
        queue.append(rainbow(LED_STRIP))
    elif data.pattern == "rainbow_cycle":
        queue.append(rainbow_cycle(LED_STRIP))
    elif data.pattern == "theater_chase":
        color = color_from_string(data.color)
        queue.append(theater_chase(LED_STRIP, color))
    elif data.pattern == "theater_chase_rainbow":
        queue.append(theater_chase_rainbow(LED_STRIP))
    else:
        return Response(content="Pattern unknown.", status_code=status.HTTP_400_BAD_REQUEST)

    return Response(status_code=status.HTTP_200_OK)


@app.post("/brightness")
async def post_brightness(data: ChangeBrightnessRequest):
    queue.append(set_led_brightness(LED_STRIP, data.value))
    return Response(status_code=status.HTTP_200_OK)


if __name__ == "__main__":
    import uvicorn

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    uvicorn_config = uvicorn.Config(app, loop=loop, host="0.0.0.0")
    uvicorn_server = uvicorn.Server(uvicorn_config)

    loop.create_task(led_control_loop(loop))
    loop.run_until_complete(uvicorn_server.serve())
