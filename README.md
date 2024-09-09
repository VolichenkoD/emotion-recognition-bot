# Emotion Recognition Telegram Bot

This project implements a Telegram bot that can recognize emotions from faces in photos. It uses `DeepFace` for emotion detection and `opencv` for image processing. The bot allows users to send a photo, and it will analyze the face(s) in the image, predict the dominant emotion(s), and send the photo back with labeled emotions along with a text response based on the detected emotion.

## Features

- Detects seven emotions: Happy, Sad, Angry, Disgust, Fear, Surprise, and Neutral.
- Works with multiple faces in a single image.
- Provides feedback to the user via both image annotations and text messages.
- Easy to use: just send a photo, and the bot will do the rest.

## Technologies Used

- **DeepFace**: For facial emotion recognition.
- **OpenCV**: For image processing, such as face detection and drawing bounding boxes.
- **Telegram Bot API**: To interact with users on Telegram.
- **Python**: Main programming language.

## How to Use

1. **Send a photo**: Simply upload a photo with a face (or multiple faces) to the bot.
2. **Receive results**: The bot will respond with:
   - An image of the faces, each labeled with their predicted emotion.
   - A personalized text message based on the predicted emotion.

### Example Usage

- **Command**: `/start`  
  Sends a welcome message and instructions on how to use the bot.
  
- **Command**: `/help`  
  Provides help information.

- **Photo**: Send a photo to the bot, and it will analyze it and return the results.


