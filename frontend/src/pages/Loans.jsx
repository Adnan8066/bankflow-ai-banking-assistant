import { useCallback, useEffect, useMemo, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Grid,
  MenuItem,
  Snackbar,
  Stack,
  Tab,
  Tabs,
  TextField,
  Typography,
} from "@mui/material";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";

import LoanCard from "../components/LoanCard.jsx";
import { EmptyState, ErrorAlert, Loader, PageHeader, SectionCard } from "../components/Common.jsx";
import bankingService from "../services/bankingService";
import { getErrorMessage } from "../services/api";
import { LOAN_TYPES, formatCurrency } from "../utils/formatCurrency.js";
import { calculateEmi, tenureLabel } from "../utils/calculations.js";

const STATUS_TABS = ["ALL", "PENDING", "APPROVED", "ACTIVE", "REJECTED", "COMPLETED"];

const EMPTY_APPLICATION = {
  loan_type: "PERSONAL",
  amount: 200000,
  interest_rate: 12.5,
  tenure_months: 24,
  monthly_income: 60000,
  employment_type: "SALARIED",
  purpose: "",
};

export default function Loans() {
  const [loans, setLoans] = useState([]);
  const [status, setStatus] = useState("ALL");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [application, setApplication] = useState(EMPTY_APPLICATION);
  const [formError, setFormError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [snack, setSnack] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setLoans(await bankingService.getLoans());
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const filtered = useMemo(
    () => (status === "ALL" ? loans : loans.filter((loan) => loan.status === status)),
    [loans, status]
  );

  const totals = useMemo(() => {
    const active = loans.filter((loan) => ["ACTIVE", "APPROVED"].includes(loan.status));
    return {
      outstanding: active.reduce((sum, loan) => sum + Number(loan.remaining_amount || 0), 0),
      emi: active.reduce((sum, loan) => sum + Number(loan.emi || 0), 0),
      count: active.length,
    };
  }, [loans]);

  const preview = calculateEmi(
    application.amount,
    application.interest_rate,
    application.tenure_months
  );

  const openDialog = () => {
    setApplication(EMPTY_APPLICATION);
    setFormError("");
    setDialogOpen(true);
  };

  const handleTypeChange = (event) => {
    const selected = LOAN_TYPES.find((type) => type.value === event.target.value);
    setApplication((prev) => ({
      ...prev,
      loan_type: event.target.value,
      interest_rate: selected?.defaultRate ?? prev.interest_rate,
    }));
  };

  const submitApplication = async () => {
    setFormError("");
    if (!application.purpose.trim()) {
      setFormError("Please add a short purpose for the demo loan.");
      return;
    }
    if (application.amount < 10000) {
      setFormError("The minimum demo loan amount is Rs 10,000.");
      return;
    }

    setSubmitting(true);
    try {
      await bankingService.applyLoan(application);
      setDialogOpen(false);
      setSnack("Demo loan application submitted and marked as pending review.");
      await load();
    } catch (err) {
      setFormError(getErrorMessage(err));
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <Loader label="Loading your demo loans..." />;

  return (
    <Box>
      <PageHeader
        title="Loans"
        subtitle="Apply for a simulated loan and monitor EMI, tenure and outstanding amount."
        action={
          <Button variant="contained" startIcon={<AddCircleOutlineIcon />} onClick={openDialog}>
            Apply for a demo loan
          </Button>
        }
      />

      <ErrorAlert message={error} onRetry={load} />

      <Grid container spacing={2.5} sx={{ mb: 2.5 }}>
        <Grid item xs={12} sm={4}>
          <SectionCard title="Active loans">
            <Typography variant="h4">{totals.count}</Typography>
            <Typography variant="caption" color="text.secondary">
              Approved or running demo loans
            </Typography>
          </SectionCard>
        </Grid>
        <Grid item xs={12} sm={4}>
          <SectionCard title="Monthly EMI total">
            <Typography variant="h4">{formatCurrency(totals.emi)}</Typography>
            <Typography variant="caption" color="text.secondary">
              Sum of every active EMI
            </Typography>
          </SectionCard>
        </Grid>
        <Grid item xs={12} sm={4}>
          <SectionCard title="Outstanding amount">
            <Typography variant="h4">{formatCurrency(totals.outstanding)}</Typography>
            <Typography variant="caption" color="text.secondary">
              Remaining demo balance to repay
            </Typography>
          </SectionCard>
        </Grid>
      </Grid>

      <Tabs
        value={status}
        onChange={(_, value) => setStatus(value)}
        variant="scrollable"
        scrollButtons="auto"
        sx={{ mb: 2, borderBottom: "1px solid #e6e9f2" }}
      >
        {STATUS_TABS.map((tab) => (
          <Tab key={tab} value={tab} label={tab === "ALL" ? "All loans" : tab.toLowerCase()} />
        ))}
      </Tabs>

      {filtered.length === 0 ? (
        <EmptyState
          title="No loans in this view"
          description="Submit a demo loan application to see it appear here with a pending status."
          action={
            <Button variant="contained" onClick={openDialog}>
              Apply for a demo loan
            </Button>
          }
        />
      ) : (
        <Grid container spacing={2.5}>
          {filtered.map((loan) => (
            <Grid item xs={12} md={6} xl={4} key={loan.id}>
              <LoanCard loan={loan} />
            </Grid>
          ))}
        </Grid>
      )}

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Apply for a demo loan</DialogTitle>
        <DialogContent dividers>
          {formError && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {formError}
            </Alert>
          )}
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                select
                label="Loan type"
                value={application.loan_type}
                onChange={handleTypeChange}
              >
                {LOAN_TYPES.map((type) => (
                  <MenuItem key={type.value} value={type.value}>
                    {type.label} ({type.defaultRate}%)
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="number"
                label="Loan amount"
                value={application.amount}
                onChange={(event) =>
                  setApplication({ ...application, amount: Number(event.target.value) })
                }
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="number"
                label="Interest rate (% p.a.)"
                value={application.interest_rate}
                onChange={(event) =>
                  setApplication({ ...application, interest_rate: Number(event.target.value) })
                }
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="number"
                label="Tenure (months)"
                value={application.tenure_months}
                onChange={(event) =>
                  setApplication({ ...application, tenure_months: Number(event.target.value) })
                }
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="number"
                label="Monthly income"
                value={application.monthly_income}
                onChange={(event) =>
                  setApplication({ ...application, monthly_income: Number(event.target.value) })
                }
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                select
                label="Employment type"
                value={application.employment_type}
                onChange={(event) =>
                  setApplication({ ...application, employment_type: event.target.value })
                }
              >
                {[
                  ["SALARIED", "Salaried"],
                  ["SELF_EMPLOYED", "Self Employed"],
                  ["STUDENT", "Student"],
                  ["RETIRED", "Retired"],
                  ["OTHER", "Other"],
                ].map(([value, label]) => (
                  <MenuItem key={value} value={value}>
                    {label}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Purpose"
                placeholder="e.g. Home renovation"
                value={application.purpose}
                onChange={(event) =>
                  setApplication({ ...application, purpose: event.target.value })
                }
              />
            </Grid>
          </Grid>

          <Box sx={{ mt: 3, p: 2, borderRadius: 3, backgroundColor: "#f8f9fd" }}>
            <Typography variant="subtitle2" sx={{ mb: 1 }}>
              Estimated EMI (live preview)
            </Typography>
            <Stack direction="row" spacing={3} sx={{ flexWrap: "wrap", gap: 1 }}>
              <Box>
                <Typography variant="caption" color="text.secondary">
                  Monthly EMI
                </Typography>
                <Typography variant="h6">{formatCurrency(preview.monthly_emi)}</Typography>
              </Box>
              <Box>
                <Typography variant="caption" color="text.secondary">
                  Total interest
                </Typography>
                <Typography variant="h6">{formatCurrency(preview.total_interest)}</Typography>
              </Box>
              <Box>
                <Typography variant="caption" color="text.secondary">
                  Total repayment
                </Typography>
                <Typography variant="h6">{formatCurrency(preview.total_payment)}</Typography>
              </Box>
              <Box>
                <Typography variant="caption" color="text.secondary">
                  Tenure
                </Typography>
                <Typography variant="h6">{tenureLabel(application.tenure_months)}</Typography>
              </Box>
            </Stack>
          </Box>
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button variant="contained" onClick={submitApplication} disabled={submitting}>
            {submitting ? "Submitting..." : "Submit application"}
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar
        open={Boolean(snack)}
        autoHideDuration={4000}
        onClose={() => setSnack("")}
        message={snack}
      />
    </Box>
  );
}
