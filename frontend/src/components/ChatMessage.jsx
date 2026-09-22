import { Avatar, Box, Chip, Paper, Stack, Typography } from "@mui/material";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import PersonIcon from "@mui/icons-material/Person";

import { initials, relativeTime } from "../utils/formatCurrency.js";

/**
 * A single chat bubble. Used for both live answers and saved chat history.
 */
export default function ChatMessage({ message, sender = "ai", userName = "You", meta }) {
  const isUser = sender === "user";

  return (
    <Stack
      direction="row"
      spacing={1.5}
      justifyContent={isUser ? "flex-end" : "flex-start"}
      sx={{ mb: 2 }}
      className="fade-in"
    >
      {!isUser && (
        <Avatar sx={{ bgcolor: "primary.main", width: 36, height: 36 }}>
          <SmartToyIcon fontSize="small" />
        </Avatar>
      )}
      <Box sx={{ maxWidth: { xs: "85%", md: "70%" } }}>
        <Paper
          elevation={0}
          sx={{
            p: 1.75,
            borderRadius: 3,
            borderTopLeftRadius: isUser ? 12 : 4,
            borderTopRightRadius: isUser ? 4 : 12,
            backgroundColor: isUser ? "primary.main" : "#ffffff",
            color: isUser ? "#ffffff" : "text.primary",
            border: isUser ? "none" : "1px solid #e6e9f2",
            whiteSpace: "pre-line",
          }}
        >
          <Typography variant="body2" sx={{ lineHeight: 1.7 }}>
            {message}
          </Typography>
        </Paper>
        <Stack direction="row" spacing={0.75} alignItems="center" sx={{ mt: 0.5, px: 0.5 }}>
          <Typography variant="caption" color="text.secondary">
            {isUser ? userName : "BankFlow AI"}
          </Typography>
          {meta?.type && !isUser && (
            <Chip size="small" variant="outlined" label={meta.type.replace(/_/g, " ")} />
          )}
          {meta?.created_at && (
            <Typography variant="caption" color="text.secondary">
              {relativeTime(meta.created_at)}
            </Typography>
          )}
        </Stack>
      </Box>
      {isUser && (
        <Avatar sx={{ bgcolor: "#111a2e", width: 36, height: 36 }}>
          {isUser && userName && userName !== "You" ? initials(userName) : <PersonIcon fontSize="small" />}
        </Avatar>
      )}
    </Stack>
  );
}
