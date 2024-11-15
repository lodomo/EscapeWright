#!/bin/bash

BUMPER="[ESCAPEWRIGHT] "

echo "$BUMPER Installing dependencies"
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

echo "$BUMPER Installing pipenv"
sudo apt install pipenv


echo "$BUMPER Installing dependencies"
pipenv install

echo "$BUMPER Installing as a service"
sudo cp ./src/escapewright.service /etc/systemd/system/

echo "$BUMPER Starting service"
sudo systemctl start escapewright

echo "$BUMPER Enabling service"
sudo systemctl enable escapewright

echo "$BUMPER Done"

echo "$BUMPER Go to localhost:12413 to make sure it's live"
echo "$BUMPER If it's not, check the logs with 'journalctl -u escapewright'"
echo "$BUMPER Now you need to update the config.yaml file with your own settings"
echo "$BUMPER You can restart the service from the API at localhost:12413"
echo "$BUMPER If you have any issues, please open an issue on the GitHub page"
echo "$BUMPER If you are not running a control panel, make sure control_panel is removed from the config.yaml"
