# Tech Espresso ☕

Your morning shot of tech. Every morning, this bot pulls the top tech stories, has an AI write a punchy
plain-English digest, and sends it to me on WhatsApp. A tiny scheduled agent —
news in, briefing out, zero effort.

## How it works

1. **`brief.py`** fetches today's top stories from the Hacker News API (free,
   no key needed) and asks Google's Gemini (free tier) to write a ~250-word
   WhatsApp-style briefing: the 5 most interesting stories, why each matters,
   and the single biggest "whoa" story of the day.
2. **`send_whatsapp.py`** delivers it via the WhatsApp Business Cloud API
   using an approved message template.
3. **`.github/workflows/daily.yml`** runs the whole thing on GitHub Actions
   every morning (~8-9am Toronto time). Free for public repos.

## Setup

1. Get a free Gemini API key at https://aistudio.google.com
2. Create an app at https://developers.facebook.com, add the WhatsApp product,
   grab the test phone number + token, add your own number as a test
   recipient, and create/approve a `daily_briefing` message template with one
   body parameter `{{1}}`.
3. Copy `.env.example` to `.env` and fill in your keys (never commit `.env`).
4. Run locally:
   ```
   pip install -r requirements.txt
   python brief.py          # builds digest.txt
   python send_whatsapp.py  # sends it
   ```
5. Push to GitHub and add the same values under repo Settings > Secrets and
   variables > Actions, then the daily schedule takes over.

## Roadmap

- [ ] Add RSS sources (TechCrunch, The Verge, Ars Technica) alongside HN
- [ ] Weekend "deep dive" edition for the week's biggest story
- [ ] Tune the prompt voice
