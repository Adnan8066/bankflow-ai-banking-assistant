import { useCallback, useEffect, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  Grid,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Skeleton,
  Stack,
  Tab,
  Tabs,
  Typography,
} from "@mui/material";
import AccountBalanceWalletIcon from "@mui/icons-material/AccountBalanceWallet";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import TrendingDownIcon from "@mui/icons-material/TrendingDown";
import RequestQuoteIcon from "@mui/icons-material/RequestQuote";
import ReceiptLongIcon from "@mui/icons-material/ReceiptLong";
import CalculateIcon from "@mui/icons-material/Calculate";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import NotificationsActiveIcon from "@mui/icons-material/NotificationsActive";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
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
  ResponsiveContainer,
  Tooltip as ChartTooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useNavigate } from "react-router-dom";

import DashboardCard from "../components/DashboardCard.jsx";
import { EmptyState, ErrorAlert, Loader, PageHeader, SectionCard, StatusChip } from "../components/Common.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import bankingService from "../services/bankingService";
import { getErrorMessage } from "../services/api";
import {
  CATEGORY_COLORS,
  formatCurrency,
  formatDate,
  greeting,
} from "../utils/formatCurrency.js";

const QUICK_ACTIONS = [
  { label: "View Transactions", icon: <ReceiptLongIcon />, to: "/transactions" },
  { label: "Apply for Loan", icon: <RequestQuoteIcon />, to: "/loans" },
  { label: "Ask AI Assistant", icon: <SmartToyIcon />, to: "/assistant" },
  { label: "EMI Calculator", icon: <CalculateIcon />, to: "/emi-calculator" },
];

