import { useCallback, useEffect, useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  Grid,
  LinearProgress,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import { useNavigate, useParams } from "react-router-dom";

import { ErrorAlert, Loader, PageHeader, SectionCard, StatusChip } from "../components/Common.jsx";
import bankingService from "../services/bankingService";
import { getErrorMessage } from "../services/api";
import { formatCurrency, formatDate } from "../utils/formatCurrency.js";
import { amortisationSchedule, tenureLabel } from "../utils/calculations.js";

export default function LoanDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loan, setLoan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setLoan(await bankingService.getLoan(id));
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    load();
  }, [load]);

  if (loading) return <Loader label="Loading loan details..." />;

  if (error) {
    return (
      <>
        <PageHeader title="Loan details" />
        <ErrorAlert message={error} onRetry={load} />
        <Button startIcon={<ArrowBackIcon />} onClick={() => navigate("/loans")}>
          Back to loans
        </Button>
      </>
    );
  }

  const schedule = amortisationSchedule(loan.amount, loan.interest_rate, loan.tenure_months, 12);

  return (
    <Box>
      <PageHeader
        title={loan.loan_type_display}
        subtitle={`Loan ID ${loan.loan_id} - applied ${formatDate(loan.applied_at)}`}
        action={
          <Button startIcon={<ArrowBackIcon />} onClick={() => navigate("/loans")}>
            Back to loans
          </Button>
        }
      />

      <Grid container spacing={2.5}>
        <Grid item xs={12} md={4}>
          <Card
            sx={{
              color: "#fff",
              background: "linear-gradient(135deg, #12295e 0%, #1b3a8f 60%, #4361ee 100%)",
              borderRadius: 4,
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Typography variant="caption" sx={{ color: "rgba(255,255,255,.8)" }}>
                  Outstanding amount
                </Typography>
                <Chip
                  size="small"
                  label={loan.status_display}
                  sx={{ bgcolor: "rgba(255,255,255,.2)", color: "#fff" }}
                />
              </Stack>
              <Typography variant="h4" sx={{ fontWeight: 800, mt: 1 }}>
                {formatCurrency(loan.remaining_amount)}
              </Typography>
              <Typography variant="body2" sx={{ mt: 1, color: "rgba(255,255,255,.85)" }}>
                of {formatCurrency(loan.amount)} sanctioned
              </Typography>

              <Box sx={{ mt: 3 }}>
                <Stack direction="row" justifyContent="space-between">
                  <Typography variant="caption" sx={{ color: "rgba(255,255,255,.8)" }}>
                    Repaid {formatCurrency(loan.paid_amount)}
                  </Typography>
                  <Typography variant="caption" fontWeight={700}>
                    {loan.progress_percent}%
                  </Typography>
                </Stack>
                <LinearProgress
                  variant="determinate"
                  value={Math.min(loan.progress_percent, 100)}
                  sx={{
                    mt: 0.75,
                    height: 8,
                    borderRadius: 4,
                    backgroundColor: "rgba(255,255,255,.25)",
                    "& .MuiLinearProgress-bar": { backgroundColor: "#4fc3f7" },
                  }}
                />
              </Box>

              <Stack direction="row" spacing={3} sx={{ mt: 3, flexWrap: "wrap", gap: 1 }}>
                <Box>
                  <Typography variant="caption" sx={{ color: "rgba(255,255,255,.7)" }}>
                    Monthly EMI
                  </Typography>
                  <Typography variant="h6">{formatCurrency(loan.emi)}</Typography>
                </Box>
                <Box>
                  <Typography variant="caption" sx={{ color: "rgba(255,255,255,.7)" }}>
                    Interest
                  </Typography>
                  <Typography variant="h6">{loan.interest_rate}%</Typography>
                </Box>
                <Box>
                  <Typography variant="caption" sx={{ color: "rgba(255,255,255,.7)" }}>
                    Tenure
                  </Typography>
                  <Typography variant="h6">{tenureLabel(loan.tenure_months)}</Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>

          <SectionCard title="Application summary" sx={{ mt: 2.5 }}>
            {[
              ["Loan ID", loan.loan_id],
              ["Loan type", loan.loan_type_display],
              ["Purpose", loan.purpose || "-"],
              ["Monthly income", formatCurrency(loan.monthly_income)],
              ["Employment", loan.employment_type_display],
              ["Applied on", formatDate(loan.applied_at)],
            ].map(([label, value]) => (
              <Box key={label}>
                <Stack direction="row" justifyContent="space-between" sx={{ py: 1.1 }}>
                  <Typography variant="body2" color="text.secondary">
                    {label}
                  </Typography>
                  <Typography variant="body2" fontWeight={700} textAlign="right">
                    {value}
                  </Typography>
                </Stack>
                <Divider />
              </Box>
            ))}
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ pt: 1.5 }}>
              <Typography variant="body2" color="text.secondary">
                Status
              </Typography>
              <StatusChip status={loan.status} />
            </Stack>
          </SectionCard>
        </Grid>

        <Grid item xs={12} md={8}>
          <SectionCard
            title="Repayment schedule (first 12 instalments)"
            subtitle="Calculated on a reducing balance basis for this demo loan"
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
      </Grid>
    </Box>
  );
}
