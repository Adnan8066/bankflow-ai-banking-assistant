import { useState } from "react";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  Link,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import MarkEmailReadOutlinedIcon from "@mui/icons-material/MarkEmailReadOutlined";
import { Link as RouterLink, useNavigate } from "react-router-dom";

import BrandLogo from "../components/BrandLogo.jsx";
import authService from "../services/authService";
import { getErrorMessage } from "../services/api";

export default function ForgotPassword() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    if (!/^\S+@\S+\.\S+$/.test(email)) {
      setError("Enter the email address you registered with.");
      return;
    }
    setLoading(true);
    try {
      setResult(await authService.requestPasswordReset(email));
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
          "radial-gradient(900px 420px at 20% 10%, var(--bf-glow) 0%, var(--bf-shell) 55%), var(--bf-shell)",
      }}
    >
      <Card sx={{ width: "100%", maxWidth: 460 }}>
        <CardContent sx={{ p: { xs: 3, md: 4 } }}>
          <Box sx={{ mb: 3 }}>
            <BrandLogo size={40} subtitle="Password help" />
          </Box>

          <Typography variant="h5" sx={{ mb: 0.5 }}>
            Forgot your password?
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Enter your email address and we will create a reset link for your demo account.
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {result ? (
            <Stack spacing={2}>
              <Alert severity={result.reset ? "success" : "info"}>{result.message}</Alert>

              {result.reset && (
                <>
                  <Typography variant="body2" color="text.secondary">
                    BankFlow has no mail server, so the link is shown here instead of being
                    emailed. Choose a new password and you are back in.
                  </Typography>
                  <Box sx={{ p: 2, borderRadius: 3, backgroundColor: "var(--bf-surface)" }}>
                    <Typography variant="caption" color="text.secondary">
                      Reset code for {result.reset.email}
                    </Typography>
                    <Typography
                      variant="body2"
                      sx={{ fontFamily: "monospace", wordBreak: "break-all", mt: 0.5 }}
                    >
                      {result.reset.uid}.{result.reset.token}
                    </Typography>
                  </Box>
                  <Button
                    variant="contained"
                    fullWidth
                    onClick={() =>
                      navigate(
                        `/reset-password?uid=${result.reset.uid}&token=${result.reset.token}`
                      )
                    }
                  >
                    Choose a new password
                  </Button>
                </>
              )}
            </Stack>
          ) : (
            <form onSubmit={handleSubmit} noValidate>
              <TextField
                fullWidth
                label="Email"
                type="email"
                autoComplete="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                size="large"
                disabled={loading}
                sx={{ mt: 3 }}
                startIcon={<MarkEmailReadOutlinedIcon />}
              >
                {loading ? "Checking..." : "Create reset link"}
              </Button>
            </form>
          )}

          <Divider sx={{ my: 3 }} />
          <Stack direction="row" spacing={1} justifyContent="center" alignItems="center">
            <Typography variant="body2" color="text.secondary">
              Remembered it?
            </Typography>
            <Link component={RouterLink} to="/login" fontWeight={700}>
              Back to login
            </Link>
            <Chip size="small" variant="outlined" label="Demo" />
          </Stack>
        </CardContent>
      </Card>
    </Box>
  );
}
