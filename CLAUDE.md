# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Run the application:**
```bash
streamlit run main.py
```

**Install dependencies:**
```bash
pipenv install
```

**Activate virtual environment:**
```bash
pipenv shell
```

## Architecture

This is a Streamlit web application for statistical analysis of pachinko/slot machine ("juggler") performance. The app uses Bayesian statistics to analyze bonus probabilities and expected values.

**Core Structure:**
- `main.py` - Main Streamlit application with two tabs: "Expected Value" and "Probability"
- `my_function.py` - Helper functions for statistical calculations (currently contains only one beta distribution PDF function)
- `setting.yaml` - Machine configuration data containing bonus probabilities and expected returns for different machine series (IAM, MY) and settings (1-6) 変更禁止
- `style.css` - Custom CSS styling to hide Streamlit UI elements and adjust layout

**Key Components:**
- **Expected Value Tab**: Uses Bayesian inference with Beta distributions to estimate machine settings based on observed bonus frequencies. Calculates posterior probabilities and expected payout rates.
- **Probability Tab**: Uses geometric distribution to calculate probability of hitting bonuses within a specified number of games for a selected machine setting.

**Data Flow:**
1. User inputs game data (series, games played, bonus counts)
2. App loads machine parameters from `setting.yaml`
3. Bayesian calculations determine most likely machine settings
4. Results visualized with Altair charts showing probability distributions

**Dependencies:**
- Streamlit for web interface
- SciPy for statistical distributions and calculations
- Altair for interactive data visualization
- PyYAML for configuration file parsing
- Pandas/NumPy for data manipulation

The application assumes Python 3.11 and uses Pipenv for dependency management.