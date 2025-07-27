#!/usr/bin/env python3
"""
D'Agri Talk Security Dashboard
Aggregates and displays security scan results
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

class SecurityDashboard:
    def __init__(self, reports_dir="security-reports"):
        self.reports_dir = Path(reports_dir)
        self.scan_results = {}
        
    def load_scan_results(self):
        """Load all security scan results"""
        scan_files = {
            'safety': 'safety-report.json',
            'bandit': 'bandit-report.json',
            'npm_audit': 'npm-audit.json',
            'trivy_backend': 'trivy-backend-image.json',
            'trivy_frontend': 'trivy-frontend-image.json',
            'checkov': 'checkov-terraform.json'
        }
        
        for scan_type, filename in scan_files.items():
            file_path = self.reports_dir / filename
            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        self.scan_results[scan_type] = json.load(f)
                except json.JSONDecodeError:
                    print(f"Warning: Could not parse {filename}")
                    self.scan_results[scan_type] = None
            else:
                self.scan_results[scan_type] = None
    
    def analyze_safety_results(self):
        """Analyze Python dependency vulnerabilities"""
        if not self.scan_results.get('safety'):
            return {"status": "no_data", "vulnerabilities": 0}
        
        vulns = self.scan_results['safety'].get('vulnerabilities', [])
        return {
            "status": "critical" if len(vulns) > 0 else "clean",
            "vulnerabilities": len(vulns),
            "details": vulns[:5]  # Top 5 vulnerabilities
        }
    
    def analyze_npm_results(self):
        """Analyze Node.js dependency vulnerabilities"""
        if not self.scan_results.get('npm_audit'):
            return {"status": "no_data", "vulnerabilities": 0}
        
        metadata = self.scan_results['npm_audit'].get('metadata', {})
        vulns = metadata.get('vulnerabilities', {})
        
        total_vulns = sum(vulns.values()) if isinstance(vulns, dict) else 0
        critical = vulns.get('critical', 0)
        high = vulns.get('high', 0)
        
        status = "critical" if critical > 0 else "warning" if high > 0 else "clean"
        
        return {
            "status": status,
            "vulnerabilities": total_vulns,
            "critical": critical,
            "high": high,
            "moderate": vulns.get('moderate', 0),
            "low": vulns.get('low', 0)
        }
    
    def analyze_container_security(self):
        """Analyze container security scan results"""
        results = {"backend": {}, "frontend": {}}
        
        for component in ["backend", "frontend"]:
            trivy_key = f'trivy_{component}'
            if not self.scan_results.get(trivy_key):
                results[component] = {"status": "no_data", "vulnerabilities": 0}
                continue
            
            trivy_results = self.scan_results[trivy_key]
            total_vulns = 0
            critical_vulns = 0
            high_vulns = 0
            
            for result in trivy_results.get('Results', []):
                vulns = result.get('Vulnerabilities', [])
                total_vulns += len(vulns)
                
                for vuln in vulns:
                    severity = vuln.get('Severity', '').upper()
                    if severity == 'CRITICAL':
                        critical_vulns += 1
                    elif severity == 'HIGH':
                        high_vulns += 1
            
            status = "critical" if critical_vulns > 0 else "warning" if high_vulns > 0 else "clean"
            
            results[component] = {
                "status": status,
                "vulnerabilities": total_vulns,
                "critical": critical_vulns,
                "high": high_vulns
            }
        
        return results
    
    def generate_dashboard_html(self):
        """Generate HTML security dashboard"""
        safety_analysis = self.analyze_safety_results()
        npm_analysis = self.analyze_npm_results()
        container_analysis = self.analyze_container_security()
        
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>D'Agri Talk Security Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .dashboard {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
                .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 20px; }}
                .status-clean {{ border-left: 5px solid #28a745; }}
                .status-warning {{ border-left: 5px solid #ffc107; }}
                .status-critical {{ border-left: 5px solid #dc3545; }}
                .status-no_data {{ border-left: 5px solid #6c757d; }}
                .metric {{ font-size: 2em; font-weight: bold; }}
                .timestamp {{ color: #666; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <h1>🔒 D'Agri Talk Security Dashboard</h1>
            <p class="timestamp">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            
            <div class="dashboard">
                <div class="card status-{safety_analysis['status']}">
                    <h3>🐍 Python Dependencies</h3>
                    <div class="metric">{safety_analysis['vulnerabilities']}</div>
                    <p>Vulnerabilities found</p>
                </div>
                
                <div class="card status-{npm_analysis['status']}">
                    <h3>📦 Node.js Dependencies</h3>
                    <div class="metric">{npm_analysis['vulnerabilities']}</div>
                    <p>Total vulnerabilities</p>
                    <small>Critical: {npm_analysis.get('critical', 0)}, High: {npm_analysis.get('high', 0)}</small>
                </div>
                
                <div class="card status-{container_analysis['backend']['status']}">
                    <h3>🐳 Backend Container</h3>
                    <div class="metric">{container_analysis['backend']['vulnerabilities']}</div>
                    <p>Container vulnerabilities</p>
                    <small>Critical: {container_analysis['backend'].get('critical', 0)}, High: {container_analysis['backend'].get('high', 0)}</small>
                </div>
                
                <div class="card status-{container_analysis['frontend']['status']}">
                    <h3>⚛️ Frontend Container</h3>
                    <div class="metric">{container_analysis['frontend']['vulnerabilities']}</div>
                    <p>Container vulnerabilities</p>
                    <small>Critical: {container_analysis['frontend'].get('critical', 0)}, High: {container_analysis['frontend'].get('high', 0)}</small>
                </div>
            </div>
            
            <h2>📊 Security Scan Summary</h2>
            <ul>
                <li><strong>Python Dependencies:</strong> {safety_analysis['vulnerabilities']} vulnerabilities found</li>
                <li><strong>Node.js Dependencies:</strong> {npm_analysis['vulnerabilities']} total vulnerabilities</li>
                <li><strong>Container Security:</strong> Backend: {container_analysis['backend']['vulnerabilities']}, Frontend: {container_analysis['frontend']['vulnerabilities']}</li>
            </ul>
            
            <h2>🛡️ Security Recommendations</h2>
            <ul>
                <li>Regularly update dependencies to latest secure versions</li>
                <li>Monitor security advisories for used packages</li>
                <li>Implement runtime security monitoring</li>
                <li>Review and address high-severity vulnerabilities promptly</li>
            </ul>
        </body>
        </html>
        """
        
        return html_template
    
    def generate_report(self):
        """Generate comprehensive security report"""
        self.load_scan_results()
        
        # Generate HTML dashboard
        html_content = self.generate_dashboard_html()
        
        # Save dashboard
        dashboard_path = self.reports_dir / "security-dashboard.html"
        with open(dashboard_path, 'w') as f:
            f.write(html_content)
        
        print(f"Security dashboard generated: {dashboard_path}")
        
        # Generate summary for CI
        safety_analysis = self.analyze_safety_results()
        npm_analysis = self.analyze_npm_results()
        container_analysis = self.analyze_container_security()
        
        total_critical = (
            (safety_analysis['vulnerabilities'] if safety_analysis['status'] == 'critical' else 0) +
            npm_analysis.get('critical', 0) +
            container_analysis['backend'].get('critical', 0) +
            container_analysis['frontend'].get('critical', 0)
        )
        
        print(f"\n🔒 Security Scan Summary:")
        print(f"   Python Dependencies: {safety_analysis['vulnerabilities']} vulnerabilities")
        print(f"   Node.js Dependencies: {npm_analysis['vulnerabilities']} vulnerabilities")
        print(f"   Backend Container: {container_analysis['backend']['vulnerabilities']} vulnerabilities")
        print(f"   Frontend Container: {container_analysis['frontend']['vulnerabilities']} vulnerabilities")
        print(f"   Total Critical: {total_critical}")
        
        return total_critical == 0

if __name__ == "__main__":
    dashboard = SecurityDashboard()
    success = dashboard.generate_report()
    sys.exit(0 if success else 1)