# 🏠 Smart Home Automation System

A Python-based Smart Home Automation System developed using Object-Oriented Programming (OOP) and Tkinter. The application allows users to manage multiple smart homes, control connected devices, update device settings, and save home configurations for future use.

## 📌 Project Overview

The Smart Home Automation System provides a desktop application for managing smart devices through an interactive graphical user interface.

Users can create multiple homes, add different types of smart devices, switch devices ON or OFF, modify device configurations, and manage their homes through a centralized dashboard.

The project demonstrates core Python programming concepts, object-oriented design, GUI development, data validation, exception handling, and file handling.

## ✨ Features

### 1. Smart Device Management
- Create and manage smart devices.
- Turn individual devices ON or OFF.
- Update device configurations.
- Delete devices from a smart home.
- Validate device settings and prevent invalid values.

### 2. Supported Smart Devices

**Smart Plug**
- Manage electricity consumption rate.
- Supports consumption values between 0 and 150 watts.
- Toggle power state.

**Smart Door**
- Manage door lock status.
- Lock and unlock functionality.
- Boolean-based configuration.

**Smart Air Fryer**
- Manage cooking modes.
- Available modes:
  - Healthy
  - Defrost
  - Crispy
- Toggle device power state.

### 3. Smart Home Management
- Add multiple smart devices.
- Set maximum device capacity.
- Retrieve and remove devices.
- Turn all devices ON or OFF.
- Count active devices.
- Update device configurations.

### 4. Graphical User Interface (GUI)
- Interactive desktop interface built with Tkinter.
- Dark-themed user interface.
- Individual device cards.
- Add, Edit, Delete, and Toggle buttons.
- Turn All On and Turn All Off controls.
- Device count display.
- Scrollable device list.

### 5. Multiple Smart Homes
- Create multiple smart homes.
- Add new homes.
- Rename existing homes.
- Remove homes.
- Open individual home dashboards.
- Manage devices separately for each home.

### 6. Data Persistence
- Save smart home configurations in a CSV file.
- Automatically load previously saved data.
- Preserve device types, settings, and power states.
- Save data when the application closes.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Tkinter | Graphical User Interface |
| OOP | Object-oriented application design |
| CSV | Data storage and persistence |
| Exception Handling | Error and input validation |
| Python Modules | Code organization |

## 📂 Project Structure

```text
smart-home-automation-system/
│
├── main.py
├── task1.py
├── task2.py
├── task3.py
├── task4.py
├── task5.py
├── homes_data.csv
│
├── README.md
└── .gitignore
```

### File Description

- **main.py:** Main application entry point and menu system.
- **task1.py:** SmartDevice base class and SmartPlug implementation.
- **task2.py:** SmartDoor and SmartAirFryer implementations.
- **task3.py:** SmartHome class and device management functionality.
- **task4.py:** Tkinter graphical user interface and device layout.
- **task5.py:** GUI interactions, multiple home management, and CSV data persistence.
- **homes_data.csv:** Stores saved smart home configurations.

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or later.
- Tkinter support.
- Git (optional).

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/smart-home-automation-system.git
```

### Step 2: Navigate to the Project Directory

```bash
cd smart-home-automation-system
```

### Step 3: Run the Application

```bash
python main.py
```

## ▶️ Application Usage

After running `main.py`, a menu will appear with the following options:

1. SmartPlug Test
2. Custom Devices Test
3. SmartHome Test
4. GUI Layout
5. GUI Interactivity Test
6. Multiple Smart Homes Test
7. Open Smart Homes Manager

Select an option to execute the corresponding functionality.

## 🧠 Concepts Demonstrated

This project demonstrates the following programming concepts:

- Object-Oriented Programming (OOP)
- Classes and Objects
- Inheritance
- Encapsulation
- Properties and Setters
- Polymorphism
- Class Methods
- Exception Handling
- Input Validation
- File Handling
- CSV Data Processing
- GUI Programming
- Modular Programming

## 🎯 Learning Objectives

The main objectives of this project are:

- Understand and implement object-oriented programming principles.
- Develop reusable and modular Python classes.
- Build an interactive desktop application.
- Implement device management functionality.
- Handle invalid inputs and application errors.
- Store and retrieve application data using CSV files.

## 🚀 Future Improvements

Potential enhancements include:

- Real-time energy consumption monitoring.
- Device scheduling and automation.
- User authentication and authorization.
- Database integration.
- Remote device control.
- Mobile application integration.

## 👨‍💻 Author

**Ahsan**

Python | Object-Oriented Programming | Software Development

---

⭐ If you find this project interesting, consider giving it a star!

