import pandas as pd


def slice_inconsis(df: pd.DataFrame) -> list[pd.DataFrame]:
    slices = []
    for i, r in df.iterrows():
        if pd.isna(r["is_inconsis"]) and i + 1 < len(df) and df.loc[i + 1, "is_inconsis"] == "inconsis":
            j = 2
            while i + j < len(df) and df.loc[i + j, "is_inconsis"] == "inconsis":
                j += 1
            slices.append(df.loc[i:i + j - 1])    # include end row

    return slices
