import { useCallback, useEffect, useMemo, useState } from "react";
import {
  Box,
  Chip,
  MenuItem,
  Paper,
  Snackbar,
  Stack,
  Switch,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Tooltip,
  Typography,
} from "@mui/material";

import { EmptyState, ErrorAlert, Loader, PageHeader, SectionCard } from "../../components/Common.jsx";
import { useAuth } from "../../context/AuthContext.jsx";
import adminService from "../../services/adminService";
import { getErrorMessage } from "../../services/api";
import { formatDate, relativeTime } from "../../utils/formatCurrency.js";

const ROLE_OPTIONS = [
  { value: "CUSTOMER", label: "Customer" },
  { value: "ADMIN", label: "Bank employee" },
];

export default function UserManagement() {
  const { user: signedInUser } = useAuth();
  const [users, setUsers] = useState([]);
  const [search, setSearch] = useState("");
  const [roleFilter, setRoleFilter] = useState("ALL");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [snack, setSnack] = useState("");
  const [busyId, setBusyId] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const data = await adminService.users();
      setUsers(data.results);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const filtered = useMemo(() => {
    const term = search.trim().toLowerCase();
    return users.filter((item) => {
      const matchesRole = roleFilter === "ALL" || item.role === roleFilter;
      const matchesTerm =
        !term ||
        item.name.toLowerCase().includes(term) ||
        item.email.toLowerCase().includes(term);
      return matchesRole && matchesTerm;
    });
  }, [users, search, roleFilter]);

  const counts = useMemo(
    () => ({
      total: users.length,
      customers: users.filter((item) => item.role === "CUSTOMER").length,
      staff: users.filter((item) => item.role === "ADMIN").length,
      disabled: users.filter((item) => !item.is_active).length,
    }),
    [users]
  );

  const change = async (account, payload, message) => {
    setBusyId(account.id);
    setError("");
    try {
      const updated = await adminService.updateUser(account.id, payload);
      setUsers((prev) => prev.map((item) => (item.id === updated.id ? updated : item)));
      setSnack(message);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setBusyId(null);
    }
  };

  return (
    <Box>
      <PageHeader
        title="User Management"
        subtitle="Who can sign in, what role they hold, and whether the account is switched on."
      />

      <ErrorAlert message={error} onRetry={load} />

      <Stack direction={{ xs: "column", sm: "row" }} spacing={2.5} sx={{ mb: 2.5 }}>
        <SectionCard title="Total accounts">
          <Typography variant="h4">{counts.total}</Typography>
          <Typography variant="caption" color="text.secondary">
            {counts.customers} customers, {counts.staff} bank employees
          </Typography>
        </SectionCard>
        <SectionCard title="Switched off">
          <Typography variant="h4">{counts.disabled}</Typography>
          <Typography variant="caption" color="text.secondary">
            Accounts that cannot log in
          </Typography>
        </SectionCard>
        <SectionCard title="Access rules">
          <Typography variant="body2" color="text.secondary">
            Only bank employees can open this area. A customer account switched off here keeps
            its demo data but cannot log in.
          </Typography>
        </SectionCard>
      </Stack>

      <Paper variant="outlined" sx={{ p: 2.5 }}>
        <Stack direction={{ xs: "column", md: "row" }} spacing={2} sx={{ mb: 2 }}>
          <TextField
            size="small"
            placeholder="Search by name or email"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            sx={{ flexGrow: 1 }}
          />
          <TextField
            size="small"
            select
            label="Role"
            value={roleFilter}
            onChange={(event) => setRoleFilter(event.target.value)}
            sx={{ minWidth: 180 }}
          >
            <MenuItem value="ALL">All roles</MenuItem>
            {ROLE_OPTIONS.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </TextField>
        </Stack>

        {loading ? (
          <Loader label="Loading accounts..." minHeight={200} />
        ) : filtered.length === 0 ? (
          <EmptyState
            title="No accounts match"
            description="Try a different name, email or role."
          />
        ) : (
          <TableContainer>
            <Table size="small" sx={{ minWidth: 820 }}>
              <TableHead>
                <TableRow>
                  <TableCell>Person</TableCell>
                  <TableCell>Role</TableCell>
                  <TableCell>Joined</TableCell>
                  <TableCell>Last login</TableCell>
                  <TableCell align="center">Can sign in</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filtered.map((account) => {
                  const isSelf = account.id === signedInUser?.id;
                  return (
                    <TableRow key={account.id} hover>
                      <TableCell>
                        <Stack direction="row" spacing={0.75} alignItems="center">
                          <Typography variant="body2" fontWeight={600}>
                            {account.name}
                          </Typography>
                          {isSelf && <Chip size="small" label="you" />}
                        </Stack>
                        <Typography variant="caption" color="text.secondary">
                          {account.email}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <TextField
                          select
                          size="small"
                          value={account.role}
                          disabled={busyId === account.id || isSelf}
                          onChange={(event) =>
                            change(
                              account,
                              { role: event.target.value },
                              `${account.name} is now a ${event.target.value === "ADMIN" ? "bank employee" : "customer"}.`
                            )
                          }
                          sx={{ minWidth: 160 }}
                        >
                          {ROLE_OPTIONS.map((option) => (
                            <MenuItem key={option.value} value={option.value}>
                              {option.label}
                            </MenuItem>
                          ))}
                        </TextField>
                      </TableCell>
                      <TableCell>{formatDate(account.joined)}</TableCell>
                      <TableCell>
                        {account.last_login ? relativeTime(account.last_login) : "never"}
                      </TableCell>
                      <TableCell align="center">
                        <Tooltip
                          title={
                            isSelf
                              ? "You cannot switch off the account you are signed in with"
                              : account.is_active
                                ? "Switch this account off"
                                : "Switch this account back on"
                          }
                        >
                          <span>
                            <Switch
                              checked={account.is_active}
                              disabled={busyId === account.id || isSelf}
                              onChange={(event) =>
                                change(
                                  account,
                                  { is_active: event.target.checked },
                                  `${account.name} ${event.target.checked ? "can" : "cannot"} sign in now.`
                                )
                              }
                            />
                          </span>
                        </Tooltip>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Paper>

      <Snackbar
        open={Boolean(snack)}
        autoHideDuration={3500}
        onClose={() => setSnack("")}
        message={snack}
      />
    </Box>
  );
}
