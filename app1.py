import streamlit as st

import google.generativeai as genai

genai.configure(api_key="AIzaSyAmfGknEYmN6fNQJlk8TG1kWkEUKFH96e8")

model = genai.GenerativeModel("gemini-1.5-flash")



def analyze_sentiment(text):
    """Analyzes sentiment of text using Gemini API."""
    prompt = f"""
    Analyze the sentiment of the following text and classify it as positive, negative, or neutral.
    Provide a confidence score between 0 and 1, where 1 is the highest confidence.

    Text: "{text}"

    Output format:
    Sentiment: [positive/negative/neutral]
    Confidence: [0.0-1.0]
    """

    try:
        response = model.generate_content(prompt)
        response_text = response.text

        # Extract sentiment and confidence
        sentiment = None
        confidence = None
        for line in response_text.splitlines():
            if "Sentiment:" in line:
                sentiment = line.split(":")[1].strip().lower()
            if "Confidence:" in line:
                try:
                    confidence = float(line.split(":")[1].strip())
                except ValueError:
                  confidence = 0.0

        return sentiment, confidence

    except Exception as e:
        return None, None, f"Error: {e}"

# Streamlit App
def main():
    st.title("Sentiment Analysis App")

    user_input = st.text_area("Enter text for sentiment analysis:")

    if st.button("Analyze Sentiment"):
        if user_input:
            with st.spinner("Analyzing sentiment..."):
                sentiment, confidence = analyze_sentiment(user_input)

            if sentiment:
                st.subheader("Sentiment Analysis Result:")
                st.write(f"Sentiment: {sentiment.capitalize()}")
                st.write(f"Confidence: {confidence:.2f}")  # Format confidence to 2 decimal places
            else:
                st.error("Sentiment analysis failed. Please try again.")
        else:
            st.warning("Please enter some text.")

if __name__ == "__main__":
    main()