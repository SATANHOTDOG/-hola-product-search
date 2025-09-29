from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>HOLA 商品查詢</title>
</head>
<body>
    <h2>輸入 HOLA 商品編號 (9位數)</h2>
    <form method="post">
        <input type="text" name="product_id" maxlength="9" required>
        <input type="submit" value="查詢">
    </form>
    {% if result %}
        <h3>查詢結果：</h3>
        <ul>
            {% for key, value in result.items() %}
                <li><strong>{{ key }}:</strong> {{ value }}</li>
            {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        product_id = request.form["product_id"]
        url = f"https://www.hola.com.tw/p/{product_id}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        result = {
            "商品編號": product_id,
            "商品品名": soup.select_one("h1.product-title").text.strip() if soup.select_one("h1.product-title") else "無資料",
            "材質": "",
            "尺寸": "",
            "重量": "",
            "產地": "",
            "最大購買數量": ""
        }

        for li in soup.select("ul.product-spec li"):
            text = li.text.strip()
            if "材質" in text:
                result["材質"] = text.split("：")[-1]
            elif "尺寸" in text:
                result["尺寸"] = text.split("：")[-1]
            elif "重量" in text:
                result["重量"] = text.split("：")[-1]
            elif "產地" in text:
                result["產地"] = text.split("：")[-1]

        qty_tag = soup.select_one("input#buyQty")
        if qty_tag and qty_tag.has_attr("max"):
            result["最大購買數量"] = qty_tag["max"]

    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == "__main__":
    app.run(debug=True)
