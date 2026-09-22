import { useCallback, useEffect, useState } from "react";
import { Box, Chip, Grid, Stack, Typography } from "@mui/material";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Pie,
  PieChart,
  RadialBar,
  RadialBarChart,
  ResponsiveContainer,
  Tooltip as ChartTooltip,
  XAxis,
  YAxis,
} from "recharts";

import { ErrorAlert, Loader, PageHeader, SectionCard } from "../../components/Common.jsx";
import adminService from "../../services/adminService";
import { getErrorMessage } from "../../services/api";
import { CATEGORY_COLORS, formatCurrency } from "../../utils/formatCurrency.js";

export default function AdminAnalytics() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setData(await adminService.analytics());
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  if (loading) return <Loader label="Crunching demo analytics..." minHeight="60vh" />;
  if (error) {
    return (
      <>
        <PageHeader title="Analytics" />
        <ErrorAlert message={error} onRetry={load} />
      </>
    );
  }

  const { totals, monthly_trend: trend, category_breakdown: categories } = data;
  const radialData = [
    {
      name: "Loans",
      value: totals.loans ? Math.round((totals.active_loans / totals.loans) * 100) : 0,
      fill: "#4361ee",
    },
  ];

  return (
    <Box>
      <PageHeader
        title="Analytics Dashboard"
        subtitle="Aggregated charts for the fictional BankFlow demo portfolio."
        action={<Chip label="Demo data" color="primary" variant="outlined" />}
      />

      <Grid container spacing={2.5}>
        <Grid item xs={12}>
          <SectionCard title="Monthly income vs expense trend" subtitle="Last 6 months, all customers">
            <Box sx={{ height: 320 }}>
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={trend}>
                  <defs>
                    <linearGradient id="aIncome" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#16a34a" stopOpacity={0.35} />
                      <stop offset="95%" stopColor="#16a34a" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="aExpense" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#e11d48" stopOpacity={0.35} />
                      <stop offset="95%" stopColor="#e11d48" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#eef1f8" />
                  <XAxis dataKey="month" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `${v / 1000}k`} />
                  <ChartTooltip formatter={(value) => formatCurrency(value)} />
                  <Legend />
                  <Area
                    type="monotone"
                    dataKey="income"
                    name="Income"
                    stroke="#16a34a"
                    fill="url(#aIncome)"
                    strokeWidth={2}
                  />
                  <Area
                    type="monotone"
                    dataKey="expense"
                    name="Expense"
                    stroke="#e11d48"
                    fill="url(#aExpense)"
                    strokeWidth={2}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </Box>
          </SectionCard>
        </Grid>

        <Grid item xs={12} lg={6}>
          <SectionCard title="Expense by category" subtitle="Portfolio-wide debit split">
            <Box sx={{ height: 300 }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={categories}
                    dataKey="amount"
                    nameKey="category"
                    outerRadius={100}
                    label={(entry) => entry.category}
                  >
                    {categories.map((entry) => (
                      <Cell key={entry.category} fill={entry.color || CATEGORY_COLORS[entry.category]} />
                    ))}
                  </Pie>
                  <ChartTooltip formatter={(value) => formatCurrency(value)} />
                </PieChart>
              </ResponsiveContainer>
            </Box>
          </SectionCard>
        </Grid>

        <Grid item xs={12} lg={6}>
          <SectionCard title="Transaction count per month" subtitle="Activity volume">
            <Box sx={{ height: 300 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={trend}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#eef1f8" />
                  <XAxis dataKey="short_month" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} allowDecimals={false} />
                  <ChartTooltip />
                  <Bar
                    dataKey="transactions"
                    name="Transactions"
                    fill="#0ea5e9"
                    radius={[6, 6, 0, 0]}
                    maxBarSize={42}
                  />
                </BarChart>
              </ResponsiveContainer>
            </Box>
          </SectionCard>
        </Grid>

        <Grid item xs={12} md={5}>
          <SectionCard title="Active loan ratio" subtitle="Share of loans currently running">
            <Box sx={{ height: 260 }}>
              <ResponsiveContainer width="100%" height="100%">
                <RadialBarChart
                  data={radialData}
                  innerRadius="62%"
                  outerRadius="100%"
                  startAngle={90}
                  endAngle={-270}
                >
                  <RadialBar dataKey="value" background cornerRadius={12} />
                </RadialBarChart>
              </ResponsiveContainer>
            </Box>
            <Stack alignItems="center" spacing={0.5}>
              <Typography variant="h4">{radialData[0].value}%</Typography>
              <Typography variant="caption" color="text.secondary">
                {totals.active_loans} of {totals.loans} demo loans are active
              </Typography>
            </Stack>
          </SectionCard>
        </Grid>

        <Grid item xs={12} md={7}>
          <SectionCard title="Portfolio summary" subtitle="Key demo numbers">
            <Grid container spacing={2}>
              {[
                ["Total customers", totals.customers],
                ["Total accounts", totals.accounts],
                ["Total transactions", totals.transactions],
                ["Total loans", totals.loans],
                ["Pending loans", totals.pending_loans],
                ["Unread notifications", totals.unread_notifications],
                ["Total deposits", formatCurrency(totals.total_deposits)],
                ["Outstanding loans", formatCurrency(totals.outstanding)],
                ["Demo transaction volume", formatCurrency(totals.demo_volume)],
              ].map(([label, value]) => (
                <Grid item xs={12} sm={6} md={4} key={label}>
                  <Box sx={{ p: 2, borderRadius: 2, backgroundColor: "#f8f9fd" }}>
                    <Typography variant="caption" color="text.secondary">
                      {label}
                    </Typography>
                    <Typography variant="h6">{value}</Typography>
                  </Box>
                </Grid>
              ))}
            </Grid>
          </SectionCard>
        </Grid>
      </Grid>
    </Box>
  );
}
