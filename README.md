# 🦉 DuoVocab Practice

> A lightweight, Duolingo-inspired vocabulary practice web app for learning Spanish ↔ Czech

[![Flask](https://img.shields.io/badge/Flask-2.3+-000000?style=flat&logo=flask)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## ✨ Features

- 🎯 **Lesson-Based Learning**: Progress through structured vocabulary lessons
- 🔄 **Bidirectional Practice**: Translate Spanish → Czech *or* Czech → Spanish (randomized)
- 🎨 **Duolingo-Style UI**: Clean, gamified interface with progress bars and instant feedback
- 📚 **Interactive Dictionary**: Searchable glossary with word types (Noun, Verb, Adjective, Phrase)
- 🛠️ **Custom Training**: Combine multiple lessons into one personalized practice session
- 💾 **Progress Tracking**: Mark lessons complete with session-based persistence
- 📱 **Responsive Design**: Works on desktop and mobile devices
- ⚡ **Zero Dependencies**: Runs with just Flask + standard library

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/masterman331/Simple-vocab.git
cd Simple-vocab

# 2. Install Flask (only dependency)
pip install flask

# 3. Ensure vocabs.txt is in the project root
#    (See "📦 vocabs.txt Format" section below)

# 4. Run the app
python app.py
```

### Access the App
Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

---

## 📁 Project Structure

```
Simple-vocab/
├── app.py                 # Main Flask application (all routes + templates)
├── vocabs.txt             # JSON file containing lessons & vocabulary ⭐
├── requirements.txt       # Python dependencies (flask)
├── README.md             # This file
└── LICENSE               # MIT License
```

> 💡 **Note**: All HTML/CSS/JS templates are embedded directly in `app.py` using Jinja2's `DictLoader` for easy distribution—no separate template files needed!

---

## 📦 vocabs.txt Format

The app loads vocabulary from a `vocabs.txt` file containing **valid JSON**. Here's the expected structure:

```json
[
  {
    "lesson_name": "Lesson 1: Basic Greetings",
    "words": [
      {
        "spanish": "hola",
        "czech": "ahoj",
        "type": "Phrase",
        "notes": "Informal greeting"
      },
      {
        "spanish": "gracias",
        "czech": "děkuji",
        "type": "Phrase",
        "notes": "Polite thank you"
      }
    ]
  },
  {
    "lesson_name": "Lesson 2: Common Nouns",
    "words": [
      {
        "spanish": "casa",
        "czech": "dům",
        "type": "Noun",
        "notes": "Feminine in Spanish"
      },
      {
        "spanish": "perro",
        "czech": "pes",
        "type": "Noun",
        "notes": "Masculine"
      }
    ]
  }
]
```

### Word Object Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `spanish` | string | ✅ | The Spanish word/phrase |
| `czech` | string | ✅ | The Czech translation |
| `type` | string | ❌ | Category: `Noun`, `Verb`, `Adjective`, `Phrase` (used for colored badges) |
| `notes` | string | ❌ | Additional context, grammar notes, or usage tips |

> ⚠️ **Important**: Save the file as `vocabs.txt` with **UTF-8 encoding** to support special characters (ñ, č, ř, etc.)

---

## 🎮 How to Use

### 🏠 Home / Syllabus
- View all available lessons with word counts
- Click **Start** to begin practicing a lesson
- Use **Skip** to mark a lesson as completed without practicing
- Click **Reset Progress** to clear all completed lessons

### 🎯 Practice Mode
1. See a word in Spanish *or* Czech (randomized direction)
2. Choose the correct translation from 4 multiple-choice options
3. Get instant feedback:
   - ✅ Green highlight + "Excellent!" for correct answers
   - ❌ Red highlight + correct answer shown for mistakes
4. Incorrect answers are added back to the end of the queue for reinforcement
5. Progress bar tracks your completion

### 📚 Dictionary
- Search across Spanish, Czech, or notes fields
- Filter by typing in the search box (real-time)
- View word types with color-coded badges
- See total counts: all words, phrases, nouns, verbs

### 🛠️ Custom Training
- Check multiple lessons to combine into one session
- Perfect for review or focused practice on specific topics
- Start a mixed practice session with your selected lessons

---

## 🛠️ Technologies Used

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3 (embedded), Vanilla JavaScript
- **Templating**: Jinja2 with `DictLoader` for embedded templates
- **Storage**: Flask sessions (client-side cookies) for progress tracking
- **Styling**: Custom CSS with Duolingo-inspired design tokens
- **Fonts**: Google Fonts (Nunito)

---

## 🔧 Customization

### Change the Secret Key
For production use, update the secret key in `app.py`:
```python
app.secret_key = 'your-secure-random-key-here'
```

### Modify Colors
Edit the CSS variables in the `<style>` section of `BASE_TEMPLATE`:
```css
:root {
    --primary: #58cc02;        /* Main green */
    --blue: #1cb0f6;           /* Accent blue */
    --danger: #ff4b4b;         /* Error red */
    /* ... more variables */
}
```

### Add More Lessons
Simply append new lesson objects to `vocabs.txt` following the JSON format above. No code changes needed!

---

## 🤝 Contributing

Contributions are welcome! Here's how to help:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Ideas for Contributions
- [ ] Add audio pronunciation support
- [ ] Implement user accounts with persistent progress
- [ ] Add more language pairs (e.g., Spanish ↔ English)
- [ ] Include spaced repetition algorithm
- [ ] Export/import progress as JSON
- [ ] Add dark mode toggle

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `vocabs.txt not found` | Ensure the file exists in the same directory as `app.py` |
| `JSONDecodeError` | Validate your `vocabs.txt` is proper JSON (use [jsonlint.com](https://jsonlint.com)) |
| Special characters display incorrectly | Save `vocabs.txt` with UTF-8 encoding |
| Session not persisting | Ensure cookies are enabled in your browser; for production, configure proper session storage |
| Flask not found | Run `pip install flask` in your virtual environment |

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

Feel free to use, modify, and distribute for personal or commercial projects. Attribution is appreciated but not required.

---

## 🙏 Acknowledgments

- Inspired by [Duolingo](https://www.duolingo.com)'s engaging learning approach
- Built with ❤️ by [Koci](https://github.com/masterman331)
- Fonts by [Google Fonts](https://fonts.google.com)

---

> 💬 **Have questions or suggestions?**  
> Open an [Issue](https://github.com/masterman331/Simple-vocab/issues) or start a [Discussion](https://github.com/masterman331/Simple-vocab/discussions)!

---

*Made with Python & Flask • Happy Learning! 🌟*

> **Disclaimer:**  
> This project has been vibe-coded please use it cautiously. - Masterman331

---

## 🪙 Support This Project

If you found this project useful, interesting, or helpful, consider supporting its development through **Monero**.

<p align="center">
  <img src="https://raw.githubusercontent.com/masterman331/masterman331/main/moneroadress.png" alt="Monero donation QR code" width="220"/>
</p>

<p align="center">
<code>47chh1Z9wvHDP6ZDpzPPETKaXUfsNnmXr8P5cL4ofAkH1fi3mrrvC7tiRoeqxtNCbB1BQ3rqk5k2tSPGoiMSTUTC3iPc9Qu</code>
</p>

<p align="center">
  <em>Privacy-respecting contributions help keep independent development alive.</em>
</p>
