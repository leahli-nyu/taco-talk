// TACO Talk · main script
(function() {
  const D = window.appData || {};

  // Update dateline
  const dl = document.getElementById('dateline-date');
  if (dl) {
    const today = new Date();
    dl.textContent = today.toLocaleDateString('en-US', {
      year: 'numeric', month: 'long', day: 'numeric'
    });
  }

  // Populate big stats
  const big = document.getElementById('big-stats');
  if (big && D) {
    const s = D.summary || {};
    const y2 = D.y2_stats || {};

    const stats = [
      { num: (s.n_threats_total || 6943).toLocaleString(), label: 'Trump posts scanned' },
      { num: s.n_threats_tariff_adjacent || 102, label: 'Tariff-adjacent A-class' },
      { num: s.n_episodes_narrow || 77, label: 'Policy episodes' },
      { num: s.n_consensus_matches || 27, label: 'Cross-LLM matches' },
      { num: y2.n_event_study_obs || 118, label: 'CAR observations' },
      { num: (s.ground_truth && s.ground_truth.tier_1_n_events) || 43, label: 'Hand-compiled GT' },
      { num: (s.ground_truth && s.ground_truth.tier_2_n_eos) || 71, label: 'Federal Register EOs' },
      { num: '9', label: 'Cox specifications' },
    ];

    big.innerHTML = stats.map(s =>
      `<div class="big-stat">
        <div class="big-stat-num">${s.num}</div>
        <div class="big-stat-label">${s.label}</div>
      </div>`
    ).join('');
  }
})();
