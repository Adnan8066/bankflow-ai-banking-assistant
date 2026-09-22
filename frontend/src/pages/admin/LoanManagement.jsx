import { useCallback, useEffect, useState } from "react";
import {
  Box,
  Button,
  Chip,
  InputAdornment,
  MenuItem,
  Paper,
  Snackbar,
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
import SearchIcon from "@mui/icons-material/Search";
import CheckCircleOutlineIcon from "@mui/icons-material/CheckCircleOutline";
import HighlightOffIcon from "@mui/icons-material/HighlightOff";
import PlayCircleOutlineIcon from "@mui/icons-material/PlayCircleOutline";

import { EmptyState, ErrorAlert, Loader, PageHeader, StatusChip } from "../../components/Common.jsx";
import adminService from "../../services/adminService";
import { getErrorMessage } from "../../services/api";
import { LOAN_TYPES, formatCurrency, formatDate } from "../../utils/formatCurrency.js";

const STATUS_OPTIONS = ["ALL", "PENDING", "APPROVED", "ACTIVE", "REJECTED", "COMPLETED"];

export default function LoanManagement() {
  const [loans, setLoans] = useState([]);
  const [filters, setFilters] = useState({ search: "", status: "ALL", type: "ALL" });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [snack, setSnack] = useState("");
  const [updatingId, setUpdatingId] = useState(null);

  const load = useCallback(async (currentFilters = filters) => {
    setLoading(true);
    setError("");
    try {
      const data = await adminService.loans({
        search: currentFilters.search || undefined,
        status: currentFilters.status,
        type: currentFilters.type,
      });
      setLoans(data.results);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters.status, filters.type]);

  const changeStatus = async (loan, status) => {
    setUpdatingId(loan.id);
    try {
      const updated = await adminService.updateLoanStatus(loan.id, status);
      setLoans((prev) => prev.map((item) => (item.id === updated.id ? updated : item)));
      setSnack(
        `${updated.loan_id} marked as ${updated.status_display}. The customer received a demo notification.`
      );
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setUpdatingId(null);
    }
  };

  const pending = loans.filter((loan) => loan.status === "PENDING").length;

  return (
    <Box>
      <PageHeader
        title="Loan Management"
        subtitle={`${loans.length} demo loan applications in view • ${pending} awaiting a decision`}
      />

      <ErrorAlert message={error} onRetry={() => load()} />

      <Paper variant="outlined" sx={{ p: 2.5, borderRadius: 3 }}>
        <Stack direction={{ xs: "column", md: "row" }} spacing={2} sx={{ mb: 2 }}>
          <TextField
            size="small"
            placeholder="Search by loan ID, customer name or email"
            value={filters.search}
            onChange={(event) => setFilters({ ...filters, search: event.target.value })}
            onKeyDown={(event) => event.key === "Enter" && load(filters)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon fontSize="small" />
                </InputAdornment>
              ),
            }}
            sx={{ flexGrow: 1 }}
          />
          <TextField
            select
            size="small"
            label="Status"
            value={filters.status}
            onChange={(event) => setFilters({ ...filters, status: event.target.value })}
            sx={{ minWidth: 160 }}
          >
            {STATUS_OPTIONS.map((status) => (
              <MenuItem key={status} value={status}>
                {status === "ALL" ? "All statuses" : status.toLowerCase()}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            size="small"
            label="Loan type"
            value={filters.type}
            onChange={(event) => setFilters({ ...filters, type: event.target.value })}
            sx={{ minWidth: 170 }}
          >
            <MenuItem value="ALL">All loan types</MenuItem>
            {LOAN_TYPES.map((type) => (
              <MenuItem key={type.value} value={type.value}>
                {type.label}
              </MenuItem>
            ))}
          </TextField>
          <Button variant="contained" onClick={() => load(filters)}>
            Apply
          </Button>
        </Stack>

        {loading ? (
          <Loader label="Loading demo loans..." minHeight={200} />
        ) : loans.length === 0 ? (
          <EmptyState title="No loans match these filters" description="Try another status or loan type." />
        ) : (
          <TableContainer>
            <Table size="small" sx={{ minWidth: 980 }}>
              <TableHead>
                <TableRow>
                  <TableCell>Loan ID</TableCell>
                  <TableCell>Customer</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell align="right">Amount</TableCell>
                  <TableCell align="right">Interest</TableCell>
                  <TableCell align="right">Tenure</TableCell>
                  <TableCell align="right">EMI</TableCell>
                  <TableCell align="right">Outstanding</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell align="right">Decision</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {loans.map((loan) => (
                  <TableRow key={loan.id} hover>
                    <TableCell>
                      <Typography variant="caption" fontWeight={700}>
                        {loan.loan_id}
                      </Typography>
                      <Typography variant="caption" color="text.secondary" display="block">
                        {formatDate(loan.applied_at)}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2" fontWeight={600}>
                        {loan.customer_name}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {loan.customer_email}
                      </Typography>
                    </TableCell>
                    <TableCell>{loan.loan_type_display}</TableCell>
                    <TableCell align="right">{formatCurrency(loan.amount)}</TableCell>
                    <TableCell align="right">{loan.interest_rate}%</TableCell>
                    <TableCell align="right">{loan.tenure_months} mo</TableCell>
                    <TableCell align="right">{formatCurrency(loan.emi)}</TableCell>
                    <TableCell align="right">{formatCurrency(loan.remaining_amount)}</TableCell>
                    <TableCell>
                      <StatusChip status={loan.status} />
                    </TableCell>
                    <TableCell align="right">
                      <Stack direction="row" spacing={0.5} justifyContent="flex-end">
                        <Button
                          size="small"
                          color="success"
                          disabled={updatingId === loan.id || loan.status === "APPROVED"}
                          startIcon={<CheckCircleOutlineIcon fontSize="small" />}
                          onClick={() => changeStatus(loan, "APPROVED")}
                        >
                          Approve
                        </Button>
                        <Button
                          size="small"
                          color="primary"
                          disabled={updatingId === loan.id || loan.status === "ACTIVE"}
                          startIcon={<PlayCircleOutlineIcon fontSize="small" />}
                          onClick={() => changeStatus(loan, "ACTIVE")}
                        >
                          Activate
                        </Button>
                        <Button
                          size="small"
                          color="error"
                          disabled={updatingId === loan.id || loan.status === "REJECTED"}
                          startIcon={<HighlightOffIcon fontSize="small" />}
                          onClick={() => changeStatus(loan, "REJECTED")}
                        >
                          Reject
                        </Button>
                      </Stack>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Paper>

      <Stack direction="row" spacing={1} sx={{ mt: 2, flexWrap: "wrap", gap: 1 }}>
        <Chip label="Approve / reject creates a customer notification" variant="outlined" />
        <Chip label="All loan decisions are simulated" variant="outlined" />
      </Stack>

      <Snackbar
        open={Boolean(snack)}
        autoHideDuration={4000}
        onClose={() => setSnack("")}
        message={snack}
      />
    </Box>
  );
}
