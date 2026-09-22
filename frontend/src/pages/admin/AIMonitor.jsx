import { useCallback, useEffect, useState } from "react";
import {
  Box,
  Chip,
  Grid,
  InputAdornment,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip as ChartTooltip, XAxis, YAxis } from "recharts";

import { EmptyState, ErrorAlert, Loader, PageHeader, SectionCard } from "../../components/Common.jsx";
import adminService from "../../services/adminService";
import { getErrorMessage } from "../../services/api";
import { relativeTime } from "../../utils/formatCurrency.js";

export default function AIMonitor() {
  const [data, setData] = useState(null);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async (term = "") => {
    setLoading(true);
    setError("");
    try {
      setData(await adminService.aiMonitor(term ? { search: term } : {}));
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  return (
    <Box>
      <PageHeader
        title="AI Assistant Monitoring"
        subtitle="What customers are asking BankFlow AI and how the intent engine answered."
      />

      <ErrorAlert message={error} onRetry={() => load(search)} />

      {loading ? (
        <Loader label="Loading assistant activity..." minHeight="50vh" />
      ) : (
        <>
          <Grid container spacing={2.5} sx={{ mb: 2.5 }}>
            <Grid item xs={12} sm={4}>
              <SectionCard title="Total messages">
                <Typography variant="h4">{data.total_messages}</Typography>
                <Typography variant="caption" color="text.secondary">
                  Saved demo conversations
                </Typography>
              </SectionCard>
            </Grid>
            <Grid item xs={12} sm={4}>
              <SectionCard title="Rule based answers">
                <Typography variant="h4">{data.providers.fallback}</Typography>
                <Typography variant="caption" color="text.secondary">
                  Works with no external API key
                </Typography>
              </SectionCard>
            </Grid>
            <Grid item xs={12} sm={4}>
              <SectionCard title="LLM answers">
                <Typography variant="h4">{data.providers.openai}</Typography>
                <Typography variant="caption" color="text.secondary">
                  Used when AI_PROVIDER=openai
                </Typography>
              </SectionCard>
            </Grid>

            {data.intent_breakdown.length > 0 && (
              <Grid item xs={12}>
                <SectionCard title="Intent breakdown" subtitle="Detected intent per question">
                  <Box sx={{ height: 260 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={data.intent_breakdown}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#eef1f8" />
                        <XAxis
                          dataKey="type"
                          tick={{ fontSize: 11 }}
                          interval={0}
                          angle={-20}
                          dy={10}
                          height={60}
                        />
                        <YAxis tick={{ fontSize: 12 }} allowDecimals={false} />
                        <ChartTooltip />
                        <Bar dataKey="count" name="Questions" fill="#4361ee" radius={[6, 6, 0, 0]} maxBarSize={40} />
                      </BarChart>
                    </ResponsiveContainer>
                  </Box>
                </SectionCard>
              </Grid>
            )}
          </Grid>

          <Paper variant="outlined" sx={{ p: 2.5, borderRadius: 3 }}>
            <Stack direction={{ xs: "column", sm: "row" }} spacing={2} sx={{ mb: 2 }}>
              <TextField
                size="small"
                placeholder="Search question or customer"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                onKeyDown={(event) => event.key === "Enter" && load(search)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon fontSize="small" />
                    </InputAdornment>
                  ),
                }}
                sx={{ flexGrow: 1 }}
              />
              <Box
                component="button"
                onClick={() => load(search)}
                sx={{
                  px: 2,
                  py: 1,
                  borderRadius: 2,
                  border: "none",
                  backgroundColor: "primary.main",
                  color: "#fff",
                  cursor: "pointer",
                  fontWeight: 600,
                }}
              >
                Search
              </Box>
            </Stack>

            {data.results.length === 0 ? (
              <EmptyState
                title="No assistant activity yet"
                description="Ask something in the AI Assistant page and it will appear here."
              />
            ) : (
              <TableContainer>
                <Table size="small" sx={{ minWidth: 900 }}>
                  <TableHead>
                    <TableRow>
                      <TableCell>Customer</TableCell>
                      <TableCell>Question</TableCell>
                      <TableCell>Answer preview</TableCell>
                      <TableCell>Intent</TableCell>
                      <TableCell>Provider</TableCell>
                      <TableCell>When</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {data.results.map((row) => (
                      <TableRow key={row.id} hover>
                        <TableCell>
                          <Stack direction="row" spacing={1} alignItems="center">
                            <SmartToyIcon fontSize="small" color="primary" />
                            <Box>
                              <Typography variant="body2" fontWeight={600}>
                                {row.customer}
                              </Typography>
                              <Typography variant="caption" color="text.secondary">
                                {row.email}
                              </Typography>
                            </Box>
                          </Stack>
                        </TableCell>
                        <TableCell sx={{ maxWidth: 240 }}>{row.message}</TableCell>
                        <TableCell sx={{ maxWidth: 320 }}>
                          <Typography variant="body2" color="text.secondary">
                            {row.response.length > 140 ? `${row.response.slice(0, 140)}...` : row.response}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Chip size="small" variant="outlined" label={row.type.replace(/_/g, " ")} />
                        </TableCell>
                        <TableCell>
                          <Chip
                            size="small"
                            color={row.provider === "openai" ? "info" : "default"}
                            label={row.provider}
                          />
                        </TableCell>
                        <TableCell>{relativeTime(row.created_at)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
          </Paper>
        </>
      )}
    </Box>
  );
}
