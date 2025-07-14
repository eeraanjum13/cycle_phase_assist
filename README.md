````markdown
# 🍃 Cycle-Aware Wellness POC

A proof-of-concept that:

1. Computes your menstrual cycle phase  
2. Queries OpenAI GPT for tailored work, energy, activity, and food advice  
3. Exposes a FastAPI `/predict` endpoint  
4. Provides a Streamlit UI to interactively view results  

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, FastAPI, Uvicorn  
- **Frontend**: Streamlit  
- **AI**: OpenAI ChatCompletion API (GPT-4)  
- **Env management**: python-dotenv  
- **Dependencies**: see `requirements.txt`  

---

## ⚡ Features

- **Phase calculation** based on last period start date and cycle length  
- **4-cycle phases**: Menstrual, Follicular, Ovulation, Luteal  
- **AI-powered advice**: work suggestions, expected energy, activities to avoid, foods to eat/avoid  
- **REST API**: JSON in, JSON out  
- **Interactive UI**: date picker + cycle length input  

---

## 🚀 Getting Started

### 1. Clone & Prep

```bash
git clone https://github.com/your-username/cycle-aware-poc.git
cd cycle-aware-poc
````

### 2. Create & Activate Virtualenv

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure

1. Copy the example env file and set your key:

   ```bash
   cp .env.example .env
   # then edit `.env`:
   # OPENAI_API_KEY=<enter_your_api_key>
   ```
2. (Optional) tweak `CYCLE_LENGTH` or `PERIOD_LENGTH` defaults in `app/utils.py`.

---

## 📂 Project Structure

```text
cycle_poc/
├── app/
│   ├── main.py         # FastAPI entrypoint
│   └── utils.py        # Phase logic + OpenAI wrapper
├── streamlit_app.py    # Streamlit frontend
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## 🔗 API Reference

### POST `/predict`

Compute day/phase & fetch AI advice.

* **Request Body**

  ```json
  {
    "last_period_start": "YYYY-MM-DD",
    "cycle_length": 28
  }
  ```
* **Response**

  ```json
  {
    "day_of_cycle": 7,
    "phase": "Follicular",
    "advice": "• Ideal Work: Creative brainstorming …\n• Energy: Medium\n• Avoid: High-intensity workouts …\n• Eat: Leafy greens, salmon, chia seeds\n• Avoid: Caffeine, processed sugar"
  }
  ```
* **Errors**

  * `400` for invalid inputs
  * `502` for OpenAI API failures

---

## 🎨 Streamlit UI

1. Run:

   ```bash
   streamlit run streamlit_app.py
   ```
2. Enter **Last period start** (calendar picker)
3. Set **Cycle length** (20–40 days)
4. Click **Get My Advice** → see day, phase, and bullet-list recommendations

---

## ♻️ Caching & Rate-Limiting

* Add `functools.lru_cache` to `fetch_cycle_advice` to memoize per day+phase.
* Use FastAPI middleware (e.g. `slowapi`) to limit abuse.

---

## 🤝 Contributing

1. Fork the repo & create a feature branch
2. Run `pre-commit` checks (linters, formatting)
3. Open a PR describing your changes
4. Ensure any new secrets are only in your local `.env`

