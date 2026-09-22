import { useCallback, useEffect, useMemo, useState } from "react";
import {
  Box,
  Button,
  Chip,
  Divider,
  Grid,
  IconButton,
  Paper,
  Stack,
  Tab,
  Tabs,
  Tooltip,
  Typography,
} from "@mui/material";
import NotificationsActiveIcon from "@mui/icons-material/NotificationsActive";
import PaymentsIcon from "@mui/icons-material/Payments";
import SecurityIcon from "@mui/icons-material/Security";
import RequestQuoteIcon from "@mui/icons-material/RequestQuote";
import InsightsIcon from "@mui/icons-material/Insights";
import DoneAllIcon from "@mui/icons-material/DoneAll";
import MarkEmailReadIcon from "@mui/icons-material/MarkEmailRead";

import { EmptyState, ErrorAlert, Loader, PageHeader } from "../components/Common.jsx";
import bankingService from "../services/bankingService";
import { getErrorMessage } from "../services/api";
import { relativeTime } from "../utils/formatCurrency.js";

const ICONS = {
  TRANSACTION: <PaymentsIcon />,
  SECURITY: <SecurityIcon />,
  LOAN: <RequestQuoteIcon />,
  SUMMARY: <InsightsIcon />,
  SYSTEM: <NotificationsActiveIcon />,
};

export default function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [tab, setTab] = useState("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setNotifications(await bankingService.getNotifications());
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const toggleRead = async (notification) => {
    try {
      const updated = await bankingService.markNotificationRead(
        notification.id,
        !notification.is_read
      );
      setNotifications((prev) =>
        prev.map((item) => (item.id === updated.id ? { ...item, is_read: updated.is_read } : item))
      );
    } catch (err) {
      setError(getErrorMessage(err));
    }
  };

  const markAll = async () => {
    try {
      await bankingService.markAllNotificationsRead();
      setNotifications((prev) => prev.map((item) => ({ ...item, is_read: true })));
    } catch (err) {
      setError(getErrorMessage(err));
    }
  };

  const filtered = useMemo(() => {
    if (tab === "unread") return notifications.filter((item) => !item.is_read);
    if (tab === "read") return notifications.filter((item) => item.is_read);
    return notifications;
  }, [notifications, tab]);

  const unread = notifications.filter((item) => !item.is_read).length;

  if (loading) return <Loader label="Loading notifications..." />;

  return (
    <Box>
      <PageHeader
        title="Notifications"
        subtitle={`${unread} unread simulated alert${unread === 1 ? "" : "s"}`}
        action={
          <Button startIcon={<DoneAllIcon />} onClick={markAll} disabled={unread === 0}>
            Mark all as read
          </Button>
        }
      />

      <ErrorAlert message={error} onRetry={load} />

      <Tabs
        value={tab}
        onChange={(_, value) => setTab(value)}
        sx={{ mb: 2, borderBottom: "1px solid #e6e9f2" }}
      >
        <Tab value="all" label={`All (${notifications.length})`} />
        <Tab value="unread" label={`Unread (${unread})`} />
        <Tab value="read" label={`Read (${notifications.length - unread})`} />
      </Tabs>

      {filtered.length === 0 ? (
        <EmptyState
          title="Nothing here"
          description="Simulated banking alerts will show up in this list."
        />
      ) : (
        <Grid container spacing={2}>
          {filtered.map((item) => (
            <Grid item xs={12} key={item.id}>
              <Paper
                variant="outlined"
                sx={{
                  p: 2,
                  borderRadius: 3,
                  borderLeft: item.is_read ? "4px solid #e6e9f2" : "4px solid #1b3a8f",
                  backgroundColor: item.is_read ? "#ffffff" : "#f8faff",
                }}
              >
                <Stack direction="row" spacing={2} alignItems="flex-start">
                  <Box
                    sx={{
                      display: "grid",
                      placeItems: "center",
                      width: 42,
                      height: 42,
                      borderRadius: 2,
                      backgroundColor: "#eef2fd",
                      color: "primary.main",
                      flexShrink: 0,
                    }}
                  >
                    {ICONS[item.notification_type] || ICONS.SYSTEM}
                  </Box>
                  <Box sx={{ flexGrow: 1 }}>
                    <Stack direction="row" spacing={1} alignItems="center" sx={{ flexWrap: "wrap" }}>
                      <Typography variant="subtitle1" fontWeight={700}>
                        {item.title}
                      </Typography>
                      {!item.is_read && <Chip size="small" color="primary" label="new" />}
                      <Chip
                        size="small"
                        variant="outlined"
                        label={item.notification_type.toLowerCase()}
                      />
                    </Stack>
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                      {item.message}
                    </Typography>
                    <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: "block" }}>
                      {relativeTime(item.created_at)}
                    </Typography>
                  </Box>
                  <Tooltip title={item.is_read ? "Mark as unread" : "Mark as read"}>
                    <IconButton onClick={() => toggleRead(item)}>
                      {item.is_read ? <MarkEmailReadIcon color="disabled" /> : <MarkEmailReadIcon color="primary" />}
                    </IconButton>
                  </Tooltip>
                </Stack>
              </Paper>
            </Grid>
          ))}
        </Grid>
      )}

      <Divider sx={{ my: 3 }} />
      <Typography variant="caption" color="text.secondary">
        These alerts are generated by the demo seed data. No real banking notifications are sent.
      </Typography>
    </Box>
  );
}
