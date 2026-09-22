/** Client side helpers used by the EMI calculator for instant feedback. */

export function calculateEmi(principal, annualRate, months) {
  const p = Number(principal) || 0;
  const r = (Number(annualRate) || 0) / 12 / 100;
  const n = Number(months) || 1;
  const emi = r === 0 ? p / n : (p * r * (1 + r) ** n) / ((1 + r) ** n - 1);
  const totalPayment = emi * n;
  return {
    monthly_emi: Number(emi.toFixed(2)),
    total_interest: Number((totalPayment - p).toFixed(2)),
    total_payment: Number(totalPayment.toFixed(2)),
    principal: Number(p.toFixed(2)),
    interest_rate: Number(annualRate) || 0,
    tenure_months: n,
  };
}

export function amortisationSchedule(principal, annualRate, months, limit = 12) {
  const p = Number(principal) || 0;
  const r = (Number(annualRate) || 0) / 12 / 100;
  const n = Number(months) || 1;
  const emi = r === 0 ? p / n : (p * r * (1 + r) ** n) / ((1 + r) ** n - 1);
  let balance = p;
  const rows = [];
  for (let month = 1; month <= Math.min(n, limit); month += 1) {
    const interest = balance * r;
    const principalPart = emi - interest;
    balance -= principalPart;
    rows.push({
      month,
      emi: Number(emi.toFixed(2)),
      principal: Number(principalPart.toFixed(2)),
      interest: Number(interest.toFixed(2)),
      balance: Number(Math.max(balance, 0).toFixed(2)),
    });
  }
  return rows;
}

export function tenureLabel(months) {
  const years = Math.floor(months / 12);
  const rest = months % 12;
  if (!years) return `${rest} months`;
  if (!rest) return `${years} year${years > 1 ? "s" : ""}`;
  return `${years} yr ${rest} mo`;
}
