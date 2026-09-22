/** Currency, date and text helpers used across every page. */

export function formatCurrency(value, { compact = false, decimals = 0 } = {}) {
  const amount = Number(value || 0);
  if (compact && Math.abs(amount) >= 10000000) {
    return `₹${(amount / 10000000).toFixed(2)} Cr`;
  }
  if (compact && Math.abs(amount) >= 100000) {
    return `₹${(amount / 100000).toFixed(2)} L`;
  }
  return `₹${amount.toLocaleString("en-IN", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  })}`;
}

export function formatSignedCurrency(value, type) {
  const sign = type === "CREDIT" ? "+" : "-";
  return `${sign}${formatCurrency(Math.abs(Number(value || 0)))}`;
}

export function formatDate(value, { withTime = false } = {}) {
  if (!value) return "-";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "-";
  return date.toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    ...(withTime ? { hour: "2-digit", minute: "2-digit" } : {}),
  });
}

export function relativeTime(value) {
  if (!value) return "";
  const diff = Date.now() - new Date(value).getTime();
  const minutes = Math.round(diff / 60000);
  if (minutes < 1) return "just now";
  if (minutes < 60) return `${minutes} min ago`;
  const hours = Math.round(minutes / 60);
  if (hours < 24) return `${hours} hr ago`;
  const days = Math.round(hours / 24);
  if (days < 30) return `${days} day${days === 1 ? "" : "s"} ago`;
  return formatDate(value);
}

export function greeting(date = new Date()) {
  const hour = date.getHours();
  if (hour < 12) return "Good Morning";
  if (hour < 17) return "Good Afternoon";
  if (hour < 21) return "Good Evening";
  return "Good Night";
}

export function initials(name = "") {
  return name
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join("");
}

export const TRANSACTION_CATEGORIES = [
  "Salary",
  "Food",
  "Shopping",
  "Travel",
  "Bills",
  "Entertainment",
  "Transfer",
  "Other",
];

export const LOAN_TYPES = [
  { value: "PERSONAL", label: "Personal Loan", defaultRate: 12.5, max: 1500000 },
  { value: "HOME", label: "Home Loan", defaultRate: 8.5, max: 10000000 },
  { value: "EDUCATION", label: "Education Loan", defaultRate: 7.25, max: 2500000 },
  { value: "VEHICLE", label: "Vehicle Loan", defaultRate: 9.75, max: 2000000 },
];

export const CATEGORY_COLORS = {
  Salary: "#16a34a",
  Food: "#f97316",
  Shopping: "#8b5cf6",
  Travel: "#0ea5e9",
  Bills: "#ef4444",
  Entertainment: "#ec4899",
  Transfer: "#64748b",
  Other: "#94a3b8",
};
