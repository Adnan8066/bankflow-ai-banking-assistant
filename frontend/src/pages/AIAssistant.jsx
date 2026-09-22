import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  Alert,
  Avatar,
  Box,
  Button,
  Chip,
  CircularProgress,
  Divider,
  Drawer,
  IconButton,
  List,
  ListItemButton,
  ListItemText,
  Paper,
  Stack,
  TextField,
  Tooltip,
  Typography,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import SendIcon from "@mui/icons-material/Send";
import AddCommentIcon from "@mui/icons-material/AddComment";
import DeleteSweepIcon from "@mui/icons-material/DeleteSweep";
import HistoryIcon from "@mui/icons-material/History";
import MenuOpenIcon from "@mui/icons-material/MenuOpen";
import { useNavigate } from "react-router-dom";

import ChatMessage from "../components/ChatMessage.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import aiService from "../services/aiService";
import { getErrorMessage } from "../services/api";
import { relativeTime } from "../utils/formatCurrency.js";

const WELCOME = {
  role: "ai",
  text:
    "Hi! I am BankFlow AI, your demo banking assistant.\n\nAsk me things like:\n" +
    "- What is my current balance?\n" +
    "- How much did I spend this month?\n" +
    "- What was my biggest expense?\n" +
    "- What loans do I have?\n" +
    "- Explain EMI",
  meta: { type: "greeting" },
};

