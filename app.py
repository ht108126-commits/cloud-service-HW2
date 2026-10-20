
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 暫時儲存運動紀錄
records = []
next_id = 1

@app.route("/")
def index():
    # 將運動紀錄傳給 HTML 模板
    return render_template("index.html", records=records)

@app.route("/add", methods=["POST"])
def add_record():
    global next_id

    activity = request.form.get("activity", "").strip()
    duration = request.form.get("duration", "").strip()
    notes = request.form.get("notes", "").strip()

    # 檢查必填欄位
    try:
        duration = int(duration)
        if duration <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return "運動時長必須是大於 0 的整數", 400

    if not activity:
        return "請輸入運動項目", 400

    # 建立一筆運動紀錄
    record = {
        "id": next_id,
        "activity": activity,
        "duration": duration,
        "notes": notes
    }

    records.append(record)
    next_id += 1

    return redirect(url_for("index"))

@app.route("/delete/<int:record_id>", methods=["POST"])
def delete_record(record_id):
    global records

    records = [
        record for record in records
        if record["id"] != record_id
    ]

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)