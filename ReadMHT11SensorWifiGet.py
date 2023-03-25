
import picoweb
import machine
import dht
import time

app = picoweb.WebApp(__name__)
DHT_PIN = 4  
sensor = dht.DHT11(machine.Pin(DHT_PIN))

def measure():
    sensor.measure()
    time.sleep(2)  
    return sensor.temperature(), sensor.humidity()

@app.route("/")
def index(req, resp):
    headers = {"Access-Control-Allow-Origin": "*"}

    try:
        json_str = '{"temp": %s, "hum": %s}' % measure()
    except OSError as e:
        error_str = 'Error reading sensor data: %s' % e
        yield from picoweb.start_response(resp, status="500", headers=headers)
        yield from resp.awrite(error_str)
        resp.stop()
        return

    yield from picoweb.start_response(resp, headers=headers)
    yield from resp.awrite(json_str)
    resp.stop()

app.run(debug=True, host="0.0.0.0")


