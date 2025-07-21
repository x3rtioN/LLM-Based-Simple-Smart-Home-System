# 🧠 Gemini Smart Home System

This project uses a **Google Gemini LLM**-powered logic agent to interpret natural language commands (even if informal or misspelled) and map them into **logical facts** to trigger appropriate **smart home actions** using a simple rule-based inference engine.

---

## 🚀 Features

- Understands informal natural language commands (e.g., "üşüyorum", "tv yi aça")
- Extracts single-word logical facts using Gemini LLM
- Rule-based inference engine triggers one or more actions
- Terminal-based interaction
- Easy to extend with new rules

---

## ⚙️ Setup

### 1. Install Python 3 and required packages

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
pip install -r requirements.txt
```

Or manually:

```bash
pip install google-generativeai
```

---

### 2. Gemini API Key

Replace the hardcoded API key in the script:

```python
genai.configure(api_key="YOUR_API_KEY_HERE")
```

You can get your API key from Google AI.

---

## ▶️ Run the Program

```bash
python 419.py
```

You’ll be prompted to enter a command:

```
>> Command: klimayı aç
[FACT] turn_on_heater
[TRIGGERED ACTIONS]:
-> heater_power_on
```

---

## 🧠 Example Input / Output

### Input:
```
film izliyorum
```

### LLM-generated Fact:
```
watching_movie
```

### Inferred Actions:
```
-> dim_lights
-> close_curtains
```

---

## 🧩 AI-Based Fact Extraction

Using Gemini, messy or slang commands are mapped into structured facts.

Example:
```
"ışığı kapat" → turn_off_light → lights_off
```

---

## 🛠 Developer Notes

- Add rules with `agent.tell_rule("condition -> action")`
- Add facts via `agent.tell_fact("fact")`
- `llm_fact_extractor(command)` uses Google Gemini to extract logical meaning

---

## 🤝 Contributing

You’re welcome to:

- Add more natural language command patterns
- Expand rule set
- Improve the CLI or add a web/voice interface

Pull requests are appreciated!

---
