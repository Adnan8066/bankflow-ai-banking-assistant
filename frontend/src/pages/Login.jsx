import { useEffect, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  IconButton,
  InputAdornment,
  Link,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import AccountBalanceWalletIcon from "@mui/icons-material/AccountBalanceWallet";
import VisibilityIcon from "@mui/icons-material/Visibility";
import VisibilityOffIcon from "@mui/icons-material/VisibilityOff";
import { Link as RouterLink, useLocation, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";
import { getErrorMessage } from "../services/api";

const DEMO_ACCOUNTS = [
  { label: "Customer", email: "mohammed@bankflow.com", password: "Demo@12345" },
  { label: "Bank employee", email: "admin@bankflow.com", password: "Admin@12345" },
];

export default function Login() {
  const { login, isAuthenticated, isAdmin } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState({ email: "", password: "" });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const sessionExpired = new URLSearchParams(location.search).get("session") === "expired";

  useEffect(() => {
    if (isAuthenticated) {
      navigate(isAdmin ? "/admin" : "/dashboard", { replace: true });
    }
  }, [isAuthenticated, isAdmin, navigate]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    if (!form.email || !form.password) {
      setError("Please enter both your email and password.");
      return;
    }

    setLoading(true);
    try {
      const profile = await login(form);
      const target =
        profile?.user?.role === "ADMIN"
          ? "/admin"
          : location.state?.from && location.state.from !== "/login"
            ? location.state.from
            : "/dashboard";
      navigate(target, { replace: true });
    } catch (err) {
      setError(
        err?.response?.status === 401
          ? "Invalid email or password. Use one of the demo logins below."
          : getErrorMessage(err)
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "grid",
        placeItems: "center",
        p: 2,
        background:
          "radial-gradient(900px 420px at 20% 10%, #e8eefc 0%, #ffffff 55%), #f4f6fb",
      }}
    >
      <Card sx={{ width: "100%", maxWidth: 440, borderRadius: 4 }}>
        <CardContent sx={{ p: { xs: 3, md: 4 } }}>
          <Stack direction="row" spacing={1.25} alignItems="center" sx={{ mb: 3 }}>
            <Box
              sx={{
                display: "grid",
                placeItems: "center",
                width: 40,
                height: 40,
                borderRadius: 2,
                backgroundColor: "primary.main",
                color: "#fff",
              }}
            >
              <AccountBalanceWalletIcon fontSize="small" />
            </Box>
            <Box>
              <Typography variant="subtitle1" fontWeight={800} lineHeight={1.1}>
                BankFlow
              </Typography>
              <Typography variant="caption" color="text.secondary">
                AI Banking Assistant
              </Typography>
            </Box>
          </Stack>

          <Typography variant="h5" sx={{ mb: 0.5 }}>
            Welcome back
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Login with a demo account to explore the dashboard.
          </Typography>

          {sessionExpired && (
            <Alert severity="warning" sx={{ mb: 2 }}>
              Your session expired. Please login again.
            </Alert>
          )}
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <form onSubmit={handleSubmit} noValidate>
            <TextField
              fullWidth
              label="Email"
              type="email"
              autoComplete="email"
              value={form.email}
              onChange={(event) => setForm({ ...form, email: event.target.value })}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Password"
              type={showPassword ? "text" : "password"}
              autoComplete="current-password"
              value={form.password}
              onChange={(event) => setForm({ ...form, password: event.target.value })}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton onClick={() => setShowPassword((prev) => !prev)} edge="end">
                      {showPassword ? <VisibilityOffIcon /> : <VisibilityIcon />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={loading}
              sx={{ mt: 3 }}
              startIcon={loading ? <CircularProgress size={18} color="inherit" /> : null}
            >
              {loading ? "Signing in..." : "Login"}
            </Button>
          </form>

          <Typography variant="body2" color="text.secondary" sx={{ mt: 2, textAlign: "center" }}>
            New to BankFlow?{" "}
            <Link component={RouterLink} to="/register" fontWeight={700}>
              Create an account
            </Link>
          </Typography>

          <Box sx={{ mt: 3, p: 2, borderRadius: 3, backgroundColor: "#f8f9fd" }}>
            <Typography variant="caption" color="text.secondary" fontWeight={700}>
              DEMO LOGINS (click to autofill)
            </Typography>
            <Stack spacing={1} sx={{ mt: 1 }}>
              {DEMO_ACCOUNTS.map((account) => (
                <Stack
                  key={account.email}
                  direction="row"
                  spacing={1}
                  alignItems="center"
                  onClick={() => setForm({ email: account.email, password: account.password })}
                  sx={{ cursor: "pointer", flexWrap: "wrap" }}
                >
                  <Chip size="small" label={account.label} color="primary" variant="outlined" />
                  <Typography variant="caption">{account.email}</Typography>
                  <Typography variant="caption" color="text.secondary">
                    {account.password}
                  </Typography>
                </Stack>
              ))}
            </Stack>
          </Box>

          <Typography variant="caption" color="text.secondary" sx={{ display: "block", mt: 2 }}>
            This is a demo application with fictional data. Never enter real banking credentials.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
}
