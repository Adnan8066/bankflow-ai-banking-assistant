import { useEffect, useMemo, useState } from "react";
import {
  Alert,
  Box,
  Card,
  CardContent,
  Divider,
  Grid,
  MenuItem,
  Slider,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import CalculateIcon from "@mui/icons-material/Calculate";
import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip as ChartTooltip } from "recharts";

import { PageHeader, SectionCard } from "../components/Common.jsx";
import bankingService from "../services/bankingService";
import { LOAN_TYPES, formatCurrency } from "../utils/formatCurrency.js";
import { amortisationSchedule, calculateEmi, tenureLabel } from "../utils/calculations.js";

export default function EMICalculator() {
  const [loanAmount, setLoanAmount] = useState(500000);
  const [interestRate, setInterestRate] = useState(9.5);
  const [tenureMonths, setTenureMonths] = useState(60);
  const [loanType, setLoanType] = useState("PERSONAL");
  const [serverResult, setServerResult] = useState(null);
  const [serverError, setServerError] = useState("");

  const result = useMemo(
    () => calculateEmi(loanAmount, interestRate, tenureMonths),
    [loanAmount, interestRate, tenureMonths]
  );

  const schedule = useMemo(
    () => amortisationSchedule(loanAmount, interestRate, tenureMonths, 12),
    [loanAmount, interestRate, tenureMonths]
  );

  const donutData = [
    { name: "Principal", value: result.principal, color: "#1b3a8f" },
    { name: "Total interest", value: result.total_interest, color: "#0ea5e9" },
  ];

  // Confirm the client side maths with the Django endpoint (also demonstrates the API).
  useEffect(() => {
    let cancelled = false;
    const timer = setTimeout(async () => {
      try {
        const data = await bankingService.calculateEmi({
          loan_amount: loanAmount,
          interest_rate: interestRate,
          tenure_months: tenureMonths,
        });
        if (!cancelled) {
          setServerResult(data);
          setServerError("");
        }
      } catch {
        if (!cancelled) {
          setServerResult(null);
          setServerError("Server verification unavailable - showing locally calculated values.");
        }
      }
    }, 450);
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [loanAmount, interestRate, tenureMonths]);

  const applyLoanType = (event) => {
    const selected = LOAN_TYPES.find((type) => type.value === event.target.value);
    setLoanType(event.target.value);
    if (selected) setInterestRate(selected.defaultRate);
  };

  return (
    <Box>
      <PageHeader
        title="EMI Calculator"
        subtitle="Adjust the amount, rate and tenure to see the EMI update instantly."
      />

      <Grid container spacing={2.5}>
        <Grid item xs={12} md={7}>
          <SectionCard title="Loan inputs" subtitle="Values are not saved - this is a calculator">
            <Grid container spacing={3}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  select
                  label="Loan type preset"
                  value={loanType}
                  onChange={applyLoanType}
                >
                  {LOAN_TYPES.map((type) => (
                    <MenuItem key={type.value} value={type.value}>
                      {type.label} - {type.defaultRate}%
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  type="number"
                  label="Loan amount"
                  value={loanAmount}
                  onChange={(event) =>
                    setLoanAmount(Math.max(Number(event.target.value) || 0, 1000))
                  }
                />
              </Grid>

              <Grid item xs={12}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Loan amount: <strong>{formatCurrency(loanAmount)}</strong>
                </Typography>
                <Slider
                  value={loanAmount}
                  min={50000}
                  max={10000000}
                  step={25000}
                  onChange={(_, value) => setLoanAmount(value)}
                  valueLabelDisplay="auto"
                  valueLabelFormat={(value) => formatCurrency(value, { compact: true })}
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  type="number"
                  label="Interest rate (% p.a.)"
                  value={interestRate}
                  onChange={(event) => setInterestRate(Number(event.target.value) || 0)}
                />
                <Slider
                  value={interestRate}
                  min={4}
                  max={20}
                  step={0.25}
                  onChange={(_, value) => setInterestRate(value)}
                  valueLabelDisplay="auto"
                  valueLabelFormat={(value) => `${value}%`}
                  sx={{ mt: 1 }}
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  type="number"
                  label="Tenure (months)"
                  value={tenureMonths}
                  onChange={(event) =>
                    setTenureMonths(Math.min(Math.max(Number(event.target.value) || 1, 1), 360))
                  }
                  helperText={tenureLabel(tenureMonths)}
                />
                <Slider
                  value={tenureMonths}
                  min={6}
                  max={360}
                  step={6}
                  onChange={(_, value) => setTenureMonths(value)}
                  valueLabelDisplay="auto"
                  sx={{ mt: 1 }}
                />
              </Grid>
            </Grid>

            {serverError && (
              <Alert severity="warning" sx={{ mt: 2 }}>
                {serverError}
              </Alert>
            )}
            {serverResult && (
              <Alert severity="success" sx={{ mt: 2 }}>
                Verified by the Django API: {formatCurrency(serverResult.monthly_emi)} monthly EMI,
                total repayment {formatCurrency(serverResult.total_payment)}.
              </Alert>
            )}
          </SectionCard>

          <SectionCard
            title="Amortisation preview"
            subtitle="How the first 12 instalments split between principal and interest"
            sx={{ mt: 2.5 }}
          >
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Month</TableCell>
                    <TableCell align="right">EMI</TableCell>
                    <TableCell align="right">Principal</TableCell>
                    <TableCell align="right">Interest</TableCell>
                    <TableCell align="right">Balance</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {schedule.map((row) => (
                    <TableRow key={row.month} hover>
                      <TableCell>{row.month}</TableCell>
                      <TableCell align="right">{formatCurrency(row.emi)}</TableCell>
                      <TableCell align="right">{formatCurrency(row.principal)}</TableCell>
                      <TableCell align="right">{formatCurrency(row.interest)}</TableCell>
                      <TableCell align="right">{formatCurrency(row.balance)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </SectionCard>
        </Grid>

        <Grid item xs={12} md={5}>
          <Card
            sx={{
              borderRadius: 4,
              background: "linear-gradient(135deg, #1b3a8f 0%, #4361ee 100%)",
              color: "#fff",
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <Stack direction="row" spacing={1.5} alignItems="center">
                <CalculateIcon />
                <Typography variant="subtitle1">Your monthly EMI</Typography>
              </Stack>
              <Typography variant="h3" sx={{ fontWeight: 800, mt: 2 }}>
                {formatCurrency(result.monthly_emi)}
              </Typography>
              <Typography variant="body2" sx={{ color: "rgba(255,255,255,.85)", mt: 0.5 }}>
                {formatCurrency(loanAmount)} at {interestRate}% for {tenureLabel(tenureMonths)}
              </Typography>

              <Divider sx={{ my: 3, borderColor: "rgba(255,255,255,.2)" }} />

              <Stack spacing={1.5}>
                <Stack direction="row" justifyContent="space-between">
                  <Typography variant="body2" sx={{ color: "rgba(255,255,255,.85)" }}>
                    Principal amount
                  </Typography>
                  <Typography variant="body2" fontWeight={700}>
                    {formatCurrency(result.principal)}
                  </Typography>
                </Stack>
                <Stack direction="row" justifyContent="space-between">
                  <Typography variant="body2" sx={{ color: "rgba(255,255,255,.85)" }}>
                    Total interest
                  </Typography>
                  <Typography variant="body2" fontWeight={700}>
                    {formatCurrency(result.total_interest)}
                  </Typography>
                </Stack>
                <Stack direction="row" justifyContent="space-between">
                  <Typography variant="body2" sx={{ color: "rgba(255,255,255,.85)" }}>
                    Total repayment
                  </Typography>
                  <Typography variant="body2" fontWeight={700}>
                    {formatCurrency(result.total_payment)}
                  </Typography>
                </Stack>
              </Stack>
            </CardContent>
          </Card>

          <SectionCard title="Principal vs interest" sx={{ mt: 2.5 }}>
            <Box sx={{ height: 240 }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={donutData}
                    dataKey="value"
                    nameKey="name"
                    innerRadius={58}
                    outerRadius={90}
                    paddingAngle={3}
                  >
                    {donutData.map((entry) => (
                      <Cell key={entry.name} fill={entry.color} />
                    ))}
                  </Pie>
                  <ChartTooltip formatter={(value) => formatCurrency(value)} />
                </PieChart>
              </ResponsiveContainer>
            </Box>
            <Stack spacing={1} sx={{ mt: 1 }}>
              {donutData.map((item) => (
                <Stack key={item.name} direction="row" justifyContent="space-between">
                  <Stack direction="row" spacing={1} alignItems="center">
                    <Box
                      sx={{
                        width: 10,
                        height: 10,
                        borderRadius: "50%",
                        backgroundColor: item.color,
                      }}
                    />
                    <Typography variant="body2">{item.name}</Typography>
                  </Stack>
                  <Typography variant="body2" fontWeight={700}>
                    {formatCurrency(item.value)}
                  </Typography>
                </Stack>
              ))}
            </Stack>
          </SectionCard>

          <Alert severity="info" sx={{ mt: 2.5, borderRadius: 3 }}>
            EMI uses the reducing balance formula: EMI = P x r x (1 + r)^n / ((1 + r)^n - 1), where
            r is the monthly interest rate and n is the number of instalments.
          </Alert>
        </Grid>
      </Grid>
    </Box>
  );
}
