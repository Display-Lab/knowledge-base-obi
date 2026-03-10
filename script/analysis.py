import argparse
import re
from pathlib import Path
from datetime import datetime
import pandas as pd

def find_identifier_column(df):
    candidates = [c for c in df.columns if 'identifier' in c.lower()]
    return candidates[0] if candidates else None

def load_practitioners(pr_file):
    if not pr_file.exists():
        return set()
    df = pd.read_csv(pr_file, dtype=str, keep_default_na=False)
    col = 'PractitionerRole.identifier' if 'PractitionerRole.identifier' in df.columns else find_identifier_column(df)
    return set(df[col].unique()) if col else set()

def month_dirs(root):
    pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    dirs = [d for d in root.iterdir() if d.is_dir() and pattern.match(d.name)]
    dirs_sorted = sorted(dirs, key=lambda p: datetime.strptime(p.name, "%Y-%m-%d"))
    return dirs_sorted

def read_month_counts(month_dir, distinct_measure=False):
    f = month_dir / 'candidates.csv'
    if not f.exists():
        return {}
    df = pd.read_csv(f, dtype=str, keep_default_na=False)
    if 'subject' not in df.columns:
        return {}
    if distinct_measure and 'measure' in df.columns:
        grouped = df.groupby('subject')['measure'].nunique()
    else:
        grouped = df['subject'].value_counts()
    return grouped.to_dict()

def main():
    p = argparse.ArgumentParser(description="Aggregate subject measure counts per month")
    p.add_argument('--root', default=str(Path(__file__).resolve().parents[1]), help='project root containing month folders and obi/')
    p.add_argument('--output', default='subjects_monthly_counts.csv', help='output CSV filename (written to root)')
    p.add_argument('--distinct', action='store_false', help='count distinct measures per subject per month instead of candidate rows')
    args = p.parse_args()

    root = Path(args.root)
    obi_pr = root / 'obi' / 'PractitionerRole.csv'

    practitioners = load_practitioners(obi_pr)

    months = month_dirs(root)
    month_keys = [m.name[:7] for m in months]  # YYYY-MM for column labels

    # collect subjects from practitioners and candidates
    subjects = set(practitioners)
    month_counts = {}
    for m in months:
        counts = read_month_counts(m, distinct_measure=args.distinct)
        month_key = m.name[:7]
        month_counts[month_key] = counts
        subjects.update(counts.keys())

    # build dataframe
    subjects = sorted(subjects)
    df_out = pd.DataFrame(index=subjects)
    for mk in month_keys:
        col = pd.Series({s: month_counts.get(mk, {}).get(s, 0) for s in subjects})
        df_out[mk] = col.astype(int)

    df_out.index.name = 'subject'
    out_path = root / args.output
    df_out.reset_index().to_csv(out_path, index=False)
    print(f"Wrote {out_path} ({df_out.shape[0]} subjects x {len(month_keys)} months)")

if __name__ == '__main__':
    main()