import { useState } from "react";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Divider,
  Link,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import LockResetIcon from "@mui/icons-material/LockReset";
import { Link as RouterLink, useNavigate, useSearchParams } from "react-router-dom";

import BrandLogo from "../components/BrandLogo.jsx";
import authService from "../services/authService";
import { getErrorMessage } from "../services/api";

export default function ResetPassword() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const uid = params.get("uid") || "";
  const token = params.get("token") || "";

  const [form, setForm] = useState({ new_password: "", confirm_password: "" });
  const [error, setError] = useState("");
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    const nextErrors = {};
    if (form.new_password.length < 8) nextErrors.new_password = "Use at least 8 characters.";
    if (form.confirm_password !== form.new_password) {
      nextErrors.confirm_password = "The two passwords do not match.";
    }
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length) return;

    setLoading(true);
    try {
      await authService.confirmPasswordReset({ uid, token, ...form });
      setDone(true);
      setTimeout(() => navigate("/login"), 2200);
    } catch (err) {
      setError(getErrorMessage(err));
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
          "radial-gradient(900px 420px at 80% 5%, var(--bf-glow) 0%, var(--bf-shell) 55%), var(--bf-shell)",
      }}
    >
      <Card sx={{ width: "100%", maxWidth: 460 }}>
        <CardContent sx={{ p: { xs: 3, md: 4 } }}>
          <Box sx={{ mb: 3 }}>
            <BrandLogo size={40} subtitle="Choose a new password" />
          </Box>

          {!uid || !token ? (
            <Alert severity="warning">
              This reset link is missing its code. Start again from the forgot password page.
            </Alert>
          ) : done ? (
            <Alert severity="success">
              Password updated. Redirecting you to the login page...
            </Alert>
          ) : (
            <>
              <Typography variant="h5" sx={{ mb: 0.5 }}>
                Set a new password
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Pick something you have not used before. At least 8 characters.
              </Typography>

              {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                  {error}
                </Alert>
              )}

              <form onSubmit={handleSubmit} noValidate>
                <TextField
                  fullWidth
                  type="password"
                  label="New password"
                  autoComplete="new-password"
                  value={form.new_password}
                  onChange={(event) =>
                    setForm({ ...form, new_password: event.target.value })
                  }
                  error={Boolean(errors.new_password)}
                  helperText={errors.new_password}
                  sx={{ mb: 2 }}
                />
                <TextField
                  fullWidth
                  type="password"
                  label="Confirm new password"
                  autoComplete="new-password"
                  value={form.confirm_password}
                  onChange={(event) =>
                    setForm({ ...form, confirm_password: event.target.value })
                  }
                  error={Boolean(errors.confirm_password)}
                  helperText={errors.confirm_password}
                />
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  size="large"
                  disabled={loading}
                  startIcon={<LockResetIcon />}
                  sx={{ mt: 3 }}
                >
                  {loading ? "Saving..." : "Save new password"}
                </Button>
              </form>
            </>
          )}

          <Divider sx={{ my: 3 }} />
          <Stack direction="row" spacing={1} justifyContent="center">
            <Typography variant="body2" color="text.secondary">
              Need a new link?
            </Typography>
            <Link component={RouterLink} to="/forgot-password" fontWeight={700}>
              Start again
            </Link>
          </Stack>
        </CardContent>
      </Card>
    </Box>
  );
}
