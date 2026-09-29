import { useState } from "react";
import { Box, Container } from "@mui/material";
import { Outlet } from "react-router-dom";

import Navbar from "./Navbar.jsx";
import Sidebar, { DRAWER_WIDTH } from "./Sidebar.jsx";
import SiteFooter from "./SiteFooter.jsx";

/** Shell used by every private page: responsive sidebar, header, content and footer. */
export default function AppLayout() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <Box sx={{ display: "flex", minHeight: "100vh", backgroundColor: "background.default" }}>
      <Sidebar mobileOpen={mobileOpen} onClose={() => setMobileOpen(false)} />
      <Box
        sx={{
          flexGrow: 1,
          display: "flex",
          flexDirection: "column",
          width: { md: `calc(100% - ${DRAWER_WIDTH}px)` },
          minHeight: "100vh",
        }}
      >
        <Navbar onMenuClick={() => setMobileOpen(true)} />
        <Container maxWidth="xl" sx={{ py: { xs: 2, md: 3 }, px: { xs: 2, md: 3 }, flexGrow: 1 }}>
          <Outlet />
        </Container>
        <SiteFooter variant="slim" />
      </Box>
    </Box>
  );
}
