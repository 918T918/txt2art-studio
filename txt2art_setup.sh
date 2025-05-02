#!/bin/bash

PYTHON_SCRIPT_NAME="txt2art.py"
COMMAND_NAME="txt2art"
LINK_TARGET_DIR="/usr/local/bin"

if [ "$EUID" -ne 0 ]; then
  echo "Error: This script requires root privileges to create a system-wide command."
  echo "Please run it using sudo: sudo ./txt2art_setup.sh"
  exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PYTHON_SCRIPT_PATH="${SCRIPT_DIR}/${PYTHON_SCRIPT_NAME}"

if [ ! -f "${PYTHON_SCRIPT_PATH}" ]; then
  echo "Error: Python script '${PYTHON_SCRIPT_NAME}' not found in the current directory."
  echo "Please make sure this setup script is in the same folder as '${PYTHON_SCRIPT_NAME}'."
  exit 1
fi

echo "Making '${PYTHON_SCRIPT_NAME}' executable..."
chmod +x "${PYTHON_SCRIPT_PATH}"
if [ $? -ne 0 ]; then
  echo "Error: Failed to make '${PYTHON_SCRIPT_NAME}' executable."
  exit 1
fi
echo "'${PYTHON_SCRIPT_NAME}' is now executable."

LINK_PATH="${LINK_TARGET_DIR}/${COMMAND_NAME}"
echo "Creating symbolic link: ${LINK_PATH} -> ${PYTHON_SCRIPT_PATH}"

if [ -L "${LINK_PATH}" ]; then
    echo "Removing existing link at ${LINK_PATH}..."
    rm "${LINK_PATH}"
fi

ln -s "${PYTHON_SCRIPT_PATH}" "${LINK_PATH}"
if [ $? -ne 0 ]; then
  echo "Error: Failed to create symbolic link in ${LINK_TARGET_DIR}."
  echo "Check permissions or if the directory exists."
  exit 1
fi

echo ""
echo "Success! The '${COMMAND_NAME}' command has been set up."
echo "You should now be able to run 'txt2art' from any terminal (you might need to open a new terminal window)."

exit 0
