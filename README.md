# GatesForRunning

## Purpose
The purpose of this project is to provide insights into the speed of players across various sports, such as football, basketball, handball, athletics, and more. This information can help clubs or individuals assess their current performance, make better decisions for the upcoming season, and optimize training plans or adjustments during ongoing competitions.

## Tech Stack
This project integrates both software and hardware components:

- **Client Application**: The front-end is built with Angular, providing a user-friendly interface to view performance insights.
- **Backend**: The backend is developed using Flask, which powers the client application's API.
- **Motion Detection**: A Raspberry Pi Pico W is used for motion detection. It runs **MicroPython** and acts as a sensor to detect when a player passes through gates.
- **Main Server**: The main server is built with Python and handles communication between the sensors (Raspberry Pi Pico W) and the UI. It also manages the testing process and stores the results.
