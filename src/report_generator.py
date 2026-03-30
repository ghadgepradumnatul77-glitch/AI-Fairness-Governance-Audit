from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


def generate_report(model_name, accuracy, dir_score, risk, decision):

    doc = SimpleDocTemplate(
        "AI_Governance_Report.pdf",
        pagesize=A4
    )

    styles = getSampleStyleSheet()
    content = []

    # -------------------------
    # TITLE
    # -------------------------
    content.append(Paragraph("AI GOVERNANCE REPORT", styles["Title"]))
    content.append(Spacer(1, 20))

    # -------------------------
    # MODEL DETAILS
    # -------------------------
    content.append(Paragraph(f"<b>Model:</b> {model_name}", styles["Normal"]))
    content.append(Paragraph(f"<b>Accuracy:</b> {round(accuracy,3)}", styles["Normal"]))
    content.append(Paragraph(f"<b>DIR:</b> {round(dir_score,3)}", styles["Normal"]))
    content.append(Paragraph(f"<b>Risk Score:</b> {round(risk,2)}", styles["Normal"]))

    content.append(Spacer(1, 20))

    # -------------------------
    # DECISION
    # -------------------------
    content.append(Paragraph("<b>Final Decision:</b>", styles["Heading2"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(decision, styles["Normal"]))
    content.append(Spacer(1, 20))

    # -------------------------
    # EXPLANATION
    # -------------------------
    explanation = """
    This report evaluates whether the AI model is safe and fair for deployment.
    The system measures bias using Disparate Impact Ratio (DIR).
    If the model shows unfair behavior across groups, mitigation techniques are applied.
    Based on fairness and accuracy, a final deployment decision is made.
    """

    content.append(Paragraph(explanation, styles["Normal"]))

    # -------------------------
    # BUILD PDF
    # -------------------------
    doc.build(content)

    print("✅ Clean Report Generated: AI_Governance_Report.pdf")