import { useState } from "react";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Grid,
  Link,
  MenuItem,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import AccountBalanceWalletIcon from "@mui/icons-material/AccountBalanceWallet";
import CheckCircleOutlineIcon from "@mui/icons-material/CheckCircleOutline";
import { Link as RouterLink, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";
import { getErrorMessage } from "../services/api";

const EMPLOYMENT_TYPES = [
  { value: "SALARIED", label: "Salaried" },
  { value: "SELF_EMPLOYED", label: "Self Employed" },
  { value: "STUDENT", label: "Student" },
  { value: "RETIRED", label: "Retired" },
  { value: "OTHER", label: "Other" },
];

const EMPTY_FORM = {
  name: "",
  email: "",
  phone: "",
  employment_type: "SALARIED",
  password: "",
  confirm_password: "",
};

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState(EMPTY_FORM);
  const [errors, setErrors] = useState({});
  const [apiError, setApiError] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const update = (field) => (event) => setForm({ ...form, [field]: event.target.value });

  const validate = () => {
    const next = {};
    if (!form.name.trim()) next.name = "Full name is required.";
    if (!form.email.trim()) next.email = "Email is required.";
    else if (!/^\S+@\S+\.\S+$/.test(form.email)) next.email = "Enter a valid email address.";
    if (form.phone && !/^[+0-9\s-]{8,20}$/.test(form.phone)) {
      next.phone = "Enter a valid phone number.";
    }
    if (!form.password) next.password = "Password is required.";
    else if (form.password.length < 8) next.password = "Use at least 8 characters.";
    else if (/^\d+$/.test(form.password)) next.password = "Password cannot be only numbers.";
    if (form.confirm_password !== form.password) {
      next.confirm_password = "Passwords do not match.";
    }
    setErrors(next);
    return Object.keys(next).length === 0;
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setApiError("");
    if (!validate()) return;

    setLoading(true);
    try {
      await register(form);
      setSuccess(true);
      setForm(EMPTY_FORM);
      setTimeout(() => navigate("/login"), 1800);
    } catch (error) {
      setApiError(getErrorMessage(error));
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
          "radial-gradient(900px 420px at 80% 5%, #e8eefc 0%, #ffffff 55%), #f4f6fb",
      }}
    >
      <Card sx={{ width: "100%", maxWidth: 720, borderRadius: 4 }}>
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
                Create your demo customer profile
              </Typography>
            </Box>
          </Stack>

          {success && (
            <Alert
              severity="success"
              icon={<CheckCircleOutlineIcon />}
              sx={{ mb: 2 }}
            >
              Registration successful. Redirecting you to the login page...
            </Alert>
          )}
          {apiError && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {apiError}
            </Alert>
          )}

          <form onSubmit={handleSubmit} noValidate>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  required
                  label="Full name"
                  value={form.name}
                  onChange={update("name")}
                  error={Boolean(errors.name)}
                  helperText={errors.name}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  required
                  label="Email"
                  type="email"
                  value={form.email}
                  onChange={update("email")}
                  error={Boolean(errors.email)}
                  helperText={errors.email}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Phone"
                  placeholder="+91 98765 43210"
                  value={form.phone}
                  onChange={update("phone")}
                  error={Boolean(errors.phone)}
                  helperText={errors.phone}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  select
                  label="Employment type"
                  value={form.employment_type}
                  onChange={update("employment_type")}
                >
                  {EMPLOYMENT_TYPES.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                      {option.label}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  required
                  label="Password"
                  type="password"
                  value={form.password}
                  onChange={update("password")}
                  error={Boolean(errors.password)}
                  helperText={errors.password || "Minimum 8 characters."}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  required
                  label="Confirm password"
                  type="password"
                  value={form.confirm_password}
                  onChange={update("confirm_password")}
                  error={Boolean(errors.confirm_password)}
                  helperText={errors.confirm_password}
                />
              </Grid>
            </Grid>

            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={loading}
              sx={{ mt: 3 }}
              startIcon={loading ? <CircularProgress size={18} color="inherit" /> : null}
            >
              {loading ? "Creating account..." : "Create demo account"}
            </Button>
          </form>

          <Typography variant="body2" color="text.secondary" sx={{ mt: 2, textAlign: "center" }}>
            Already registered?{" "}
            <Link component={RouterLink} to="/login" fontWeight={700}>
              Login instead
            </Link>
          </Typography>
          <Typography variant="caption" color="text.secondary" sx={{ display: "block", mt: 2 }}>
            New demo customers automatically get a simulated savings account and welcome
            notification. No real banking data is used or stored.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
}
