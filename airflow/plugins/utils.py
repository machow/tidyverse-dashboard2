# from https://github.com/chriscardillo/ABSQL/blob/main/absql/functions/time.py
def previous_date(tz="utc", days=1):
    from pendulum import now
    from datetime import timedelta

    return (now(tz=tz) - timedelta(days=days)).to_date_string()

