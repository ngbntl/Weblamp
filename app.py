import asyncio
import websockets
import json
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
connected = set()
# LED
LED_PINS = [2, 3, 4]
LED_STATE = [0, 0, 0]
COLORS = ['red', 'green', 'blue']

for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    
def get_led_state():
    led_state = {}
    for i in range(len(COLORS)):
        led_state[COLORS[i]] = LED_STATE[i]
    return led_state

async def server(websocket, path):
    # Register.
    connected.add(websocket)
    print(f"Client connected: {websocket.remote_address}")
    try:
        await websocket.send(json.dumps(get_led_state()))
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            color = data.get('color', None)
            if color is None:
                continue
            state = 1 if data['state'] == 1 else 0
            index = COLORS.index(color)
            LED_STATE[index] = state
            GPIO.output(LED_PINS[index], state)
            led_state = json.dumps(get_led_state())
            await broadcast(json.dumps(get_led_state()))
    except websockets.exceptions.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Unregister.
        connected.remove(websocket)
# BUTTON
async def broadcast(message):
    if connected:
        await asyncio.gather(*(ws.send(message) for ws in connected))

def button_callback(channel):
    index = BUTTON_PINS.index(channel)
    message = json.dumps({'button': index + 1})
    #loop.call_soon_threadsafe(loop.create_task, broadcast(message))
    asyncio.run(broadcast(message))

BUTTON_PINS = [17, 27, 22]
for pin in BUTTON_PINS:
    GPIO.setup(pin, GPIO.IN)
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=button_callback, bouncetime=200)
#
loop = asyncio.get_event_loop()
start_server = websockets.serve(server, '0.0.0.0', 6789)
loop.run_until_complete(start_server)
loop.run_forever()
