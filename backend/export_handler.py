"""
Export Handler for Repository Analysis
Supports JSON, CSV, and PDF export formats
"""

import json
import csv
import io
from typing import Dict, Any
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT

class ExportHandler:
    """Handle export of analysis data to various formats"""
    
    def export_json(self, analysis_data: Dict[str, Any]) -> str:
        """Export analysis as formatted JSON"""
        # Add export metadata
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "format": "json",
            "version": "1.0",
            "data": analysis_data
        }
        return json.dumps(export_data, indent=2, default=str)
    
    def export_csv(self, analysis_data: Dict[str, Any]) -> str:
        """Export analysis as CSV (flattened structure)"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow(["GitHub Repository Analysis Report"])
        writer.writerow(["Exported at", datetime.now().isoformat()])
        writer.writerow([])  # Empty row
        
        # Flatten and write repository metadata
        if "repository_metadata" in analysis_data:
            meta = analysis_data["repository_metadata"]
            writer.writerow(["Repository Metadata"])
            writer.writerow(["Field", "Value"])
            writer.writerow(["Name", meta.get("name", "N/A")])
            writer.writerow(["Owner", meta.get("owner", "N/A")])
            writer.writerow(["Description", meta.get("description", "N/A")])
            writer.writerow(["Stars", meta.get("stars", 0)])
            writer.writerow(["Forks", meta.get("forks", 0)])
            writer.writerow(["Primary Language", meta.get("primary_language", "N/A")])
            writer.writerow(["License", meta.get("license", "N/A")])
            writer.writerow([])
        
        # Architecture Synopsis
        if "architecture_synopsis" in analysis_data:
            arch = analysis_data["architecture_synopsis"]
            writer.writerow(["Architecture Synopsis"])
            writer.writerow(["Field", "Value"])
            writer.writerow(["Core Language", arch.get("core_language", "N/A")])
            writer.writerow(["Framework", arch.get("framework_identification", "N/A")])
            writer.writerow(["Build System", arch.get("build_system", "N/A")])
            writer.writerow([])
        
        # Code Quality Metrics
        if "code_quality_metrics" in analysis_data:
            quality = analysis_data["code_quality_metrics"]
            writer.writerow(["Code Quality Metrics"])
            writer.writerow(["Metric", "Value"])
            writer.writerow(["Testing Framework", quality.get("testing_framework", "N/A")])
            writer.writerow(["CI/CD Pipeline", quality.get("ci_cd_pipeline", "N/A")])
            writer.writerow(["Documentation Quality", quality.get("documentation_quality", "N/A")])
            writer.writerow([])
        
        # Development Activity
        if "development_activity" in analysis_data:
            activity = analysis_data["development_activity"]
            writer.writerow(["Development Activity"])
            writer.writerow(["Metric", "Value"])
            writer.writerow(["Recent Commits", activity.get("recent_commit_patterns", "N/A")])
            writer.writerow(["Commit Frequency", activity.get("commit_frequency_per_day", 0)])
            writer.writerow(["Open Issues", activity.get("open_issues_count", 0)])
            writer.writerow(["Open PRs", activity.get("open_pull_requests", 0)])
            writer.writerow([])
        
        # Technical Debt
        if "technical_debt_assessment" in analysis_data:
            debt = analysis_data["technical_debt_assessment"]
            writer.writerow(["Technical Debt Assessment"])
            writer.writerow(["Maintenance Burden", debt.get("maintenance_burden", "N/A")])
            if "debt_indicators" in debt:
                for indicator in debt["debt_indicators"]:
                    writer.writerow(["Debt Indicator", indicator])
        
        return output.getvalue()
    
    def export_pdf(self, analysis_data: Dict[str, Any]) -> bytes:
        """Export analysis as PDF report"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title style
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#211D49'),
            alignment=TA_CENTER,
            spaceAfter=30
        )
        
        # Section style
        section_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#8D5EB7'),
            spaceAfter=12
        )
        
        # Add title
        story.append(Paragraph("GitHub Repository Analysis Report", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Add export date
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Repository Metadata Section
        if "repository_metadata" in analysis_data:
            meta = analysis_data["repository_metadata"]
            story.append(Paragraph("Repository Metadata", section_style))
            
            meta_data = [
                ["Field", "Value"],
                ["Name", str(meta.get("name", "N/A"))],
                ["Owner", str(meta.get("owner", "N/A"))],
                ["Description", str(meta.get("description", "N/A"))[:100] + "..." if len(str(meta.get("description", ""))) > 100 else str(meta.get("description", "N/A"))],
                ["Stars", str(meta.get("stars", 0))],
                ["Forks", str(meta.get("forks", 0))],
                ["Primary Language", str(meta.get("primary_language", "N/A"))],
                ["License", str(meta.get("license", "N/A"))]
            ]
            
            meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
            meta_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EECEE6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#211D49')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#EEEEEE'))
            ]))
            story.append(meta_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Architecture Synopsis
        if "architecture_synopsis" in analysis_data:
            arch = analysis_data["architecture_synopsis"]
            story.append(Paragraph("Architecture Synopsis", section_style))
            
            arch_data = [
                ["Aspect", "Details"],
                ["Core Language", str(arch.get("core_language", "N/A"))],
                ["Framework", str(arch.get("framework_identification", "N/A"))],
                ["Build System", str(arch.get("build_system", "N/A"))],
                ["Architecture Pattern", str(arch.get("architecture_pattern", "N/A"))]
            ]
            
            arch_table = Table(arch_data, colWidths=[2*inch, 4*inch])
            arch_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EECEE6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#211D49')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#EEEEEE'))
            ]))
            story.append(arch_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Development Activity
        if "development_activity" in analysis_data:
            activity = analysis_data["development_activity"]
            story.append(Paragraph("Development Activity", section_style))
            
            activity_data = [
                ["Metric", "Value"],
                ["Recent Commits", str(activity.get("recent_commit_patterns", "N/A"))],
                ["Commit Frequency", f"{activity.get('commit_frequency_per_day', 0)} per day"],
                ["Open Issues", str(activity.get("open_issues_count", 0))],
                ["Open Pull Requests", str(activity.get("open_pull_requests", 0))],
                ["Release Cadence", str(activity.get("release_cadence", "N/A"))]
            ]
            
            activity_table = Table(activity_data, colWidths=[2*inch, 4*inch])
            activity_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EECEE6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#211D49')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#EEEEEE'))
            ]))
            story.append(activity_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Technical Debt Assessment
        if "technical_debt_assessment" in analysis_data:
            debt = analysis_data["technical_debt_assessment"]
            story.append(Paragraph("Technical Debt Assessment", section_style))
            
            # Add maintenance burden
            story.append(Paragraph(f"<b>Maintenance Burden:</b> {debt.get('maintenance_burden', 'N/A')}", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
            
            # Add debt indicators
            if "debt_indicators" in debt and debt["debt_indicators"]:
                story.append(Paragraph("<b>Debt Indicators:</b>", styles['Normal']))
                for indicator in debt["debt_indicators"]:
                    story.append(Paragraph(f"• {indicator}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph("Generated by GitHub Repository Analyzer", styles['Normal']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.read()

# Create singleton instance
export_handler = ExportHandler()