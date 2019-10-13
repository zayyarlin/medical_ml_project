from flask import Flask, redirect, url_for, render_template, request, session, jsonify
import json

from drqa.reader import Predictor

app = Flask(__name__)

# Initiates the DrQA predictor using Spacy tokenizer
predictor = Predictor(None, "spacy", num_workers=0,
                      normalize=False)

@app.route('/qa', methods=['POST'])
def qa_service():
    content = request.json

    doc = content['context']
    q = content['question']

    print(doc)
    print(q)

    predictions = predictor.predict(doc, q, None, 1)

    if len(predictions) > 0:
        result = {}
        result['answer'] = predictions[0][0]
        return jsonify(result)
    else:
        return json.dumps('{"answer": null}')

# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=8080, host='0.0.0.0')