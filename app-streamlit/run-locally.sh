#usr/zsh
export $(cat .env | xargs)
poetry shell
poetry run streamlit run main.py