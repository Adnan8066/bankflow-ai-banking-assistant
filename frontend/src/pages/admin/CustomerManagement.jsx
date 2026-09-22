import { useCallback, useEffect, useState } from "react";
import {
  Box,
  Button,
  Chip,
  Dialog,
  DialogContent,
  DialogTitle,
  Divider,
  Grid,
  InputAdornment,
  Paper,
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
import VisibilityIcon from "@mui/icons-material/Visibility";

import { ErrorAlert, Loader, PageHeader, SectionCard, StatusChip } from "../../components/Common.jsx";
import adminService from "../../services/adminService";
import { getErrorMessage } from "../../services/api";
import { formatCurrency, formatDate } from "../../utils/formatCurrency.js";

export default function CustomerManagement() {
  const [customers, setCustomers] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [detail, setDetail] = useState(null);
  const [detailLoading, setDetailLoading] = useState(false);

  const load = useCallback(async (term = "") => {
    setLoading(true);
    setError("");
    try {
      const data = await adminService.customers(term ? { search: term } : {});
      setCustomers(data.results);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const openDetail = async (id) => {
    setDetailLoading(true);
    setDetail({});
    try {
      setDetail(await adminService.customer(id));
    } catch (err) {
      setError(getErrorMessage(err));
      setDetail(null);
    } finally {
      setDetailLoading(false);
    }
  };

  return (
    <Box>
      <PageHeader
        title="Customer Management"
        subtitle={`${customers.length} fictional demo customer${customers.length === 1 ? "" : "s"} in the portfolio.`}
      />

      <ErrorAlert message={error} onRetry={() => load(search)} />

      <Paper variant="outlined" sx={{ p: 2.5, borderRadius: 3 }}>
        <Stack direction={{ xs: "column", sm: "row" }} spacing={2} sx={{ mb: 2 }}>
          <TextField
            size="small"
            placeholder="Search by name or email"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            onKeyDown={(event) => event.key === "Enter" && load(search)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon fontSize="small" />
                </InputAdornment>
              ),
            }}
            sx={{ flexGrow: 1 }}
          />
          <Button variant="contained" onClick={() => load(search)}>
            Search
          </Button>
          <Button
            onClick={() => {
              setSearch("");
              load("");
            }}
          >
            Clear
          </Button>
        </Stack>

        {loading ? (
          <Loader label="Loading customers..." minHeight={200} />
        ) : (
          <TableContainer>
            <Table size="small" sx={{ minWidth: 860 }}>
              <TableHead>
                <TableRow>
                  <TableCell>Customer</TableCell>
                  <TableCell>Phone</TableCell>
                  <TableCell>Account</TableCell>
                  <TableCell align="right">Balance</TableCell>
                  <TableCell align="right">Txns</TableCell>
                  <TableCell align="right">Loans</TableCell>
                  <TableCell>Joined</TableCell>
                  <TableCell align="right">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {customers.map((customer) => (
                  <TableRow key={customer.id} hover>
                    <TableCell>
                      <Typography variant="body2" fontWeight={600}>
                        {customer.name}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {customer.email}
                      </Typography>
                    </TableCell>
                    <TableCell>{customer.phone || "-"}</TableCell>
                    <TableCell>
                      <Typography variant="caption">{customer.masked_account_number || "-"}</Typography>
                      <Typography variant="caption" color="text.secondary" display="block">
                        {customer.account_type || ""}
                      </Typography>
                    </TableCell>
                    <TableCell align="right">{formatCurrency(customer.balance)}</TableCell>
                    <TableCell align="right">{customer.transaction_count}</TableCell>
                    <TableCell align="right">{customer.loan_count}</TableCell>
                    <TableCell>{formatDate(customer.joined)}</TableCell>
                    <TableCell align="right">
                      <Button
                        size="small"
                        startIcon={<VisibilityIcon fontSize="small" />}
                        onClick={() => openDetail(customer.id)}
                      >
                        View
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Paper>

      <Dialog open={Boolean(detail)} onClose={() => setDetail(null)} maxWidth="md" fullWidth>
        <DialogTitle>Customer 360 view</DialogTitle>
        <DialogContent dividers>
          {detailLoading ? (
            <Loader label="Loading customer profile..." minHeight={200} />
          ) : (
            detail?.customer && (
              <Box>
                <Stack
                  direction={{ xs: "column", sm: "row" }}
                  spacing={2}
                  alignItems={{ xs: "flex-start", sm: "center" }}
                  sx={{ mb: 2 }}
                >
                  <Box sx={{ flexGrow: 1 }}>
                    <Typography variant="h6">{detail.customer.name}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {detail.customer.email} • joined {formatDate(detail.customer.joined)}
                    </Typography>
                  </Box>
                  <Chip
                    label={detail.customer.is_active ? "Active login" : "Disabled"}
                    color={detail.customer.is_active ? "success" : "default"}
                  />
                  <Chip label={detail.customer.role} color="primary" variant="outlined" />
                </Stack>

                <Grid container spacing={2}>
                  {detail.accounts.map((account) => (
                    <Grid item xs={12} sm={6} key={account.id}>
                      <SectionCard title={account.account_type_display} subtitle={account.masked_account_number}>
                        <Typography variant="h6">{formatCurrency(account.balance)}</Typography>
                        <Stack direction="row" spacing={1} sx={{ mt: 1 }}>
                          <StatusChip status={account.status} />
                          <Chip size="small" variant="outlined" label={account.ifsc_code} />
                        </Stack>
                      </SectionCard>
                    </Grid>
                  ))}
                  <Grid item xs={12} sm={6}>
                    <SectionCard title="Profile details">
                      {[
                        ["Phone", detail.customer.profile?.phone || "-"],
                        ["Occupation", detail.customer.profile?.occupation || "-"],
                        [
                          "Employment",
                          detail.customer.profile?.employment_type?.replace("_", " ").toLowerCase() || "-",
                        ],
                        ["Monthly income", formatCurrency(detail.customer.profile?.monthly_income || 0)],
                      ].map(([label, value]) => (
                        <Stack key={label} direction="row" justifyContent="space-between" sx={{ py: 0.75 }}>
                          <Typography variant="body2" color="text.secondary">
                            {label}
                          </Typography>
                          <Typography variant="body2" fontWeight={600}>
                            {value}
                          </Typography>
                        </Stack>
                      ))}
                    </SectionCard>
                  </Grid>
                </Grid>

                <Typography variant="subtitle1" sx={{ mt: 3, mb: 1 }}>
                  Demo loans
                </Typography>
                {detail.loans.length === 0 ? (
                  <Typography variant="body2" color="text.secondary">
                    No loans on record for this customer.
                  </Typography>
                ) : (
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Loan</TableCell>
                          <TableCell align="right">Amount</TableCell>
                          <TableCell align="right">EMI</TableCell>
                          <TableCell align="right">Outstanding</TableCell>
                          <TableCell>Status</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {detail.loans.map((loan) => (
                          <TableRow key={loan.id}>
                            <TableCell>
                              {loan.loan_type_display}
                              <Typography variant="caption" color="text.secondary" display="block">
                                {loan.loan_id}
                              </Typography>
                            </TableCell>
                            <TableCell align="right">{formatCurrency(loan.amount)}</TableCell>
                            <TableCell align="right">{formatCurrency(loan.emi)}</TableCell>
                            <TableCell align="right">
                              {formatCurrency(loan.remaining_amount)}
                            </TableCell>
                            <TableCell>
                              <StatusChip status={loan.status} />
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                )}

                <Divider sx={{ my: 3 }} />
                <Typography variant="caption" color="text.secondary">
                  This dialog only exposes simulated demo data. No real customer information is
                  stored in BankFlow.
                </Typography>
              </Box>
            )
          )}
        </DialogContent>
      </Dialog>
    </Box>
  );
}
