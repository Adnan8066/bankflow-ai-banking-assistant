import { useEffect, useState } from "react";
import {
  Alert,
  Avatar,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  Grid,
  Snackbar,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import SaveIcon from "@mui/icons-material/Save";

import { ErrorAlert, Loader, PageHeader, SectionCard } from "../components/Common.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import authService from "../services/authService";
import { getErrorMessage } from "../services/api";
import { formatCurrency, formatDate, initials } from "../utils/formatCurrency.js";

export default function Profile() {
  const { reloadProfile, user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [form, setForm] = useState({ name: "", phone: "", address: "", occupation: "", monthly_income: 0 });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [errors, setErrors] = useState({});
  const [snack, setSnack] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const data = await authService.profile();
        setProfile(data);
        setForm({
          name: data.user.name || "",
          phone: data.phone || "",
          address: data.address || "",
          occupation: data.occupation || "",
          monthly_income: data.monthly_income || 0,
        });
      } catch (err) {
        setError(getErrorMessage(err));
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const handleSave = async (event) => {
    event.preventDefault();
    const nextErrors = {};
    if (!form.name.trim()) nextErrors.name = "Name cannot be empty.";
    if (form.phone && !/^[+0-9\s-]{8,20}$/.test(form.phone)) {
      nextErrors.phone = "Enter a valid phone number.";
    }
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length) return;

    setSaving(true);
    setError("");
    try {
      const updated = await authService.updateProfile(form);
      setProfile(updated);
      await reloadProfile();
      setSnack("Profile updated successfully.");
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <Loader label="Loading your demo profile..." />;

  return (
    <Box>
      <PageHeader title="Profile" subtitle="Update your demo contact details and review your account." />
      <ErrorAlert message={error} />

      <Grid container spacing={2.5}>
        <Grid item xs={12} md={4}>
          <Card sx={{ borderRadius: 4 }}>
            <CardContent sx={{ textAlign: "center", py: 4 }}>
              <Avatar
                sx={{
                  width: 88,
                  height: 88,
                  mx: "auto",
                  bgcolor: "primary.main",
                  fontSize: 30,
                  fontWeight: 700,
                }}
              >
                {initials(form.name || user?.name || "BF")}
              </Avatar>
              <Typography variant="h6" sx={{ mt: 2 }}>
                {form.name || user?.name}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {user?.email}
              </Typography>
              <Stack direction="row" spacing={1} justifyContent="center" sx={{ mt: 2 }}>
                <Chip size="small" color="primary" label={user?.role === "ADMIN" ? "Bank Employee" : "Customer"} />
                <Chip size="small" variant="outlined" label="Demo profile" />
              </Stack>
              <Divider sx={{ my: 3 }} />
              <Stack spacing={1} sx={{ textAlign: "left", px: 1 }}>
                <Stack direction="row" justifyContent="space-between">
                  <Typography variant="body2" color="text.secondary">
                    Member since
                  </Typography>
                  <Typography variant="body2" fontWeight={700}>
                    {formatDate(profile?.user?.date_joined || profile?.created_at)}
                  </Typography>
                </Stack>
                <Stack direction="row" justifyContent="space-between">
                  <Typography variant="body2" color="text.secondary">
                    Employment
                  </Typography>
                  <Typography variant="body2" fontWeight={700}>
                    {profile?.employment_type?.replace("_", " ").toLowerCase()}
                  </Typography>
                </Stack>
                <Stack direction="row" justifyContent="space-between">
                  <Typography variant="body2" color="text.secondary">
                    Monthly income
                  </Typography>
                  <Typography variant="body2" fontWeight={700}>
                    {formatCurrency(profile?.monthly_income || 0)}
                  </Typography>
                </Stack>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <SectionCard title="Personal details" subtitle="Name and phone are editable in this demo">
            <form onSubmit={handleSave}>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Full name"
                    value={form.name}
                    onChange={(event) => setForm({ ...form, name: event.target.value })}
                    error={Boolean(errors.name)}
                    helperText={errors.name}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Email (read only)"
                    value={user?.email || ""}
                    disabled
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Phone"
                    value={form.phone}
                    onChange={(event) => setForm({ ...form, phone: event.target.value })}
                    error={Boolean(errors.phone)}
                    helperText={errors.phone}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Occupation"
                    value={form.occupation}
                    onChange={(event) => setForm({ ...form, occupation: event.target.value })}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Address"
                    value={form.address}
                    onChange={(event) => setForm({ ...form, address: event.target.value })}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    type="number"
                    label="Monthly income"
                    value={form.monthly_income}
                    onChange={(event) =>
                      setForm({ ...form, monthly_income: Number(event.target.value) })
                    }
                  />
                </Grid>
              </Grid>

              <Stack direction="row" spacing={2} sx={{ mt: 3 }}>
                <Button
                  type="submit"
                  variant="contained"
                  startIcon={<SaveIcon />}
                  disabled={saving}
                >
                  {saving ? "Saving..." : "Save changes"}
                </Button>
                <Button
                  onClick={() =>
                    setForm({
                      name: profile?.user?.name || "",
                      phone: profile?.phone || "",
                      address: profile?.address || "",
                      occupation: profile?.occupation || "",
                      monthly_income: profile?.monthly_income || 0,
                    })
                  }
                >
                  Reset
                </Button>
              </Stack>
            </form>
          </SectionCard>

          <Alert severity="info" sx={{ mt: 2.5, borderRadius: 3 }}>
            Profile pictures are shown as initials in this demo. Email addresses cannot be changed
            because they identify the login.
          </Alert>
        </Grid>
      </Grid>

      <Snackbar
        open={Boolean(snack)}
        autoHideDuration={3000}
        onClose={() => setSnack("")}
        message={snack}
      />
    </Box>
  );
}
