import { Box, Button, Container, Stack, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";

export default function NotFound() {
  const navigate = useNavigate();
  const { isAuthenticated, isAdmin } = useAuth();

  return (
    <Container maxWidth="sm">
      <Box sx={{ minHeight: "100vh", display: "grid", placeItems: "center", textAlign: "center" }}>
        <Stack spacing={2} alignItems="center">
          <Typography variant="h1" sx={{ fontSize: 84, color: "primary.main", fontWeight: 800 }}>
            404
          </Typography>
          <Typography variant="h5">This page is not part of the demo</Typography>
          <Typography color="text.secondary">
            The link you followed may be broken, or the page may have moved. Everything else in
            BankFlow is still working fine.
          </Typography>
          <Stack direction={{ xs: "column", sm: "row" }} spacing={2} sx={{ pt: 1 }}>
            <Button variant="contained" onClick={() => navigate(isAuthenticated ? (isAdmin ? "/admin" : "/dashboard") : "/")}>
              {isAuthenticated ? "Back to dashboard" : "Back to home"}
            </Button>
            <Button variant="outlined" onClick={() => navigate("/assistant")}>
              Ask BankFlow AI
            </Button>
          </Stack>
        </Stack>
      </Box>
    </Container>
  );
}
