# This file will get everything prepped for the Escape Wright Pis.
# It will install the necessary packages, create the necessary directories,
# and set up the necessary services.

# Create a variable for the current user name
USER=$(whoami)

# Install packages
echo "[ESCAPEWRIGHT] Preparing to install packages"

echo "[ESCAPEWRIGHT] Updating apt-get"
sudo apt-get update

echo "[ESCAPEWRIGHT] Upgrading apt-get" 
sudo apt-get upgrade -y

echo "[ESCAPEWRIGHT] Installing flask"
sudo apt install python3-flask

echo "[ESCAPEWRIGHT] Installing git"
sudo apt install git -y

# If the EscapeWright directory already exists, run a fetch and pull on it.
# Otherwise, clone the repository.
if [ -d "/home/${USER}/EscapeWright" ]; then
    echo "[ESCAPEWRIGHT] EscapeWright exists. Fetching and pulling now"
    cd /home/${USER}/EscapeWright
    git fetch
    git pull
else
    echo "[ESCAPEWRIGHT] EscapeWright does not exist. Cloning now"
    cd /home/${USER}
    git clone https://github.com/lodomo/EscapeWright
fi

# Create bash_aliases if it doesn't exist
if [ ! -f "/home/${USER}/.bash_aliases" ]; then
    echo "[ESCAPEWRIGHT] Creating .bash_aliases" 
    touch /home/${USER}/.bash_aliases
else 
    echo "[ESCAPEWRIGHT] .bash_aliases exists adding EscapeWright to PYTHONPATH"
fi

# Source .bash_aliases if it exists and is not already sourced
if [ -f /home/${USER}/.bash_aliases ]; then
    source /home/${USER}/.bash_aliases
fi

# Adds a directory to the PYTHONPATH only if it is not already included
if [[ ":$PYTHONPATH:" != *":/home/${USER}/EscapeWright/escapewright:"* ]]; then
    echo "[ESCAPEWRIGHT] Adding EscapeWright to PYTHONPATH in .bash_aliases"
    echo 'if [[ ":$PYTHONPATH:" != *":/home/'"${USER}"'/EscapeWright/escapewright:"* ]]; then' >> /home/${USER}/.bash_aliases
    echo '    export PYTHONPATH="/home/'"${USER}"'/EscapeWright/escapewright:$PYTHONPATH"' >> /home/${USER}/.bash_aliases
    echo 'fi' >> /home/${USER}/.bash_aliases
else
    echo "[ESCAPEWRIGHT] PYTHONPATH already includes /home/${USER}/EscapeWright/escapewright"
fi

echo "[ESCAPEWRIGHT] Sourcing .bashrc to permanently update PYTHONPATH" 
source ~/.bashrc 

# Create a directory for the files for it's purpose if it doesn't exist
if [ ! -d "/home/${USER}/ew_local" ]; then
    echo "[ESCAPEWRIGHT] Creating ew_local"
    mkdir /home/${USER}/ew_local
else 
    echo "[ESCAPEWRIGHT] ew_local already exists"
fi

# Move the setup files from EscapeWright to ew_node
if [ -f "/home/${USER}/ew_local/setup.py" ]; then
    echo "[ESCAPEWRIGHT] setup.py exists. Running now"
else
    echo "Moving setup.py"
    mv /home/${USER}/EscapeWright/setup/setup.py /home/${USER}/ew_local
fi

# Run the setup script
python3 /home/${USER}/ew_local/setup.py