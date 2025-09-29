const fs = require("fs");
const path = require("path");

const [, , inputFile, outputDir] = process.argv;
const audit = JSON.parse(fs.readFileSync(inputFile, "utf8"));

fs.mkdirSync(outputDir, { recursive: true });

// Handle both npm and pnpm audit formats
const issues = audit.vulnerabilities || audit.advisories || {};
const metadata = audit.metadata || {};
const vulnCount = metadata.vulnerabilities || 0;

// For pnpm format, check if we have any vulnerabilities
const hasVulns =
  Object.keys(issues).length > 0 ||
  (typeof vulnCount === "object"
    ? Object.values(vulnCount).some((v) => v > 0)
    : vulnCount > 0);

// Create summary for description
let summary = "No vulnerabilities found";
if (hasVulns) {
  if (metadata.vulnerabilities) {
    const counts = metadata.vulnerabilities;
    summary = `Found vulnerabilities: ${counts.critical || 0} critical, ${
      counts.high || 0
    } high, ${counts.moderate || 0} moderate, ${counts.low || 0} low`;
  } else {
    summary = `Found ${Object.keys(issues).length} vulnerability issues`;
  }
}

const result = {
  uuid: "security-scan",
  historyId: "security-scan",
  name: "Dependency Vulnerability Scan",
  status: hasVulns ? "failed" : "passed",
  description: summary,
  attachments: [
    {
      name: "pnpm audit report",
      type: "application/json",
      source: "audit.json",
    },
  ],
  parameters: [],
  labels: [{ name: "feature", value: "Security" }],
  start: Date.now(),
  stop: Date.now(),
};

fs.writeFileSync(
  path.join(outputDir, "security-scan-result.json"),
  JSON.stringify(result, null, 2)
);

// Copy original audit.json so it's available in Allure attachments
fs.copyFileSync(inputFile, path.join(outputDir, "audit.json"));
