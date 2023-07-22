def load_options(df):
    available_days = df['day'].unique()
    available_months = df['month'].unique()
    available_years = sorted(df['year'].unique().tolist())
    available_cats = df['group'].unique()
    return available_days,available_months,available_years,available_cats
