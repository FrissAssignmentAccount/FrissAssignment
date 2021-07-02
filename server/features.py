import pandas as pd

COLUMNS = ['sys_sector', 'sys_label', 'sys_process', 'sys_product',
        'sys_dataspecification_version', 'sys_claimid', 'sys_currency_code',
        'claim_amount_claimed_total', 'claim_causetype', 'claim_date_occurred',
        'claim_date_reported', 'claim_location_urban_area', 'object_make',
        'object_year_construction', 'ph_firstname', 'ph_gender', 'ph_name',
        'policy_fleet_flag', 'policy_insured_amount', 'policy_profitability']

NOISY_COLUMNS = ['sys_sector', 'sys_product', 'sys_label', 'sys_process', 
        'sys_product', 'sys_currency_code', 
        'sys_dataspecification_version', 'sys_claimid']

SENSITIVE_COLUMNS = ['ph_gender', 'ph_name', 'ph_firstname']

CATEGORICALS = ["occurred_date_season", "claim_causetype", "claim_location_urban_area", 
        "object_make", "policy_fleet_flag", "policy_profitability"]


CLAIM_DATE_FORMAT = "%Y%m%d"

def drop_noise_columns(data):
    return data.drop(columns=NOISY_COLUMNS)

def drop_sensitive_columns(data):
    return data.drop(columns=SENSITIVE_COLUMNS)


def process_categoricals(data):
    claim_reported_time = pd.to_datetime(data["claim_date_reported"], format=CLAIM_DATE_FORMAT)
    claim_occurred_time = pd.to_datetime(data["claim_date_occurred"], format=CLAIM_DATE_FORMAT)
    data["report_time_delta"] = (claim_reported_time - claim_occurred_time).dt.total_seconds()
    data["occurred_date_season"] = pd.DatetimeIndex(claim_occurred_time).month // 4
    categoricals = CATEGORICALS
    for column in categoricals:
        data = data.join(
            pd.get_dummies(data[column].astype("category"), prefix=column),
            rsuffix="_"
        )
    return data.drop(columns=categoricals)


def make_vehicle_age_feature(data):
    claim_occurred_time = pd.to_datetime(data["claim_date_occurred"], format=CLAIM_DATE_FORMAT)
    data["vehicle_age_years"] = pd.DatetimeIndex(claim_occurred_time).year - data["object_year_construction"].astype(int)
    return data

def final_cleanup(data):
    data["policy_insured_amount"] = data["policy_insured_amount"].fillna(0)
    return data.drop(columns=["claim_date_occurred", "claim_date_reported", "object_year_construction"])

def process_features(data):
    data_cleaned = drop_noise_columns(data)
    data_cleaned = drop_sensitive_columns(data_cleaned)
    data_cleaned = process_categoricals(data_cleaned)
    data_cleaned = make_vehicle_age_feature(data_cleaned)
    data_cleaned = final_cleanup(data_cleaned)
    return data_cleaned

def cleaned_df_from_string(input_string):
    df = pd.DataFrame(data=[input_string.split(",")], columns=COLUMNS)
    return process_features(df).to_numpy()
