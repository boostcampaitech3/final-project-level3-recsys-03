from google.oauth2 import service_account

cd = service_account.Credentials.from_service_account_file('/opt/ml/clear-shell-351201-702c702ea7fc.json')
project_id = 'clear-shell-351201'

def load_to_bigquery(result,destination_table):
    result.to_gbq(destination_table, project_id, if_exists='append',credentials=cd)
    print(
            f"df uploaded to {destination_table}."
        )
