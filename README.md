# Smart-Seeker

A Drone companion that can help you find things with object recognition, image tracking, and a chat interface

## Project Overview

This project is a drone assistant that utilizes object recognition, image tracking, and a chat interface to control a DJI Tello drone. The assistant allows users to interact with the drone using natural language commands, which are processed via OpenAI's API. The drone can execute various commands such as takeoff, landing, and movement, while also providing a video feed for real-time monitoring.

## Installation Instructions

### Prerequisites

- Python 3.8 or higher
- DJI Tello drone
- OpenAI API Key
- Required Python packages (listed below)

### Clone the Repository

```bash
git clone https://github.com/yourusername/drone-assistant.git
cd drone-assistant
```

### Install Required Python Packages

```bash
pip install djitellopy opencv-python openai
```

### Set Up OpenAI API Key

You need to replace the placeholder API key in the chat_interface.py file with your actual OpenAI API key.

```python
# chat_interface.py
openai.api_key = 'your-openai-api-key'
```

## Usage Guide

### Running the Drone Assistant

To start the drone assistant, simply run the main.py script:

```bash
python main.py
```

### Available Commands

The assistant supports the following basic commands:

- Take Off: Initiates the drone's takeoff.
- Land: Lands the drone safely.
- Move Up/Down: Moves the drone up or down by a specified distance.
- Move Forward/Back: Moves the drone forward or backward by a specified distance.
- Rotate Clockwise/Counterclockwise: Rotates the drone by a specified angle.

### Real-time Video Feed

Once the drone is airborne, the video feed can be viewed by using the start_video_stream method in the VisionSystem class. This feature allows for real-time monitoring and can be extended to include advanced image processing or object tracking.

## Key Components

1. `main.py`
   The entry point of the application.
   Initializes the DroneControl, VisionSystem, and ChatInterface.
   Listens for user commands via the chat interface and executes corresponding drone commands.

2. `drone_control.py`
   Defines the DroneControl class that interfaces with the DJI Tello drone using the djitellopy library.
   Includes methods for basic drone operations such as takeoff, landing, movement, and rotation.

3. `vision_system.py`
   Defines the VisionSystem class, which handles the drone’s video stream.
   Displays real-time video feed and can be extended for image tracking and object recognition.

4. `chat_interface.py`
   Defines the ChatInterface class that uses the OpenAI API to generate instructions from natural language prompts.
   Processes user input and provides commands to the drone based on the generated responses.

## Future Enhancements

- Object Recognition: Integrate advanced object recognition algorithms to allow the drone to identify and track specific objects.
- Path Planning: Implement path planning algorithms to autonomously navigate the drone to a specified location.
- Voice Commands: Enhance the chat interface to accept voice commands, making the interaction more intuitive.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
