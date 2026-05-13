"""Cox v7: human-validated matches (from Packet E annotation).

Rules:
- For each narrow episode, find user's answer in CONSENSUS or DISAGREE case (not fake)
- If user picked an event [N] -> use that event
- If user picked "tie [N]/[M]" -> use the earlier of the two (candidates are date-sorted)
- If user said "none" -> unmatched (censored)
- Episodes not in Packet E -> use original cross-LLM consensus match

This yields a "human-anchored" match set; reruns the Cox primary specification.
"""
from __future__ import annotations
import warnings, json
from pathlib import Path
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]


# Parse user answers
def parse_answers(fp):
    out = {}
    import re
    for line in open(fp):
        line = line.strip()
        if not line or line.startswith('#'): continue
        m = re.match(r'case_(\d+):\s*(.+)', line)
        if not m: continue
        case = int(m.group(1)); val = m.group(2).strip()
        if val.lower()=='none' or val=='0':
            out[case] = ('none', None)
        elif val.startswith('tie'):
            nums = [int(n) for n in re.findall(r'\d+', val)]
            out[case] = ('tie', nums[:2])
        elif val.isdigit():
            out[case] = ('pick', int(val))
    return out


def main():
    answers = parse_answers(ROOT / 'data/processed/packet_E_user_answers.txt')
    key = pd.read_parquet(ROOT / 'data/processed/annotation_packet_E_key.parquet')

    # Build episode -> (user_pick_evt_idx or None) lookup
    # Priority: consensus case over fake case (same episode_id may appear in both)
    # If only fake case exists for an episode, skip it (use original LLM consensus for that)
    ep_human_match = {}
    ep_user_decision = {}  # 'human_pick' / 'human_none' / 'no_packet'

    # First pass: consensus and disagree (use these as primary)
    for _, r in key.iterrows():
        ct = r['case_type']
        ep = int(r['episode_id'])
        item = int(r['item'])
        if item not in answers: continue
        if ct == 'fake': continue  # skip fakes for episode-level resolution
        kind, val = answers[item]
        if kind == 'pick':
            ep_human_match[ep] = val
            ep_user_decision[ep] = 'human_pick'
        elif kind == 'tie':
            ep_human_match[ep] = val[0]  # take first (earlier date)
            ep_user_decision[ep] = 'human_tie'
        else:  # none
            ep_human_match[ep] = None
            ep_user_decision[ep] = 'human_none'

    print(f'Human-resolved (pick or tie): {sum(1 for v in ep_human_match.values() if v is not None)}')
    print(f'Human said none:               {sum(1 for v in ep_human_match.values() if v is None)}')

    # Apply to narrow episodes
    eps_narrow = pd.read_parquet(ROOT / 'data/processed/episodes_v2_narrow.parquet')
    narrow_ids = set(eps_narrow['episode_id'])

    # Original cross-LLM consensus matches (V5)
    eps_hc = pd.read_parquet(ROOT / 'data/processed/episodes_with_hc_outcomes_narrow.parquet')
    # For each narrow episode:
    # if in ep_human_match: use that
    # else: fall back to original v5 consensus

    gt = json.load(open(ROOT / 'data/raw/tariff_timeline_ground_truth.json'))['events']
    bucket = {
        'in_effect': 'executed',
        'modified': 'modified_or_withdrawn',
        'withdrawn': 'modified_or_withdrawn',
        'paused': 'modified_or_withdrawn',
        'struck_down': 'struck_down',
        'investigation': 'investigation',
    }

    def assign(ep_id, first_post_date):
        if ep_id in ep_human_match:
            v = ep_human_match[ep_id]
            if v is None:
                return None, 'human_none'
            if v < 0 or v >= len(gt):
                print(f'[warn] invalid event idx {v} for episode {ep_id}; treating as none')
                return None, 'human_none'
            evt = gt[v]
            return evt, 'human_pick'
        # Fall back to original LLM consensus
        row = eps_hc[eps_hc['episode_id']==ep_id]
        if row.empty: return None, 'no_match'
        row = row.iloc[0]
        if row.get('match_status') == 'consensus_match' and not pd.isna(row.get('matched_evt_idx')):
            return gt[int(row['matched_evt_idx'])], 'llm_only'
        return None, 'no_match'

    new_rows = []
    for _, ep in eps_narrow.iterrows():
        evt, source = assign(ep['episode_id'], ep['first_post_date'])
        if evt is not None:
            ann_d = pd.to_datetime(evt['announced']).date()
            fp_d = pd.to_datetime(ep['first_post_date']).date()
            ant = (ann_d - fp_d).days
            y1 = bucket.get(evt['status'], 'other')
        else:
            ant = None
            y1 = 'no_policy_event_found'
        new_rows.append({
            **{k: ep[k] for k in eps_narrow.columns},
            'y1_outcome': y1,
            'anticipation_days': ant,
            'match_source': source,
        })
    final = pd.DataFrame(new_rows)
    final.to_parquet(ROOT / 'data/processed/episodes_with_human_validated_outcomes.parquet')
    print(f'\nSaved human-validated outcomes')
    print(f'Match source breakdown:')
    print(final['match_source'].value_counts())
    print(f'\nY1 outcome:')
    print(final['y1_outcome'].value_counts())

    # Cox v7
    bt = pd.read_parquet(ROOT / 'data/processed/episodes_bt_scores.parquet')
    FEATS = ['btz__commitment_strength','btz__hedging_level','btz__specificity','btz__audience_cost']

    df = final.merge(bt[['episode_id']+FEATS], on='episode_id', how='left')
    df['event'] = df['y1_outcome'].isin(['executed','modified_or_withdrawn','struck_down']).astype(int)
    df['duration_days'] = df['anticipation_days']
    cutoff = pd.Timestamp('2026-05-12', tz='UTC')
    pending = df['duration_days'].isna()
    if pending.any():
        fp = pd.to_datetime(df.loc[pending,'first_post_date'], errors='coerce', utc=True)
        df.loc[pending,'duration_days'] = (cutoff - fp).dt.days
    df['duration_days'] = pd.to_numeric(df['duration_days'], errors='coerce')
    df = df[df['duration_days']>0].dropna(subset=FEATS).copy()

    print(f'\n=== Cox v7 (human-validated) ===')
    print(f'N={len(df)}, events={int(df["event"].sum())}')

    from lifelines import CoxPHFitter
    cph = CoxPHFitter(penalizer=0.05)
    cph.fit(df[['duration_days','event']+FEATS], duration_col='duration_days', event_col='event')
    print(cph.summary[['exp(coef)','exp(coef) lower 95%','exp(coef) upper 95%','p']].round(3))

    # Bootstrap
    rng = np.random.RandomState(42)
    boot = []
    for b in range(1000):
        idx = rng.choice(len(df), len(df), replace=True)
        try:
            c2 = CoxPHFitter(penalizer=0.05)
            c2.fit(df.iloc[idx][['duration_days','event']+FEATS], duration_col='duration_days', event_col='event')
            boot.append(c2.params_.to_dict())
        except: pass
    bdf = pd.DataFrame(boot)

    print('\nBootstrap 95% CIs:')
    out_rows = []
    for f in FEATS:
        s = bdf[f].dropna()
        if len(s)<100: continue
        lo, hi = np.percentile(np.exp(s), [2.5, 97.5])
        med = np.median(np.exp(s))
        p_emp = min((s>=0).mean(),(s<=0).mean())*2
        hr = cph.summary.loc[f,'exp(coef)']
        p_ana = cph.summary.loc[f,'p']
        star = '***' if p_emp<0.01 else ('**' if p_emp<0.05 else ('*' if p_emp<0.10 else ''))
        print(f'  {f:32s}  HR={hr:.2f}  [{lo:.2f},{hi:.2f}]  p_emp={p_emp:.3f}  {star}')
        out_rows.append({'label':'V7 human-validated','feature':f.split('__')[-1],'hr':hr,
                         'boot_lo':lo,'boot_hi':hi,'boot_med':med,
                         'p_analytic':p_ana,'p_empirical':p_emp,
                         'n':len(df),'events':int(df['event'].sum())})
    pd.DataFrame(out_rows).to_parquet(ROOT / 'data/processed/cox_v7_summary.parquet')
    print(f'\n[saved] cox_v7_summary.parquet')


if __name__ == '__main__':
    main()
