from machine import I2C, Pin
import time

# Import the MAX30102 library
# You need to find or write a library compatible with MicroPython for the MAX30102 sensor
import MAX30102

# Constants
RATE_SIZE = 4
rates = [0] * RATE_SIZE
rateSpot = 0
lastBeat = 0

beatsPerMinute = 0
beatAvg = 0

# I2C setup
i2c = I2C(scl=Pin(22), sda=Pin(21))

# Initialize sensor
particleSensor = MAX30102.MAX30102(i2c)
particleSensor.setup()

def loop():
    global rateSpot, lastBeat, beatsPerMinute, beatAvg

    irValue = particleSensor.get_ir()

    if particleSensor.check_for_beat(irValue):
        delta = time.ticks_ms() - lastBeat
        lastBeat = time.ticks_ms()

        beatsPerMinute = 60 / (delta / 1000.0)

        if 20 < beatsPerMinute < 255:
            rates[rateSpot] = beatsPerMinute
            rateSpot = (rateSpot + 1) % RATE_SIZE

            beatAvg = sum(rates) // RATE_SIZE

    print("IR={}, BPM={}, Avg BPM={}".format(irValue, beatsPerMinute, beatAvg))

    if irValue < 50000:
        print(" No finger?")

# Main loop
while True:
    loop()
    time.sleep(0.1)  # Add delay to avoid flooding with data

