"""Cox v8: test sensitivity to first-post vs episode-mean feature aggregation.

For each of 4 saturated features, compute:
  - fp_feat  = first-post claude_med__feature (current V5 convention)
  - mean_feat = mean across all consensus-A posts in the episode

Run Cox with both, compare HR / p.
If similar → first-post choice doesn't bias results.
If different → first-post-only is a modeling assumption worth flagging.
"""
from __future__ import annotations
import warnings
from pathlib import Path
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]

FEATS = ['commitment_strength', 'hedging_level', 'specificity', 'audience_cost']
COLS_BT = [f'btz__{f}' for f in FEATS]

def main():
    eps_n = pd.read_parquet(ROOT / 'data/processed/episodes_with_hc_outcomes_narrow.parquet')
    af = pd.read_parquet(ROOT / 'data/processed/all_features.parquet')
    print(f'narrow episodes: {len(eps_n)}; consensus matched: {(eps_n["match_status"]=="consensus_match").sum()}')
    print(f'all consensus A posts: {len(af)}')

    # Compute episode-mean Claude features
    mean_feats = af.groupby('episode_id')[[f'claude_med__{f}' for f in FEATS]].mean().reset_index()
    mean_feats.columns = ['episode_id'] + [f'mean__claude_med__{f}' for f in FEATS]
    print(f'Episode-mean features computed for {len(mean_feats)} episodes')

    # Merge into modeling df
    df = eps_n.merge(mean_feats, on='episode_id', how='left')

    # Z-standardize both fp and mean
    for f in FEATS:
        fp_col = f'fp__claude_med__{f}'
        mean_col = f'mean__claude_med__{f}'
        df[f'fpZ__{f}'] = (df[fp_col] - df[fp_col].mean()) / df[fp_col].std()
        df[f'meanZ__{f}'] = (df[mean_col] - df[mean_col].mean()) / df[mean_col].std()

    # Build modeling sample
    df['event'] = df['y1_outcome'].isin(['executed','modified_or_withdrawn','struck_down']).astype(int)
    df['duration_days'] = df['anticipation_days']
    cutoff = pd.Timestamp('2026-05-12', tz='UTC')
    pending = df['duration_days'].isna()
    if pending.any():
        fp = pd.to_datetime(df.loc[pending,'first_post_date'], errors='coerce', utc=True)
        df.loc[pending,'duration_days'] = (cutoff - fp).dt.days
    df['duration_days'] = pd.to_numeric(df['duration_days'], errors='coerce')
    df = df[df['duration_days']>0].copy()

    fp_feats = [f'fpZ__{f}' for f in FEATS]
    mean_feats_z = [f'meanZ__{f}' for f in FEATS]

    df_fp = df.dropna(subset=fp_feats)
    df_mean = df.dropna(subset=mean_feats_z)

    print(f'\nfp modeling: N={len(df_fp)}, events={int(df_fp["event"].sum())}')
    print(f'mean modeling: N={len(df_mean)}, events={int(df_mean["event"].sum())}')

    from lifelines import CoxPHFitter

    def fit_and_boot(df, feats, label, n_boot=1000):
        cph = CoxPHFitter(penalizer=0.05)
        cph.fit(df[['duration_days','event']+feats], duration_col='duration_days', event_col='event')
        print(f'\n=== {label} ===')
        print(cph.summary[['exp(coef)','exp(coef) lower 95%','exp(coef) upper 95%','p']].round(3))
        rng = np.random.RandomState(42)
        boot = []
        for b in range(n_boot):
            idx = rng.choice(len(df), len(df), replace=True)
            try:
                c2 = CoxPHFitter(penalizer=0.05)
                c2.fit(df.iloc[idx][['duration_days','event']+feats], duration_col='duration_days', event_col='event')
                boot.append(c2.params_.to_dict())
            except: pass
        bdf = pd.DataFrame(boot)
        rows = []
        print('Bootstrap CIs:')
        for f in feats:
            s = bdf[f].dropna()
            if len(s)<100: continue
            lo, hi = np.percentile(np.exp(s), [2.5, 97.5])
            med = np.median(np.exp(s))
            p_emp = min((s>=0).mean(),(s<=0).mean())*2
            hr = cph.summary.loc[f,'exp(coef)']
            p_ana = cph.summary.loc[f,'p']
            star = '***' if p_emp<0.01 else ('**' if p_emp<0.05 else ('*' if p_emp<0.10 else ''))
            print(f'  {f:24s}  HR={hr:.2f}  [{lo:.2f},{hi:.2f}]  p_emp={p_emp:.3f}  {star}')
            rows.append({'label':label,'feature':f.split('__')[-1],'hr':hr,
                         'boot_lo':lo,'boot_hi':hi,'p_emp':p_emp,
                         'n':len(df),'events':int(df['event'].sum())})
        return rows

    rows1 = fit_and_boot(df_fp, fp_feats, 'V5 first-post 0-10 (current)')
    rows2 = fit_and_boot(df_mean, mean_feats_z, 'V8 episode-mean 0-10')

    out = pd.DataFrame(rows1 + rows2)
    out.to_parquet(ROOT / 'data/processed/cox_v8_aggregation_sensitivity.parquet')
    print(f'\n[saved] cox_v8_aggregation_sensitivity.parquet')

    # Side by side specificity
    print('\n=== Specificity side-by-side ===')
    spec = out[out['feature']=='specificity']
    print(spec[['label','n','events','hr','boot_lo','boot_hi','p_emp']].to_string(index=False))

    # Also check correlation between fp and mean features
    print('\n=== Within-episode feature consistency (multi-post episodes only) ===')
    multi = df[df['n_posts']>1]
    for f in FEATS:
        if len(multi) < 3: continue
        r = multi[[f'fp__claude_med__{f}', f'mean__claude_med__{f}']].corr().iloc[0,1]
        diff = (multi[f'mean__claude_med__{f}'] - multi[f'fp__claude_med__{f}']).abs().mean()
        print(f'  {f:24s}  r(fp, mean) = {r:.3f}  mean |diff| = {diff:.2f}')


if __name__ == '__main__':
    main()
