document.addEventListener('DOMContentLoaded', () => {
  // Initialize Lucide Icons
  lucide.createIcons();

  // Elements
  const loanForm = document.getElementById('loan-form');
  const submitBtn = document.getElementById('submit-btn');
  const spinner = submitBtn.querySelector('.loader-spinner');
  const btnText = submitBtn.querySelector('span');
  const btnArrow = submitBtn.querySelector('.btn-arrow');
  
  const hdiSlider = document.getElementById('hdiIndex');
  const hdiBadge = document.getElementById('hdi-value-badge');

  const loanList = document.getElementById('loan-list');
  const emptyState = document.getElementById('empty-state');
  const skeleton = document.getElementById('loading-skeleton');
  const refreshBtn = document.getElementById('refresh-btn');

  // KPI elements
  const kpiTotal = document.getElementById('kpi-total');
  const kpiApproval = document.getElementById('kpi-approval');
  const kpiCredit = document.getElementById('kpi-credit');
  const kpiAmount = document.getElementById('kpi-amount');
  const kpiApprovalSub = document.getElementById('kpi-approval-sub');

  // Modal elements
  const modal = document.getElementById('verdict-modal');
  const closeModalBtn = document.getElementById('close-modal-btn');
  const modalName = document.getElementById('modal-borrower-name');
  const modalProbabilityVal = document.getElementById('modal-probability-val');
  const modalProbabilityFill = document.getElementById('modal-probability-fill');
  const modalStatus = document.getElementById('modal-status');
  const modalRiskRating = document.getElementById('modal-risk-rating');
  const modalCredit = document.getElementById('modal-credit-score');
  const modalHdi = document.getElementById('modal-hdi-index');
  const modalAmount = document.getElementById('modal-loan-amount');
  const modalTerm = document.getElementById('modal-monthly-payment');
  const modalVerdictBadge = document.getElementById('modal-verdict-badge');
  const adviceCard = document.getElementById('modal-recommendation-card');
  const adviceTitle = document.getElementById('verdict-title');
  const adviceDesc = document.getElementById('verdict-description');

  // Dynamic slider update
  hdiSlider.addEventListener('input', (e) => {
    hdiBadge.textContent = parseFloat(e.target.value).toFixed(2);
  });

  // Open / Close Modal Logic
  const openModal = (loan) => {
    modalName.textContent = loan.borrowerName;
    
    const probPercentage = Math.round(loan.probability * 100);
    modalProbabilityVal.textContent = `${probPercentage}%`;
    modalProbabilityFill.style.width = `${probPercentage}%`;

    modalStatus.textContent = loan.status;
    modalRiskRating.textContent = loan.riskRating;
    modalCredit.textContent = loan.creditScore;
    modalHdi.textContent = parseFloat(loan.hdiIndex).toFixed(2);
    modalAmount.textContent = `$${loan.loanAmount.toLocaleString()}`;
    
    const monthlyAmort = Math.round(loan.loanAmount / loan.loanTerm);
    modalTerm.textContent = `$${monthlyAmort.toLocaleString()}/mo`;

    // Reset status classes
    modalStatus.className = 'detail-value';
    modalRiskRating.className = 'detail-value';
    modalVerdictBadge.className = 'verdict-icon-container';
    adviceCard.className = 'modal-verdict-card';

    if (loan.status === 'APPROVED') {
      modalStatus.classList.add('text-emerald');
      modalVerdictBadge.textContent = '✔';
      modalVerdictBadge.classList.add('approved');
      adviceCard.classList.add('approved-advice');
      adviceTitle.textContent = 'Model Approval Recommendation';
      
      let riskNote = 'Borrower meets credit score requirements. ';
      if (loan.riskRating === 'LOW') {
        modalRiskRating.classList.add('text-emerald');
        riskNote += 'The low debt-to-income profile indicates high financial resilience. Proceed with fast-track underwriting.';
      } else {
        modalRiskRating.classList.add('text-amber');
        riskNote += 'The moderate debt profile suggests minor monitoring. Standard loan terms apply.';
      }
      adviceDesc.textContent = riskNote;
    } else {
      modalStatus.classList.add('text-red');
      modalRiskRating.classList.add('text-red');
      modalVerdictBadge.textContent = '✖';
      modalVerdictBadge.classList.add('rejected');
      adviceCard.classList.add('rejected-advice');
      adviceTitle.textContent = 'Risk Advisory & Reject Details';
      
      let rejectNote = 'Application fails core underwriting metrics. ';
      if (loan.creditScore < 500) {
        rejectNote += 'Reason: Credit score falls below critical risk cutoff of 500. ';
      }
      const monthlyPayment = (loan.loanAmount / loan.loanTerm);
      if (monthlyPayment > (loan.income / 12) * 0.45) {
        rejectNote += 'Reason: Monthly payment exceeds 45% debt-to-income limit. ';
      }
      rejectNote += 'Advise restructuring by requesting a lower loan principal or introducing a qualified co-signer.';
      adviceDesc.textContent = rejectNote;
    }

    modal.classList.remove('hidden');
  };

  const closeModal = () => {
    modal.classList.add('hidden');
  };

  closeModalBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });

  // Fetch and update metrics
  const fetchStats = async () => {
    try {
      const res = await fetch('/api/loans/stats');
      if (!res.ok) throw new Error('Stats API failed');
      const stats = await res.json();

      kpiTotal.textContent = stats.totalApplications.toLocaleString();
      
      const appRatePercent = Math.round(stats.approvalRate * 100);
      kpiApproval.textContent = `${appRatePercent}%`;
      kpiApprovalSub.textContent = `${stats.approvedCount} approved vs ${stats.rejectedCount} rejected`;

      kpiCredit.textContent = stats.averageCreditScore > 0 ? stats.averageCreditScore : '-';
      kpiAmount.textContent = stats.averageLoanAmount > 0 ? `$${stats.averageLoanAmount.toLocaleString()}` : '-';
    } catch (err) {
      console.error('Error fetching statistics:', err);
    }
  };

  // Render log list
  const renderLoans = (loans) => {
    loanList.innerHTML = '';
    
    if (loans.length === 0) {
      emptyState.classList.remove('hidden');
      return;
    }

    emptyState.classList.add('hidden');
    loans.forEach(loan => {
      const li = document.createElement('li');
      li.className = 'loan-item';
      li.addEventListener('click', () => openModal(loan));

      const isApproved = loan.status === 'APPROVED';
      const badgeClass = isApproved ? 'badge-approved' : 'badge-rejected';
      const probPercent = Math.round(loan.probability * 100);

      li.innerHTML = `
        <div class="loan-item-info">
          <span class="borrower-name">${loan.borrowerName}</span>
          <div class="loan-sub-info">
            <span>Score: ${loan.creditScore}</span>
            <span>$${loan.loanAmount.toLocaleString()}</span>
            <span>Term: ${loan.loanTerm}mo</span>
          </div>
        </div>
        <div class="loan-action-badge">
          <span class="badge ${badgeClass}">${loan.status}</span>
          <span class="probability-indicator">${probPercent}%</span>
        </div>
      `;
      loanList.appendChild(li);
    });
  };

  // Fetch list
  const fetchLoans = async () => {
    skeleton.classList.remove('hidden');
    loanList.classList.add('hidden');
    emptyState.classList.add('hidden');

    try {
      const res = await fetch('/api/loans');
      if (!res.ok) throw new Error('Loans API failed');
      const loans = await res.json();
      renderLoans(loans);
    } catch (err) {
      console.error('Error fetching loans list:', err);
      loanList.innerHTML = `<li class="loan-item text-red" style="pointer-events: none; justify-content: center;">Failed to retrieve credit logs.</li>`;
      loanList.classList.remove('hidden');
    } finally {
      skeleton.classList.add('hidden');
      loanList.classList.remove('hidden');
    }
  };

  // Form submission handler
  loanForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Toggle loading UI
    submitBtn.disabled = true;
    spinner.classList.remove('hidden');
    btnText.textContent = 'Analyzing credit risk...';
    btnArrow.classList.add('hidden');

    const payload = {
      borrowerName: document.getElementById('borrowerName').value,
      age: parseInt(document.getElementById('age').value),
      creditScore: parseInt(document.getElementById('creditScore').value),
      income: parseFloat(document.getElementById('income').value),
      loanAmount: parseFloat(document.getElementById('loanAmount').value),
      loanTerm: parseInt(document.getElementById('loanTerm').value),
      hdiIndex: parseFloat(hdiSlider.value)
    };

    try {
      const res = await fetch('/api/loans', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error('Submission endpoint rejected application');
      
      const newLoanRecord = await res.json();
      
      // Reset form fields
      loanForm.reset();
      hdiBadge.textContent = '0.75';
      hdiSlider.value = '0.75';

      // Reload dashboard list & statistics
      await fetchStats();
      await fetchLoans();

      // Show model details modal directly
      openModal(newLoanRecord);
    } catch (err) {
      alert(`Analytic Prediction Error: ${err.message}`);
    } finally {
      submitBtn.disabled = false;
      spinner.classList.add('hidden');
      btnText.textContent = 'Calculate Prediction Verdict';
      btnArrow.classList.remove('hidden');
    }
  });

  // Manual refresh trigger
  refreshBtn.addEventListener('click', () => {
    fetchStats();
    fetchLoans();
  });

  // Initial load
  fetchStats();
  fetchLoans();
});
