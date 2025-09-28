const fs = require("fs");
const path = require("path");

const [, , inputFile, outputDir] = process.argv;
const audit = JSON.parse(fs.readFileSync(inputFile, "utf8"));

fs.mkdirSync(outputDir, { recursive: true });

const issues = audit.vulnerabilities || {};
const hasVulns = Object.keys(issues).length > 0;

const result = {
  uuid: "security-scan",
  historyId: "security-scan",
  name: "Dependency Vulnerability Scan",
  status: hasVulns ? "failed" : "passed",
  attachments: [
    {
      name: "npm audit report",
      type: "application/json",
      source: "audit.json",
    },
  ],
  parameters: [],
  labels: [{ name: "feature", value: "Security" }],
};

fs.writeFileSync(
  path.join(outputDir, "security-scan-result.json"),
  JSON.stringify(result, null, 2)
);

// Copy original audit.json so it's available in Allure attachments
fs.copyFileSync(inputFile, path.join(outputDir, "audit.json"));