export default function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [trendTab, setTrendTab] = useState("both");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const [dashboard, notif] = await Promise.all([
        bankingService.getDashboard(),
        bankingService.getNotifications(),
      ]);
      setData(dashboard);
      setNotifications(notif.slice(0, 4));
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  if (loading) return <Loader label="Loading your banking dashboard..." minHeight="60vh" />;

  if (error) {
    return (
      <>
        <PageHeader title="Dashboard" />
        <ErrorAlert message={error} onRetry={load} />
      </>
    );
  }

  const firstName = (user?.name || "Customer").split(" ")[0];
  const categories = data.spending_categories || [];
  const trend = data.monthly_trend || [];

  return (
    <Box>
      <PageHeader
        title={`${greeting()}, ${firstName}`}
        subtitle={`Here is your financial snapshot for ${new Date().toLocaleDateString("en-IN", {
          month: "long",
          year: "numeric",
        })}. All figures are simulated demo data.`}
        action={
          <Chip
            color="primary"
            variant="outlined"
            icon={<AccountBalanceWalletIcon />}
            label="Demo account"
          />
        }
      />

      {/* -------------------------------------------------------------- cards */}
      <Grid container spacing={2.5}>
        <Grid item xs={12} sm={6} lg={3}>
          <DashboardCard
            title="Available Balance"
            value={formatCurrency(data.balance)}
            icon={<AccountBalanceWalletIcon />}
            caption="Across all active demo accounts"
            gradient="linear-gradient(135deg, #1b3a8f 0%, #4361ee 100%)"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <DashboardCard
            title="Monthly Income"
            value={formatCurrency(data.monthly_income)}
            icon={<TrendingUpIcon />}
            caption="Salary and other credits"
            color="#16a34a"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <DashboardCard
            title="Monthly Expenses"
            value={formatCurrency(data.monthly_expenses)}
            icon={<TrendingDownIcon />}
            caption="vs last month"
            trend={data.expense_change_percent}
            color="#e11d48"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <DashboardCard
            title="Active Loans"
            value={data.active_loans}
            icon={<RequestQuoteIcon />}
            caption={`${formatCurrency(data.monthly_emi_total)} monthly EMI`}
            color="#f59e0b"
          />
        </Grid>
      </Grid>

      {/* ----------------------------------------------------- quick actions */}
      <SectionCard
        title="Quick actions"
        subtitle="Jump straight into the most used demo features"
        sx={{ mt: 2.5 }}
      >
        <Grid container spacing={2}>
          {QUICK_ACTIONS.map((action) => (
            <Grid item xs={12} sm={6} md={3} key={action.label}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={action.icon}
                onClick={() => navigate(action.to)}
                sx={{ justifyContent: "flex-start", py: 1.4 }}
              >
                {action.label}
              </Button>
            </Grid>
          ))}
        </Grid>
      </SectionCard>

      {/* ------------------------------------------------------------ charts */}
      <Grid container spacing={2.5} sx={{ mt: 0.5 }}>
        <Grid item xs={12} lg={8}>
          <SectionCard
            title="Income vs Expenses"
            subtitle="Last 6 months (demo data)"
            action={
              <Tabs
                value={trendTab}
                onChange={(_, value) => setTrendTab(value)}
                sx={{ minHeight: 34 }}
              >
                <Tab value="both" label="Both" sx={{ minHeight: 34, fontSize: 12 }} />
                <Tab value="income" label="Income" sx={{ minHeight: 34, fontSize: 12 }} />
                <Tab value="expense" label="Expense" sx={{ minHeight: 34, fontSize: 12 }} />
              </Tabs>
            }
          >
            <Box sx={{ height: 300 }}>
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={trend}>
                  <defs>
                    <linearGradient id="incomeFill" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#16a34a" stopOpacity={0.35} />
                      <stop offset="95%" stopColor="#16a34a" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="expenseFill" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#e11d48" stopOpacity={0.35} />
                      <stop offset="95%" stopColor="#e11d48" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#eef1f8" />
                  <XAxis dataKey="short_month" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} tickFormatter={(value) => `${value / 1000}k`} />
                  <ChartTooltip formatter={(value) => formatCurrency(value)} />
                  <Legend />
                  {trendTab !== "expense" && (
                    <Area
                      type="monotone"
                      dataKey="income"
                      name="Income"
                      stroke="#16a34a"
                      fill="url(#incomeFill)"
                      strokeWidth={2}
                    />
                  )}
                  {trendTab !== "income" && (
                    <Area
                      type="monotone"
                      dataKey="expense"
                      name="Expense"
                      stroke="#e11d48"
                      fill="url(#expenseFill)"
                      strokeWidth={2}
                    />
                  )}
                </AreaChart>
              </ResponsiveContainer>
            </Box>
          </SectionCard>
        </Grid>

        <Grid item xs={12} lg={4}>
          <SectionCard title="Spending by category" subtitle="This month">
            {categories.length === 0 ? (
              <EmptyState title="No spending yet" description="Debit transactions will appear here." />
            ) : (
              <>
                <Box sx={{ height: 210 }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={categories}
                        dataKey="amount"
                        nameKey="category"
                        innerRadius={52}
                        outerRadius={82}
                        paddingAngle={3}
                      >
                        {categories.map((entry) => (
                          <Cell
                            key={entry.category}
                            fill={entry.color || CATEGORY_COLORS[entry.category] || "#94a3b8"}
                          />
                        ))}
                      </Pie>
                      <ChartTooltip formatter={(value) => formatCurrency(value)} />
                    </PieChart>
                  </ResponsiveContainer>
                </Box>
                <Stack spacing={1} sx={{ mt: 1 }}>
                  {categories.slice(0, 5).map((item) => (
                    <Stack key={item.category} direction="row" justifyContent="space-between">
                      <Stack direction="row" spacing={1} alignItems="center">
                        <Box
                          sx={{
                            width: 10,
                            height: 10,
                            borderRadius: "50%",
                            backgroundColor: item.color || CATEGORY_COLORS[item.category],
                          }}
                        />
                        <Typography variant="body2">{item.category}</Typography>
                      </Stack>
                      <Typography variant="body2" fontWeight={700}>
                        {formatCurrency(item.amount)}
                      </Typography>
                    </Stack>
                  ))}
                </Stack>
              </>
            )}
          </SectionCard>
        </Grid>

        <Grid item xs={12} md={7}>
          <SectionCard title="Monthly spending trend" subtitle="Number of transactions per month">
            <Box sx={{ height: 260 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={trend}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#eef1f8" />
                  <XAxis dataKey="short_month" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} allowDecimals={false} />
                  <ChartTooltip />
                  <Legend />
                  <Bar
                    dataKey="transactions"
                    name="Transactions"
                    fill="#4361ee"
                    radius={[6, 6, 0, 0]}
                    maxBarSize={44}
                  />
                </BarChart>
              </ResponsiveContainer>
            </Box>
          </SectionCard>
        </Grid>

        <Grid item xs={12} md={5}>
          <SectionCard title="Loan status" subtitle="Demo loan applications">
            <Stack spacing={1.5}>
              {(data.loan_status_breakdown || []).map((item) => (
                <Stack key={item.status} direction="row" justifyContent="space-between" alignItems="center">
                  <Stack direction="row" spacing={1.25} alignItems="center">
                    <StatusChip status={item.status} />
                    <Typography variant="body2" color="text.secondary">
                      {item.label}
                    </Typography>
                  </Stack>
                  <Typography variant="h6">{item.count}</Typography>
                </Stack>
              ))}
              <Divider sx={{ my: 0.5 }} />
              <Stack direction="row" justifyContent="space-between">
                <Typography variant="body2" color="text.secondary">
                  Total outstanding
                </Typography>
                <Typography variant="body2" fontWeight={700}>
                  {formatCurrency(data.total_outstanding)}
                </Typography>
              </Stack>
              <Stack direction="row" justifyContent="space-between">
                <Typography variant="body2" color="text.secondary">
                  Monthly EMI total
                </Typography>
                <Typography variant="body2" fontWeight={700}>
                  {formatCurrency(data.monthly_emi_total)}
                </Typography>
              </Stack>
              <Button endIcon={<ArrowForwardIcon />} onClick={() => navigate("/loans")}>
                Manage loans
              </Button>
            </Stack>
          </SectionCard>
        </Grid>
      </Grid>

      {/* --------------------------------------------- transactions + alerts */}
      <Grid container spacing={2.5} sx={{ mt: 0.5 }}>
        <Grid item xs={12} md={8}>
          <SectionCard
            title="Recent transactions"
            subtitle="Latest 5 movements in your demo account"
            action={
              <Button size="small" endIcon={<ArrowForwardIcon />} onClick={() => navigate("/transactions")}>
                View all
              </Button>
            }
          >
            <List disablePadding>
              {(data.recent_transactions || []).map((txn, index) => (
                <Box key={txn.id}>
                  <ListItem
                    disableGutters
                    sx={{ cursor: "pointer" }}
                    onClick={() => navigate(`/transactions/${txn.id}`)}
                    secondaryAction={
                      <Typography
                        fontWeight={700}
                        color={txn.transaction_type === "CREDIT" ? "success.main" : "text.primary"}
                      >
                        {txn.transaction_type === "CREDIT" ? "+" : "-"}
                        {formatCurrency(txn.amount)}
                      </Typography>
                    }
                  >
                    <ListItemAvatar>
                      <Box
                        sx={{
                          display: "grid",
                          placeItems: "center",
                          width: 40,
                          height: 40,
                          borderRadius: 2,
                          backgroundColor: "#f2f5fd",
                          color: "primary.main",
                        }}
                      >
                        {txn.transaction_type === "CREDIT" ? (
                          <TrendingUpIcon fontSize="small" />
                        ) : (
                          <TrendingDownIcon fontSize="small" />
                        )}
                      </Box>
                    </ListItemAvatar>
                    <ListItemText
                      primary={txn.description}
                      secondary={`${formatDate(txn.date)} • ${txn.category} • ${txn.transaction_id}`}
                      primaryTypographyProps={{ fontWeight: 600, fontSize: 14 }}
                    />
                  </ListItem>
                  {index < data.recent_transactions.length - 1 && <Divider component="li" />}
                </Box>
              ))}
            </List>
          </SectionCard>
        </Grid>

        <Grid item xs={12} md={4}>
          <SectionCard
            title="Notifications"
            subtitle={`${data.unread_notifications} unread`}
            action={
              <Button size="small" onClick={() => navigate("/notifications")}>
                See all
              </Button>
            }
          >
            {notifications.length === 0 ? (
              <EmptyState title="No notifications" description="Simulated alerts will appear here." />
            ) : (
              <Stack spacing={1.5}>
                {notifications.map((item) => (
                  <Stack
                    key={item.id}
                    direction="row"
                    spacing={1.5}
                    alignItems="flex-start"
                    sx={{ p: 1.25, borderRadius: 2, backgroundColor: item.is_read ? "#fbfcff" : "#eef2fd" }}
                  >
                    <NotificationsActiveIcon fontSize="small" color="primary" />
                    <Box>
                      <Typography variant="subtitle2" fontSize={13}>
                        {item.title}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {item.message.length > 90 ? `${item.message.slice(0, 90)}...` : item.message}
                      </Typography>
                    </Box>
                  </Stack>
                ))}
              </Stack>
            )}
          </SectionCard>
        </Grid>
      </Grid>

      <Alert severity="info" sx={{ mt: 3, borderRadius: 3 }}>
        BankFlow is a demonstration application. Balances, transactions, loans and notifications are
        fictional and no real money movement takes place.
      </Alert>
    </Box>
  );
}
