import base64
import io
import os.path as path
from glob import glob, iglob
import cv2
import flask
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from tqdm import tqdm
import rec.script.utility as rec_util
from . import utility as util


_db = SQLAlchemy()

class Fig(_db.Model):
    seq    = _db.Column(_db.Integer, autoincrement=True, primary_key=True)
    ts_seq = _db.Column(_db.Integer, _db.ForeignKey("ts.seq"), nullable=False)
    digit  = _db.Column(_db.Integer, nullable=False)
    img    = _db.Column(_db.LargeBinary, nullable=False)
    recog  = _db.Column(_db.Integer, nullable=False)
    label  = _db.Column(_db.Integer)

class Slice(_db.Model):
    seq      = _db.Column(_db.Integer, autoincrement=True, primary_key=True)
    cam_name = _db.Column(_db.String, nullable=False)
    vid_idx  = _db.Column(_db.Integer, nullable=False)
    tss      = _db.relationship("Ts", backref="slice")

class Ts(_db.Model):
    seq       = _db.Column(_db.Integer, autoincrement=True, primary_key=True)
    slice_seq = _db.Column(_db.Integer, _db.ForeignKey("slice.seq"), nullable=False)
    frm_idx   = _db.Column(_db.Integer, nullable=False)
    figs      = _db.relationship("Fig", backref="ts")

class DbHandler:
    app = flask.Flask(__name__, static_folder=path.join(path.dirname(__file__), "../static"), template_folder=path.join(path.dirname(__file__), "../templates"))

    def __new__(cls, result_dir: str, vid_dir: str, ver: int = 0) -> None:
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + path.join(result_dir, "label.db")
        _db.init_app(cls.app)
        with cls.app.app_context():
            _db.create_all()

            if _db.session.query(Ts).count() == 0:
                for f in tqdm(sorted(iglob(path.join(result_dir, f"*/??-??-??_*/version_{ver}/predict_results.csv"))), desc="creating database"):
                    df = pd.read_csv(f, usecols=("cam", "vid_idx", "frm_idx", "recog", "is_inconsis"))
                    vid_files = glob(path.join(vid_dir, f"camera{df.loc[0, 'cam']}/video_??-??-??_{df.loc[0, 'vid_idx']:02d}.mp4"))
                    if len(vid_files) != 1:
                        raise Exception("video index must be unique")
                    cap = cv2.VideoCapture(filename=vid_files[0])
                    if cap.get(cv2.CAP_PROP_FRAME_COUNT) != len(df):
                        raise Exception("number of video frames and length of prediction result do not match")

                    cap_pos = 0
                    for s in util.slice_inconsis(df):
                        tmp = Slice(cam_name=s.iloc[0]["cam"], vid_idx=int(s.iloc[0]["vid_idx"]))
                        _db.session.add(tmp)
                        _db.session.flush()
                        slice_seq = tmp.seq
                        _db.session.commit()

                        for _, r in s.iterrows():
                            tmp = Ts(slice_seq=slice_seq, frm_idx=r["frm_idx"])
                            _db.session.add(tmp)
                            _db.session.flush()
                            ts_seq = tmp.seq
                            _db.session.commit()

                            while cap_pos < r["frm_idx"]:
                                cap.read()
                                cap_pos += 1
                            for i, img in enumerate(rec_util.extract_ts_fig(cap.read()[1])):
                                buf = io.BytesIO()
                                Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).save(buf, format="JPEG")
                                _db.session.add(Fig(ts_seq=ts_seq, digit=i, img=base64.b64encode(buf.getvalue()), recog=int(r["recog"][i + i // 2])))
                                _db.session.commit()
                            cap_pos += 1

                    cap.release()

        return super().__new__(cls)

    @app.route("/")
    def get() -> tuple[str, int]:
        for s in _db.session.query(Slice):
            if s.tss[0].figs[0].label is None:
                return flask.render_template(
                    "index.html",
                    cam_name=s.cam_name,
                    vid_idx=s.vid_idx,
                    tss=[{"frm_idx": t.frm_idx, "figs": [{"seq": f.seq, "img": f.img.decode(), "recog": f.recog} for f in t.figs]} for t in s.tss]
                ), 200
        return "Completed", 200

    @app.route("/label", methods=["PUT"])
    def post_label() -> tuple[str, int]:
        for d in flask.request.get_json():
            _db.get_or_404(Fig, d["seq"]).label = d["label"]
            _db.session.commit()
        return "No Content", 204

    @classmethod
    def serve(cls, host: str, port: int) -> None:
        cls.app.run(host=host, port=port, debug=True)
