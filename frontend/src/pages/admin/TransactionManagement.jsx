import { useCallback, useEffect, useMemo, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Grid,
  InputAdornment,
  MenuItem,
  Paper,
  Stack,
  Snackbar,
  TablePagination,
  TextField,
  Typography,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";

import TransactionTable from "../../components/TransactionTable.jsx";
import { ErrorAlert, PageHeader } from "../../components/Common.jsx";
import adminService from "../../services/adminService";
import { getErrorMessage } from "../../services/api";
import { TRANSACTION_CATEGORIES, formatCurrency } from "../../utils/formatCurrency.js";

const EMPTY_FORM = {
  customer: "",
  amount: 1500,
  transaction_type: "DEBIT",
  category: "Other",
  description: "",
  date: "",
};

export default function TransactionManagement() {
  const [filters, setFilters] = useState({
    search: "",
    category: "ALL",
    type: "ALL",
    start_date: "",
    end_date: "",
  });
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [data, setData] = useState({ results: [], count: 0, summary: null });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [customers, setCustomers] = useState([]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [form, setForm] = useState(EMPTY_FORM);
  const [formError, setFormError] = useState("");
  const [saving, setSaving] = useState(false);
  const [snack, setSnack] = useState("");

  useEffect(() => {
    const timer = setTimeout(() => setSearch(filters.search), 400);
    return () => clearTimeout(timer);
  }, [filters.search]);

  const query = useMemo(
    () => ({
      page: page + 1,
      page_size: rowsPerPage,
      search: search || undefined,
      category: filters.category,
      type: filters.type,
      start_date: filters.start_date || undefined,
      end_date: filters.end_date || undefined,
    }),
    [page, rowsPerPage, search, filters.category, filters.type, filters.start_date, filters.end_date]
  );

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const response = await adminService.transactions(query);
      setData({ results: response.results, count: response.count, summary: response.summary });
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [query]);

  useEffect(() => {
    load();
  }, [load]);

  const openDialog = async () => {
    setForm(EMPTY_FORM);
    setFormError("");
    setDialogOpen(true);
    try {
      const data = await adminService.customers();
      setCustomers(data.results);
    } catch (err) {
      setFormError(getErrorMessage(err));
    }
  };

  const save = async () => {
    setFormError("");
    if (!form.customer) {
      setFormError("Choose the customer this transaction belongs to.");
      return;
    }
    if (!form.description.trim()) {
      setFormError("Add a short description.");
      return;
    }
    setSaving(true);
    try {
      await adminService.createTransaction({
        customer: Number(form.customer),
        amount: Number(form.amount),
        transaction_type: form.transaction_type,
        category: form.category,
        description: form.description,
        ...(form.date ? { date: `${form.date}T12:00:00` } : {}),
      });
      setDialogOpen(false);
      setSnack("Demo transaction recorded and the account balance updated.");
      await load();
    } catch (err) {
      setFormError(getErrorMessage(err));
    } finally {
      setSaving(false);
    }
  };

  return (
    <Box>
      <PageHeader
        title="Transaction Management"
        subtitle="Every simulated transaction across all demo customers."
        action={
          <Button variant="contained" startIcon={<AddCircleOutlineIcon />} onClick={openDialog}>
            Record a transaction
          </Button>
        }
      />

      <ErrorAlert message={error} onRetry={load} />

      <Grid container spacing={2.5} sx={{ mb: 2.5 }}>
        <Grid item xs={12} sm={6}>
          <Card>
            <CardContent>
              <Typography variant="caption" color="text.secondary">
                Filtered transactions
              </Typography>
              <Typography variant="h6">{data.summary?.count ?? data.count}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Card>
            <CardContent>
              <Typography variant="caption" color="text.secondary">
                Filtered demo volume
              </Typography>
              <Typography variant="h6">{formatCurrency(data.summary?.volume || 0)}</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Paper variant="outlined" sx={{ p: 2.5, borderRadius: 3 }}>
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              size="small"
              placeholder="Search customer, description or ID"
              value={filters.search}
              onChange={(event) => {
                setPage(0);
                setFilters({ ...filters, search: event.target.value });
              }}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon fontSize="small" />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          <Grid item xs={6} md={2}>
            <TextField
              fullWidth
              select
              size="small"
              label="Category"
              value={filters.category}
              onChange={(event) => {
                setPage(0);
                setFilters({ ...filters, category: event.target.value });
              }}
            >
              <MenuItem value="ALL">All categories</MenuItem>
              {TRANSACTION_CATEGORIES.map((category) => (
                <MenuItem key={category} value={category}>
                  {category}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={6} md={2}>
            <TextField
              fullWidth
              select
              size="small"
              label="Type"
              value={filters.type}
              onChange={(event) => {
                setPage(0);
                setFilters({ ...filters, type: event.target.value });
              }}
            >
              <MenuItem value="ALL">All types</MenuItem>
              <MenuItem value="CREDIT">Credit</MenuItem>
              <MenuItem value="DEBIT">Debit</MenuItem>
            </TextField>
          </Grid>
          <Grid item xs={6} md={2}>
            <TextField
              fullWidth
              size="small"
              type="date"
              label="From"
              InputLabelProps={{ shrink: true }}
              value={filters.start_date}
              onChange={(event) => {
                setPage(0);
                setFilters({ ...filters, start_date: event.target.value });
              }}
            />
          </Grid>
          <Grid item xs={6} md={2}>
            <TextField
              fullWidth
              size="small"
              type="date"
              label="To"
              InputLabelProps={{ shrink: true }}
              value={filters.end_date}
              onChange={(event) => {
                setPage(0);
                setFilters({ ...filters, end_date: event.target.value });
              }}
            />
          </Grid>
        </Grid>

        <TransactionTable
          transactions={data.results}
          loading={loading}
          showCustomer
          basePath="/admin/transactions"
          emptyTitle="No transactions match these filters"
        />

        {!loading && data.count > 0 && (
          <TablePagination
            component="div"
            count={data.count}
            page={page}
            onPageChange={(_, newPage) => setPage(newPage)}
            rowsPerPage={rowsPerPage}
            onRowsPerPageChange={(event) => {
              setRowsPerPage(parseInt(event.target.value, 10));
              setPage(0);
            }}
            rowsPerPageOptions={[5, 10, 25]}
          />
        )}
      </Paper>

      <Stack sx={{ mt: 2 }}>
        <Typography variant="caption" color="text.secondary">
          A recorded transaction updates the demo balance and notifies the customer. No real money
          moves anywhere in this project.
        </Typography>
      </Stack>

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Record a demo transaction</DialogTitle>
        <DialogContent dividers>
          {formError && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {formError}
            </Alert>
          )}
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                select
                label="Customer"
                value={form.customer}
                onChange={(event) => setForm({ ...form, customer: event.target.value })}
              >
                {customers.map((customer) => (
                  <MenuItem key={customer.id} value={customer.id}>
                    {customer.name} - {customer.masked_account_number} ({formatCurrency(customer.balance)})
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="number"
                label="Amount"
                value={form.amount}
                onChange={(event) => setForm({ ...form, amount: Number(event.target.value) })}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                select
                label="Type"
                value={form.transaction_type}
                onChange={(event) => setForm({ ...form, transaction_type: event.target.value })}
              >
                <MenuItem value="DEBIT">Debit (money out)</MenuItem>
                <MenuItem value="CREDIT">Credit (money in)</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                select
                label="Category"
                value={form.category}
                onChange={(event) => setForm({ ...form, category: event.target.value })}
              >
                {TRANSACTION_CATEGORIES.map((category) => (
                  <MenuItem key={category} value={category}>
                    {category}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="date"
                label="Date (optional)"
                InputLabelProps={{ shrink: true }}
                value={form.date}
                onChange={(event) => setForm({ ...form, date: event.target.value })}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Description"
                placeholder="e.g. Branch correction - ATM reconciliation"
                value={form.description}
                onChange={(event) => setForm({ ...form, description: event.target.value })}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button variant="contained" onClick={save} disabled={saving}>
            {saving ? "Saving..." : "Record transaction"}
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
