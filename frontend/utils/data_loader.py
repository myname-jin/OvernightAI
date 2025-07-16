import os
import pandas as pd

def get_excel_files(directory):
    return [
        f for f in os.listdir(directory)
        if f.endswith(".xlsx") and not f.startswith("~$")
    ]
def load_team_scores(file_path, team_name=None):
    df = pd.read_excel(file_path)
    if team_name is None:
        return df, None
    team_row = df[df["팀명"] == team_name]
    if team_row.empty:
        return df, None
    score_dict = {
        col: team_row[col].values[0]
        for col in df.columns if col != "팀명" and "총점" not in col
    }
    return df, score_dict

def get_team_names(df):
    return df["팀명"].dropna().unique().tolist()
