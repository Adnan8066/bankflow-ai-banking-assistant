import { useCallback, useEffect, useMemo, useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Grid,
  InputAdornment,
  MenuItem,
  Paper,
  Stack,
  TablePagination,
  TextField,
  Typography,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import FilterAltOffIcon from "@mui/icons-material/FilterAltOff";

import TransactionTable from "../components/TransactionTable.jsx";
import { ErrorAlert, PageHeader } from "../components/Common.jsx";
import bankingService from "../services/bankingService";
import { getErrorMessage } from "../services/api";
import { TRANSACTION_CATEGORIES, formatCurrency } from "../utils/formatCurrency.js";

const EMPTY_FILTERS = {
  search: "",
  category: "ALL",
  type: "ALL",
  status: "ALL",
  start_date: "",
  end_date: "",
  ordering: "-date",
};

export default function Transactions() {
  const [filters, setFilters] = useState(EMPTY_FILTERS);
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [data, setData] = useState({ results: [], count: 0, summary: null });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Debounce the search box so we do not fire a request on every keystroke.
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(filters.search), 400);
    return () => clearTimeout(timer);
  }, [filters.search]);

  const query = useMemo(
    () => ({
      page: page + 1,
      page_size: rowsPerPage,
      search: debouncedSearch || undefined,
      category: filters.category,
      type: filters.type,
      status: filters.status,
      start_date: filters.start_date || undefined,
      end_date: filters.end_date || undefined,
      ordering: filters.ordering,
    }),
    [page, rowsPerPage, debouncedSearch, filters.category, filters.type, filters.status,
     filters.start_date, filters.end_date, filters.ordering]
  );

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const response = await bankingService.getTransactions(query);
      setData({
        results: response.results,
        count: response.count,
        summary: response.summary,
      });
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [query]);

  useEffect(() => {
    load();
  }, [load]);

  const updateFilter = (field) => (event) => {
    setPage(0);
    setFilters((prev) => ({ ...prev, [field]: event.target.value }));
  };

  const resetFilters = () => {
    setFilters(EMPTY_FILTERS);
    setPage(0);
  };

  const activeFilterCount = Object.entries(filters).filter(
    ([key, value]) => value && value !== "ALL" && key !== "ordering" && key !== "search"
  ).length;

  return (
    <Box>
      <PageHeader
        title="Transactions"
        subtitle="Search, filter and inspect every simulated movement in your demo account."
        action={
          <Button
            variant="outlined"
            startIcon={<FilterAltOffIcon />}
            onClick={resetFilters}
            disabled={activeFilterCount === 0 && !filters.search}
          >
            Reset filters{activeFilterCount ? ` (${activeFilterCount})` : ""}
          </Button>
        }
      />

      <ErrorAlert message={error} onRetry={load} />

      <Grid container spacing={2.5} sx={{ mb: 2.5 }}>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography variant="caption" color="text.secondary">
                Total credit (filtered)
              </Typography>
              <Typography variant="h6" color="success.main">
                {formatCurrency(data.summary?.total_credit || 0)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography variant="caption" color="text.secondary">
                Total debit (filtered)
              </Typography>
              <Typography variant="h6" color="error.main">
                {formatCurrency(data.summary?.total_debit || 0)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography variant="caption" color="text.secondary">
                Net movement
              </Typography>
              <Typography variant="h6">{formatCurrency(data.summary?.net || 0)}</Typography>
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
              placeholder="Search description, ID or category"
              value={filters.search}
              onChange={updateFilter("search")}
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
              onChange={updateFilter("category")}
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
              onChange={updateFilter("type")}
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
              onChange={updateFilter("start_date")}
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
              onChange={updateFilter("end_date")}
            />
          </Grid>
        </Grid>

        <Stack direction="row" spacing={1} sx={{ mb: 1.5, flexWrap: "wrap", gap: 1 }}>
          <Typography variant="caption" color="text.secondary" sx={{ alignSelf: "center" }}>
            Sort by:
          </Typography>
          {[
            { value: "-date", label: "Newest" },
            { value: "date", label: "Oldest" },
            { value: "-amount", label: "Highest amount" },
            { value: "amount", label: "Lowest amount" },
          ].map((option) => (
            <Chip
              key={option.value}
              size="small"
              label={option.label}
              color={filters.ordering === option.value ? "primary" : "default"}
              variant={filters.ordering === option.value ? "filled" : "outlined"}
              onClick={() => {
                setPage(0);
                setFilters((prev) => ({ ...prev, ordering: option.value }));
              }}
            />
          ))}
        </Stack>

        <TransactionTable transactions={data.results} loading={loading} />

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
    </Box>
  );
}
