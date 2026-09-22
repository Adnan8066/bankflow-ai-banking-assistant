import { useCallback, useEffect, useState } from "react";
import {
  Box,
  Button,
  Divider,
  Grid,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import GroupIcon from "@mui/icons-material/Group";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";
import ReceiptLongIcon from "@mui/icons-material/ReceiptLong";
import RequestQuoteIcon from "@mui/icons-material/RequestQuote";
import HourglassBottomIcon from "@mui/icons-material/HourglassBottom";
import PaymentsIcon from "@mui/icons-material/Payments";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip as ChartTooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useNavigate } from "react-router-dom";

import DashboardCard from "../../components/DashboardCard.jsx";
import { ErrorAlert, Loader, PageHeader, SectionCard, StatusChip } from "../../components/Common.jsx";
import adminService from "../../services/adminService";
import { getErrorMessage } from "../../services/api";
import { CATEGORY_COLORS, formatCurrency } from "../../utils/formatCurrency.js";

export default function AdminDashboard() {
  const navigate = useNavigate();
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

  if (loading) return <Loader label="Loading bank employee dashboard..." minHeight="60vh" />;

  if (error) {
    return (
      <>
        <PageHeader title="Admin Dashboard" />
        <ErrorAlert message={error} onRetry={load} />
      </>
    );
  }

  const { totals, monthly_trend: trend, category_breakdown: categories } = data;

  return (
    <Box>
      <PageHeader
        title="Bank employee dashboard"
        subtitle="Demo portfolio overview across every fictional customer."
        action={
          <Button endIcon={<ArrowForwardIcon />} onClick={() => navigate("/admin/analytics")}>
            Open analytics
          </Button>
        }
      />

      <Grid container spacing={2.5}>
        <Grid item xs={12} sm={6} lg={4} xl={2}>
          <DashboardCard
            title="Total Customers"
            value={totals.customers}
            icon={<GroupIcon />}
            caption="Fictional demo customers"
            gradient="linear-gradient(135deg, #1b3a8f 0%, #4361ee 100%)"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={4} xl={2}>
          <DashboardCard
            title="Total Accounts"
            value={totals.accounts}
            icon={<AccountBalanceIcon />}
            caption={`Deposits ${formatCurrency(totals.total_deposits, { compact: true })}`}
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={4} xl={2}>
          <DashboardCard
            title="Total Transactions"
            value={totals.transactions}
            icon={<ReceiptLongIcon />}
            caption="Across all demo accounts"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={4} xl={2}>
          <DashboardCard
            title="Total Loans"
            value={totals.loans}
            icon={<RequestQuoteIcon />}
            caption={`Outstanding ${formatCurrency(totals.outstanding, { compact: true })}`}
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={4} xl={2}>
          <DashboardCard
            title="Pending Loans"
            value={totals.pending_loans}
            icon={<HourglassBottomIcon />}
            caption="Awaiting employee review"
            color="#f59e0b"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={4} xl={2}>
          <DashboardCard
            title="Demo Volume"
            value={formatCurrency(totals.demo_volume, { compact: true })}
            icon={<PaymentsIcon />}
            caption="Simulated transaction volume"
            color="#16a34a"
          />
        </Grid>
      </Grid>

      <Grid container spacing={2.5} sx={{ mt: 0.5 }}>
        <Grid item xs={12} lg={7}>
          <SectionCard title="Portfolio income vs expenses" subtitle="Last 6 months">
            <Box sx={{ height: 300 }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={trend}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#eef1f8" />
                  <XAxis dataKey="short_month" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `${v / 1000}k`} />
                  <ChartTooltip formatter={(value) => formatCurrency(value)} />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="income"
                    name="Income"
                    stroke="#16a34a"
                    strokeWidth={2.5}
                    dot={{ r: 3 }}
                  />
                  <Line
                    type="monotone"
                    dataKey="expense"
                    name="Expense"
                    stroke="#e11d48"
                    strokeWidth={2.5}
                    dot={{ r: 3 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </Box>
          </SectionCard>
        </Grid>

        <Grid item xs={12} lg={5}>
          <SectionCard title="Demo transaction volume by category" subtitle="All customers">
            <Box sx={{ height: 300 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={categories}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#eef1f8" />
                  <XAxis dataKey="category" tick={{ fontSize: 11 }} interval={0} angle={-20} dy={10} height={50} />
                  <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `${v / 1000}k`} />
                  <ChartTooltip formatter={(value) => formatCurrency(value)} />
                  <Bar dataKey="amount" name="Amount" radius={[6, 6, 0, 0]} maxBarSize={38}>
                    {categories.map((entry) => (
                      <Cell key={entry.category} fill={entry.color || CATEGORY_COLORS[entry.category]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </Box>
          </SectionCard>
        </Grid>

        <Grid item xs={12} md={5}>
          <SectionCard title="Loan status mix" subtitle="Every demo loan application">
            <Box sx={{ height: 240 }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={data.loan_status_breakdown.filter((item) => item.count > 0)}
                    dataKey="count"
                    nameKey="label"
                    innerRadius={50}
                    outerRadius={82}
                    paddingAngle={3}
                  >
                    {data.loan_status_breakdown.map((entry, index) => (
                      <Cell
                        key={entry.status}
                        fill={["#f59e0b", "#0ea5e9", "#e11d48", "#16a34a", "#64748b"][index % 5]}
                      />
                    ))}
                  </Pie>
                  <ChartTooltip />
                </PieChart>
              </ResponsiveContainer>
            </Box>
            <Stack spacing={1} sx={{ mt: 1 }}>
              {data.loan_status_breakdown.map((item) => (
                <Stack key={item.status} direction="row" justifyContent="space-between">
                  <StatusChip status={item.status} />
                  <Typography variant="body2" fontWeight={700}>
                    {item.count}
                  </Typography>
                </Stack>
              ))}
            </Stack>
          </SectionCard>
        </Grid>

        <Grid item xs={12} md={7}>
          <SectionCard
            title="Top customers by balance"
            subtitle="Fictional demo customers only"
            action={
              <Button size="small" onClick={() => navigate("/admin/customers")}>
                Manage customers
              </Button>
            }
          >
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Customer</TableCell>
                    <TableCell align="right">Balance</TableCell>
                    <TableCell align="right">Transactions</TableCell>
                    <TableCell align="right">Loans</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {data.top_customers.map((customer) => (
                    <TableRow key={customer.id} hover>
                      <TableCell>
                        <Typography variant="body2" fontWeight={600}>
                          {customer.name}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {customer.email}
                        </Typography>
                      </TableCell>
                      <TableCell align="right">{formatCurrency(customer.balance)}</TableCell>
                      <TableCell align="right">{customer.transactions}</TableCell>
                      <TableCell align="right">{customer.loans}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
            <Divider sx={{ my: 2 }} />
            <Stack direction="row" spacing={2} sx={{ flexWrap: "wrap", gap: 2 }}>
              {data.transaction_type_split.map((item) => (
                <Box key={item.type}>
                  <Typography variant="caption" color="text.secondary">
                    {item.label}
                  </Typography>
                  <Typography variant="h6">{item.count}</Typography>
                </Box>
              ))}
            </Stack>
          </SectionCard>
        </Grid>
      </Grid>
    </Box>
  );
}
