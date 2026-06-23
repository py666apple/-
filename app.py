来自flaskimportFlask、render_template、request、jsonify
导入日期时间
import os

app = Flask(__name__)
quote_records = []
DATA_FILE = "quote_data.txt"

# 确保文件一开始就存在
if not os.path.exists(DATA_FILE):
    在 打开(DATA_FILE, "w", 编码="utf-8")时作为 f:
        f.写入("===== 鑫成机械报价数据汇总 =====\n\n")


def save_to_file(data):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = f"""
提交时间：{now}
姓名：{data['name']}
电话：{data['phone']}
材质：{data['material']}
数量：{data['quantity']}
需求：{data['product']}
----------------------------------------
"""
    # 强制写入磁盘，不缓存
    with open(DATA_FILE, "a", encoding="utf-8") as fp:
        fp.write(text)
        fp.flush()
    os.fsync(os.open(DATA_FILE, os.O_RDWR))


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/api/quote", methods=["POST"])
def quote_submit():
    try:
        data = request.get_json()
        keys = ["name", "phone", "material", "quantity", "product"]
        对于 k 在 keys 中：
            如果 不 data.get(k, "").strip():
                return jsonify({"code": 400, "msg": "请填写完整所有信息"}), 400

        quote_records.append(data)
        save_to_file(data)

        print("\n【新报价单】")
        print(f"姓名：{data['name']}")
        print(f"电话：{data['phone']}")
        print(f"材质：{data['material']}")
        print(f"数量：{data['quantity']}")
        print(f"需求：{data['product']}\n")

        返回 jsonify({"code": 200, "msg": "提交成功！已保存数据"})
    except:
        return jsonify({"code": 500, "msg": "提交失败"})


@app.route("/api/quote/all")
def all_quote():
    return jsonify(quote_records)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
