# KAU Guide Model

**The NLP backend for [Your KAU Guide](https://github.com/Majed90alfaifi/YourKAUGuideApp), an Arabic chatbot that answers student questions about the Faculty of Computing and Information Technology (FCIT) at King Abdulaziz University.**

This repository has the intent-classification model, the training pipeline, and the Flask API that the Android app calls. It was built as part of a graduation project at King Abdulaziz University.

---

## How It Works

```
Student question (Arabic)
        │
        ▼
Tokenize (NLTK) ──► Stem (ISRI Arabic stemmer) ──► Bag-of-words vector
                                                          │
                                                          ▼
                                          Feed-forward neural network (PyTorch)
                                                          │
                                                          ▼
                              Predicted intent + confidence ──► Response from data.json
```

1. The question is tokenized with NLTK and each word is reduced to its root with the **ISRI Arabic stemmer**. Stemming lets different forms of the same Arabic word match.
2. The stemmed words become a bag-of-words vector over the training vocabulary.
3. A 3-layer feed-forward network classifies the vector into one of the known intents.
4. If the model's confidence is above **0.75**, the bot answers with a random response for that intent. Otherwise it replies `! لم أفهم ما تقصده` ("I didn't understand what you mean").

## Supported Topics

The model is trained on 14 intents defined in [`data.json`](data.json):

| Category | Intents |
|---|---|
| Greetings | General greeting, good morning, good evening |
| Academics | FCIT majors, study plans (general, IT, IS), academic programs |
| Admission | Admission requirements, required qualifications |
| Contacts | Email addresses of faculty members |
| Small talk | Responding to the user's name |

To add a topic, add a new intent with its `tag`, `patterns` (sample questions) and `responses` to `data.json`, then retrain.

## Model

| Setting | Value |
|---|---|
| Architecture | Linear → ReLU → Linear → ReLU → Linear |
| Hidden size | 8 |
| Loss / optimizer | Cross-entropy / Adam |
| Learning rate | 0.001 |
| Epochs | 1000 |
| Batch size | 8 |

The trained weights, vocabulary and tags are saved together in `data.pth`.

### Mobile Export

`model_to_onnx.py` converts the trained model for on-device use:

```
PyTorch ──► ONNX (model.onnx) ──► TensorFlow SavedModel (model.pb/) ──► TensorFlow Lite (model.tflite)
```

## Getting Started

### Prerequisites

- Python 3.8 or later

### 1. Install dependencies

```bash
pip install torch nltk numpy flask
python -c "import nltk; nltk.download('punkt')"
```

For the mobile export only, also install `onnx`, `onnx-tf` and `tensorflow`.

> **Windows note:** `data.json` contains Arabic text. If you get a `UnicodeDecodeError`, run Python in UTF-8 mode: `set PYTHONUTF8=1`.

### 2. Train the model

```bash
python train.py
```

This writes `data.pth`. A trained `data.pth` is already included, so you can skip this step unless you change `data.json`.

### 3. Chat in the terminal

```bash
python chat.py
```

Type `quit` to exit.

### 4. Run the API server

```bash
python flasktest.py
```

The server listens on port `5000`.

## API Reference

### `POST /getresponse`

Returns the chatbot's reply to a message.

**Request** (form data)

| Field | Description |
|---|---|
| `msg` | The user's question |

```bash
curl -X POST -d "msg=ما هي التخصصات" http://localhost:5000/getresponse
```

**Response:** the reply as plain text.

## Project Structure

```
KAUGuideModel/
├── data.json           # Intents: tags, sample questions and responses
├── main.py             # NLP helpers: tokenize, stem, bag_of_words
├── model.py            # Neural network definition
├── train.py            # Training script, writes data.pth
├── chat.py             # Inference (get_response) and terminal chat
├── flasktest.py        # Flask API server used by the Android app
├── model_to_onnx.py    # PyTorch → ONNX → TensorFlow → TFLite export
├── data.pth            # Trained model
├── model.onnx          # Exported ONNX model
├── model.pb/           # Exported TensorFlow SavedModel
└── model.tflite        # Exported TensorFlow Lite model
```

## Tech Stack

Python · PyTorch · NLTK (ISRI Arabic stemmer) · NumPy · Flask · ONNX · TensorFlow Lite

## Related

- **[YourKAUGuideApp](https://github.com/Majed90alfaifi/YourKAUGuideApp)**: the Android app that uses this API.

## Limitations

- A bag-of-words model ignores word order, and it only recognizes questions similar to the training patterns.
- The dataset is small (14 intents, 3–6 patterns each), so phrasing that differs a lot from the examples may not be understood.
- Answers are fixed responses from `data.json`, not generated text.
