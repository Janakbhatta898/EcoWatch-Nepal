from flask import Flask, request, jsonify, Response
from inference_engine import run_audio_inference
import threading
import time
import io
import requests

lock=threading.Lock()
audio_url=None
audio_label="Analysing..."
audio_pred=0

app=Flask(__name__)


@app.route("/")
def home():
    return "Running! go at /audio for the audio live streaming!"

@app.route("/setting_audio",methods=["POST"])
def set_audio():
    global audio_url

    data=request.json
    ip=data.get("ip")

    if not ip:
        return jsonify({"Error":"No Ip address has been found!"})
    
    audio_url=f"hettp://{ip}/audio.wav"
    return jsonify({"Status":"Audio Link Established"})

def get_audio_inference():
    global audio_label,audio_pred,audio_url

    while True:
        if audio_url is None:
            time.sleep(1)
            continue
        try:
            with requests.get(audio_url,stream=True,timeout=5) as r:
                audio_buffer=io.BytesIO()
                first_time=time.time()

                for chunk in r.iter_content(chunk_size=1024):
                    audio_buffer.write(chunk)
                    if time.time()-first_time>3:
                        break
                audio_buffer.seek(0)
                label,pred=run_audio_inference(FRAME_ARRAY=audio_buffer)
                with lock:
                    audio_pred=pred
                    audio_label=label

        except:
            print("Audio Error, Cannot Fetch and infer it!")
            time.sleep(2)


def stream_audio():
    """
    this should fetch all the audios and yields it.
    ps: this is not vibecoded even when there is comment like this because i just dont want to forget what i wrote
        -Moss Pants ;)
    """

    global audio_url


    try:
        with requests.get(audio_url,stream=True) as r:
            for chunk in r.iter_content(chunk_size=1024):
                yield(chunk)

    except Exception as e:
        print(f"Error streaming audio! code={e}")



@app.route("/audio_feed")
def audio_feed():
    return Response(stream_audio(),mimetype="audio/wav")

@app.route("/status")
def get_status():
    return jsonify({"Audio_Label":audio_label,"Audio_Prediction":audio_pred})


if __name__=="__main__":
    threading.Thread(target=get_audio_inference,daemon=True).start()
    app.run(host="0.0.0.0",port=1235,threaded=True)

    