export interface Scenario {
  id: string;
  name: string;
  description: string;
  platform: string;
  tactic: string;
  technique_id: string;
  technique_name: string;
  severity: string;
  enabled: boolean;
  mode: string;
  expected_detection: string | null;
  created_at: string;
}

export interface SimulationRun {
  id: string;
  scenario_id: string;
  status: string;
  started_at: string;
  finished_at: string | null;
  mode: string;
  result_summary: string | null;
}

export interface LogEvent {
  id: number;
  run_id: string;
  timestamp: string;
  source: string;
  host: string;
  user: string;
  event_type: string;
  event_id: number | null;
  process_name: string | null;
  command_line: string | null;
  src_ip: string | null;
  dst_ip: string | null;
  raw_message: string | null;
}

export interface Alert {
  id: number;
  run_id: string;
  rule_id: string;
  timestamp: string;
  title: string;
  severity: string;
  matched_event_id: number | null;
  reason: string;
  mitre_technique_id: string;
  mitre_tactic: string;
}

export interface ValidationResult {
  run_id: string;
  scenario_id: string;
  expected_detection: string | null;
  detected: boolean;
  alerts_count: number;
  coverage_status: string;
}

export interface TechniqueCoverage {
  scenario_id: string;
  technique_id: string;
  technique_name: string;
  tactic: string;
  status: 'covered' | 'not_detected' | 'not_tested';
}

export interface Coverage {
  total_scenarios: number;
  total_techniques: number;
  total_tactics: number;
  detected_scenarios: number;
  undetected_scenarios: number;
  coverage_rate: number;
  alerts_by_severity: Record<string, number>;
  technique_coverage: TechniqueCoverage[];
}
