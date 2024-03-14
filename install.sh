#!/bin/bash

# Update package lists
sudo apt-get update

# Install required packages
sudo apt-get install -y git python3 python3-pip

# Clone the repository
git clone https://github.com/ara9900/tik.git

# Navigate to the project directory
cd tik

# Install Python dependencies
pip3 install -r requirements.txt

# Run the bot
python3 bot.py
