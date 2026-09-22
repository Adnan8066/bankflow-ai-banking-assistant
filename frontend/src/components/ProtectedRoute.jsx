import { Box, CircularProgress } from "@mui/material";
import { Navigate, Outlet, useLocation } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";

/**
 * Route guard.
 * <ProtectedRoute />                    -> any logged in customer
 * <ProtectedRoute role="ADMIN" />       -> bank employee area only
 */
export default function ProtectedRoute({ role }) {
  const { isAuthenticated, isAdmin, booting } = useAuth();
  const location = useLocation();

  if (booting) {
    return (
      <Box sx={{ display: "grid", placeItems: "center", minHeight: "60vh" }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  if (role === "ADMIN" && !isAdmin) {
    return <Navigate to="/dashboard" replace />;
  }

  return <Outlet />;
}
