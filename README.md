
# termify

Termify is a terminal-based application for controlling Spotify from the command line. With a simple and intuitive CLI, you can manage playback, view track details, and control your Spotify music without leaving the terminal.

<p align="center">
  <img src="https://github.com/evanlaube/termify/blob/main/assets/readme/demo.gif" alt="Demo of basic usage of termify"/>
</p>

## Features
- **Playback control**: Play, pause, skip, and change playback device

- **Track information**: Get details about current song or podcast

- **Easy Navigation**: Use arrow keys or Vim-style keybinds to navigate UI

## Installation

#### Prerequisites
- Python 3.7 or higher
- `curses` library
- `requests` library
- `dotenv` library

#### Create a Virtual Environment (Optional but recommended)
This step can be safely skipped if you are already using a default virtual Environment.
```bash
python -m venv venv
source venv/bin/activate # On Windows use: venv\Scripts\activate
```

#### Install Termify
```bash
pip install termify-py
```


#### Configure Spotify Access
1. **Create a Spotify Developer Account:** Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and create an application
1. **Configure Application Settings:** Make the following changes to the settings of your app:
    - Set `APIs used` to `Web API`
    - Add `http://localhost:8888/callback` to `Redirect URIs`
1. **Copy or Take Note of Your `Client ID`**: You will need it when first launching termify


## Usage

#### Running the Application
```bash
termify
```

#### Controls
Navigate through menus using arrow keys or `Vim` style keys (h, j, k, l)

## Versioning
- **Stable Versions**: Available on [PyPI](https://pypi.org/project/termify-py/). Install the latest stable version using `pip install termify-py`
- **Unstable Versions**: If you want to try the latest features or development version, you can install directly from source using `pip install .` after cloning the repository. Be aware that this version may have new features or bugs not present in the stable release.

## Contributing
Contributions are not only welcome, but encouraged! Feel free to fork the repository and submit pull requests. Be sure to review the [CONTRIBUTING](CONTRIBUTING.md) guidelines for more information on how to contribute to this project.

## Get Involved
 
If you have any questions, suggestions, or feedback, please don't hesitate to [open an issue](https://github.com/evanlaube/termify/issues) or [contact me](mailto:laubeevan@gmail.com).