export default function AIAssistant() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));
  const { user } = useAuth();
  const navigate = useNavigate();

  const [messages, setMessages] = useState([WELCOME]);
  const [history, setHistory] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const [historyOpen, setHistoryOpen] = useState(false);
  const bottomRef = useRef(null);

  const loadHistory = useCallback(async () => {
    try {
      const data = await aiService.history();
      setHistory(data.results.slice().reverse());
      setSuggestions(data.suggestions || []);
    } catch (err) {
      setError(getErrorMessage(err));
    }
  }, []);

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, sending]);

  const send = async (question) => {
    const text = (question ?? input).trim();
    if (!text || sending) return;

    setError("");
    setInput("");
    setMessages((prev) => [...prev, { role: "user", text }]);
    setSending(true);

    try {
      const data = await aiService.chat(text);
      setMessages((prev) => [
        ...prev,
        { role: "ai", text: data.response, meta: { type: data.type, provider: data.provider } },
      ]);
      await loadHistory();
    } catch (err) {
      setError(getErrorMessage(err));
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: "I could not reach the banking service just now. Please try again in a moment.",
          meta: { type: "error" },
        },
      ]);
    } finally {
      setSending(false);
    }
  };

  const clearHistory = async () => {
    try {
      await aiService.clearHistory();
      setHistory([]);
      setMessages([WELCOME]);
    } catch (err) {
      setError(getErrorMessage(err));
    }
  };

  const startNewChat = () => {
    setMessages([WELCOME]);
    setHistoryOpen(false);
  };

  const historyPanel = useMemo(
    () => (
      <Box sx={{ display: "flex", flexDirection: "column", height: "100%" }}>
        <Stack direction="row" alignItems="center" spacing={1} sx={{ p: 2 }}>
          <HistoryIcon fontSize="small" color="primary" />
          <Typography variant="subtitle2" sx={{ flexGrow: 1 }}>
            Chat history
          </Typography>
          <Tooltip title="Clear saved history">
            <IconButton size="small" onClick={clearHistory}>
              <DeleteSweepIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </Stack>
        <Divider />
        <Box sx={{ p: 1.5 }}>
          <Button
            fullWidth
            variant="outlined"
            startIcon={<AddCommentIcon />}
            onClick={startNewChat}
          >
            New chat
          </Button>
        </Box>
        <Divider />
        <List sx={{ px: 1, overflowY: "auto", flexGrow: 1 }}>
          {history.length === 0 && (
            <Typography variant="caption" color="text.secondary" sx={{ p: 2, display: "block" }}>
              No saved conversations yet. Your questions are stored in the demo database so you can
              revisit them.
            </Typography>
          )}
          {history.map((item) => (
            <ListItemButton
              key={item.id}
              sx={{ borderRadius: 2, mb: 0.5, alignItems: "flex-start" }}
              onClick={() => {
                setMessages((prev) => [
                  ...prev,
                  { role: "user", text: item.message },
                  {
                    role: "ai",
                    text: item.response,
                    meta: { type: item.response_type, created_at: item.created_at },
                  },
                ]);
                setHistoryOpen(false);
              }}
            >
              <ListItemText
                primary={item.message}
                secondary={`${item.response_type.replace(/_/g, " ")} - ${relativeTime(item.created_at)}`}
                primaryTypographyProps={{ fontSize: 13, fontWeight: 600, noWrap: false }}
                secondaryTypographyProps={{ fontSize: 11 }}
              />
            </ListItemButton>
          ))}
        </List>
      </Box>
    ),
    [history]
  );

  return (
    <Box sx={{ display: "flex", gap: 2.5, height: { xs: "calc(100vh - 150px)", md: "calc(100vh - 150px)" } }}>
      {/* -------------------------------------------------- history sidebar */}
      {!isMobile && (
        <Paper
          variant="outlined"
          sx={{ width: 280, flexShrink: 0, borderRadius: 3, overflow: "hidden" }}
        >
          {historyPanel}
        </Paper>
      )}

      <Drawer
        anchor="left"
        open={historyOpen}
        onClose={() => setHistoryOpen(false)}
        sx={{ display: { md: "none" } }}
      >
        <Box sx={{ width: 290 }}>{historyPanel}</Box>
      </Drawer>

      {/* ----------------------------------------------------------- chat */}
      <Paper
        variant="outlined"
        sx={{ flexGrow: 1, borderRadius: 3, display: "flex", flexDirection: "column", overflow: "hidden" }}
      >
        <Stack
          direction="row"
          spacing={1.5}
          alignItems="center"
          sx={{ p: 2, borderBottom: "1px solid #e6e9f2" }}
        >
          {isMobile && (
            <IconButton size="small" onClick={() => setHistoryOpen(true)}>
              <MenuOpenIcon />
            </IconButton>
          )}
          <Avatar sx={{ bgcolor: "primary.main" }}>
            <SmartToyIcon fontSize="small" />
          </Avatar>
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="subtitle1" fontWeight={700} lineHeight={1.2}>
              BankFlow AI
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Grounded in your simulated banking data
            </Typography>
          </Box>
          <Chip size="small" color="success" label="online" />
        </Stack>

        <Box sx={{ flexGrow: 1, overflowY: "auto", p: { xs: 2, md: 3 }, backgroundColor: "#fbfcff" }}>
          {error && (
            <Alert severity="warning" sx={{ mb: 2 }} onClose={() => setError("")}>
              {error}
            </Alert>
          )}

          {messages.map((message, index) => (
            <ChatMessage
              key={`${message.role}-${index}`}
              sender={message.role}
              message={message.text}
              meta={message.meta}
              userName={user?.name}
            />
          ))}

          {sending && (
            <Stack direction="row" spacing={1.5} alignItems="center" sx={{ pl: 1 }}>
              <Avatar sx={{ bgcolor: "primary.main", width: 36, height: 36 }}>
                <SmartToyIcon fontSize="small" />
              </Avatar>
              <Stack direction="row" spacing={1} alignItems="center">
                <CircularProgress size={16} />
                <Typography variant="caption" color="text.secondary">
                  BankFlow AI is checking your demo data...
                </Typography>
              </Stack>
            </Stack>
          )}
          <div ref={bottomRef} />
        </Box>

        {/* ------------------------------------------- suggestions + input */}
        <Box sx={{ p: 2, borderTop: "1px solid #e6e9f2" }}>
          <Stack
            direction="row"
            spacing={1}
            sx={{ mb: 1.5, overflowX: "auto", pb: 0.5 }}
          >
            {suggestions.slice(0, 8).map((suggestion) => (
              <Chip
                key={suggestion}
                label={suggestion}
                size="small"
                variant="outlined"
                onClick={() => send(suggestion)}
                sx={{ whiteSpace: "nowrap" }}
              />
            ))}
          </Stack>

          <Stack direction="row" spacing={1.5} alignItems="flex-end">
            <TextField
              fullWidth
              multiline
              maxRows={4}
              size="small"
              placeholder="Ask about your balance, spending, loans or a banking term..."
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter" && !event.shiftKey) {
                  event.preventDefault();
                  send();
                }
              }}
            />
            <Button
              variant="contained"
              onClick={() => send()}
              disabled={sending || !input.trim()}
              endIcon={<SendIcon />}
              sx={{ height: 42 }}
            >
              Send
            </Button>
          </Stack>
          <Typography variant="caption" color="text.secondary" sx={{ display: "block", mt: 1 }}>
            Answers use only your simulated demo data. BankFlow AI cannot move money or access real
            accounts.{" "}
            <Box
              component="span"
              sx={{ color: "primary.main", cursor: "pointer", fontWeight: 600 }}
              onClick={() => navigate("/emi-calculator")}
            >
              Try the EMI calculator
            </Box>
          </Typography>
        </Box>
      </Paper>
    </Box>
  );
}
