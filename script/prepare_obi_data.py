import pandas as pd

def prepare_practitioner_role_csv():
    # Read the Excel file and the specific tab
    df = pd.read_excel(
        'obi/OBI_data.xlsx',
        sheet_name='ZLL_grant_request_012626',
        dtype=str
    )

    # Select relevant columns and drop duplicates by provider
    df_unique = df[['external_mdhhs_site_id', 'site_name']].drop_duplicates()

    # Prepare the output DataFrame
    out_df = pd.DataFrame({
        'PractitionerRole.identifier': df_unique['external_mdhhs_site_id'],
        'PractitionerRole.practitioner': '',
        'PractitionerRole.organization': df_unique['site_name'],
        'PractitionerRole.code': ' '
    })

    # Write to CSV
    out_df.to_csv('obi/PractitionerRole.csv', index=False)


import uuid
from datetime import datetime
import calendar

def prepare_performance_measure_report_csv():
    # Read both relevant tabs
    df = pd.read_excel(
        'obi/OBI_data.xlsx',
        sheet_name='ZLL_grant_request_012626',
        dtype=str
    )
    measures_df = pd.read_excel(
        'obi/OBI_data.xlsx',
        sheet_name='measures',
        dtype=str
    )

    measure_ids = measures_df['id'].dropna().unique()

    rows = []
    for _, row in df.iterrows():
        subject = row['external_mdhhs_site_id']
        period_start = row['period.start']
        # Calculate period_end as last day of month
        try:
            dt = datetime.strptime(period_start, '%Y-%m-%d')
            last_day = calendar.monthrange(dt.year, dt.month)[1]
            period_end = dt.replace(day=last_day).strftime('%Y-%m-%d')
        except Exception:
            period_end = ''
        for measure_id in measure_ids:
            num_col = f'{measure_id}_num'
            denom_col = f'{measure_id}_denom'
            rate_col = f'{measure_id}_rate'
            rate = row.get(rate_col, '')
            denom = row.get(denom_col, '')
            rows.append({
                'identifier': str(uuid.uuid4()),
                'measure': measure_id,
                'subject': subject,
                'period.start': period_start,
                'period.end': period_end,
                'measureScore.rate': round(float(rate),3) if rate != '' else '',
                'measureScore.denominator': round(float(denom),3) if denom != '' else '',
                'measureScore.range': 0
            })

    out_df = pd.DataFrame(rows)
    out_df.to_csv('obi/PerformanceMeasureReport.csv', index=False)


def prepare_comparator_measure_report_csv():
        df = pd.read_excel(
            'obi/OBI_data.xlsx',
            sheet_name='ZLL_grant_request_012626',
            dtype=str
        )
        measures_df = pd.read_excel(
            'obi/OBI_data.xlsx',
            sheet_name='measures',
            dtype=str
        )
        measure_ids = measures_df['id'].dropna().unique()

        rows = []
        for _, row in df.iterrows():
            site_name = row['site_name']
            period_start = row['period.start']
            ces_estimate = row.get('ces_estimate', '')
            try:
                dt = datetime.strptime(period_start, '%Y-%m-%d')
                last_day = calendar.monthrange(dt.year, dt.month)[1]
                period_end = dt.replace(day=last_day).strftime('%Y-%m-%d')
            except Exception:
                period_end = ''
            for measure_id in measure_ids:
                rows.append({
                    'identifier': str(uuid.uuid4()),
                    'measure': measure_id,
                    'period.start': period_start,
                    'period.end': period_end,
                    'measureScore.rate': ces_estimate,
                    'measureScore.denominator': '',
                    'group.subject': site_name,
                    'group.code': 'http://purl.obolibrary.org/obo/PSDO_0000094',
                    'PractitionerRole.code': ' '
                })

        out_df = pd.DataFrame(rows)
        out_df.to_csv('obi/ComparatorMeasureReport.csv', index=False)

if __name__ == '__main__':
    prepare_practitioner_role_csv()
    prepare_performance_measure_report_csv()
    # prepare_comparator_measure_report_csv() need to use 80 as goal for desired increase measures and not all desired decrease measures has a goal value
